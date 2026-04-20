"""
Cairo Marble ERP — Premium Design System
==========================================
styles.py  |  QSS (Qt Style Sheet) + Python color/font constants

Design language: "Refined Stone" — inspired by the material itself.
Marble is simultaneously ancient and modern, heavy yet elegant.
The palette draws from natural stone: deep forest veins, warm cream
surfaces, and the crisp precision of a polished edge.

Aesthetic direction: Stripe meets Notion — clean data hierarchy,
generous breathing room, subtle depth through shadow not decoration.

Usage:
    from styles import apply_app_styles, COLORS, FONTS
    app = QApplication(sys.argv)
    apply_app_styles(app)
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import Qt


# ═══════════════════════════════════════════════════════════════════════
# COLOR TOKENS
# All colors defined as constants — never hard-code hex values elsewhere.
# ═══════════════════════════════════════════════════════════════════════

class COLORS:
    # ── Brand / Primary ─────────────────────────────────────────────
    PRIMARY          = "#1B5E20"   # Forest Green — primary actions, accents
    PRIMARY_HOVER    = "#2E7D32"   # Slightly lighter on hover
    PRIMARY_LIGHT    = "#388E3C"   # Active/pressed states
    PRIMARY_ULTRA    = "#E8F5E9"   # Tinted background for highlight areas
    PRIMARY_BORDER   = "#A5D6A7"   # Soft green border

    # ── Surface / Background ────────────────────────────────────────
    BG_APP           = "#F0F2F5"   # Main app background (cool gray)
    BG_CARD          = "#FFFFFF"   # Card surface
    BG_SIDEBAR       = "#1A2332"   # Deep navy-slate sidebar
    BG_SIDEBAR_HOVER = "#243447"   # Sidebar item hover
    BG_SIDEBAR_ACT   = "#2D4A6B"   # Sidebar active item
    BG_INPUT         = "#F8F9FA"   # Input field background
    BG_TABLE_ALT     = "#F7F9FC"   # Alternating table row
    BG_HEADER        = "#1B5E20"   # Table header

    # ── Text ────────────────────────────────────────────────────────
    TEXT_PRIMARY     = "#1A1D23"   # Near-black — headings
    TEXT_SECONDARY   = "#5A6478"   # Muted — labels, captions
    TEXT_TERTIARY    = "#9BA5B7"   # Disabled, placeholders
    TEXT_ON_PRIMARY  = "#FFFFFF"   # White text on green
    TEXT_ON_SIDEBAR  = "#CBD5E1"   # Sidebar labels
    TEXT_SIDEBAR_ACT = "#FFFFFF"   # Active sidebar label

    # ── Semantic ────────────────────────────────────────────────────
    SUCCESS          = "#1B5E20"   # Revenue, positive values
    SUCCESS_BG       = "#E8F5E9"   # Revenue chip background
    SUCCESS_TEXT     = "#2E7D32"   # Revenue text
    WARNING          = "#E65100"   # Expenses, warnings
    WARNING_BG       = "#FFF3E0"   # Warning chip background
    WARNING_TEXT     = "#BF360C"   # Warning text
    DANGER           = "#C62828"   # Delete, critical
    DANGER_HOVER     = "#B71C1C"
    DANGER_BG        = "#FFEBEE"
    INFO             = "#0277BD"
    INFO_BG          = "#E1F5FE"

    # ── Borders / Dividers ──────────────────────────────────────────
    BORDER           = "#E2E8F0"   # Default border
    BORDER_FOCUS     = "#1B5E20"   # Green on focus
    BORDER_INPUT     = "#CBD5E1"   # Input border
    DIVIDER          = "#EEF2F7"   # Subtle divider lines

    # ── Shadow ──────────────────────────────────────────────────────
    # Note: QSS box-shadow is limited; we simulate via border/background tricks
    SHADOW_SM        = "rgba(0,0,0,0.06)"
    SHADOW_MD        = "rgba(0,0,0,0.10)"

    # ── Sidebar gradient stops ───────────────────────────────────────
    SIDEBAR_GRAD_TOP = "#1A2332"
    SIDEBAR_GRAD_BOT = "#162030"

    # ── Metric card accent bar colors ───────────────────────────────
    ACCENT_EMPLOYEES = "#1B5E20"
    ACCENT_CLIENTS   = "#0277BD"
    ACCENT_QUOTES    = "#6A1B9A"
    ACCENT_INVOICES  = "#E65100"
    ACCENT_PROJECTS  = "#00695C"
    ACCENT_FINANCE   = "#283593"


# ═══════════════════════════════════════════════════════════════════════
# TYPOGRAPHY TOKENS
# ═══════════════════════════════════════════════════════════════════════

class FONTS:
    # Arabic-optimised stack — falls back gracefully
    FAMILY           = "Cairo, Tajawal, Segoe UI, Tahoma, Arial"
    FAMILY_MONO      = "JetBrains Mono, Consolas, Courier New, monospace"

    SIZE_XS          = 10
    SIZE_SM          = 11
    SIZE_BASE        = 13
    SIZE_MD          = 15
    SIZE_LG          = 18
    SIZE_XL          = 22
    SIZE_2XL         = 28
    SIZE_3XL         = 36


# ═══════════════════════════════════════════════════════════════════════
# SPACING / SHAPE TOKENS
# ═══════════════════════════════════════════════════════════════════════

class SHAPE:
    RADIUS_SM   = "6px"
    RADIUS_MD   = "10px"
    RADIUS_LG   = "14px"
    RADIUS_XL   = "18px"
    RADIUS_PILL = "50px"

class SPACING:
    XS  =  4
    SM  =  8
    MD  = 16
    LG  = 24
    XL  = 32
    XXL = 48


# ═══════════════════════════════════════════════════════════════════════
# ICON SVG STRINGS  (inline SVG for sidebar icons via QLabel pixmap)
# ═══════════════════════════════════════════════════════════════════════

ICONS = {
    "dashboard": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>""",
    "employees": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>""",
    "clients":   """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 7H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>""",
    "logistics": """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>""",
    "projects":  """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>""",
    "finance":   """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>""",
}


# ═══════════════════════════════════════════════════════════════════════
# MASTER QSS STYLESHEET
# Organized by component category with extensive comments.
# ═══════════════════════════════════════════════════════════════════════

def _build_qss() -> str:
    C = COLORS
    F = FONTS

    return f"""

