"""CLI entry point for Trust WEDO."""

import click
import json
import asyncio
from pathlib import Path
from trust_wedo import __version__
from trust_wedo.parsers.site_parser import SiteParser
from trust_wedo.core.entity_scorer import EntityScorer
from trust_wedo.core.afb_builder import AFBBuilder
from trust_wedo.core.citation_evaluator import CitationEvaluator
from trust_wedo.core.graph_builder import GraphBuilder
from trust_wedo.core.report_generator import ReportGenerator
from trust_wedo.core.capture_manager import CaptureManager
from trust_wedo.core.diff_analyzer import DiffAnalyzer
from trust_wedo.validators.schema_validator import SchemaValidator


@click.group()
@click.version_option(version=__version__)
@click.option("--verbose", "-v", is_flag=True, help="顯示詳細日誌")
@click.option("--quiet", "-q", is_flag=True, help="只顯示錯誤訊息")
@click.pass_context
def main(ctx: click.Context, verbose: bool, quiet: bool) -> None:
    """Trust WEDO - Answer Trust Infrastructure for Generative Systems.
    
    把網站內容轉換為「AI 可評估、可拒絕、可引用」的答案物件。
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet


@main.command()
@click.argument("url")
@click.option("--output", "-o", default="output", help="輸出目錄")
@click.option("--max-pages", default=10, help="最大掃描頁面數")
@click.pass_context
def scan(ctx: click.Context, url: str, output: str, max_pages: int) -> None:
    """掃描網站內容並抽取基礎結構。
    
    輸出：output/site.json
    """
    click.echo(f"🔍 掃描網站: {url}")
    
    parser = SiteParser(url, max_pages=max_pages)
    result = asyncio.run(parser.scan())
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    site_json_path = output_path / "site.json"
    
    with open(site_json_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    click.echo(f"📁 已儲存至: {site_json_path}")
    
    validator = SchemaValidator()
    is_valid, error = validator.validate_file(site_json_path, "site")
    if is_valid:
        click.echo("✅ Schema 驗證成功")
    else:
        click.echo(f"❌ Schema 驗證失敗: {error}")
        ctx.exit(1)


@main.group()
@click.pass_context
def entity(ctx: click.Context) -> None:
    """實體相關指令。"""
    pass


@entity.command(name="score")
@click.argument("site_json", type=click.Path(exists=True))
@click.option("--output", "-o", default="output", help="輸出目錄")
@click.pass_context
def entity_score(ctx: click.Context, site_json: str, output: str) -> None:
    """計算實體信任評分。
    
    輸出：output/entity_profile.json
    """
    click.echo(f"📊 計算實體信任評分: {site_json}")
    
    with open(site_json) as f:
        site_data = json.load(f)
    
    scorer = EntityScorer(site_data)
    result = scorer.calculate_score(input_source=site_json)
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    entity_json_path = output_path / "entity_profile.json"
    
    with open(entity_json_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    click.echo(f"👤 已產生實體檔案: {entity_json_path}")
    click.echo(f"📈 信任評分 (EC): {result['entity_confidence']} ({result['eligibility']})")
    
    validator = SchemaValidator()
    is_valid, error = validator.validate_file(entity_json_path, "entity")
    if is_valid:
        click.echo("✅ Schema 驗證成功")
    else:
        click.echo(f"❌ Schema 驗證失敗: {error}")
        ctx.exit(1)


@main.group()
@click.pass_context
def afb(ctx: click.Context) -> None:
    """AFB 相關指令。"""
    pass


@afb.command(name="build")
@click.argument("page_html", type=click.Path(exists=True))
@click.option("--entity", "entity_file", required=True, type=click.Path(exists=True), help="實體信任檔案")
@click.option("--output", "-o", default="output", help="輸出目錄")
@click.pass_context
def afb_build(ctx: click.Context, page_html: str, entity_file: str, output: str) -> None:
    """產生 Answer-First Block。
    
    輸出：output/afb.json
    """
    click.echo(f"🎯 產生 AFB: {page_html}")
    
    with open(entity_file) as f:
        entity_profile = json.load(f)
    
    with open(page_html, encoding="utf-8") as f:
        html_content = f.read()
    
    builder = AFBBuilder(html_content, entity_profile)
    result = builder.build(input_source=page_html)
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    afb_json_path = output_path / "afb.json"
    
    with open(afb_json_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    click.echo(f"📄 已產生 AFB 檔案: {afb_json_path}")
    
    if result.get("eligibility") == "fail":
        click.echo(f"⚠️  實體信任分過低 (EC={result['confidence_signals']['entity_confidence']:.2f} < 0.60)，AFB 已標記為 fail")
    
    validator = SchemaValidator()
    is_valid, error = validator.validate_file(afb_json_path, "afb")
    if is_valid:
        click.echo("✅ Schema 驗證成功")
    else:
        click.echo(f"❌ Schema 驗證失敗: {error}")
        ctx.exit(1)


@main.group()
@click.pass_context
def citation(ctx: click.Context) -> None:
    """引用相關指令。"""
    pass


@citation.command(name="eval")
@click.argument("afb_json", type=click.Path(exists=True))
@click.option("--output", "-o", default="output", help="輸出目錄")
@click.pass_context
def citation_eval(ctx: click.Context, afb_json: str, output: str) -> None:
    """評估引用可信度。
    
    輸出：output/citation_eval.json
    """
    click.echo(f"📝 評估引用: {afb_json}")
    
    with open(afb_json) as f:
        afb_data = json.load(f)
    
    afb_id = afb_data.get("afb_id", "afb:unknown")
    
    # Try to find citations.json in the same directory
    citations_path = Path(afb_json).parent / "citations.json"
    if citations_path.exists():
        with open(citations_path) as f:
            citations = json.load(f)
    else:
        # Provide some dummy citations if none found for MVP demonstration
        click.echo("ℹ️  找不到 citations.json，使用示範資料")
        citations = [
            {"citation_id": "cite:001", "url": "https://trusted-source.org/fact", "status": "verified"},
            {"citation_id": "cite:002", "url": "https://twitter.com/someone/status/123", "status": "unverified"}
        ]
    
    evaluator = CitationEvaluator(afb_id, citations)
    result = evaluator.evaluate(input_source=afb_json)
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    citation_eval_json_path = output_path / "citation_eval.json"
    
    with open(citation_eval_json_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    click.echo(f"📋 已產生引用評估檔案: {citation_eval_json_path}")
    click.echo(f"⚖️  最終決策: {result['decision']}")
    
    validator = SchemaValidator()
    is_valid, error = validator.validate_file(citation_eval_json_path, "citation")
    if is_valid:
        click.echo("✅ Schema 驗證成功")
    else:
        click.echo(f"❌ Schema 驗證失敗: {error}")
        ctx.exit(1)


@main.group()
@click.pass_context
def graph(ctx: click.Context) -> None:
    """圖譜相關指令。"""
    pass


@graph.command(name="build")
@click.argument("bundle_dir", type=click.Path(exists=True))
@click.option("--output", "-o", default="output", help="輸出目錄")
@click.pass_context
def graph_build(ctx: click.Context, bundle_dir: str, output: str) -> None:
    """建立實體關係圖並檢測風險。
    
    輸出：output/entity_graph.json
    """
    click.echo(f"🕸️  建立關係圖: {bundle_dir}")
    
    bundle_path = Path(bundle_dir)
    bundle_data = {}
    
    files_to_load = {
        "entity": "entity_profile.json",
        "afb": "afb.json",
        "citation": "citation_eval.json"
    }
    
    for key, filename in files_to_load.items():
        file_path = bundle_path / filename
        if file_path.exists():
            with open(file_path) as f:
                bundle_data[key] = json.load(f)
        else:
            click.echo(f"⚠️  找不到 {filename}")
    
    builder = GraphBuilder(bundle_data)
    result = builder.build(input_source=bundle_dir)
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    graph_json_path = output_path / "entity_graph.json"
    
    with open(graph_json_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    click.echo(f"🔗 已產生關係圖檔案: {graph_json_path}")
    metrics = result['metrics']
    click.echo(f"📊 指標: 來源數={metrics['distinct_sources']}, 孤立={metrics['is_isolated']}, 單一來源風險={metrics['single_source_risk']}")
    
    validator = SchemaValidator()
    is_valid, error = validator.validate_file(graph_json_path, "graph")
    if is_valid:
        click.echo("✅ Schema 驗證成功")
    else:
        click.echo(f"❌ Schema 驗證失敗: {error}")
        ctx.exit(1)


@main.command()
@click.argument("afb_id")
@click.option("--ai-output", required=True, help="AI 的回答內容")
@click.option("--source", default="unknown", help="AI 來源名稱")
@click.option("--output", "-o", default="output/captures", help="輸出目錄")
@click.pass_context
def capture(ctx: click.Context, afb_id: str, ai_output: str, source: str, output: str) -> None:
    """捕獲 AI 輸出資料。
    
    輸出：output/captures/capture_<afb_id>_<source>_<timestamp>.json
    """
    click.echo(f"📥 捕獲 AI 輸出: {afb_id} (來源: {source})")
    
    manager = CaptureManager(output_dir=output)
    result = manager.capture(afb_id, ai_output, source)
    
    # Find the latest file in output directory
    latest_file = max(Path(output).glob("capture_*.json"), key=lambda p: p.stat().st_mtime)
    
    click.echo(f"📄 已儲存至: {latest_file}")
    
    validator = SchemaValidator()
    is_valid, error = validator.validate_file(latest_file, "capture")
    if is_valid:
        click.echo("✅ Schema 驗證成功")
    else:
        click.echo(f"❌ Schema 驗證失敗: {error}")
        ctx.exit(1)


@main.command()
@click.argument("afb_id")
@click.option("--captures-dir", default="output/captures", help="Capture 輸出目錄")
@click.option("--output", "-o", default="output/diffs", help="輸出目錄")
@click.pass_context
def diff(ctx: click.Context, afb_id: str, captures_dir: str, output: str) -> None:
    """比對 AFB 與 Capture 的差異。
    
    輸出：output/diffs/diff_<afb_id>_<timestamp>.json
    """
    click.echo(f"🔍 開始差異分析: {afb_id}")
    
    # 1. Load AFB
    afb_path = Path("output/afb.json") # Default for MVP
    if not afb_path.exists():
        click.echo(f"❌ 找不到 AFB 檔案: {afb_path}")
        ctx.exit(1)
        
    with open(afb_path) as f:
        afb_data = json.load(f)
        
    if afb_data.get("afb_id") != afb_id:
        click.echo(f"⚠️  警告: 檔案內的 AFB ID ({afb_data.get('afb_id')}) 與參數 ({afb_id}) 不符")
    
    # 2. Load related Captures
    captures = []
    for cap_file in Path(captures_dir).glob("capture_*.json"):
        with open(cap_file) as f:
            cap_data = json.load(f)
            if cap_data.get("afb_id") == afb_id:
                captures.append(cap_data)
                
    if not captures:
        click.echo(f"❌ 找不到與 {afb_id} 相關的 Capture 檔案")
        ctx.exit(1)
        
    click.echo(f"📂 找到 {len(captures)} 個相關 Capture")
    
    # 3. Analyze
    analyzer = DiffAnalyzer(afb_data, captures)
    result = analyzer.analyze(input_source=afb_id)
    
    # 4. Save
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_afb = afb_id.replace(":", "-")
    diff_json_path = output_path / f"diff_{clean_afb}_{timestamp}.json"
    
    with open(diff_json_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        
    click.echo(f"📄 已產生 Diff 檔案: {diff_json_path}")
    
    validator = SchemaValidator()
    is_valid, error = validator.validate_file(diff_json_path, "diff")
    if is_valid:
        click.echo("✅ Schema 驗證成功")
    else:
        click.echo(f"❌ Schema 驗證失敗: {error}")
        ctx.exit(1)


@main.command()
@click.argument("bundle_dir", type=click.Path(exists=True))
@click.option("--output", "-o", default="output", help="輸出目錄")
@click.option("--format", "report_format", type=click.Choice(["md", "json", "both"]), default="both", help="報告格式")
@click.pass_context
def report(ctx: click.Context, bundle_dir: str, output: str, report_format: str) -> None:
    """產生最終信任報告。
    
    輸出：output/trust-wedo-report.md, output/trust-wedo-report.json
    """
    click.echo(f"📋 產生報告: {bundle_dir}")
    
    generator = ReportGenerator(bundle_dir)
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    if report_format in ["json", "both"]:
        report_json = generator.generate_json()
        report_json_path = output_path / "trust-wedo-report.json"
        with open(report_json_path, "w") as f:
            json.dump(report_json, f, indent=2, ensure_ascii=False)
        click.echo(f"📄 已產生 JSON 報告: {report_json_path}")
        
    if report_format in ["md", "both"]:
        report_md = generator.generate_markdown()
        report_md_path = output_path / "trust-wedo-report.md"
        with open(report_md_path, "w") as f:
            f.write(report_md)
        click.echo(f"📄 已產生 Markdown 報告: {report_md_path}")


if __name__ == "__main__":
    main()
