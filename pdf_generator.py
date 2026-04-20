"""
Cairo Marble ERP - PDF Generator
==================================
Generates professional Arabic RTL PDF documents using ReportLab.
Handles: Quotes, Invoices, Salary Slips, Driver Reports, Project Reports, Finance Statements.

Arabic reshaping (optional, greatly improves Arabic rendering):
    pip install arabic-reshaper python-bidi

Arabic fonts (optional, improves output quality):
    Place Cairo-Regular.ttf + Cairo-Bold.ttf  (or Amiri-Regular.ttf + Amiri-Bold.ttf)
    inside a  fonts/  sub-folder next to this file.
    Download free: https://fonts.google.com/specimen/Cairo
"""

import os
from datetime import date
from typing import List, Dict

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─────────────────────────────────────────────────────────────────────
# Page geometry  (A4 = 595 pt wide, 1.5 cm margins each side)
# usable width ≈ 510 pt — all table colWidths must sum to exactly this
# ─────────────────────────────────────────────────────────────────────
_MARGIN = 1.5 * cm
_W      = A4[0] - 2 * _MARGIN   # ≈ 510.24 pt


# ─────────────────────────────────────────────────────────────────────
# Arabic text reshaping
# ─────────────────────────────────────────────────────────────────────
def _ar(text: str) -> str:
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(str(text)))
    except ImportError:
        return str(text)


# ─────────────────────────────────────────────────────────────────────
# Brand colours
# ─────────────────────────────────────────────────────────────────────
GREEN      = colors.HexColor("#00713D")
GREEN_LITE = colors.HexColor("#E8F5E9")
GRAY       = colors.HexColor("#BDBDBD")
WHITE      = colors.white
BLACK      = colors.black

COMPANY_NAME    = "Cairo Marblestone & Marble Works"
COMPANY_NAME_AR = "كايرو ماربل لأعمال الرخام والحجر"
COMPANY_ADDRESS = "معسكر الشركات - العين - أبوظبي"
COMPANY_PHONE   = "+971543495414"
COMPANY_EMAIL   = "cairo.marble1@gmail.com"

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────
# Font registration
# ─────────────────────────────────────────────────────────────────────
_FR = "Helvetica"
_FB = "Helvetica-Bold"

def _register_fonts():
    global _FR, _FB
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
    candidates = [
        ("Cairo-Regular.ttf",  "Cairo-Bold.ttf",  "CairoAr", "CairoArB"),
        ("Amiri-Regular.ttf",  "Amiri-Bold.ttf",  "AmiriAr", "AmiriArB"),
    ]
    dirs = [
        base,
        "/usr/share/fonts/truetype/arabic",
        "/usr/share/fonts/truetype/amiri",
        "/usr/share/fonts/truetype/fonts-arabeyes",
        "/System/Library/Fonts/Supplemental",
        "C:/Windows/Fonts",
    ]
    for reg_name, bold_name, ra, ba in candidates:
        for d in dirs:
            rp = os.path.join(d, reg_name)
            if os.path.exists(rp):
                try:
                    pdfmetrics.registerFont(TTFont(ra, rp))
                    _FR = ra
                    bp = os.path.join(d, bold_name)
                    if os.path.exists(bp):
                        pdfmetrics.registerFont(TTFont(ba, bp))
                        _FB = ba
                    return
                except Exception:
                    pass

_register_fonts()


# ─────────────────────────────────────────────────────────────────────
# Style factory — zero padding on paragraph itself; padding lives in TableStyle
# ─────────────────────────────────────────────────────────────────────
def _mk(name, size=9, bold=False, align=TA_RIGHT, color=BLACK, leading=13):
    return ParagraphStyle(
        name, fontName=(_FB if bold else _FR), fontSize=size,
        alignment=align, textColor=color, leading=leading,
        leftPadding=0, rightPadding=0, spaceBefore=0, spaceAfter=0,
    )

S_TITLE = _mk("title", 18, True,  TA_CENTER, GREEN,  22)
S_SUB   = _mk("sub",   11, True,  TA_CENTER, GREEN,  14)
S_BODY  = _mk("body",   9, False, TA_RIGHT,  BLACK)
S_BODYL = _mk("bodyl",  9, False, TA_LEFT,   BLACK)
S_BODYC = _mk("bodyc",  9, False, TA_CENTER, BLACK)
S_BOLD  = _mk("bold",   9, True,  TA_RIGHT,  BLACK)
S_WHC   = _mk("whc",    9, True,  TA_CENTER, WHITE)
S_WHR   = _mk("whr",    9, True,  TA_RIGHT,  WHITE)
S_WHL   = _mk("whl",   11, True,  TA_LEFT,   WHITE)
S_SM    = _mk("sm",     8, False, TA_CENTER, GRAY)
S_COEN  = _mk("coen",  12, True,  TA_RIGHT,  GREEN,  15)
S_COAR  = _mk("coar",  12, True,  TA_LEFT,   GREEN,  15)
S_CI    = _mk("ci",     8, False, TA_RIGHT,  BLACK)
S_CIAR  = _mk("ciar",  8,  False, TA_LEFT,   BLACK)