/* ═══════════════════════════════════════════════════════
   RESET & BASE
   ═══════════════════════════════════════════════════════ */

QWidget {{
    font-family: {F.FAMILY};
    font-size: {F.SIZE_BASE}px;
    color: {C.TEXT_PRIMARY};
    background-color: transparent;
    outline: none;
}}

QMainWindow,
QDialog {{
    background-color: {C.BG_APP};
}}

/* ═══════════════════════════════════════════════════════
   SIDEBAR — deep navy with gradient simulation
   ═══════════════════════════════════════════════════════ */

#Sidebar {{
    background-color: {C.BG_SIDEBAR};
    border-right: 1px solid #0F1825;
}}

#SidebarLogo {{
    background-color: {C.PRIMARY};
    color: {C.TEXT_ON_PRIMARY};
    font-size: {F.SIZE_MD}px;
    font-weight: bold;
    padding: 22px 16px;
    letter-spacing: 0.5px;
}}

#SidebarLogoSub {{
    background-color: {C.PRIMARY};
    color: rgba(255,255,255,0.65);
    font-size: {F.SIZE_SM}px;
    padding: 0px 16px 18px 16px;
}}

#SidebarSection {{
    color: rgba(203,213,225,0.45);
    font-size: {F.SIZE_XS}px;
    font-weight: bold;
    letter-spacing: 1.5px;
    padding: 20px 20px 6px 20px;
    text-transform: uppercase;
    background-color: transparent;
}}

/* ── Sidebar navigation buttons ── */
#NavBtn {{
    background-color: transparent;
    color: {C.TEXT_ON_SIDEBAR};
    border: none;
    border-radius: 0;
    text-align: right;
    padding: 0px 20px 0px 12px;
    font-size: {F.SIZE_SM}px;
    font-weight: normal;
    letter-spacing: 0.2px;
    min-height: 46px;
}}

#NavBtn:hover {{
    background-color: {C.BG_SIDEBAR_HOVER};
    color: #FFFFFF;
}}

