"""CLI entry point for Trust WEDO."""

import click
from trust_wedo import __version__


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
    click.echo(f"📁 輸出目錄: {output}")
    click.echo(f"📄 最大頁面數: {max_pages}")
    click.echo("⚠️  此功能尚未實作")


@main.command()
@click.argument("site_json", type=click.Path(exists=True))
@click.option("--output", "-o", default="output", help="輸出目錄")
@click.pass_context
def entity(ctx: click.Context, site_json: str, output: str) -> None:
    """計算實體信任評分。
    
    輸出：output/entity_profile.json
    """
    click.echo(f"📊 計算實體信任評分: {site_json}")
    click.echo(f"📁 輸出目錄: {output}")
    click.echo("⚠️  此功能尚未實作")


@main.command()
@click.argument("page_html", type=click.Path(exists=True))
@click.option("--entity", required=True, type=click.Path(exists=True), help="實體信任檔案")
@click.option("--output", "-o", default="output", help="輸出目錄")
@click.pass_context
def afb(ctx: click.Context, page_html: str, entity: str, output: str) -> None:
    """產生 Answer-First Block。
    
    輸出：output/afb.json
    """
    click.echo(f"🎯 產生 AFB: {page_html}")
    click.echo(f"👤 實體檔案: {entity}")
    click.echo(f"📁 輸出目錄: {output}")
    click.echo("⚠️  此功能尚未實作")


@main.command()
@click.argument("afb_json", type=click.Path(exists=True))
@click.option("--output", "-o", default="output", help="輸出目錄")
@click.pass_context
def citation(ctx: click.Context, afb_json: str, output: str) -> None:
    """評估引用可信度。
    
    輸出：output/citation_eval.json
    """
    click.echo(f"📝 評估引用: {afb_json}")
    click.echo(f"📁 輸出目錄: {output}")
    click.echo("⚠️  此功能尚未實作")


@main.command()
@click.argument("bundle_dir", type=click.Path(exists=True))
@click.option("--output", "-o", default="output", help="輸出目錄")
@click.pass_context
def graph(ctx: click.Context, bundle_dir: str, output: str) -> None:
    """建立實體關係圖並檢測風險。
    
    輸出：output/entity_graph.json
    """
    click.echo(f"🕸️  建立關係圖: {bundle_dir}")
    click.echo(f"📁 輸出目錄: {output}")
    click.echo("⚠️  此功能尚未實作")


@main.command()
@click.argument("bundle_dir", type=click.Path(exists=True))
@click.option("--output", "-o", default="output", help="輸出目錄")
@click.option("--format", type=click.Choice(["md", "json", "both"]), default="both", help="報告格式")
@click.pass_context
def report(ctx: click.Context, bundle_dir: str, output: str, format: str) -> None:
    """產生最終信任報告。
    
    輸出：output/trust-wedo-report.md, output/trust-wedo-report.json
    """
    click.echo(f"📋 產生報告: {bundle_dir}")
    click.echo(f"📁 輸出目錄: {output}")
    click.echo(f"📄 格式: {format}")
    click.echo("⚠️  此功能尚未實作")


if __name__ == "__main__":
    main()
