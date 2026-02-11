import os
import requests
from fpdf import FPDF
from datetime import datetime
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

# Font Configuration
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/notosanstc/NotoSansTC-Regular.ttf"
FONT_PATH = "app/fonts/NotoSansTC-Regular.ttf"
FONT_FAMILY = "NotoSansTC"

def ensure_chinese_font():
    """Ensure Noto Sans TC font exists, download if missing."""
    if not os.path.exists(FONT_PATH):
        try:
            os.makedirs(os.path.dirname(FONT_PATH), exist_ok=True)
            logger.info(f"Downloading font from {FONT_URL}...")
            response = requests.get(FONT_URL, timeout=30)
            response.raise_for_status()
            with open(FONT_PATH, "wb") as f:
                f.write(response.content)
            logger.info("Font downloaded successfully.")
        except Exception as e:
            logger.error(f"Failed to download Chinese font: {e}")
            # Fallback handling might be needed here, or raise error
            raise RuntimeError("Chinese font required for PDF generation")

class TrustWedoReportPDF(FPDF):
    def __init__(self, report_data: dict, dimensions: dict):
        super().__init__()
        self.report = report_data
        self.dimensions = dimensions
        self.url = report_data.get("url", "Unknown URL")
        self.domain = urlparse(self.url).netloc.replace("www.", "")
        self.date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Initialize Font
        ensure_chinese_font()
        self.add_font(FONT_FAMILY, "", FONT_PATH)
        self.add_font(FONT_FAMILY, "B", FONT_PATH) # Bold mapping to Regular for now if bold missing
        
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font(FONT_FAMILY, "", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Trust WEDO AI Report - {self.domain} ({self.date_str})", 0, 1, "R")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font(FONT_FAMILY, "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def chapter_title(self, title):
        self.set_font(FONT_FAMILY, "", 24)
        self.set_text_color(30, 58, 138)  # Brand Navy
        self.cell(0, 15, title, 0, 1, "L")
        self.ln(5)

    def chapter_subtitle(self, title):
        self.set_font(FONT_FAMILY, "", 16)
        self.set_text_color(59, 130, 246) # Brand Blue
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(2)

    def add_summary_page(self):
        self.add_page()
        
        # Title
        self.chapter_title("AI 信任度健檢報告")
        
        # Score Card
        self.set_fill_color(243, 244, 246) # Gray-100
        self.rect(10, 40, 190, 60, 'F')
        
        self.set_xy(20, 50)
        self.set_font(FONT_FAMILY, "", 40)
        self.set_text_color(30, 58, 138)
        self.cell(60, 20, f"{self.dimensions.get('total_score', 0)}/100", 0, 0)
        
        self.set_font(FONT_FAMILY, "", 20)
        self.cell(50, 20, f"等級: {self.report.get('summary', {}).get('grade', 'N/A')}", 0, 1)
        
        self.set_xy(20, 70)
        self.set_font(FONT_FAMILY, "", 12)
        self.set_text_color(75, 85, 99) # Gray-600
        conclusion = self.report.get("summary", {}).get("conclusion", "無結論")
        self.multi_cell(170, 8, conclusion)
        
        self.ln(20)

    def add_dimensions_page(self):
        self.add_page()
        self.chapter_title("五大維度分析")
        
        dims = self.dimensions.get("dimensions", {})
        
        for key, data in dims.items():
            name_map = {
                'discoverability': 'AI 可發現性',
                'identity': '身分可信度',
                'structure': '內容結構化',
                'social': '社群信任',
                'technical': '技術基礎'
            }
            name = name_map.get(key, key)
            score = data.get("score", 0)
            max_score = data.get("max", 0)
            percentage = int((score / max_score) * 100) if max_score > 0 else 0
            
            self.set_font(FONT_FAMILY, "", 14)
            self.set_text_color(0, 0, 0)
            self.cell(60, 10, f"{name}", 0, 0)
            
            # Progress Bar Background
            self.set_fill_color(229, 231, 235)
            self.rect(80, self.get_y() + 2, 100, 6, 'F')
            
            # Progress Bar Fill
            if percentage < 60:
                self.set_fill_color(239, 68, 68) # Red
            elif percentage < 80:
                self.set_fill_color(245, 158, 11) # Yellow
            else:
                self.set_fill_color(34, 197, 94) # Green
                
            self.rect(80, self.get_y() + 2, percentage, 6, 'F')
            
            self.set_font(FONT_FAMILY, "", 12)
            self.cell(30, 10, f"{score}/{max_score}", 0, 1, "R")
            self.ln(5)

    def add_quick_wins(self):
        quick_wins = self.dimensions.get("quick_wins", [])
        if not quick_wins:
            return
            
        self.add_page()
        self.chapter_title("快速勝利 (Quick Wins)")
        self.set_font(FONT_FAMILY, "", 12)
        self.multi_cell(0, 8, "以下建議能以最小投入帶來最大分數提升：")
        self.ln(5)
        
        for idx, win in enumerate(quick_wins, 1):
            self.set_font(FONT_FAMILY, "", 14)
            self.set_text_color(30, 58, 138)
            self.cell(0, 10, f"{idx}. {win.get('title')}", 0, 1)
            
            self.set_font(FONT_FAMILY, "", 12)
            self.set_text_color(75, 85, 99)
            impact = win.get('impact', '')
            effort = win.get('effort', '')
            self.cell(0, 8, f"影響: {impact} | 難度: {effort}", 0, 1)
            
            self.multi_cell(0, 8, win.get('description', ''))
            self.ln(5)

    def generate(self) -> bytes:
        self.add_summary_page()
        self.add_dimensions_page()
        self.add_quick_wins()
        return self.output()

def generate_report_pdf(report_data: dict, dimensions: dict) -> tuple[str, bytes]:
    """
    Generate PDF for the report.
    Returns (filename, pdf_content_bytes)
    """
    pdf = TrustWedoReportPDF(report_data, dimensions)
    content = pdf.generate()
    
    # Sanitize URL for filename (remove protocol, replace slashes with underscores)
    safe_url = report_data.get("url", "").replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "").strip("_")
    # Truncate if too long to avoid filesystem errors
    if len(safe_url) > 50:
        safe_url = safe_url[:50]
        
    filename = f"Trust_WEDO_{safe_url}_{pdf.date_str}.pdf"
    return filename, content