#NavBtn:checked {{
    background-color: {C.BG_SIDEBAR_ACT};
    color: {C.TEXT_SIDEBAR_ACT};
    font-weight: bold;
    border-left: 3px solid {C.PRIMARY_LIGHT};
}}

#SidebarVersion {{
    color: rgba(203,213,225,0.30);
    font-size: {F.SIZE_XS}px;
    padding: 12px 20px;
    background-color: transparent;
}}

/* ═══════════════════════════════════════════════════════
   CONTENT AREA
   ═══════════════════════════════════════════════════════ */

#ContentArea {{
    background-color: {C.BG_APP};
}}

#PageHeader {{
    background-color: {C.BG_CARD};
    border-bottom: 1px solid {C.BORDER};
    padding: 0px 32px;
    min-height: 64px;
}}

#PageTitle {{
    font-size: {F.SIZE_XL}px;
    font-weight: bold;
    color: {C.TEXT_PRIMARY};
}}

#PageSubtitle {{
    font-size: {F.SIZE_SM}px;
    color: {C.TEXT_SECONDARY};
    margin-top: 2px;
}}

/* ═══════════════════════════════════════════════════════
   METRIC / STAT CARDS  (Dashboard)
   ═══════════════════════════════════════════════════════ */

#MetricCard {{
    background-color: {C.BG_CARD};
    border-radius: 14px;
    border: 1px solid {C.BORDER};
    padding: 0px;
}}

#MetricCard:hover {{
    border-color: {C.PRIMARY_BORDER};
    background-color: #FAFFFE;
}}

#MetricIcon {{
    font-size: 22px;
    background-color: transparent;
}}

#MetricValue {{
    font-size: {F.SIZE_2XL}px;
    font-weight: bold;
    color: {C.TEXT_PRIMARY};
    background-color: transparent;
}}

#MetricLabel {{
    font-size: {F.SIZE_SM}px;
    color: {C.TEXT_SECONDARY};
    font-weight: normal;
    background-color: transparent;
}}

#MetricChange {{
    font-size: {F.SIZE_XS}px;
    font-weight: bold;
    border-radius: 10px;
    padding: 2px 8px;
    background-color: transparent;
}}

/* ── Finance summary cards ── */
#FinanceCard {{
    background-color: {C.BG_CARD};
    border-radius: 14px;
    border: 1px solid {C.BORDER};
}}

#FinanceCard[type="revenue"] {{
    border-top: 4px solid {C.SUCCESS};
}}
#FinanceCard[type="expense"] {{
    border-top: 4px solid {C.WARNING};
}}
#FinanceCard[type="profit"] {{
    border-top: 4px solid {C.INFO};
}}

#FinanceValue[type="revenue"] {{
    color: {C.SUCCESS_TEXT};
    font-size: {F.SIZE_XL}px;
    font-weight: bold;
    background-color: transparent;
}}
#FinanceValue[type="expense"] {{
    color: {C.WARNING_TEXT};
    font-size: {F.SIZE_XL}px;
    font-weight: bold;
    background-color: transparent;
}}
#FinanceValue[type="profit"] {{
    color: {C.INFO};
    font-size: {F.SIZE_XL}px;
    font-weight: bold;
    background-color: transparent;
}}

#FinanceLabel {{
    font-size: {F.SIZE_SM}px;
    color: {C.TEXT_SECONDARY};
    background-color: transparent;
}}

/* ═══════════════════════════════════════════════════════
   SECTION HEADERS (inside module pages)
   ═══════════════════════════════════════════════════════ */

#SectionTitle {{
    font-size: {F.SIZE_LG}px;
    font-weight: bold;
    color: {C.TEXT_PRIMARY};
    background-color: transparent;
    padding: 0px;
}}

#SectionBadge {{
    background-color: {C.PRIMARY_ULTRA};
    color: {C.SUCCESS_TEXT};
    font-size: {F.SIZE_XS}px;
    font-weight: bold;
    border-radius: 10px;
    padding: 2px 10px;
}}

/* ═══════════════════════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════════════════════ */

/* Primary button — green gradient */
#BtnPrimary {{
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 {C.PRIMARY_HOVER},
        stop:1 {C.PRIMARY}
    );
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 9px 20px;
    font-size: {F.SIZE_SM}px;
    font-weight: bold;
    letter-spacing: 0.3px;
    min-height: 36px;
}}

