"""
Cairo Marble ERP — Premium Enterprise UI
==========================================
main.py  |  PyQt6 Application Entry Point

Design: "Refined Stone" — Forest Green (#1B5E20) on Soft Neutral (#F0F2F5)
RTL Arabic-first layout. Every module in a scrollable card-based layout.

Run:  python main.py
Deps: pip install PyQt6 reportlab arabic-reshaper python-bidi
"""

import sys
import os
from datetime import date

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame, QSizePolicy,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog,
    QLineEdit, QFormLayout, QComboBox, QTextEdit, QDoubleSpinBox,
    QSpinBox, QDateEdit, QMessageBox, QScrollArea, QSplitter,
    QGroupBox, QTabWidget, QAbstractItemView, QGridLayout,
    QSpacerItem, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import (
    Qt, QDate, QSize, pyqtSignal, QTimer, QPropertyAnimation,
    QEasingCurve, QPoint, QRect
)
from PyQt6.QtGui import (
    QColor, QFont, QIcon, QPixmap, QPainter, QLinearGradient,
    QBrush, QPen, QCursor
)

# ── Local modules ──────────────────────────────────────────────────────
from db_manager import DatabaseManager
from pdf_generator import PDFGenerator
from styles import (
    apply_app_styles, COLORS as C, FONTS as F, ICONS,
    make_btn, make_label, make_input, make_date,
    make_card, make_divider, make_scroll_area, make_action_bar
)

# ── Singletons ─────────────────────────────────────────────────────────
DB  = DatabaseManager()
PDF = PDFGenerator()

RTL = Qt.LayoutDirection.RightToLeft


# ═══════════════════════════════════════════════════════════════════════
# SHADOW EFFECT FACTORY
# ═══════════════════════════════════════════════════════════════════════

def card_shadow(blur: int = 18, offset_y: int = 4,
                opacity: float = 0.10) -> QGraphicsDropShadowEffect:
    eff = QGraphicsDropShadowEffect()
    eff.setBlurRadius(blur)
    eff.setOffset(0, offset_y)
    eff.setColor(QColor(0, 0, 0, int(opacity * 255)))
    return eff


# ═══════════════════════════════════════════════════════════════════════
# REUSABLE WIDGET PRIMITIVES
# ═══════════════════════════════════════════════════════════════════════

def rtl(widget: QWidget) -> QWidget:
    widget.setLayoutDirection(RTL)
    return widget


def make_table(columns: list) -> QTableWidget:
    t = QTableWidget()
    t.setColumnCount(len(columns))
    t.setHorizontalHeaderLabels(columns)
    t.setLayoutDirection(RTL)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    t.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    t.setAlternatingRowColors(True)
    t.setShowGrid(True)
    t.verticalHeader().setVisible(False)
    t.setFrameShape(QFrame.Shape.NoFrame)
    t.horizontalHeader().setHighlightSections(False)
    t.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    return t


def table_item(text: str, align=Qt.AlignmentFlag.AlignCenter,
               data=None) -> QTableWidgetItem:
    item = QTableWidgetItem(str(text))
    item.setTextAlignment(align | Qt.AlignmentFlag.AlignVCenter)
    if data is not None:
        item.setData(Qt.ItemDataRole.UserRole, data)
    return item


def confirm_dialog(parent, title: str, message: str) -> bool:
    dlg = QMessageBox(parent)
    dlg.setWindowTitle(title)
    dlg.setText(message)
    dlg.setIcon(QMessageBox.Icon.Warning)
    dlg.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    dlg.setLayoutDirection(RTL)
    return dlg.exec() == QMessageBox.StandardButton.Yes


def info_dialog(parent, title: str, message: str) -> None:
    dlg = QMessageBox(parent)
    dlg.setWindowTitle(title)
    dlg.setText(message)
    dlg.setIcon(QMessageBox.Icon.Information)
    dlg.setLayoutDirection(RTL)
    dlg.exec()


# ═══════════════════════════════════════════════════════════════════════
# PAGE WRAPPER — every module uses this
# ═══════════════════════════════════════════════════════════════════════

class PageWrapper(QWidget):
    """
    Standard page layout:
      ┌──────────────────────────────────────┐
      │  [Icon]  Title          Subtitle     │  ← header bar (white)
      ├──────────────────────────────────────┤
      │                                      │
      │   content (scrollable)               │
      │                                      │
      └──────────────────────────────────────┘
    """
    def __init__(self, title: str, subtitle: str = "", icon: str = ""):
        super().__init__()
        self.setLayoutDirection(RTL)
        self.setObjectName("ContentArea")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header bar ──────────────────────────────────────────────
        header = QWidget()
        header.setObjectName("PageHeader")
        header.setFixedHeight(68)
        hlay = QHBoxLayout(header)
        hlay.setContentsMargins(32, 0, 32, 0)
        hlay.setSpacing(12)

        if icon:
            ico_lbl = QLabel(icon)
            ico_lbl.setStyleSheet(
                f"font-size:22px; background:transparent; color:{C.PRIMARY};"
            )
            hlay.addWidget(ico_lbl)

        title_col = QVBoxLayout()
        title_col.setSpacing(1)
        t_lbl = QLabel(title)
        t_lbl.setObjectName("PageTitle")
        title_col.addWidget(t_lbl)
        if subtitle:
            s_lbl = QLabel(subtitle)
            s_lbl.setObjectName("PageSubtitle")
            title_col.addWidget(s_lbl)
        hlay.addLayout(title_col)
        hlay.addStretch()
        root.addWidget(header)

        # ── Scrollable content area ──────────────────────────────────
        self._content = QWidget()
        self._content.setObjectName("ContentArea")
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(28, 24, 28, 28)
        self._content_layout.setSpacing(20)

        scroll = QScrollArea()
        scroll.setWidget(self._content)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setObjectName("ContentArea")
        root.addWidget(scroll)

    def layout(self) -> QVBoxLayout:          # type: ignore[override]
        return self._content_layout

    def add(self, widget: QWidget) -> None:
        self._content_layout.addWidget(widget)

    def add_stretch(self) -> None:
        self._content_layout.addStretch()


# ═══════════════════════════════════════════════════════════════════════
# ITEMS EDITOR  (reusable line-items table for quotes / invoices)
# ═══════════════════════════════════════════════════════════════════════

