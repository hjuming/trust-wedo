"""Schema 驗證工具模組"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

from jsonschema import validate, ValidationError


class SchemaValidator:
    """JSON Schema 驗證器"""

    def __init__(self, schema_dir: str = "schemas"):
        self.schema_dir = Path(schema_dir)
        self.schemas: Dict[str, dict] = {}
        self._load_schemas()

    def _load_schemas(self) -> None:
        """載入所有 schema 檔案"""
        schema_files = {
            "site": "site_scan.schema.json",
            "entity": "entity_profile.schema.json",
            "afb": "afb.schema.json",
            "citation": "citation_eval.schema.json",
            "graph": "entity_graph.schema.json",
        }

        for name, filename in schema_files.items():
            schema_path = self.schema_dir / filename
            if schema_path.exists():
                with open(schema_path) as f:
                    self.schemas[name] = json.load(f)

    def validate_file(self, file_path: Path, schema_name: str) -> Tuple[bool, str]:
        """驗證單一檔案

        Args:
            file_path: 要驗證的檔案路徑
            schema_name: schema 名稱 (site/entity/afb/citation/graph)

        Returns:
            (是否通過, 錯誤訊息)
        """
        if schema_name not in self.schemas:
            return False, f"找不到 schema: {schema_name}"

        if not file_path.exists():
            return False, f"檔案不存在: {file_path}"

        try:
            with open(file_path) as f:
                data = json.load(f)

            validate(instance=data, schema=self.schemas[schema_name])
            return True, ""
        except ValidationError as e:
            return False, f"Schema 驗證失敗: {e.message}"
        except json.JSONDecodeError as e:
            return False, f"JSON 格式錯誤: {str(e)}"
        except Exception as e:
            return False, f"驗證時發生錯誤: {str(e)}"

    def validate_bundle(self, bundle_dir: str) -> List[Tuple[str, bool, str]]:
        """驗證整個 bundle 目錄

        Args:
            bundle_dir: bundle 目錄路徑

        Returns:
            [(檔案名稱, 是否通過, 錯誤訊息), ...]
        """
        bundle_path = Path(bundle_dir)
        results = []

        file_schema_mapping = {
            "site.json": "site",
            "entity_profile.json": "entity",
            "afb.json": "afb",
            "citation_eval.json": "citation",
            "entity_graph.json": "graph",
        }

        for filename, schema_name in file_schema_mapping.items():
            file_path = bundle_path / filename
            is_valid, error_msg = self.validate_file(file_path, schema_name)
            results.append((filename, is_valid, error_msg))

        return results


def validate_all(bundle_dir: str) -> int:
    """驗證所有檔案並輸出結果

    Args:
        bundle_dir: bundle 目錄路徑

    Returns:
        退出碼 (0: 成功, 1: 失敗)
    """
    validator = SchemaValidator()
    results = validator.validate_bundle(bundle_dir)

    print(f"\n📋 驗證 {bundle_dir} 中的 JSON 檔案")
    print("=" * 50)

    all_passed = True
    for filename, is_valid, error_msg in results:
        if is_valid:
            print(f"✅ {filename} 通過驗證")
        else:
            print(f"❌ {filename} 驗證失敗")
            if error_msg:
                print(f"   錯誤: {error_msg}")
            all_passed = False

    print("=" * 50)
    if all_passed:
        print("✅ 所有檔案都通過驗證")
        return 0
    else:
        print("❌ 部分檔案驗證失敗")
        return 1


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python -m trust_wedo.validators.schema_validator <bundle_dir>")
        sys.exit(1)

    exit_code = validate_all(sys.argv[1])
    sys.exit(exit_code)