#BtnPrimary:hover {{
    background-color: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 {C.PRIMARY_LIGHT},
        stop:1 {C.PRIMARY_HOVER}
    );
}}

#BtnPrimary:pressed {{
    background-color: {C.PRIMARY};
    padding-top: 10px;
    padding-bottom: 8px;
}}

#BtnPrimary:disabled {{
    background-color: {C.TEXT_TERTIARY};
    color: rgba(255,255,255,0.5);
}}

/* Secondary / outline button */
#BtnSecondary {{
    background-color: {C.BG_CARD};
    color: {C.PRIMARY};
    border: 1.5px solid {C.PRIMARY_BORDER};
    border-radius: 8px;
    padding: 8px 18px;
    font-size: {F.SIZE_SM}px;
    font-weight: bold;
    min-height: 36px;
}}

#BtnSecondary:hover {{
    background-color: {C.PRIMARY_ULTRA};
    border-color: {C.PRIMARY};
}}

#BtnSecondary:pressed {{
    background-color: #D5EDD7;
}}

/* Danger button */
#BtnDanger {{
    background-color: {C.BG_CARD};
    color: {C.DANGER};
    border: 1.5px solid #FFCDD2;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: {F.SIZE_SM}px;
    font-weight: bold;
    min-height: 36px;
}}

#BtnDanger:hover {{
    background-color: {C.DANGER_BG};
    border-color: {C.DANGER};
}}

#BtnDanger:pressed {{
    background-color: #FFCDD2;
}}

/* Ghost / icon-only button */
#BtnGhost {{
    background-color: transparent;
    color: {C.TEXT_SECONDARY};
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: {F.SIZE_SM}px;
    min-height: 32px;
}}

#BtnGhost:hover {{
    background-color: {C.BG_TABLE_ALT};
    color: {C.TEXT_PRIMARY};
}}

/* Convert to invoice — special accent */
#BtnAccent {{
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #0277BD,
        stop:1 #01579B
    );
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 9px 20px;
    font-size: {F.SIZE_SM}px;
    font-weight: bold;
    min-height: 36px;
}}

#BtnAccent:hover {{
    background-color: #0288D1;
}}

/* ═══════════════════════════════════════════════════════
   INPUT FIELDS
   ═══════════════════════════════════════════════════════ */

QLineEdit,
QTextEdit,
QPlainTextEdit {{
    background-color: {C.BG_INPUT};
    border: 1.5px solid {C.BORDER_INPUT};
    border-radius: 8px;
    padding: 8px 12px;
    font-size: {F.SIZE_BASE}px;
    color: {C.TEXT_PRIMARY};
    selection-background-color: {C.PRIMARY_ULTRA};
    selection-color: {C.PRIMARY};
    min-height: 36px;
}}

QLineEdit:focus,
QTextEdit:focus,
QPlainTextEdit:focus {{
    border-color: {C.BORDER_FOCUS};
    background-color: {C.BG_CARD};
}}

QLineEdit:disabled,
QTextEdit:disabled {{
    background-color: {C.BG_TABLE_ALT};
    color: {C.TEXT_TERTIARY};
    border-color: {C.BORDER};
}}

QLineEdit::placeholder {{
    color: {C.TEXT_TERTIARY};
}}

/* ═══════════════════════════════════════════════════════
   COMBO BOX
   ═══════════════════════════════════════════════════════ */

QComboBox {{
    background-color: {C.BG_INPUT};
    border: 1.5px solid {C.BORDER_INPUT};
    border-radius: 8px;
    padding: 7px 12px;
    font-size: {F.SIZE_BASE}px;
    color: {C.TEXT_PRIMARY};
    min-height: 36px;
    combobox-popup: 0;
}}

QComboBox:focus {{
    border-color: {C.BORDER_FOCUS};
}}

QComboBox::drop-down {{
    border: none;
    width: 28px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {C.TEXT_SECONDARY};
    width: 0;
    height: 0;
    margin-right: 8px;
}}

QComboBox QAbstractItemView {{
    background-color: {C.BG_CARD};
    border: 1px solid {C.BORDER};
    border-radius: 8px;
    padding: 4px;
    selection-background-color: {C.PRIMARY_ULTRA};
    selection-color: {C.PRIMARY};
    outline: none;
}}