def _p(text, style=None) -> Paragraph:
    return Paragraph(_ar(str(text)), style or S_BODY)


# ─────────────────────────────────────────────────────────────────────
# Shared table-style pieces
# ─────────────────────────────────────────────────────────────────────
_PAD = [
    ("TOPPADDING",    (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING",   (0, 0), (-1, -1), 5),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
]
_HDR = [
    ("BACKGROUND", (0, 0), (-1, 0), GREEN),
    ("FONTNAME",   (0, 0), (-1, 0), _FB),
]
_ALT = [("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GREEN_LITE])]
_GRID = [("GRID", (0, 0), (-1, -1), 0.5, GRAY)]


def _ts(*extras):
    return TableStyle(_PAD + _GRID + list(extras))


def _ts_data(*extras):
    return TableStyle(_PAD + _GRID + _HDR + _ALT + list(extras))


# ─────────────────────────────────────────────────────────────────────
# PDF Generator
# ─────────────────────────────────────────────────────────────────────
class PDFGenerator:
    """Generate professional PDFs for all Cairo Marble ERP document types."""

    # ── private builders ──────────────────────────────────────────

    @staticmethod
    def _doc(filename: str):
        path = os.path.join(OUTPUT_DIR, filename)
        doc  = SimpleDocTemplate(
            path, pagesize=A4,
            rightMargin=_MARGIN, leftMargin=_MARGIN,
            topMargin=_MARGIN,   bottomMargin=_MARGIN,
        )
        return doc, path

    @staticmethod
    def _company_header() -> Table:
        data = [
            [_p(COMPANY_NAME, S_COEN),                               _p(COMPANY_NAME_AR, S_COAR)],
            [_p(f"Tel: {COMPANY_PHONE}  |  {COMPANY_EMAIL}", S_CI),  _p(COMPANY_ADDRESS, S_CIAR)],
        ]
        t = Table(data, colWidths=[_W * 0.50, _W * 0.50])
        t.setStyle(TableStyle([
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 0),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
            ("LINEBELOW",     (0, -1), (-1, -1), 1.5, GREEN),
        ]))
        return t

    @staticmethod
    def _meta_table(left: Dict, right: Dict) -> Table:
        """
        4-column label/value table.
        Columns: [right_val | right_label | left_val | left_label]
        Using 4 columns (not 5) avoids the tiny-separator crash in ReportLab.
        """
        li = list(left.items())
        ri = list(right.items())
        n  = max(len(li), len(ri), 1)
        while len(li) < n: li.append(("", ""))
        while len(ri) < n: ri.append(("", ""))

        rows = []
        for (rl, rv), (ll, lv) in zip(ri, li):
            rows.append([
                _p(rv, S_BODYL), _p(rl, S_BOLD),
                _p(lv, S_BODYL), _p(ll, S_BOLD),
            ])

        t = Table(rows, colWidths=[_W*0.28, _W*0.22, _W*0.28, _W*0.22])
        t.setStyle(_ts())
        return t

    @staticmethod
    def _items_table(items: List[Dict]) -> Table:
        """Standard 5-column invoice/quote line-items table."""
        hdr = [_p("المبلغ", S_WHC), _p("الضرائب", S_WHC),
               _p("سعر الوحدة", S_WHC), _p("الكمية", S_WHC), _p("الوصف", S_WHR)]
        rows = [hdr]
        for it in items:
            rows.append([
                _p(f"{it.get('amount',0):,.2f}",      S_BODYC),
                _p(f"{it.get('tax_rate',0):.1f}%",    S_BODYC),
                _p(f"{it.get('unit_price',0):,.2f}",  S_BODYC),
                _p(f"{it.get('quantity',0):g}",        S_BODYC),
                _p(it.get("description", ""),           S_BODY),
            ])
        t = Table(rows, colWidths=[_W*.18, _W*.11, _W*.17, _W*.11, _W*.43])
        t.setStyle(_ts_data())
        return t

    @staticmethod
    def _total_bar(amount: float, label: str = "الإجمالي", currency: str = "AED") -> Table:
        data = [[_p(f"{amount:,.2f} {currency}", S_WHL), _p(label, S_WHR)]]
        t = Table(data, colWidths=[_W * 0.50, _W * 0.50])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), GREEN),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ]))
        return t

    @staticmethod
    def _kv_table(pairs: List[tuple]) -> Table:
        rows = [[_p(k, S_BOLD), _p(v, S_BODYL)] for k, v in pairs]
        t = Table(rows, colWidths=[_W * 0.55, _W * 0.45])
        t.setStyle(_ts_data())
        return t

    @staticmethod
    def _footer() -> list:
        return [
            Spacer(1, 16),
            HRFlowable(width="100%", thickness=0.8, color=GRAY),
            Spacer(1, 4),
            _p(f"{COMPANY_EMAIL}  |  {COMPANY_PHONE}", S_SM),
        ]

    @classmethod
    def _story(cls, title_ar: str, serial: str,
               left_meta: Dict, right_meta: Dict, body: list) -> list:
        s = []
        s.append(cls._company_header())
        s.append(Spacer(1, 10))
        s.append(_p(title_ar, S_TITLE))
        s.append(_p(serial,   S_SUB))
        s.append(Spacer(1, 8))
        s.append(cls._meta_table(left_meta, right_meta))
        s.append(Spacer(1, 10))
        s.extend(body)
        s.extend(cls._footer())
        return s

    # ── public API ────────────────────────────────────────────────

    def export_quote(self, quote: Dict, items: List[Dict], client_name: str) -> str:
        doc, path = self._doc(f"quote_{quote.get('serial','Q')}.pdf")
        body = [self._items_table(items), Spacer(1, 4),
                self._total_bar(quote.get("total", 0))]
        if quote.get("notes"):
            body += [Spacer(1, 8), _p(f"ملاحظات: {quote['notes']}", S_BODY)]
        doc.build(self._story(
            "عرض سعر", quote.get("serial", ""),
            left_meta={
                "تاريخ عرض السعر:": quote.get("quote_date", ""),
                "انتهاء الصلاحية:": quote.get("expiry_date", ""),
            },
            right_meta={
                "العميل:":         client_name,
                "مندوب المبيعات:": quote.get("salesperson", ""),
            },
            body=body,
        ))
        return path

    def export_invoice(self, invoice: Dict, items: List[Dict], client_name: str) -> str:
        doc, path = self._doc(f"invoice_{invoice.get('serial','INV')}.pdf")
        paid      = invoice.get("paid_amount", 0)
        remaining = invoice.get("total", 0) - paid
        status_ar = {"unpaid": "غير مسدد", "paid": "مسدد", "partial": "جزئي"}.get(
            invoice.get("status", ""), "")
        body = [
            self._items_table(items), Spacer(1, 4),
            self._total_bar(invoice.get("total", 0)),
            Spacer(1, 6),
            self._kv_table([
                ("المبلغ المدفوع:", f"{paid:,.2f} AED"),
                ("المبلغ المتبقي:", f"{remaining:,.2f} AED"),
            ]),
        ]
        if invoice.get("notes"):
            body += [Spacer(1, 8), _p(f"ملاحظات: {invoice['notes']}", S_BODY)]
        doc.build(self._story(
            "فاتورة", invoice.get("serial", ""),
            left_meta={
                "تاريخ الفاتورة:":  invoice.get("invoice_date", ""),
                "تاريخ الاستحقاق:": invoice.get("due_date", ""),
                "الحالة:":           status_ar,
            },
            right_meta={"العميل:": client_name},
            body=body,
        ))
        return path

    def export_salary_slip(self, employee: Dict, salary_data: Dict, month: str) -> str:
        doc, path = self._doc(f"salary_{employee.get('id',0)}_{month}.pdf")
        body = [
            self._kv_table([
                ("الراتب الأساسي:",         f"{salary_data.get('base_salary',0):,.2f} AED"),
                ("أيام الحضور:",            str(salary_data.get("present_days", 0))),
                ("أيام الغياب:",            str(salary_data.get("absent_days", 0))),
                ("ساعات إضافية:",           str(salary_data.get("overtime_hours", 0))),
                ("بدل الساعات الإضافية:",   f"{salary_data.get('overtime_pay',0):,.2f} AED"),
                ("خصم الغياب:",             f"- {salary_data.get('deductions',0):,.2f} AED"),
                ("خصم السلفة:",             f"- {salary_data.get('advance_deduction',0):,.2f} AED"),
            ]),
            Spacer(1, 4),
            self._total_bar(salary_data.get("net_salary", 0), "صافي الراتب"),
        ]
        doc.build(self._story(
            "قسيمة راتب", f"الشهر: {month}",
            left_meta={
                "الوظيفة:":       employee.get("job_title", ""),
                "تاريخ التعيين:": employee.get("hire_date", ""),
            },
            right_meta={"الموظف:": employee.get("name", "")},
            body=body,
        ))
        return path

    def export_driver_report(self, driver: Dict, trips: List[Dict],
                              from_date: str = "", to_date: str = "") -> str:
        doc, path = self._doc(f"driver_{driver.get('id',0)}_report.pdf")
        hdr  = [_p("المبلغ", S_WHC), _p("الوجهة", S_WHC), _p("التاريخ", S_WHC)]
        rows = [hdr]
        total = 0.0
        for trip in trips:
            rows.append([
                _p(f"{trip.get('price',0):,.2f} AED", S_BODYC),
                _p(trip.get("destination", ""),         S_BODY),
                _p(trip.get("trip_date", ""),            S_BODYC),
            ])
            total += trip.get("price", 0)
        t = Table(rows, colWidths=[_W*0.25, _W*0.50, _W*0.25])
        t.setStyle(_ts_data())
        body = [t, Spacer(1, 4), self._total_bar(total)]
        doc.build(self._story(
            "تقرير سائق", driver.get("name", ""),
            left_meta={"الفترة من:": from_date, "إلى:": to_date},
            right_meta={
                "الهاتف:": driver.get("phone", ""),
                "الرخصة:": driver.get("license", ""),
            },
            body=body,
        ))
        return path

    def export_project_report(self, project: Dict, materials: List[Dict]) -> str:
        doc, path = self._doc(f"project_{project.get('id',0)}_report.pdf")
        hdr  = [_p("الإجمالي", S_WHC), _p("سعر الوحدة", S_WHC),
                _p("الكمية", S_WHC), _p("التاريخ", S_WHC), _p("الوصف", S_WHR)]
        rows = [hdr]
        for m in materials:
            rows.append([
                _p(f"{m.get('amount',0):,.2f}",     S_BODYC),
                _p(f"{m.get('unit_price',0):,.2f}", S_BODYC),
                _p(f"{m.get('quantity',0):g}",       S_BODYC),
                _p(m.get("entry_date", ""),           S_BODYC),
                _p(m.get("description", ""),          S_BODY),
            ])
        t = Table(rows, colWidths=[_W*.18, _W*.17, _W*.12, _W*.15, _W*.38])
        t.setStyle(_ts_data())
        body = [t, Spacer(1, 4), self._total_bar(project.get("total_cost", 0))]
        if project.get("notes"):
            body += [Spacer(1, 8), _p(f"ملاحظات: {project['notes']}", S_BODY)]
        doc.build(self._story(
            "تقرير مشروع", project.get("name", ""),
            left_meta={
                "تاريخ البداية:": project.get("start_date", ""),
                "تاريخ النهاية:": project.get("end_date", ""),
            },
            right_meta={
                "صاحب المشروع:": project.get("owner", ""),
                "الحالة:":        project.get("status", ""),
            },
            body=body,
        ))
        return path

    def export_finance_statement(self, entries: List[Dict], summary: Dict,
                                  title: str = "كشف حساب مالي", period: str = "") -> str:
        doc, path = self._doc(f"finance_{date.today().isoformat()}.pdf")
        hdr  = [_p("المبلغ", S_WHC), _p("النوع", S_WHC),
                _p("المصدر", S_WHC), _p("التاريخ", S_WHC), _p("الوصف", S_WHR)]
        rows = [hdr]
        for e in entries:
            cat_ar = "إيراد" if e.get("category") == "revenue" else "مصروف"
            rows.append([
                _p(f"{e.get('amount',0):,.2f}", S_BODYC),
                _p(cat_ar,                       S_BODYC),
                _p(e.get("source", ""),          S_BODYC),
                _p(e.get("entry_date", ""),      S_BODYC),
                _p(e.get("description", ""),     S_BODY),
            ])
        t = Table(rows, colWidths=[_W*.16, _W*.11, _W*.14, _W*.15, _W*.44])
        t.setStyle(_ts_data())
        body = [t, Spacer(1, 4), self._total_bar(summary.get("profit", 0), "صافي الربح")]
        doc.build(self._story(
            title, period,
            left_meta={
                "إجمالي الإيرادات:": f"{summary.get('revenues',0):,.2f} AED",
                "إجمالي المصروفات:": f"{summary.get('expenses',0):,.2f} AED",
            },
            right_meta={"صافي الربح:": f"{summary.get('profit',0):,.2f} AED"},
            body=body,
        ))
        return path
