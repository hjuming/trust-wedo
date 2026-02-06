#!/usr/bin/env bash
set -euo pipefail

# Trust WEDO MVP 驗收腳本
# 用途：一鍵執行完整 CLI 流程並驗證輸出

echo "🚀 Trust WEDO MVP 驗收測試"
echo "======================================"

# 設定輸出目錄
OUT=${1:-output}
echo "📁 輸出目錄: $OUT"

# 清理舊輸出
rm -rf "$OUT"
mkdir -p "$OUT"

# 確保在虛擬環境中
if [ -z "${VIRTUAL_ENV:-}" ]; then
    echo "⚠️  警告：未偵測到虛擬環境，請先執行 'source .venv/bin/activate'"
    exit 1
fi

# 檢查 tw 指令是否可用
if ! command -v tw &> /dev/null; then
    echo "❌ 錯誤：找不到 tw 指令，請先執行 'pip install -e .'"
    exit 1
fi

echo ""
echo "步驟 1/6: 掃描網站"
echo "--------------------------------------"
# 使用 file:// URL 指向 sample_page.html（避免依賴外部網站）
SAMPLE_URL="file://$(pwd)/samples/sample_page.html"
tw scan "$SAMPLE_URL" -o "$OUT" --max-pages 3 || {
    echo "❌ scan 失敗"
    exit 1
}
echo "✅ scan 完成"

echo ""
echo "步驟 2/6: 計算實體信任評分"
echo "--------------------------------------"
tw entity score "$OUT/site.json" -o "$OUT" || {
    echo "❌ entity score 失敗"
    exit 1
}
echo "✅ entity score 完成"

echo ""
echo "步驟 3/6: 產生 AFB"
echo "--------------------------------------"
tw afb build samples/sample_page.html --entity "$OUT/entity_profile.json" -o "$OUT" || {
    echo "❌ afb build 失敗"
    exit 1
}
echo "✅ afb build 完成"

echo ""
echo "步驟 4/6: 評估引用"
echo "--------------------------------------"
tw citation eval "$OUT/afb.json" -o "$OUT" || {
    echo "❌ citation eval 失敗"
    exit 1
}
echo "✅ citation eval 完成"

echo ""
echo "步驟 5/6: 建立關係圖"
echo "--------------------------------------"
tw graph build "$OUT" -o "$OUT" || {
    echo "❌ graph build 失敗"
    exit 1
}
echo "✅ graph build 完成"

echo ""
echo "步驟 6/6: 產生報告"
echo "--------------------------------------"
tw report "$OUT" -o "$OUT" || {
    echo "❌ report 失敗"
    exit 1
}
echo "✅ report 完成"

echo ""
echo "步驟 7/7: 捕獲 AI 輸出 (Phase 3)"
echo "--------------------------------------"
tw capture afb:trust-wedo:definition --ai-output "Trust WEDO 是一個信任工程系統" --source "test-ai" -o "$OUT/captures" || {
    echo "❌ capture 失敗"
    exit 1
}
echo "✅ capture 完成"

echo ""
echo "步驟 8/8: 差異分析 (Phase 4)"
echo "--------------------------------------"
tw diff afb:trust-wedo:definition --captures-dir "$OUT/captures" -o "$OUT/diffs" || {
    echo "❌ diff 失敗"
    exit 1
}
echo "✅ diff 完成"

echo ""
echo "======================================"
echo "📋 驗證 JSON Schema"
echo "======================================"

# Schema 驗證（使用 Python jsonschema）
python3 -c "
import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

schemas = {
    'site.json': 'schemas/site_scan.schema.json',
    'entity_profile.json': 'schemas/entity_profile.schema.json',
    'afb.json': 'schemas/afb.schema.json',
    'citation_eval.json': 'schemas/citation_eval.schema.json',
    'entity_graph.json': 'schemas/entity_graph.schema.json',
}

output_dir = Path('$OUT')
failed = False

for output_file, schema_file in schemas.items():
    output_path = output_dir / output_file
    schema_path = Path(schema_file)
    
    if not output_path.exists():
        print(f'❌ {output_file} 不存在')
        failed = True
        continue
    
    try:
        with open(output_path) as f:
            data = json.load(f)
        with open(schema_path) as f:
            schema = json.load(f)
        
        validate(instance=data, schema=schema)
        print(f'✅ {output_file} 通過 schema 驗證')
    except ValidationError as e:
        print(f'❌ {output_file} schema 驗證失敗: {e.message}')
        failed = True
    except Exception as e:
        print(f'❌ {output_file} 驗證時發生錯誤: {str(e)}')
        failed = True

# 驗證 Capture
capture_files = list((output_dir / 'captures').glob('*.json'))
if not capture_files:
    print('❌ 未發現 capture 檔案')
    failed = True
else:
    capture_schema_path = Path('schemas/capture.schema.json')
    with open(capture_schema_path) as f:
        capture_schema = json.load(f)
    for cap_file in capture_files:
        try:
            with open(cap_file) as f:
                data = json.load(f)
            validate(instance=data, schema=capture_schema)
            print(f'✅ {cap_file.name} 通過 schema 驗證')
        except Exception as e:
            print(f'❌ {cap_file.name} 驗證失敗: {str(e)}')
            failed = True

# 驗證 Diff
diff_files = list((output_dir / 'diffs').glob('*.json'))
if not diff_files:
    print('❌ 未發現 diff 檔案')
    failed = True
else:
    diff_schema_path = Path('schemas/diff.schema.json')
    with open(diff_schema_path) as f:
        diff_schema = json.load(f)
    for diff_file in diff_files:
        try:
            with open(diff_file) as f:
                data = json.load(f)
            validate(instance=data, schema=diff_schema)
            print(f'✅ {diff_file.name} 通過 schema 驗證')
        except Exception as e:
            print(f'❌ {diff_file.name} 驗證失敗: {str(e)}')
            failed = True

if failed:
    sys.exit(1)
" || {
    echo ""
    echo "❌ Schema 驗證失敗"
    exit 1
}

echo ""
echo "======================================"
echo "✅ MVP 驗收測試通過！"
echo "======================================"
echo ""
echo "產生的檔案："
ls -lh "$OUT"