QComboBox QAbstractItemView::item {{
    min-height: 32px;
    padding: 4px 12px;
    border-radius: 6px;
}}

/* ═══════════════════════════════════════════════════════
   SPIN BOXES
   ═══════════════════════════════════════════════════════ */

QDoubleSpinBox,
QSpinBox {{
    background-color: {C.BG_INPUT};
    border: 1.5px solid {C.BORDER_INPUT};
    border-radius: 8px;
    padding: 7px 10px;
    font-size: {F.SIZE_BASE}px;
    color: {C.TEXT_PRIMARY};
    min-height: 36px;
}}

QDoubleSpinBox:focus,
QSpinBox:focus {{
    border-color: {C.BORDER_FOCUS};
}}

QDoubleSpinBox::up-button,
QDoubleSpinBox::down-button,
QSpinBox::up-button,
QSpinBox::down-button {{
    border: none;
    background-color: transparent;
    width: 18px;
}}

/* ═══════════════════════════════════════════════════════
   DATE EDIT
   ═══════════════════════════════════════════════════════ */

QDateEdit {{
    background-color: {C.BG_INPUT};
    border: 1.5px solid {C.BORDER_INPUT};
    border-radius: 8px;
    padding: 7px 10px;
    font-size: {F.SIZE_BASE}px;
    color: {C.TEXT_PRIMARY};
    min-height: 36px;
}}

QDateEdit:focus {{
    border-color: {C.BORDER_FOCUS};
}}

QDateEdit::drop-down {{
    border: none;
    width: 24px;
}}

QCalendarWidget {{
    background-color: {C.BG_CARD};
    border: 1px solid {C.BORDER};
    border-radius: 10px;
    font-size: {F.SIZE_SM}px;
}}

QCalendarWidget QToolButton {{
    background-color: transparent;
    color: {C.TEXT_PRIMARY};
    font-weight: bold;
    border: none;
    border-radius: 6px;
    padding: 4px 8px;
}}

QCalendarWidget QToolButton:hover {{
    background-color: {C.PRIMARY_ULTRA};
}}

QCalendarWidget QAbstractItemView:enabled {{
    color: {C.TEXT_PRIMARY};
    selection-background-color: {C.PRIMARY};
    selection-color: {C.TEXT_ON_PRIMARY};
}}

/* ═══════════════════════════════════════════════════════
   TABLE WIDGET
   ═══════════════════════════════════════════════════════ */

QTableWidget {{
    background-color: {C.BG_CARD};
    alternate-background-color: {C.BG_TABLE_ALT};
    border: 1px solid {C.BORDER};
    border-radius: 10px;
    gridline-color: {C.DIVIDER};
    font-size: {F.SIZE_SM}px;
    selection-background-color: {C.PRIMARY_ULTRA};
    selection-color: {C.TEXT_PRIMARY};
    outline: none;
}}

QTableWidget::item {{
    padding: 10px 12px;
    border-bottom: 1px solid {C.DIVIDER};
}}

QTableWidget::item:selected {{
    background-color: {C.PRIMARY_ULTRA};
    color: {C.TEXT_PRIMARY};
    border-left: 3px solid {C.PRIMARY};
}}

QTableWidget::item:hover {{
    background-color: #F2F8F3;
}}

QHeaderView::section {{
    background-color: {C.BG_HEADER};
    color: {C.TEXT_ON_PRIMARY};
    font-size: {F.SIZE_SM}px;
    font-weight: bold;
    padding: 12px 12px;
    border: none;
    border-right: 1px solid rgba(255,255,255,0.08);
    letter-spacing: 0.3px;
}}

QHeaderView::section:first {{
    border-top-right-radius: 10px;
}}

QHeaderView::section:last {{
    border-top-left-radius: 10px;
    border-right: none;
}}

QHeaderView::section:hover {{
    background-color: {C.PRIMARY_HOVER};
}}

/* ═══════════════════════════════════════════════════════
   TAB WIDGET
   ═══════════════════════════════════════════════════════ */

QTabWidget::pane {{
    border: 1px solid {C.BORDER};
    border-radius: 0 0 12px 12px;
    background-color: {C.BG_CARD};
    top: -1px;
}}

QTabBar {{
    background-color: transparent;
}}