class ItemsEditor(QWidget):
    """Editable line-items grid with auto-computed totals."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayoutDirection(RTL)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.table = make_table(["الوصف", "الكمية", "سعر الوحدة", "ضريبة %", "الإجمالي"])
        self.table.setMinimumHeight(160)
        layout.addWidget(self.table)

        bar = QHBoxLayout()
        add = make_btn("+ إضافة بند", "primary")
        rem = make_btn("حذف البند", "danger")
        add.clicked.connect(self._add_row)
        rem.clicked.connect(self._del_row)
        bar.addWidget(rem)
        bar.addStretch()
        bar.addWidget(add)
        layout.addLayout(bar)

        self._add_row()

    def _add_row(self):
        r = self.table.rowCount()
        self.table.insertRow(r)
        for col, val in enumerate(["", "1", "0.00", "0", "0.00"]):
            self.table.setItem(r, col, QTableWidgetItem(val))
        self.table.cellChanged.connect(self._recalc)

    def _del_row(self):
        r = self.table.currentRow()
        if r >= 0:
            self.table.removeRow(r)

    def _recalc(self, row: int, col: int):
        if col not in (1, 2, 3):
            return
        try:
            qty   = float(self.table.item(row, 1).text() or 0)
            price = float(self.table.item(row, 2).text() or 0)
            tax   = float(self.table.item(row, 3).text() or 0)
            amt   = qty * price * (1 + tax / 100)
            self.table.blockSignals(True)
            self.table.item(row, 4).setText(f"{amt:,.2f}")
            self.table.blockSignals(False)
        except (ValueError, AttributeError):
            pass

    def get_items(self) -> list:
        items = []
        for r in range(self.table.rowCount()):
            try:
                desc  = (self.table.item(r, 0) or QTableWidgetItem()).text().strip()
                qty   = float((self.table.item(r, 1) or QTableWidgetItem("1")).text() or 1)
                price = float((self.table.item(r, 2) or QTableWidgetItem("0")).text() or 0)
                tax   = float((self.table.item(r, 3) or QTableWidgetItem("0")).text() or 0)
                amt   = qty * price * (1 + tax / 100)
                if desc:
                    items.append({"description": desc, "quantity": qty,
                                  "unit_price": price, "tax_rate": tax, "amount": amt})
            except ValueError:
                pass
        return items

    def load_items(self, items: list):
        self.table.setRowCount(0)
        for it in items:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for col, val in enumerate([
                it.get("description", ""),
                str(it.get("quantity", 1)),
                f"{it.get('unit_price', 0):.2f}",
                str(it.get("tax_rate", 0)),
                f"{it.get('amount', 0):,.2f}",
            ]):
                self.table.setItem(r, col, QTableWidgetItem(val))


# ═══════════════════════════════════════════════════════════════════════
# PREMIUM DIALOG BASE
# ═══════════════════════════════════════════════════════════════════════

class PremiumDialog(QDialog):
    """Base dialog with branded green header bar."""

    def __init__(self, parent, title: str, min_width: int = 480):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(min_width)
        self.setLayoutDirection(RTL)
        self.setObjectName("PremiumDialog")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Green header
        hdr = QWidget()
        hdr.setObjectName("DialogHeader")
        hdr.setFixedHeight(60)
        hdr_lay = QHBoxLayout(hdr)
        hdr_lay.setContentsMargins(24, 0, 24, 0)
        t = QLabel(title)
        t.setObjectName("DialogHeaderTitle")
        hdr_lay.addWidget(t)
        root.addWidget(hdr)

        # Body area
        self._body = QWidget()
        self._body.setStyleSheet(f"background-color: {C.BG_CARD};")
        self._form = QVBoxLayout(self._body)
        self._form.setContentsMargins(28, 24, 28, 24)
        self._form.setSpacing(14)
        root.addWidget(self._body)

        # Footer buttons
        footer = QWidget()
        footer.setStyleSheet(
            f"background-color:{C.BG_CARD}; border-top:1px solid {C.BORDER};"
        )
        f_lay = QHBoxLayout(footer)
        f_lay.setContentsMargins(24, 12, 24, 12)
        f_lay.setSpacing(8)

        cancel = make_btn("إلغاء", "secondary")
        cancel.clicked.connect(self.reject)
        self._save_btn = make_btn("حفظ", "primary")
        self._save_btn.clicked.connect(self.accept)

        f_lay.addWidget(cancel)
        f_lay.addStretch()
        f_lay.addWidget(self._save_btn)
        root.addWidget(footer)

    def body(self) -> QVBoxLayout:
        return self._form

    def _add_field(self, label: str, widget: QWidget):
        lbl = QLabel(label)
        lbl.setStyleSheet(
            f"font-size:{F.SIZE_SM}px; font-weight:bold; "
            f"color:{C.TEXT_SECONDARY}; background:transparent;"
        )
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        self._form.addWidget(lbl)
        self._form.addWidget(widget)

    def set_save_text(self, text: str):
        self._save_btn.setText(text)


# ═══════════════════════════════════════════════════════════════════════
# ── MODULE: DASHBOARD ────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════

class MetricCard(QFrame):
    """
    Single KPI card with icon, large number, label and accent bar.
    Supports hover animation via stylesheet.
    """

    def __init__(self, label: str, value: str, icon: str,
                 accent_color: str, parent=None):
        super().__init__(parent)
        self.setObjectName("MetricCard")
        self.setFixedHeight(130)
        self.setGraphicsEffect(card_shadow())
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Accent bar at top
        bar = QFrame()
        bar.setFixedHeight(4)
        bar.setStyleSheet(f"background-color:{accent_color}; border-radius:14px 14px 0 0;")
        outer.addWidget(bar)

        # Content
        body = QWidget()
        body.setStyleSheet("background-color:transparent;")
        body_lay = QHBoxLayout(body)
        body_lay.setContentsMargins(20, 16, 20, 16)
        body_lay.setSpacing(16)

        # Text column
        text_col = QVBoxLayout()
        text_col.setSpacing(4)
        self.value_lbl = QLabel(value)
        self.value_lbl.setObjectName("MetricValue")
        self.label_lbl = QLabel(label)
        self.label_lbl.setObjectName("MetricLabel")
        text_col.addWidget(self.value_lbl)
        text_col.addWidget(self.label_lbl)
        text_col.addStretch()

        # Icon
        ico = QLabel(icon)
        ico.setObjectName("MetricIcon")
        ico.setFixedSize(52, 52)
        ico.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ico.setStyleSheet(
            f"background-color:{accent_color}22; border-radius:14px; "
            f"color:{accent_color}; font-size:24px;"
        )

        body_lay.addLayout(text_col)
        body_lay.addStretch()
        body_lay.addWidget(ico)
        outer.addWidget(body)

    def update_value(self, value: str):
        self.value_lbl.setText(value)


class FinanceSummaryCard(QFrame):
    """Revenue / Expense / Profit card with semantic colour coding."""

    def __init__(self, label: str, value: str,
                 card_type: str, icon: str, parent=None):
        super().__init__(parent)
        self.setObjectName("FinanceCard")
        self.setProperty("type", card_type)
        self.setFixedHeight(120)
        self.setGraphicsEffect(card_shadow(blur=14))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)

        top = QHBoxLayout()
        ico = QLabel(icon)
        ico.setStyleSheet("font-size:20px; background:transparent;")
        lbl = QLabel(label)
        lbl.setObjectName("FinanceLabel")
        top.addWidget(lbl)
        top.addStretch()
        top.addWidget(ico)
        layout.addLayout(top)

        self.value_lbl = QLabel(value)
        self.value_lbl.setObjectName("FinanceValue")
        self.value_lbl.setProperty("type", card_type)
        layout.addWidget(self.value_lbl)
        layout.addStretch()

    def update_value(self, value: str):
        self.value_lbl.setText(value)


class DashboardWidget(PageWrapper):
    """
    Premium dashboard with:
      - Row of 6 KPI metric cards
      - Finance summary strip (Revenue / Expenses / Profit)
      - Quick-action shortcut buttons
    """

    def __init__(self):
        super().__init__(
            "لوحة التحكم",
            "مرحباً بك في كايرو ماربل — نظرة عامة على الأعمال",
            "🏛"
        )
        self._build()

    def _build(self):
        lay = self.layout()

        # ── KPI metric cards ─────────────────────────────────────
        kpi_frame = QWidget()
        kpi_frame.setStyleSheet("background:transparent;")
        kpi_grid = QGridLayout(kpi_frame)
        kpi_grid.setSpacing(16)
        kpi_grid.setContentsMargins(0, 0, 0, 0)

        metrics_cfg = [
            ("الموظفون",       lambda: str(len(DB.get_employees())),    "👥", C.ACCENT_EMPLOYEES),
            ("العملاء",        lambda: str(len(DB.get_clients())),       "🧑‍💼", C.ACCENT_CLIENTS),
            ("عروض الأسعار",  lambda: str(len(DB.get_quotes())),        "📋", C.ACCENT_QUOTES),
            ("الفواتير",       lambda: str(len(DB.get_invoices())),      "🧾", C.ACCENT_INVOICES),
            ("المشاريع",       lambda: str(len(DB.get_projects())),      "🏗",  C.ACCENT_PROJECTS),
            ("السائقون",       lambda: str(len(DB.get_drivers())),       "🚛", C.ACCENT_FINANCE),
        ]

        self._metric_cards = []
        for col, (label, val_fn, icon, color) in enumerate(metrics_cfg):
            card = MetricCard(label, val_fn(), icon, color)
            kpi_grid.addWidget(card, 0, col)
            self._metric_cards.append((card, val_fn))

        lay.addWidget(kpi_frame)

        # ── Finance summary ───────────────────────────────────────
        summary = DB.get_finance_summary()
        fin_frame = QWidget()
        fin_frame.setStyleSheet("background:transparent;")
        fin_lay = QHBoxLayout(fin_frame)
        fin_lay.setSpacing(16)
        fin_lay.setContentsMargins(0, 0, 0, 0)

        self._rev_card  = FinanceSummaryCard(
            "إجمالي الإيرادات",
            f"{summary['revenues']:,.2f} AED", "revenue", "💚"
        )
        self._exp_card  = FinanceSummaryCard(
            "إجمالي المصروفات",
            f"{summary['expenses']:,.2f} AED", "expense", "🔴"
        )
        self._prof_card = FinanceSummaryCard(
            "صافي الربح",
            f"{summary['profit']:,.2f} AED",   "profit",  "📈"
        )

        for c in [self._rev_card, self._exp_card, self._prof_card]:
            fin_lay.addWidget(c)
        lay.addWidget(fin_frame)

        # ── Quick actions ─────────────────────────────────────────
        qa_card = make_card()
        qa_card.setGraphicsEffect(card_shadow(blur=12, opacity=0.07))
        qa_lay = QVBoxLayout(qa_card)
        qa_lay.setContentsMargins(20, 16, 20, 16)
        qa_lay.setSpacing(12)

        qa_title = QLabel("إجراءات سريعة")
        qa_title.setObjectName("SectionTitle")
        qa_lay.addWidget(qa_title)

        qa_btns = QHBoxLayout()
        qa_btns.setSpacing(10)
        for label, variant in [
            ("+ عرض سعر جديد", "primary"),
            ("+ فاتورة جديدة", "accent"),
            ("+ موظف جديد",    "secondary"),
            ("+ مشروع",        "secondary"),
        ]:
            b = make_btn(label, variant)
            qa_btns.addWidget(b)
        qa_btns.addStretch()
        qa_lay.addLayout(qa_btns)
        lay.addWidget(qa_card)
        lay.addStretch()

    def refresh(self):
        """Reload all KPI values from the database."""
        for card, val_fn in self._metric_cards:
            card.update_value(val_fn())
        summary = DB.get_finance_summary()
        self._rev_card.update_value(f"{summary['revenues']:,.2f} AED")
        self._exp_card.update_value(f"{summary['expenses']:,.2f} AED")
        self._prof_card.update_value(f"{summary['profit']:,.2f} AED")


# ═══════════════════════════════════════════════════════════════════════
# ── MODULE: HR / EMPLOYEES ───────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════

class EmployeeDialog(PremiumDialog):
    def __init__(self, parent, employee=None):
        title = "موظف جديد" if not employee else "تعديل بيانات موظف"
        super().__init__(parent, title, min_width=500)
        self.employee = employee

        self.name   = make_input("الاسم الكامل")
        self.job    = make_input("المسمى الوظيفي")
        self.phone  = make_input("رقم الهاتف")
        self.hire   = make_date()
        self.salary = QDoubleSpinBox()
        self.salary.setMaximum(999_999)
        self.salary.setPrefix("AED  ")
        self.salary.setGroupSeparatorShown(True)
        self.notes  = QTextEdit()
        self.notes.setMaximumHeight(80)
        self.notes.setPlaceholderText("ملاحظات اختيارية...")

        for label, widget in [
            ("الاسم الكامل:", self.name),
            ("المسمى الوظيفي:", self.job),
            ("رقم الهاتف:", self.phone),
            ("تاريخ التعيين:", self.hire),
            ("الراتب الأساسي:", self.salary),
            ("ملاحظات:", self.notes),
        ]:
            self._add_field(label, widget)

        if employee:
            self.name.setText(employee["name"])
            self.job.setText(employee["job_title"] or "")
            self.phone.setText(employee["phone"] or "")
            if employee["hire_date"]:
                self.hire.setDate(QDate.fromString(employee["hire_date"], "yyyy-MM-dd"))
            self.salary.setValue(employee["base_salary"] or 0)
            self.notes.setPlainText(employee["notes"] or "")

    def get_data(self) -> dict:
        return {
            "name":        self.name.text().strip(),
            "job_title":   self.job.text().strip(),
            "phone":       self.phone.text().strip(),
            "hire_date":   self.hire.date().toString("yyyy-MM-dd"),
            "base_salary": self.salary.value(),
            "notes":       self.notes.toPlainText().strip(),
        }


class EmployeeDetailDialog(QDialog):
    """Full employee dossier: salary calculator, advances, attendance."""

    def __init__(self, parent, emp_id: int):
        super().__init__(parent)
        self.emp_id = emp_id
        emp = DB.get_employee(emp_id)
        self.setWindowTitle(f"ملف الموظف  —  {emp['name']}")
        self.setMinimumSize(740, 540)
        self.setLayoutDirection(RTL)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        hdr = QWidget()
        hdr.setFixedHeight(70)
        hdr.setStyleSheet(
            f"background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            f"stop:0 {C.PRIMARY},stop:1 {C.PRIMARY_HOVER});"
        )
        hlay = QHBoxLayout(hdr)
        hlay.setContentsMargins(24, 0, 24, 0)
        n = QLabel(emp["name"])
        n.setStyleSheet(
            f"color:white;font-size:{F.SIZE_LG}px;font-weight:bold;background:transparent;"
        )
        j = QLabel(emp["job_title"] or "")
        j.setStyleSheet("color:rgba(255,255,255,0.7);font-size:13px;background:transparent;")
        vl = QVBoxLayout()
        vl.setSpacing(2)
        vl.addWidget(n)
        vl.addWidget(j)
        hlay.addLayout(vl)
        hlay.addStretch()
        sal_lbl = QLabel(f"الراتب الأساسي: {emp['base_salary']:,.0f} AED")
        sal_lbl.setStyleSheet(
            "color:rgba(255,255,255,0.85);font-weight:bold;background:transparent;"
        )
        hlay.addWidget(sal_lbl)
        root.addWidget(hdr)

        # Tabs
        body = QWidget()
        body.setStyleSheet(f"background-color:{C.BG_CARD};")
        blay = QVBoxLayout(body)
        blay.setContentsMargins(20, 16, 20, 16)

        tabs = QTabWidget()
        tabs.setLayoutDirection(RTL)

        # ── Salary ──
        sal_tab = QWidget()
        sv = QVBoxLayout(sal_tab)
        sv.setSpacing(12)
        month_bar = QHBoxLayout()
        self.month_inp = make_input("YYYY-MM")
        self.month_inp.setText(date.today().strftime("%Y-%m"))
        self.month_inp.setMaximumWidth(130)
        calc_btn = make_btn("احتساب الراتب", "primary")
        pdf_btn  = make_btn("تصدير PDF",     "secondary")
        calc_btn.clicked.connect(self._calc_salary)
        pdf_btn.clicked.connect(self._export_salary)
        month_bar.addWidget(QLabel("الشهر:"))
        month_bar.addWidget(self.month_inp)
        month_bar.addStretch()
        month_bar.addWidget(calc_btn)
        month_bar.addWidget(pdf_btn)
        sv.addLayout(month_bar)

        self.salary_card = QFrame()
        self.salary_card.setObjectName("Card")
        self.salary_card.setStyleSheet(
            f"border-radius:12px; border:1px solid {C.BORDER}; padding:16px;"
        )
        self._sal_lay = QVBoxLayout(self.salary_card)
        self._sal_lay.addWidget(QLabel("اختر الشهر ثم اضغط 'احتساب الراتب'"))
        sv.addWidget(self.salary_card)
        tabs.addTab(sal_tab, "الراتب الشهري")

        # ── Advances ──
        adv_tab = QWidget()
        av = QVBoxLayout(adv_tab)
        add_adv = make_btn("+ إضافة سلفة", "primary")
        add_adv.clicked.connect(self._add_advance)
        av.addWidget(add_adv)
        self.adv_table = make_table(["المبلغ", "التاريخ", "ملاحظات", "الحالة"])
        av.addWidget(self.adv_table)
        self.total_adv_lbl = QLabel()
        self.total_adv_lbl.setObjectName("LabelWarning")
        av.addWidget(self.total_adv_lbl)
        tabs.addTab(adv_tab, "السلف")

        # ── Attendance ──
        att_tab = QWidget()
        atv = QVBoxLayout(att_tab)
        add_att = make_btn("+ تسجيل حضور", "primary")
        add_att.clicked.connect(self._add_attendance)
        atv.addWidget(add_att)
        self.att_table = make_table(["التاريخ", "الحالة", "ساعات إضافية"])
        atv.addWidget(self.att_table)
        tabs.addTab(att_tab, "الحضور")

        blay.addWidget(tabs)
        root.addWidget(body)

        self._load_advances()
        self._load_attendance()
        self._salary_data = None

    # ── Salary ──
    def _calc_salary(self):
        month = self.month_inp.text().strip()
        data  = DB.calc_monthly_salary(self.emp_id, month)
        if not data:
            return
        self._salary_data = data
        # Clear and rebuild card
        while self._sal_lay.count():
            w = self._sal_lay.takeAt(0).widget()
            if w:
                w.deleteLater()

        rows = [
            ("الراتب الأساسي",         f"{data['base_salary']:,.2f} AED",         "body"),
            ("أيام الحضور",            str(data["present_days"]),                  "body"),
            ("أيام الغياب",            str(data["absent_days"]),                   "body"),
            ("ساعات إضافية",           str(data["overtime_hours"]),                "body"),
            ("بدل إضافي",              f"+ {data['overtime_pay']:,.2f} AED",       "success"),
            ("خصم الغياب",             f"− {data['deductions']:,.2f} AED",         "warning"),
            ("خصم السلفة",             f"− {data['advance_deduction']:,.2f} AED",  "warning"),
        ]
        for lbl, val, variant in rows:
            row_w = QWidget()
            row_w.setStyleSheet("background:transparent;")
            rlay = QHBoxLayout(row_w)
            rlay.setContentsMargins(0, 0, 0, 0)
            l = QLabel(lbl)
            l.setStyleSheet(f"color:{C.TEXT_SECONDARY};background:transparent;")
            v = QLabel(val)
            color_map = {
                "success": C.SUCCESS_TEXT,
                "warning": C.WARNING_TEXT,
                "body":    C.TEXT_PRIMARY,
            }
            v.setStyleSheet(
                f"font-weight:bold; color:{color_map[variant]}; background:transparent;"
            )
            rlay.addWidget(l)
            rlay.addStretch()
            rlay.addWidget(v)
            self._sal_lay.addWidget(row_w)
            self._sal_lay.addWidget(make_divider())

        # Net salary
        net_w = QWidget()
        net_w.setStyleSheet(
            f"background-color:{C.PRIMARY_ULTRA}; border-radius:8px;"
        )
        net_lay = QHBoxLayout(net_w)
        net_lay.setContentsMargins(12, 10, 12, 10)
        net_lbl = QLabel("صافي الراتب")
        net_lbl.setStyleSheet(
            f"font-weight:bold; color:{C.PRIMARY}; font-size:{F.SIZE_MD}px; background:transparent;"
        )
        net_val = QLabel(f"{data['net_salary']:,.2f} AED")
        net_val.setStyleSheet(
            f"font-weight:bold; color:{C.PRIMARY}; font-size:{F.SIZE_LG}px; background:transparent;"
        )
        net_lay.addWidget(net_lbl)
        net_lay.addStretch()
        net_lay.addWidget(net_val)
        self._sal_lay.addWidget(net_w)

    def _export_salary(self):
        if not self._salary_data:
            self._calc_salary()
        if self._salary_data:
            emp  = dict(DB.get_employee(self.emp_id))
            path = PDF.export_salary_slip(emp, self._salary_data, self.month_inp.text().strip())
            info_dialog(self, "تم التصدير", f"تم حفظ الملف:\n{path}")

    # ── Advances ──
    def _load_advances(self):
        advances = DB.get_advances(self.emp_id)
        self.adv_table.setRowCount(0)
        for adv in advances:
            r = self.adv_table.rowCount()
            self.adv_table.insertRow(r)
            status = "مسدد ✓" if adv["repaid"] else "مستحق"
            for col, val in enumerate([
                f"{adv['amount']:,.2f} AED",
                adv["advance_date"],
                adv["notes"] or "",
                status,
            ]):
                self.adv_table.setItem(r, col, QTableWidgetItem(val))
        total = DB.get_total_advances(self.emp_id)
        self.total_adv_lbl.setText(f"إجمالي السلف المستحقة: {total:,.2f} AED")

    def _add_advance(self):
        dlg = PremiumDialog(self, "إضافة سلفة", 400)
        amount   = QDoubleSpinBox()
        amount.setMaximum(999_999)
        amount.setPrefix("AED  ")
        adv_date = make_date()
        notes    = make_input("ملاحظات اختيارية")
        dlg._add_field("المبلغ:", amount)
        dlg._add_field("التاريخ:", adv_date)
        dlg._add_field("ملاحظات:", notes)
        if dlg.exec():
            DB.add_advance(
                self.emp_id, amount.value(),
                adv_date.date().toString("yyyy-MM-dd"),
                notes.text()
            )
            self._load_advances()

    # ── Attendance ──
    def _load_attendance(self):
        records = DB.get_attendance(self.emp_id)
        self.att_table.setRowCount(0)
        status_ar = {"present": "✅ حاضر", "absent": "❌ غائب", "late": "⚠ متأخر"}
        for rec in records:
            r = self.att_table.rowCount()
            self.att_table.insertRow(r)
            for col, val in enumerate([
                rec["work_date"],
                status_ar.get(rec["status"], rec["status"]),
                str(rec["overtime_hours"]),
            ]):
                self.att_table.setItem(r, col, QTableWidgetItem(val))

    def _add_attendance(self):
        dlg = PremiumDialog(self, "تسجيل حضور", 380)
        work_date = make_date()
        status_cb = QComboBox()
        status_cb.setLayoutDirection(RTL)
        status_cb.addItems(["حاضر|present", "غائب|absent", "متأخر|late"])
        overtime  = QDoubleSpinBox()
        overtime.setMaximum(24)
        overtime.setSuffix("  ساعة")
        dlg._add_field("التاريخ:", work_date)
        dlg._add_field("الحالة:", status_cb)
        dlg._add_field("ساعات إضافية:", overtime)
        if dlg.exec():
            status = status_cb.currentText().split("|")[1]
            DB.add_attendance(
                self.emp_id,
                work_date.date().toString("yyyy-MM-dd"),
                status, overtime.value()
            )
            self._load_attendance()


class HRWidget(PageWrapper):
    """Employee management module."""

    def __init__(self):
        super().__init__("الموارد البشرية", "إدارة الموظفين والرواتب والسلف", "👥")
        self._build()

    def _build(self):
        lay = self.layout()

        # Action bar
        bar = QHBoxLayout()
        add_btn     = make_btn("+ موظف جديد", "primary")
        refresh_btn = make_btn("تحديث", "ghost")
        add_btn.clicked.connect(self._add_employee)
        refresh_btn.clicked.connect(self._load)
        bar.addWidget(refresh_btn)
        bar.addStretch()
        bar.addWidget(add_btn)

        bar_w = QWidget()
        bar_w.setLayout(bar)
        lay.addWidget(bar_w)

        # Table card
        table_card = make_card()
        table_card.setGraphicsEffect(card_shadow())
        tc_lay = QVBoxLayout(table_card)
        tc_lay.setContentsMargins(0, 0, 0, 0)
        tc_lay.setSpacing(0)

        self.table = make_table(
            ["الاسم", "الوظيفة", "الهاتف", "الراتب الأساسي", "تاريخ التعيين"]
        )
        self.table.cellDoubleClicked.connect(
            lambda r, c: self._open_detail()
        )
        tc_lay.addWidget(self.table)
        lay.addWidget(table_card)

        # Row actions
        act = QHBoxLayout()
        detail_btn = make_btn("ملف الموظف الكامل", "accent")
        edit_btn   = make_btn("تعديل", "secondary")
        del_btn    = make_btn("حذف", "danger")
        detail_btn.clicked.connect(self._open_detail)
        edit_btn.clicked.connect(self._edit)
        del_btn.clicked.connect(self._delete)
        act.addWidget(del_btn)
        act.addStretch()
        act.addWidget(edit_btn)
        act.addWidget(detail_btn)
        lay.addLayout(act)
        lay.addStretch()

        self._load()

    def _load(self):
        emps = DB.get_employees()
        self.table.setRowCount(0)
        for emp in emps:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for col, val in enumerate([
                emp["name"],
                emp["job_title"] or "",
                emp["phone"] or "",
                f"{emp['base_salary']:,.0f} AED",
                emp["hire_date"] or "",
            ]):
                it = table_item(
                    val,
                    Qt.AlignmentFlag.AlignRight if col == 0 else Qt.AlignmentFlag.AlignCenter,
                    emp["id"] if col == 0 else None,
                )
                self.table.setItem(r, col, it)

    def _selected_id(self):
        r = self.table.currentRow()
        if r < 0:
            return None
        return self.table.item(r, 0).data(Qt.ItemDataRole.UserRole)

    def _add_employee(self):
        dlg = EmployeeDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            if data["name"]:
                DB.add_employee(**data)
                self._load()

    def _edit(self):
        eid = self._selected_id()
        if not eid:
            return
        dlg = EmployeeDialog(self, DB.get_employee(eid))
        if dlg.exec():
            DB.update_employee(eid, **dlg.get_data())
            self._load()

    def _delete(self):
        eid = self._selected_id()
        if eid and confirm_dialog(self, "تأكيد", "هل تريد حذف (أرشفة) هذا الموظف؟"):
            DB.delete_employee(eid)
            self._load()

    def _open_detail(self):
        eid = self._selected_id()
        if eid:
            EmployeeDetailDialog(self, eid).exec()


# ═══════════════════════════════════════════════════════════════════════
# ── MODULE: CLIENTS & SALES ──────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════

class QuoteInvoiceDialog(PremiumDialog):
    def __init__(self, parent, title="عرض سعر جديد"):
        super().__init__(parent, title, min_width=680)
        self.setMinimumHeight(580)
        self.client_cb = QComboBox()
        self.client_cb.setLayoutDirection(RTL)
        self._client_ids = []
        self._load_clients()
        self.doc_date    = make_date()
        self.end_date    = make_date()
        self.end_date.setDate(QDate.currentDate().addDays(30))
        self.salesperson = make_input("اسم المندوب")
        self.notes       = make_input("ملاحظات اختيارية")
        self._add_field("العميل:", self.client_cb)
        self._add_field("التاريخ:", self.doc_date)
        self._add_field("تاريخ الانتهاء / الاستحقاق:", self.end_date)
        self._add_field("مندوب المبيعات:", self.salesperson)
        self._add_field("ملاحظات:", self.notes)
        self._form.addWidget(QLabel("بنود الوثيقة:"))
        self.items_editor = ItemsEditor()
        self._form.addWidget(self.items_editor)

    def _load_clients(self):
        self.client_cb.clear(); self._client_ids = []
        for c in DB.get_clients():
            self.client_cb.addItem(c["name"]); self._client_ids.append(c["id"])

    def get_data(self):
        idx = self.client_cb.currentIndex()
        return {
            "client_id":   self._client_ids[idx] if idx >= 0 and self._client_ids else None,
            "quote_date":  self.doc_date.date().toString("yyyy-MM-dd"),
            "expiry_date": self.end_date.date().toString("yyyy-MM-dd"),
            "salesperson": self.salesperson.text().strip(),
            "items":       self.items_editor.get_items(),
            "notes":       self.notes.text().strip(),
        }


class ClientWidget(PageWrapper):
    def __init__(self):
        super().__init__("العملاء والمبيعات", "إدارة العملاء وعروض الأسعار والفواتير", "🧾")
        self._build()

    def _build(self):
        lay = self.layout()
        tabs = QTabWidget(); tabs.setLayoutDirection(RTL)
        tabs.addTab(self._build_clients_tab(),  "العملاء")
        tabs.addTab(self._build_quotes_tab(),   "عروض الأسعار")
        tabs.addTab(self._build_invoices_tab(), "الفواتير")
        lay.addWidget(tabs)

    def _build_clients_tab(self):
        w = QWidget(); v = QVBoxLayout(w); v.setSpacing(12)
        bar = QHBoxLayout()
        add = make_btn("+ عميل جديد", "primary"); add.clicked.connect(self._add_client)
        ref = make_btn("تحديث", "ghost");          ref.clicked.connect(self._load_clients)
        bar.addWidget(ref); bar.addStretch(); bar.addWidget(add); v.addLayout(bar)
        card = make_card(); card.setGraphicsEffect(card_shadow())
        cl = QVBoxLayout(card); cl.setContentsMargins(0,0,0,0)
        self.client_table = make_table(["الاسم", "الهاتف", "العنوان"])
        cl.addWidget(self.client_table); v.addWidget(card)
        act = QHBoxLayout()
        del_c  = make_btn("حذف", "danger");           del_c.clicked.connect(self._del_client)
        hist_c = make_btn("سجل المعاملات", "accent"); hist_c.clicked.connect(self._client_history)
        act.addWidget(del_c); act.addStretch(); act.addWidget(hist_c); v.addLayout(act)
        self._load_clients(); return w

    def _load_clients(self):
        self.client_table.setRowCount(0)
        for c in DB.get_clients():
            r = self.client_table.rowCount(); self.client_table.insertRow(r)
            for col, val in enumerate([c["name"], c["phone"] or "", c["address"] or ""]):
                self.client_table.setItem(r, col, table_item(val, Qt.AlignmentFlag.AlignCenter, c["id"] if col==0 else None))

    def _add_client(self):
        dlg = PremiumDialog(self, "عميل جديد", 420)
        name=make_input("الاسم الكامل"); phone=make_input("رقم الهاتف")
        addr=make_input("العنوان");      notes=make_input("ملاحظات")
        for l,w in [("الاسم:",name),("الهاتف:",phone),("العنوان:",addr),("ملاحظات:",notes)]: dlg._add_field(l,w)
        if dlg.exec() and name.text().strip():
            DB.add_client(name.text().strip(), phone.text().strip(), addr.text().strip(), notes.text().strip())
            self._load_clients()

    def _del_client(self):
        r = self.client_table.currentRow()
        if r < 0: return
        cid = self.client_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        if cid and confirm_dialog(self,"تأكيد","حذف هذا العميل؟"):
            DB.delete_client(cid); self._load_clients()

    def _client_history(self):
        r = self.client_table.currentRow()
        if r < 0: return
        cid=self.client_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        cname=self.client_table.item(r,0).text()
        txns=DB.get_client_transactions(cid)
        dlg=QDialog(self); dlg.setWindowTitle(f"سجل معاملات: {cname}")
        dlg.setMinimumSize(620,420); dlg.setLayoutDirection(RTL)
        lay=QVBoxLayout(dlg); tabs=QTabWidget()
        qt=QWidget(); qtv=QVBoxLayout(qt); qt_t=make_table(["الرقم","التاريخ","الإجمالي","الحالة"])
        sm={"draft":"مسودة","sent":"مرسل","converted":"محوّل","expired":"منتهي"}
        for q in txns["quotes"]:
            rr=qt_t.rowCount(); qt_t.insertRow(rr)
            for col,val in enumerate([q["serial"],q["quote_date"],f"{q['total']:,.2f}",sm.get(q["status"],q["status"])]): qt_t.setItem(rr,col,QTableWidgetItem(val))
        qtv.addWidget(qt_t); tabs.addTab(qt,"عروض الأسعار")
        it=QWidget(); itv=QVBoxLayout(it); it_t=make_table(["الرقم","التاريخ","الإجمالي","الحالة"])
        sm2={"unpaid":"غير مسدد","paid":"مسدد","partial":"جزئي"}
        for inv in txns["invoices"]:
            rr=it_t.rowCount(); it_t.insertRow(rr)
            for col,val in enumerate([inv["serial"],inv["invoice_date"],f"{inv['total']:,.2f}",sm2.get(inv["status"],inv["status"])]): it_t.setItem(rr,col,QTableWidgetItem(val))
        itv.addWidget(it_t); tabs.addTab(it,"الفواتير"); lay.addWidget(tabs); dlg.exec()

    def _build_quotes_tab(self):
        w=QWidget(); v=QVBoxLayout(w); v.setSpacing(12)
        bar=QHBoxLayout()
        add=make_btn("+ عرض سعر جديد","primary"); add.clicked.connect(self._add_quote)
        ref=make_btn("تحديث","ghost");             ref.clicked.connect(self._load_quotes)
        pdf=make_btn("تصدير PDF","secondary");     pdf.clicked.connect(self._export_quote)
        conv=make_btn("تحويل إلى فاتورة ◀","accent"); conv.clicked.connect(self._convert_to_invoice)
        bar.addWidget(ref); bar.addStretch(); bar.addWidget(pdf); bar.addWidget(conv); bar.addWidget(add); v.addLayout(bar)
        card=make_card(); card.setGraphicsEffect(card_shadow())
        cl=QVBoxLayout(card); cl.setContentsMargins(0,0,0,0)
        self.quote_table=make_table(["الرقم التسلسلي","العميل","التاريخ","الانتهاء","الإجمالي","الحالة"])
        cl.addWidget(self.quote_table); v.addWidget(card)
        del_btn=make_btn("حذف","danger"); del_btn.clicked.connect(self._del_quote); v.addWidget(del_btn)
        self._load_quotes(); return w

    def _load_quotes(self):
        self.quote_table.setRowCount(0)
        sm={"draft":"مسودة","sent":"مرسل","converted":"محوّل","expired":"منتهي"}
        for q in DB.get_quotes():
            r=self.quote_table.rowCount(); self.quote_table.insertRow(r)
            for col,val in enumerate([q["serial"],q.get("client_name",""),q["quote_date"],q["expiry_date"] or "",f"{q['total']:,.2f} AED",sm.get(q["status"],q["status"])]):
                self.quote_table.setItem(r,col,table_item(val,Qt.AlignmentFlag.AlignCenter,q["id"] if col==0 else None))

    def _add_quote(self):
        dlg=QuoteInvoiceDialog(self,"عرض سعر جديد")
        if dlg.exec():
            data=dlg.get_data()
            if data["client_id"] and data["items"]: DB.add_quote(**data); self._load_quotes()

    def _export_quote(self):
        r=self.quote_table.currentRow()
        if r<0: return
        qid=self.quote_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        if not qid: return
        path=PDF.export_quote(dict(DB.get_quote(qid)),[dict(i) for i in DB.get_quote_items(qid)],self.quote_table.item(r,1).text())
        info_dialog(self,"تم التصدير",f"تم حفظ الملف:\n{path}")

    def _convert_to_invoice(self):
        r=self.quote_table.currentRow()
        if r<0: return
        qid=self.quote_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        if not qid: return
        dlg=PremiumDialog(self,"تحويل إلى فاتورة",420)
        inv_date=make_date(); due_date=make_date(); due_date.setDate(QDate.currentDate().addDays(30))
        dlg._add_field("تاريخ الفاتورة:",inv_date); dlg._add_field("تاريخ الاستحقاق:",due_date)
        dlg.set_save_text("تحويل الآن")
        if dlg.exec():
            try:
                DB.convert_quote_to_invoice(qid,inv_date.date().toString("yyyy-MM-dd"),due_date.date().toString("yyyy-MM-dd"))
                self._load_quotes(); self._load_invoices()
                info_dialog(self,"تم التحويل","تم تحويل عرض السعر إلى فاتورة بنجاح ✓")
            except Exception as e: info_dialog(self,"خطأ",str(e))

    def _del_quote(self):
        r=self.quote_table.currentRow()
        if r<0: return
        qid=self.quote_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        if qid and confirm_dialog(self,"تأكيد","حذف عرض السعر هذا؟"):
            DB.delete_quote(qid); self._load_quotes()

    def _build_invoices_tab(self):
        w=QWidget(); v=QVBoxLayout(w); v.setSpacing(12)
        bar=QHBoxLayout()
        add=make_btn("+ فاتورة جديدة","primary");   add.clicked.connect(self._add_invoice)
        ref=make_btn("تحديث","ghost");               ref.clicked.connect(self._load_invoices)
        pdf=make_btn("تصدير PDF","secondary");       pdf.clicked.connect(self._export_invoice)
        settle=make_btn("تسوية / دفع ✓","accent");  settle.clicked.connect(self._settle)
        bar.addWidget(ref); bar.addStretch(); bar.addWidget(pdf); bar.addWidget(settle); bar.addWidget(add); v.addLayout(bar)
        card=make_card(); card.setGraphicsEffect(card_shadow())
        cl=QVBoxLayout(card); cl.setContentsMargins(0,0,0,0)
        self.inv_table=make_table(["الرقم","العميل","التاريخ","الإجمالي","المدفوع","المتبقي","الحالة"])
        cl.addWidget(self.inv_table); v.addWidget(card)
        del_btn=make_btn("حذف","danger"); del_btn.clicked.connect(self._del_invoice); v.addWidget(del_btn)
        self._load_invoices(); return w

    def _load_invoices(self):
        self.inv_table.setRowCount(0)
        sm={"unpaid":"غير مسدد","paid":"مسدد ✓","partial":"جزئي"}
        for inv in DB.get_invoices():
            r=self.inv_table.rowCount(); self.inv_table.insertRow(r)
            rem=inv["total"]-inv["paid_amount"]
            for col,val in enumerate([inv["serial"],inv.get("client_name",""),inv["invoice_date"],f"{inv['total']:,.2f}",f"{inv['paid_amount']:,.2f}",f"{rem:,.2f}",sm.get(inv["status"],inv["status"])]):
                it=table_item(val,Qt.AlignmentFlag.AlignCenter,inv["id"] if col==0 else None)
                if col==6 and inv["status"]=="paid": it.setForeground(QColor(C.SUCCESS_TEXT))
                elif col==6 and inv["status"]=="unpaid": it.setForeground(QColor(C.WARNING_TEXT))
                self.inv_table.setItem(r,col,it)

    def _add_invoice(self):
        dlg=QuoteInvoiceDialog(self,"فاتورة جديدة")
        if dlg.exec():
            data=dlg.get_data()
            if data["client_id"] and data["items"]:
                DB.add_invoice(data["client_id"],data["quote_date"],data["expiry_date"],data["items"],data["notes"]); self._load_invoices()

    def _export_invoice(self):
        r=self.inv_table.currentRow()
        if r<0: return
        iid=self.inv_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        if not iid: return
        path=PDF.export_invoice(dict(DB.get_invoice(iid)),[dict(i) for i in DB.get_invoice_items(iid)],self.inv_table.item(r,1).text())
        info_dialog(self,"تم التصدير",f"تم حفظ الملف:\n{path}")

    def _settle(self):
        r=self.inv_table.currentRow()
        if r<0: return
        iid=self.inv_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        if not iid: return
        dlg=PremiumDialog(self,"تسوية فاتورة",400)
        amount=QDoubleSpinBox(); amount.setMaximum(9_999_999); amount.setPrefix("AED  "); amount.setGroupSeparatorShown(True)
        dlg._add_field("المبلغ المدفوع:",amount); dlg.set_save_text("تأكيد التسوية")
        if dlg.exec():
            DB.settle_invoice(iid,amount.value()); self._load_invoices()
            info_dialog(self,"تمت التسوية","تمت التسوية وتم إضافة الإيراد إلى سجل المالية ✓")

    def _del_invoice(self):
        r=self.inv_table.currentRow()
        if r<0: return
        iid=self.inv_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        if iid and confirm_dialog(self,"تأكيد","حذف هذه الفاتورة؟"):
            DB.delete_invoice(iid); self._load_invoices()


# ═══════════════════════════════════════════════════════════════════════
# ── MODULE: LOGISTICS ────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════

class LogisticsWidget(PageWrapper):
    def __init__(self):
        super().__init__("اللوجستيك","إدارة السائقين والرحلات وتكاليف النقل","🚛")
        self._build()

    def _build(self):
        lay=self.layout(); tabs=QTabWidget(); tabs.setLayoutDirection(RTL)
        tabs.addTab(self._build_drivers_tab(),"السائقون")
        tabs.addTab(self._build_trips_tab(),"الرحلات")
        lay.addWidget(tabs)

    def _build_drivers_tab(self):
        w=QWidget(); v=QVBoxLayout(w); v.setSpacing(12)
        bar=QHBoxLayout(); add=make_btn("+ سائق جديد","primary"); add.clicked.connect(self._add_driver)
        bar.addStretch(); bar.addWidget(add); v.addLayout(bar)
        card=make_card(); card.setGraphicsEffect(card_shadow())
        cl=QVBoxLayout(card); cl.setContentsMargins(0,0,0,0)
        self.drv_table=make_table(["الاسم","الهاتف","رقم الرخصة"])
        cl.addWidget(self.drv_table); v.addWidget(card)
        act=QHBoxLayout()
        del_d=make_btn("حذف","danger");                del_d.clicked.connect(self._del_driver)
        hist_d=make_btn("سجل الرحلات + PDF","accent"); hist_d.clicked.connect(self._driver_history)
        act.addWidget(del_d); act.addStretch(); act.addWidget(hist_d); v.addLayout(act)
        self._load_drivers(); return w

    def _load_drivers(self):
        self.drv_table.setRowCount(0)
        for d in DB.get_drivers():
            r=self.drv_table.rowCount(); self.drv_table.insertRow(r)
            for col,val in enumerate([d["name"],d["phone"] or "",d["license"] or ""]):
                self.drv_table.setItem(r,col,table_item(val,Qt.AlignmentFlag.AlignCenter,d["id"] if col==0 else None))

    def _add_driver(self):
        dlg=PremiumDialog(self,"سائق جديد",420)
        name=make_input("الاسم الكامل"); phone=make_input("رقم الهاتف")
        lic=make_input("رقم الرخصة"); notes=make_input("ملاحظات")
        for l,w in [("الاسم:",name),("الهاتف:",phone),("رقم الرخصة:",lic),("ملاحظات:",notes)]: dlg._add_field(l,w)
        if dlg.exec() and name.text().strip():
            DB.add_driver(name.text().strip(),phone.text().strip(),lic.text().strip(),notes.text().strip())
            self._load_drivers()

    def _del_driver(self):
        r=self.drv_table.currentRow()
        if r<0: return
        did=self.drv_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        if did and confirm_dialog(self,"تأكيد","حذف هذا السائق؟"):
            DB.delete_driver(did); self._load_drivers()

    def _driver_history(self):
        r=self.drv_table.currentRow()
        if r<0: return
        did=self.drv_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        dname=self.drv_table.item(r,0).text()
        trips=DB.get_trips(did)
        dlg=QDialog(self); dlg.setWindowTitle(f"رحلات: {dname}")
        dlg.setMinimumSize(500,380); dlg.setLayoutDirection(RTL)
        lay=QVBoxLayout(dlg); lay.setContentsMargins(20,20,20,20)
        t=make_table(["التاريخ","الوجهة","السعر"]); total=0.0
        for trip in trips:
            rr=t.rowCount(); t.insertRow(rr)
            for col,val in enumerate([trip["trip_date"],trip["destination"] or "",f"{trip['price']:,.2f} AED"]): t.setItem(rr,col,QTableWidgetItem(val))
            total+=trip["price"]
        lay.addWidget(t)
        tl=QLabel(f"الإجمالي: {total:,.2f} AED"); tl.setStyleSheet(f"font-size:{F.SIZE_MD}px;font-weight:bold;color:{C.SUCCESS_TEXT};padding:8px 0;"); lay.addWidget(tl)
        pdf_btn=make_btn("تصدير تقرير PDF","primary")
        def do_pdf():
            drv=dict(DB.get_driver(did)); path=PDF.export_driver_report(drv,[dict(t2) for t2 in trips]); info_dialog(dlg,"تم التصدير",f"تم حفظ الملف:\n{path}")
        pdf_btn.clicked.connect(do_pdf); lay.addWidget(pdf_btn); dlg.exec()

    def _build_trips_tab(self):
        w=QWidget(); v=QVBoxLayout(w); v.setSpacing(12)
        bar=QHBoxLayout()
        add=make_btn("+ رحلة جديدة","primary"); add.clicked.connect(self._add_trip)
        ref=make_btn("تحديث","ghost");           ref.clicked.connect(self._load_trips)
        bar.addWidget(ref); bar.addStretch(); bar.addWidget(add); v.addLayout(bar)
        card=make_card(); card.setGraphicsEffect(card_shadow())
        cl=QVBoxLayout(card); cl.setContentsMargins(0,0,0,0)
        self.trip_table=make_table(["السائق","التاريخ","الوجهة","السعر","ملاحظات"])
        cl.addWidget(self.trip_table); v.addWidget(card)
        del_btn=make_btn("حذف الرحلة","danger"); del_btn.clicked.connect(self._del_trip); v.addWidget(del_btn)
        self._load_trips(); return w

    def _load_trips(self):
        self.trip_table.setRowCount(0)
        for trip in DB.get_trips():
            r=self.trip_table.rowCount(); self.trip_table.insertRow(r)
            for col,val in enumerate([trip.get("driver_name",""),trip["trip_date"],trip["destination"] or "",f"{trip['price']:,.2f} AED",trip["notes"] or ""]):
                self.trip_table.setItem(r,col,table_item(val,Qt.AlignmentFlag.AlignCenter,trip["id"] if col==0 else None))

    def _add_trip(self):
        drivers=DB.get_drivers()
        if not drivers: info_dialog(self,"تنبيه","أضف سائقاً أولاً"); return
        dlg=PremiumDialog(self,"رحلة جديدة",440)
        drv_cb=QComboBox(); drv_cb.setLayoutDirection(RTL); drv_ids=[]
        for d in drivers: drv_cb.addItem(d["name"]); drv_ids.append(d["id"])
        trip_date=make_date(); dest=make_input("الوجهة / المدينة")
        price=QDoubleSpinBox(); price.setMaximum(999_999); price.setPrefix("AED  ")
        notes=make_input("ملاحظات اختيارية")
        for l,ww in [("السائق:",drv_cb),("التاريخ:",trip_date),("الوجهة:",dest),("السعر:",price),("ملاحظات:",notes)]: dlg._add_field(l,ww)
        if dlg.exec() and drv_ids:
            idx=drv_cb.currentIndex()
            DB.add_trip(drv_ids[idx],trip_date.date().toString("yyyy-MM-dd"),dest.text().strip(),price.value(),notes.text().strip())
            self._load_trips()

    def _del_trip(self):
        r=self.trip_table.currentRow()
        if r<0: return
        tid=self.trip_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        if tid and confirm_dialog(self,"تأكيد","حذف هذه الرحلة؟"):
            DB.delete_trip(tid); self._load_trips()


# ═══════════════════════════════════════════════════════════════════════
# ── MODULE: PROJECTS ─────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════

class ProjectsWidget(PageWrapper):
    def __init__(self):
        super().__init__("المشاريع","تتبع تكاليف المشاريع والمواد الخام","🏗")
        self._current_proj=None; self._build()

    def _build(self):
        lay=self.layout(); splitter=QSplitter(Qt.Orientation.Horizontal); splitter.setChildrenCollapsible(False)
        left=QWidget(); left.setObjectName("ContentArea"); lv=QVBoxLayout(left); lv.setSpacing(12); lv.setContentsMargins(0,0,8,0)
        lbl=QLabel("المشاريع"); lbl.setObjectName("SectionTitle"); lv.addWidget(lbl)
        add_p=make_btn("+ مشروع جديد","primary"); add_p.clicked.connect(self._add_project); lv.addWidget(add_p)
        card_l=make_card(); card_l.setGraphicsEffect(card_shadow())
        cl=QVBoxLayout(card_l); cl.setContentsMargins(0,0,0,0)
        self.proj_table=make_table(["اسم المشروع","المالك","التكلفة"])
        self.proj_table.selectionModel().selectionChanged.connect(self._on_proj_select)
        cl.addWidget(self.proj_table); lv.addWidget(card_l)
        act_l=QHBoxLayout()
        del_p=make_btn("حذف","danger"); del_p.clicked.connect(self._del_project)
        pdf_p=make_btn("تصدير PDF","secondary"); pdf_p.clicked.connect(self._export_project)
        act_l.addWidget(del_p); act_l.addStretch(); act_l.addWidget(pdf_p); lv.addLayout(act_l)
        splitter.addWidget(left)
        right=QWidget(); right.setObjectName("ContentArea"); rv=QVBoxLayout(right); rv.setSpacing(12); rv.setContentsMargins(8,0,0,0)
        self.proj_name_lbl=QLabel("اختر مشروعاً لعرض موادّه"); self.proj_name_lbl.setObjectName("SectionTitle"); rv.addWidget(self.proj_name_lbl)
        add_m=make_btn("+ إضافة مادة خام","primary"); add_m.clicked.connect(self._add_material); rv.addWidget(add_m)
        card_r=make_card(); card_r.setGraphicsEffect(card_shadow())
        cr=QVBoxLayout(card_r); cr.setContentsMargins(0,0,0,0)
        self.mat_table=make_table(["الوصف","الكمية","سعر الوحدة","الإجمالي","التاريخ"])
        cr.addWidget(self.mat_table); rv.addWidget(card_r)
        del_m=make_btn("حذف المادة","danger"); del_m.clicked.connect(self._del_material); rv.addWidget(del_m)
        splitter.addWidget(right); splitter.setSizes([340,560]); lay.addWidget(splitter)
        self._load_projects()

    def _load_projects(self):
        self.proj_table.setRowCount(0)
        for p in DB.get_projects():
            r=self.proj_table.rowCount(); self.proj_table.insertRow(r)
            for col,val in enumerate([p["name"],p["owner"] or "",f"{p['total_cost']:,.2f} AED"]):
                self.proj_table.setItem(r,col,table_item(val,Qt.AlignmentFlag.AlignCenter,p["id"] if col==0 else None))

    def _on_proj_select(self):
        r=self.proj_table.currentRow()
        if r<0: return
        self._current_proj=self.proj_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        self.proj_name_lbl.setText(f"مواد المشروع: {self.proj_table.item(r,0).text()}")
        self._load_materials()

    def _load_materials(self):
        if not self._current_proj: return
        self.mat_table.setRowCount(0)
        for m in DB.get_project_materials(self._current_proj):
            r=self.mat_table.rowCount(); self.mat_table.insertRow(r)
            for col,val in enumerate([m["description"],f"{m['quantity']:g}",f"{m['unit_price']:,.2f}",f"{m['amount']:,.2f} AED",m["entry_date"]]):
                self.mat_table.setItem(r,col,table_item(val,Qt.AlignmentFlag.AlignCenter,m["id"] if col==0 else None))

    def _add_project(self):
        dlg=PremiumDialog(self,"مشروع جديد",460)
        name=make_input("اسم المشروع"); owner=make_input("اسم المالك / العميل")
        start=make_date(); end=make_date(); end.setDate(QDate.currentDate().addDays(90))
        notes=make_input("ملاحظات")
        for l,w in [("اسم المشروع:",name),("المالك:",owner),("تاريخ البداية:",start),("تاريخ النهاية:",end),("ملاحظات:",notes)]: dlg._add_field(l,w)
        if dlg.exec() and name.text().strip():
            DB.add_project(name.text().strip(),owner.text().strip(),start.date().toString("yyyy-MM-dd"),end.date().toString("yyyy-MM-dd"),notes.text().strip())
            self._load_projects()

    def _del_project(self):
        r=self.proj_table.currentRow()
        if r<0: return
        pid=self.proj_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        if pid and confirm_dialog(self,"تأكيد","حذف هذا المشروع وجميع موادّه؟"):
            DB.delete_project(pid); self._load_projects(); self.mat_table.setRowCount(0)

    def _add_material(self):
        if not self._current_proj: info_dialog(self,"تنبيه","اختر مشروعاً أولاً"); return
        dlg=PremiumDialog(self,"إضافة مادة خام",440)
        desc=make_input("وصف المادة"); qty=QDoubleSpinBox(); qty.setMaximum(999_999); qty.setValue(1)
        price=QDoubleSpinBox(); price.setMaximum(999_999); price.setPrefix("AED  "); entry=make_date()
        for l,w in [("الوصف:",desc),("الكمية:",qty),("سعر الوحدة:",price),("التاريخ:",entry)]: dlg._add_field(l,w)
        if dlg.exec() and desc.text().strip():
            DB.add_project_material(self._current_proj,desc.text().strip(),qty.value(),price.value(),entry.date().toString("yyyy-MM-dd"))
            self._load_materials(); self._load_projects()

    def _del_material(self):
        r=self.mat_table.currentRow()
        if r<0: return
        mid=self.mat_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        if mid and confirm_dialog(self,"تأكيد","حذف هذه المادة؟"):
            DB.delete_project_material(mid); self._load_materials()

    def _export_project(self):
        r=self.proj_table.currentRow()
        if r<0: return
        pid=self.proj_table.item(r,0).data(Qt.ItemDataRole.UserRole)
        if not pid: return
        path=PDF.export_project_report(dict(DB.get_project(pid)),[dict(m) for m in DB.get_project_materials(pid)])
        info_dialog(self,"تم التصدير",f"تم حفظ الملف:\n{path}")


# ═══════════════════════════════════════════════════════════════════════
# ── MODULE: FINANCE ──────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════

class FinanceWidget(PageWrapper):
    def __init__(self):
        super().__init__("الإدارة المالية","كشف الحسابات والإيرادات والمصروفات","💰")
        self._build()

    def _build(self):
        lay=self.layout()
        summary=DB.get_finance_summary()
        cards_row=QHBoxLayout(); cards_row.setSpacing(16)
        self._rev_card  =FinanceSummaryCard("إجمالي الإيرادات", f"{summary['revenues']:,.2f} AED","revenue","💚")
        self._exp_card  =FinanceSummaryCard("إجمالي المصروفات",f"{summary['expenses']:,.2f} AED","expense","🔴")
        self._prof_card =FinanceSummaryCard("صافي الربح",        f"{summary['profit']:,.2f} AED","profit","📈")
        for c in [self._rev_card,self._exp_card,self._prof_card]: cards_row.addWidget(c)
        cf=QWidget(); cf.setStyleSheet("background:transparent;"); cf.setLayout(cards_row); lay.addWidget(cf)

        filter_card=make_card(); filter_card.setGraphicsEffect(card_shadow(blur=10,opacity=0.06))
        fl=QHBoxLayout(filter_card); fl.setContentsMargins(16,12,16,12); fl.setSpacing(12)
        fl.addWidget(QLabel("الشهر:"))
        self.month_filter=make_input("YYYY-MM"); self.month_filter.setMaximumWidth(130); fl.addWidget(self.month_filter)
        fl.addWidget(QLabel("النوع:"))
        self.cat_filter=QComboBox(); self.cat_filter.setLayoutDirection(RTL)
        self.cat_filter.addItems(["الكل","إيرادات فقط","مصروفات فقط"]); self.cat_filter.setMaximumWidth(160); fl.addWidget(self.cat_filter)
        filter_btn=make_btn("تصفية","primary"); filter_btn.clicked.connect(self._load); fl.addWidget(filter_btn)
        fl.addStretch()
        pdf_btn=make_btn("تصدير كشف PDF","secondary"); pdf_btn.clicked.connect(self._export); fl.addWidget(pdf_btn)
        add_btn=make_btn("+ إدخال يدوي","primary"); add_btn.clicked.connect(self._add_entry); fl.addWidget(add_btn)
        lay.addWidget(filter_card)

        table_card=make_card(); table_card.setGraphicsEffect(card_shadow())
        tc=QVBoxLayout(table_card); tc.setContentsMargins(0,0,0,0)
        self.table=make_table(["التاريخ","النوع","المصدر","الوصف","المبلغ"])
        tc.addWidget(self.table); lay.addWidget(table_card)
        del_btn=make_btn("حذف القيد","danger"); del_btn.clicked.connect(self._del_entry); lay.addWidget(del_btn)
        lay.addStretch(); self._load()

    def _load(self):
        month=self.month_filter.text().strip() or None
        cat={0:None,1:"revenue",2:"expense"}[self.cat_filter.currentIndex()]
        entries=DB.get_finance(cat,month); summary=DB.get_finance_summary(month)
        self._rev_card.update_value(f"{summary['revenues']:,.2f} AED")
        self._exp_card.update_value(f"{summary['expenses']:,.2f} AED")
        self._prof_card.update_value(f"{summary['profit']:,.2f} AED")
        self.table.setRowCount(0)
        for e in entries:
            r=self.table.rowCount(); self.table.insertRow(r)
            cat_ar="إيراد" if e["category"]=="revenue" else "مصروف"
            for col,val in enumerate([e["entry_date"],cat_ar,e["source"] or "",e["description"] or "",f"{e['amount']:,.2f} AED"]):
                it=table_item(val,Qt.AlignmentFlag.AlignCenter,e["id"] if col==0 else None)
                if col==1: it.setForeground(QColor(C.SUCCESS_TEXT if e["category"]=="revenue" else C.WARNING_TEXT))
                self.table.setItem(r,col,it)

    def _add_entry(self):
        dlg=PremiumDialog(self,"إدخال مالي يدوي",460)
        entry_date=make_date(); category=QComboBox(); category.setLayoutDirection(RTL)
        category.addItems(["إيراد|revenue","مصروف|expense"])
        source=make_input("المصدر"); desc=make_input("وصف تفصيلي")
        amount=QDoubleSpinBox(); amount.setMaximum(9_999_999); amount.setPrefix("AED  "); amount.setGroupSeparatorShown(True)
        for l,w in [("التاريخ:",entry_date),("النوع:",category),("المصدر:",source),("الوصف:",desc),("المبلغ:",amount)]: dlg._add_field(l,w)
        if dlg.exec():
            cat=category.currentText().split("|")[1]
            DB.add_finance_entry(entry_date.date().toString("yyyy-MM-dd"),cat,source.text().strip(),desc.text().strip(),amount.value())
            self._load()

    def _del_entry(self):
        r=self.table.currentRow()
        if r<0: return
        eid=self.table.item(r,0).data(Qt.ItemDataRole.UserRole)
        if eid and confirm_dialog(self,"تأكيد","حذف هذا القيد المالي؟"):
            DB.delete_finance_entry(eid); self._load()

    def _export(self):
        month=self.month_filter.text().strip() or None
        path=PDF.export_finance_statement([dict(e) for e in DB.get_finance(month=month)],DB.get_finance_summary(month),period=month or "إجمالي الفترات")
        info_dialog(self,"تم التصدير",f"تم حفظ الملف:\n{path}")


# ═══════════════════════════════════════════════════════════════════════
# ── SIDEBAR BUTTON ───────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════

class NavButton(QPushButton):
    def __init__(self, label, icon, parent=None):
        super().__init__(parent)
        self.setText(f"  {icon}  {label}")
        self.setObjectName("NavBtn")
        self.setCheckable(True)
        self.setFixedHeight(50)
        self.setLayoutDirection(RTL)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


# ═══════════════════════════════════════════════════════════════════════
# ── MAIN WINDOW ──────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cairo Marble — نظام إدارة الأعمال المتكامل")
        self.setMinimumSize(1180, 720)
        self.resize(1360, 800)
        self.setLayoutDirection(RTL)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────────────
        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(252)
        sb_lay = QVBoxLayout(sidebar)
        sb_lay.setContentsMargins(0, 0, 0, 0)
        sb_lay.setSpacing(0)

        # Logo
        logo = QWidget()
        logo.setFixedHeight(72)
        logo.setStyleSheet(f"background-color:{C.PRIMARY};")
        ll = QVBoxLayout(logo)
        ll.setContentsMargins(20, 16, 20, 0)
        ll.setSpacing(2)
        lt = QLabel("🏛 Cairo Marble")
        lt.setStyleSheet(f"background:transparent;color:white;font-size:{F.SIZE_MD}px;font-weight:bold;padding:0;")
        ls = QLabel("نظام إدارة الأعمال")
        ls.setStyleSheet("background:transparent;color:rgba(255,255,255,0.65);font-size:11px;padding:0;")
        ll.addWidget(lt); ll.addWidget(ls)
        sb_lay.addWidget(logo)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background:rgba(255,255,255,0.12);")
        sb_lay.addWidget(sep)

        sec = QLabel("القائمة الرئيسية")
        sec.setStyleSheet("color:rgba(203,213,225,0.45);font-size:10px;font-weight:bold;letter-spacing:1px;padding:18px 20px 6px 20px;background:transparent;")
        sb_lay.addWidget(sec)

        nav_cfg = [
            ("لوحة التحكم",       "🏠",  DashboardWidget),
            ("الموارد البشرية",   "👥",  HRWidget),
            ("العملاء والمبيعات", "🧾",  ClientWidget),
            ("اللوجستيك",         "🚛",  LogisticsWidget),
            ("المشاريع",           "🏗",  ProjectsWidget),
            ("الإدارة المالية",   "💰",  FinanceWidget),
        ]

        self.stack = QStackedWidget()
        self.nav_buttons = []
        self.pages = []

        for label, icon, WidgetClass in nav_cfg:
            btn  = NavButton(label, icon)
            page = WidgetClass()
            sb_lay.addWidget(btn)
            self.stack.addWidget(page)
            self.nav_buttons.append(btn)
            self.pages.append(page)
            idx = len(self.nav_buttons) - 1
            btn.clicked.connect(lambda _, i=idx: self._navigate(i))

        sb_lay.addStretch()
        ver = QLabel("v2.0  •  Cairo Marble ERP")
        ver.setStyleSheet("color:rgba(203,213,225,0.30);font-size:10px;padding:12px 20px;background:transparent;")
        sb_lay.addWidget(ver)

        root.addWidget(sidebar)
        root.addWidget(self.stack)
        self._navigate(0)

    def _navigate(self, index):
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        self.stack.setCurrentIndex(index)
        if index == 0:
            try: self.pages[0].refresh()
            except AttributeError: pass


# ═══════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Cairo Marble ERP")
    apply_app_styles(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