QTabBar::tab {{
    background-color: {C.BG_APP};
    color: {C.TEXT_SECONDARY};
    border: 1px solid {C.BORDER};
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    padding: 10px 22px;
    font-size: {F.SIZE_SM}px;
    font-weight: normal;
    margin-right: 2px;
    min-width: 80px;
}}

QTabBar::tab:selected {{
    background-color: {C.BG_CARD};
    color: {C.PRIMARY};
    font-weight: bold;
    border-color: {C.BORDER};
    border-bottom: 2px solid {C.PRIMARY};
}}

QTabBar::tab:hover:!selected {{
    background-color: {C.BG_CARD};
    color: {C.TEXT_PRIMARY};
}}

/* ═══════════════════════════════════════════════════════
   SCROLL BAR
   ═══════════════════════════════════════════════════════ */

QScrollBar:vertical {{
    background-color: {C.BG_APP};
    width: 8px;
    border-radius: 4px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background-color: {C.BORDER_INPUT};
    border-radius: 4px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {C.TEXT_TERTIARY};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background: none;
    height: 0;
}}

QScrollBar:horizontal {{
    background-color: {C.BG_APP};
    height: 8px;
    border-radius: 4px;
    margin: 2px;
}}

QScrollBar::handle:horizontal {{
    background-color: {C.BORDER_INPUT};
    border-radius: 4px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {C.TEXT_TERTIARY};
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    background: none;
    width: 0;
}}

/* ═══════════════════════════════════════════════════════
   SCROLL AREA
   ═══════════════════════════════════════════════════════ */

QScrollArea {{
    border: none;
    background-color: transparent;
}}

QScrollArea > QWidget > QWidget {{
    background-color: transparent;
}}

/* ═══════════════════════════════════════════════════════
   DIALOG
   ═══════════════════════════════════════════════════════ */

QDialog {{
    background-color: {C.BG_CARD};
    border-radius: 14px;
}}

#DialogHeader {{
    background-color: {C.PRIMARY};
    border-radius: 14px 14px 0 0;
    padding: 18px 24px;
}}

#DialogHeaderTitle {{
    color: {C.TEXT_ON_PRIMARY};
    font-size: {F.SIZE_LG}px;
    font-weight: bold;
    background-color: transparent;
}}

/* Form layout labels inside dialogs */
QDialog QLabel {{
    font-size: {F.SIZE_SM}px;
    color: {C.TEXT_SECONDARY};
    font-weight: bold;
    background-color: transparent;
}}

/* ═══════════════════════════════════════════════════════
   GROUP BOX
   ═══════════════════════════════════════════════════════ */

QGroupBox {{
    background-color: {C.BG_CARD};
    border: 1px solid {C.BORDER};
    border-radius: 10px;
    margin-top: 16px;
    padding: 16px 12px 12px 12px;
    font-size: {F.SIZE_SM}px;
    font-weight: bold;
    color: {C.TEXT_PRIMARY};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top right;
    padding: 0 8px;
    color: {C.PRIMARY};
    background-color: {C.BG_CARD};
}}

/* ═══════════════════════════════════════════════════════
   FRAME CARD  (generic card wrapper)
   ═══════════════════════════════════════════════════════ */

#Card {{
    background-color: {C.BG_CARD};
    border: 1px solid {C.BORDER};
    border-radius: 14px;
}}

#CardHeader {{
    background-color: {C.BG_CARD};
    border-bottom: 1px solid {C.BORDER};
    border-radius: 14px 14px 0 0;
    padding: 16px 20px;
}}

/* ═══════════════════════════════════════════════════════
   SPLITTER
   ═══════════════════════════════════════════════════════ */

QSplitter::handle {{
    background-color: {C.BORDER};
    width: 1px;
    height: 1px;
}}

QSplitter::handle:hover {{
    background-color: {C.PRIMARY_BORDER};
}}

/* ═══════════════════════════════════════════════════════
   MESSAGE BOX
   ═══════════════════════════════════════════════════════ */

QMessageBox {{
    background-color: {C.BG_CARD};
    font-size: {F.SIZE_BASE}px;
}}

QMessageBox QLabel {{
    color: {C.TEXT_PRIMARY};
    font-size: {F.SIZE_BASE}px;
    font-weight: normal;
    background-color: transparent;
}}

QMessageBox QPushButton {{
    background-color: {C.PRIMARY};
    color: white;
    border: none;
    border-radius: 7px;
    padding: 8px 20px;
    font-weight: bold;
    min-width: 80px;
}}

QMessageBox QPushButton:hover {{
    background-color: {C.PRIMARY_HOVER};
}}

/* ═══════════════════════════════════════════════════════
   TOOLTIP
   ═══════════════════════════════════════════════════════ */

QToolTip {{
    background-color: {C.TEXT_PRIMARY};
    color: {C.TEXT_ON_PRIMARY};
    border: none;
    border-radius: 6px;
    padding: 5px 10px;
    font-size: {F.SIZE_XS}px;
}}

/* ═══════════════════════════════════════════════════════
   STATUS / BADGE LABELS
   ═══════════════════════════════════════════════════════ */

#StatusPaid {{
    background-color: {C.SUCCESS_BG};
    color: {C.SUCCESS_TEXT};
    border-radius: 10px;
    padding: 2px 10px;
    font-size: {F.SIZE_XS}px;
    font-weight: bold;
}}

#StatusUnpaid {{
    background-color: {C.WARNING_BG};
    color: {C.WARNING_TEXT};
    border-radius: 10px;
    padding: 2px 10px;
    font-size: {F.SIZE_XS}px;
    font-weight: bold;
}}

#StatusDraft {{
    background-color: {C.BG_TABLE_ALT};
    color: {C.TEXT_SECONDARY};
    border-radius: 10px;
    padding: 2px 10px;
    font-size: {F.SIZE_XS}px;
    font-weight: bold;
}}

/* ═══════════════════════════════════════════════════════
   SEARCH BAR
   ═══════════════════════════════════════════════════════ */

#SearchBar {{
    background-color: {C.BG_CARD};
    border: 1.5px solid {C.BORDER};
    border-radius: 20px;
    padding: 8px 16px 8px 36px;
    font-size: {F.SIZE_SM}px;
    color: {C.TEXT_PRIMARY};
    min-height: 36px;
}}

#SearchBar:focus {{
    border-color: {C.BORDER_FOCUS};
}}

/* ═══════════════════════════════════════════════════════
   PROGRESS BAR
   ═══════════════════════════════════════════════════════ */

QProgressBar {{
    background-color: {C.BORDER};
    border: none;
    border-radius: 4px;
    height: 6px;
    text-align: center;
    font-size: 0px;
}}

QProgressBar::chunk {{
    background-color: {C.PRIMARY};
    border-radius: 4px;
}}

/* ═══════════════════════════════════════════════════════
   CHECK BOX & RADIO BUTTON
   ═══════════════════════════════════════════════════════ */

QCheckBox {{
    color: {C.TEXT_PRIMARY};
    font-size: {F.SIZE_SM}px;
    spacing: 8px;
    background-color: transparent;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 1.5px solid {C.BORDER_INPUT};
    border-radius: 4px;
    background-color: {C.BG_INPUT};
}}

QCheckBox::indicator:checked {{
    background-color: {C.PRIMARY};
    border-color: {C.PRIMARY};
}}

QCheckBox::indicator:hover {{
    border-color: {C.PRIMARY};
}}

/* ═══════════════════════════════════════════════════════
   LABEL VARIANTS
   ═══════════════════════════════════════════════════════ */

#LabelCaption {{
    font-size: {F.SIZE_XS}px;
    color: {C.TEXT_TERTIARY};
    background-color: transparent;
}}

#LabelValue {{
    font-size: {F.SIZE_MD}px;
    font-weight: bold;
    color: {C.TEXT_PRIMARY};
    background-color: transparent;
}}

#LabelSuccess {{
    color: {C.SUCCESS_TEXT};
    font-weight: bold;
    background-color: transparent;
}}

#LabelWarning {{
    color: {C.WARNING_TEXT};
    font-weight: bold;
    background-color: transparent;
}}

#LabelInfo {{
    color: {C.INFO};
    font-weight: bold;
    background-color: transparent;
}}

/* ═══════════════════════════════════════════════════════
   TOOLBAR / ACTION BAR
   ═══════════════════════════════════════════════════════ */

#ActionBar {{
    background-color: {C.BG_CARD};
    border: 1px solid {C.BORDER};
    border-radius: 10px;
    padding: 8px 16px;
}}

/* ═══════════════════════════════════════════════════════
   DIVIDER LINE
   ═══════════════════════════════════════════════════════ */

#Divider {{
    background-color: {C.BORDER};
    max-height: 1px;
    min-height: 1px;
}}

"""

# ═══════════════════════════════════════════════════════════════════════
# APPLY FUNCTION
# ═══════════════════════════════════════════════════════════════════════

def apply_app_styles(app: QApplication) -> None:
    """Apply the complete design system to a QApplication instance."""
    # RTL layout direction
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    # Font
    font = QFont("Cairo")
    if not font.exactMatch():
        font = QFont("Tajawal")
    if not font.exactMatch():
        font = QFont("Segoe UI")
    font.setPointSize(FONTS.SIZE_BASE - 3)   # QFont uses points; adjust
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    app.setFont(font)

    # Apply QSS
    app.setStyleSheet(_build_qss())


# ═══════════════════════════════════════════════════════════════════════
# WIDGET FACTORY HELPERS
# Convenience functions for creating consistently-styled widgets.
# These are imported and used throughout main.py.
# ═══════════════════════════════════════════════════════════════════════

from PyQt6.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QFrame, QWidget,
    QHBoxLayout, QVBoxLayout, QDateEdit, QScrollArea
)
from PyQt6.QtCore import QDate, QSize
from PyQt6.QtGui import QColor


def make_btn(text: str, variant: str = "primary", icon: str = "") -> QPushButton:
    """
    Create a styled button.
    variant: 'primary' | 'secondary' | 'danger' | 'ghost' | 'accent'
    """
    btn = QPushButton(f"{icon}  {text}".strip() if icon else text)
    id_map = {
        "primary":   "BtnPrimary",
        "secondary": "BtnSecondary",
        "danger":    "BtnDanger",
        "ghost":     "BtnGhost",
        "accent":    "BtnAccent",
    }
    btn.setObjectName(id_map.get(variant, "BtnPrimary"))
    btn.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    return btn


def make_label(text: str, variant: str = "body") -> QLabel:
    """
    Create a styled label.
    variant: 'title' | 'section' | 'caption' | 'value' | 'success' | 'warning' | 'info' | 'body'
    """
    lbl = QLabel(text)
    lbl.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    id_map = {
        "section": "SectionTitle",
        "caption": "LabelCaption",
        "value":   "LabelValue",
        "success": "LabelSuccess",
        "warning": "LabelWarning",
        "info":    "LabelInfo",
    }
    if variant in id_map:
        lbl.setObjectName(id_map[variant])
    return lbl


def make_input(placeholder: str = "") -> QLineEdit:
    """Create a styled input field."""
    inp = QLineEdit()
    inp.setPlaceholderText(placeholder)
    inp.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    return inp


def make_date(default_today: bool = True) -> QDateEdit:
    """Create a styled date picker."""
    d = QDateEdit()
    d.setCalendarPopup(True)
    d.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    if default_today:
        d.setDate(QDate.currentDate())
    return d


def make_card(object_name: str = "Card") -> QFrame:
    """Create a styled card frame."""
    card = QFrame()
    card.setObjectName(object_name)
    card.setFrameShape(QFrame.Shape.NoFrame)
    return card


def make_divider(vertical: bool = False) -> QFrame:
    """Create a thin divider line."""
    div = QFrame()
    div.setObjectName("Divider")
    if vertical:
        div.setFrameShape(QFrame.Shape.VLine)
        div.setMaximumWidth(1)
    else:
        div.setFrameShape(QFrame.Shape.HLine)
        div.setMaximumHeight(1)
    return div


def make_scroll_area(widget: QWidget) -> QScrollArea:
    """Wrap a widget in a styled scroll area."""
    scroll = QScrollArea()
    scroll.setWidget(widget)
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    return scroll


def make_action_bar(*buttons) -> QWidget:
    """Create a horizontal action bar with a group of buttons."""
    bar = QWidget()
    bar.setObjectName("ActionBar")
    layout = QHBoxLayout(bar)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    layout.addStretch()
    for btn in buttons:
        layout.addWidget(btn)
    return bar
