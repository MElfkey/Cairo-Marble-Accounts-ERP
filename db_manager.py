"""
Cairo Marble ERP - Database Manager
====================================
Handles all SQLite database operations.
"""

import sqlite3
import os
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Tuple


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cairo_marble.db")


class DatabaseManager:
    """Central database manager for Cairo Marble ERP."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    # ─────────────────────────────────────────────
    # Connection helpers
    # ─────────────────────────────────────────────

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            return cur

    def _fetchall(self, sql: str, params: tuple = ()) -> List[sqlite3.Row]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchall()

    def _fetchone(self, sql: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchone()

    # ─────────────────────────────────────────────
    # Schema initialisation
    # ─────────────────────────────────────────────

    def _init_db(self):
        ddl_statements = [
            # Employees
            """CREATE TABLE IF NOT EXISTS employees (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                job_title   TEXT,
                phone       TEXT,
                hire_date   TEXT,
                base_salary REAL DEFAULT 0,
                notes       TEXT,
                active      INTEGER DEFAULT 1
            )""",

            # Attendance
            """CREATE TABLE IF NOT EXISTS attendance (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL REFERENCES employees(id),
                work_date   TEXT NOT NULL,
                status      TEXT DEFAULT 'present',   -- present / absent / late
                overtime_hours REAL DEFAULT 0
            )""",

            # Advances (سلف)
            """CREATE TABLE IF NOT EXISTS advances (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL REFERENCES employees(id),
                amount      REAL NOT NULL,
                advance_date TEXT NOT NULL,
                notes       TEXT,
                repaid      INTEGER DEFAULT 0
            )""",

            # Clients
            """CREATE TABLE IF NOT EXISTS clients (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT NOT NULL,
                phone   TEXT,
                address TEXT,
                notes   TEXT
            )""",

            # Quotes (عروض أسعار)
            """CREATE TABLE IF NOT EXISTS quotes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                serial      TEXT UNIQUE NOT NULL,
                client_id   INTEGER REFERENCES clients(id),
                quote_date  TEXT NOT NULL,
                expiry_date TEXT,
                salesperson TEXT,
                status      TEXT DEFAULT 'draft',   -- draft / sent / converted / expired
                notes       TEXT,
                total       REAL DEFAULT 0
            )""",

            # Quote line items
            """CREATE TABLE IF NOT EXISTS quote_items (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                quote_id    INTEGER NOT NULL REFERENCES quotes(id) ON DELETE CASCADE,
                description TEXT NOT NULL,
                quantity    REAL DEFAULT 1,
                unit_price  REAL DEFAULT 0,
                tax_rate    REAL DEFAULT 0,
                amount      REAL DEFAULT 0
            )""",

            # Invoices (فواتير)
            """CREATE TABLE IF NOT EXISTS invoices (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                serial       TEXT UNIQUE NOT NULL,
                quote_id     INTEGER REFERENCES quotes(id),
                client_id    INTEGER REFERENCES clients(id),
                invoice_date TEXT NOT NULL,
                due_date     TEXT,
                status       TEXT DEFAULT 'unpaid',   -- unpaid / paid / partial
                paid_amount  REAL DEFAULT 0,
                notes        TEXT,
                total        REAL DEFAULT 0
            )""",

            # Invoice line items
            """CREATE TABLE IF NOT EXISTS invoice_items (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id  INTEGER NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
                description TEXT NOT NULL,
                quantity    REAL DEFAULT 1,
                unit_price  REAL DEFAULT 0,
                tax_rate    REAL DEFAULT 0,
                amount      REAL DEFAULT 0
            )""",

            # Drivers
            """CREATE TABLE IF NOT EXISTS drivers (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT NOT NULL,
                phone   TEXT,
                license TEXT,
                notes   TEXT,
                active  INTEGER DEFAULT 1
            )""",

            # Trips (رحلات)
            """CREATE TABLE IF NOT EXISTS trips (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                driver_id   INTEGER NOT NULL REFERENCES drivers(id),
                trip_date   TEXT NOT NULL,
                destination TEXT,
                price       REAL DEFAULT 0,
                notes       TEXT
            )""",

            # Projects
            """CREATE TABLE IF NOT EXISTS projects (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                owner       TEXT,
                start_date  TEXT,
                end_date    TEXT,
                status      TEXT DEFAULT 'active',
                notes       TEXT,
                total_cost  REAL DEFAULT 0
            )""",

            # Project raw materials
            """CREATE TABLE IF NOT EXISTS project_materials (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id  INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                description TEXT NOT NULL,
                quantity    REAL DEFAULT 1,
                unit_price  REAL DEFAULT 0,
                amount      REAL DEFAULT 0,
                entry_date  TEXT NOT NULL
            )""",

            # Finance: Expenses & Revenues
            """CREATE TABLE IF NOT EXISTS finance (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date  TEXT NOT NULL,
                category    TEXT NOT NULL,   -- 'expense' or 'revenue'
                source      TEXT,            -- 'invoice' / 'trip' / 'project' / 'manual'
                ref_id      INTEGER,         -- foreign key to source table
                description TEXT,
                amount      REAL DEFAULT 0
            )""",
        ]

        with self._get_conn() as conn:
            for ddl in ddl_statements:
                conn.execute(ddl)
            conn.commit()

    # ─────────────────────────────────────────────
    # Serial number generation
    # ─────────────────────────────────────────────

    def next_serial(self, prefix: str, table: str) -> str:
        """Generate next serial like S00501."""
        row = self._fetchone(f"SELECT COUNT(*) as cnt FROM {table}")
        n = (row["cnt"] if row else 0) + 1
        return f"{prefix}{n:05d}"

    # ═══════════════════════════════════════════════
    # EMPLOYEES
    # ═══════════════════════════════════════════════

    def add_employee(self, name: str, job_title: str, phone: str,
                     hire_date: str, base_salary: float, notes: str = "") -> int:
        cur = self._execute(
            "INSERT INTO employees (name,job_title,phone,hire_date,base_salary,notes) VALUES (?,?,?,?,?,?)",
            (name, job_title, phone, hire_date, base_salary, notes)
        )
        return cur.lastrowid

    def update_employee(self, emp_id: int, **fields) -> None:
        sets = ", ".join(f"{k}=?" for k in fields)
        self._execute(f"UPDATE employees SET {sets} WHERE id=?", (*fields.values(), emp_id))

    def get_employees(self, active_only: bool = True) -> List[sqlite3.Row]:
        sql = "SELECT * FROM employees"
        if active_only:
            sql += " WHERE active=1"
        sql += " ORDER BY name"
        return self._fetchall(sql)

    def get_employee(self, emp_id: int) -> Optional[sqlite3.Row]:
        return self._fetchone("SELECT * FROM employees WHERE id=?", (emp_id,))

    def delete_employee(self, emp_id: int) -> None:
        self._execute("UPDATE employees SET active=0 WHERE id=?", (emp_id,))

    # Attendance
    def add_attendance(self, emp_id: int, work_date: str, status: str, overtime: float = 0) -> int:
        cur = self._execute(
            "INSERT INTO attendance (employee_id,work_date,status,overtime_hours) VALUES (?,?,?,?)",
            (emp_id, work_date, status, overtime)
        )
        return cur.lastrowid

    def get_attendance(self, emp_id: int, month: str = None) -> List[sqlite3.Row]:
        if month:
            return self._fetchall(
                "SELECT * FROM attendance WHERE employee_id=? AND work_date LIKE ? ORDER BY work_date",
                (emp_id, f"{month}%")
            )
        return self._fetchall(
            "SELECT * FROM attendance WHERE employee_id=? ORDER BY work_date DESC",
            (emp_id,)
        )

    # Advances
    def add_advance(self, emp_id: int, amount: float, advance_date: str, notes: str = "") -> int:
        cur = self._execute(
            "INSERT INTO advances (employee_id,amount,advance_date,notes) VALUES (?,?,?,?)",
            (emp_id, amount, advance_date, notes)
        )
        return cur.lastrowid

    def get_advances(self, emp_id: int) -> List[sqlite3.Row]:
        return self._fetchall(
            "SELECT * FROM advances WHERE employee_id=? ORDER BY advance_date DESC", (emp_id,)
        )

    def get_total_advances(self, emp_id: int) -> float:
        row = self._fetchone(
            "SELECT SUM(amount) as total FROM advances WHERE employee_id=? AND repaid=0", (emp_id,)
        )
        return row["total"] or 0.0

    def mark_advance_repaid(self, advance_id: int) -> None:
        self._execute("UPDATE advances SET repaid=1 WHERE id=?", (advance_id,))

    def calc_monthly_salary(self, emp_id: int, month: str) -> Dict[str, float]:
        """Calculate net salary for a given month (YYYY-MM)."""
        emp = self.get_employee(emp_id)
        if not emp:
            return {}
        base = emp["base_salary"]
        attendance = self.get_attendance(emp_id, month)
        present_days = sum(1 for r in attendance if r["status"] == "present")
        absent_days  = sum(1 for r in attendance if r["status"] == "absent")
        overtime_hrs = sum(r["overtime_hours"] for r in attendance)
        overtime_rate = (base / 30 / 8) * 1.5
        overtime_pay  = overtime_hrs * overtime_rate
        deductions    = (base / 30) * absent_days
        advances_month = self._fetchone(
            "SELECT SUM(amount) as total FROM advances WHERE employee_id=? AND advance_date LIKE ? AND repaid=0",
            (emp_id, f"{month}%")
        )
        advance_deduction = advances_month["total"] or 0.0
        net = base + overtime_pay - deductions - advance_deduction
        return {
            "base_salary": base,
            "present_days": present_days,
            "absent_days": absent_days,
            "overtime_hours": overtime_hrs,
            "overtime_pay": overtime_pay,
            "deductions": deductions,
            "advance_deduction": advance_deduction,
            "net_salary": net,
        }

    # ═══════════════════════════════════════════════
    # CLIENTS
    # ═══════════════════════════════════════════════

    def add_client(self, name: str, phone: str, address: str, notes: str = "") -> int:
        cur = self._execute(
            "INSERT INTO clients (name,phone,address,notes) VALUES (?,?,?,?)",
            (name, phone, address, notes)
        )
        return cur.lastrowid

    def update_client(self, client_id: int, **fields) -> None:
        sets = ", ".join(f"{k}=?" for k in fields)
        self._execute(f"UPDATE clients SET {sets} WHERE id=?", (*fields.values(), client_id))

    def get_clients(self) -> List[sqlite3.Row]:
        return self._fetchall("SELECT * FROM clients ORDER BY name")

    def get_client(self, client_id: int) -> Optional[sqlite3.Row]:
        return self._fetchone("SELECT * FROM clients WHERE id=?", (client_id,))

    def delete_client(self, client_id: int) -> None:
        self._execute("DELETE FROM clients WHERE id=?", (client_id,))

    def get_client_transactions(self, client_id: int) -> Dict:
        quotes   = self._fetchall("SELECT * FROM quotes WHERE client_id=? ORDER BY quote_date DESC", (client_id,))
        invoices = self._fetchall("SELECT * FROM invoices WHERE client_id=? ORDER BY invoice_date DESC", (client_id,))
        return {"quotes": quotes, "invoices": invoices}

    # ═══════════════════════════════════════════════
    # QUOTES
    # ═══════════════════════════════════════════════

    def add_quote(self, client_id: int, quote_date: str, expiry_date: str,
                  salesperson: str, items: List[Dict], notes: str = "") -> int:
        serial = self.next_serial("S", "quotes")
        total  = sum(i["amount"] for i in items)
        cur    = self._execute(
            "INSERT INTO quotes (serial,client_id,quote_date,expiry_date,salesperson,notes,total) VALUES (?,?,?,?,?,?,?)",
            (serial, client_id, quote_date, expiry_date, salesperson, notes, total)
        )
        qid = cur.lastrowid
        for item in items:
            self._execute(
                "INSERT INTO quote_items (quote_id,description,quantity,unit_price,tax_rate,amount) VALUES (?,?,?,?,?,?)",
                (qid, item["description"], item["quantity"], item["unit_price"], item.get("tax_rate", 0), item["amount"])
            )
        return qid

    def get_quotes(self, client_id: int = None) -> List[sqlite3.Row]:
        if client_id:
            return self._fetchall(
                "SELECT q.*,c.name as client_name FROM quotes q LEFT JOIN clients c ON q.client_id=c.id WHERE q.client_id=? ORDER BY q.quote_date DESC",
                (client_id,)
            )
        return self._fetchall(
            "SELECT q.*,c.name as client_name FROM quotes q LEFT JOIN clients c ON q.client_id=c.id ORDER BY q.quote_date DESC"
        )

    def get_quote(self, quote_id: int) -> Optional[sqlite3.Row]:
        return self._fetchone("SELECT * FROM quotes WHERE id=?", (quote_id,))

    def get_quote_items(self, quote_id: int) -> List[sqlite3.Row]:
        return self._fetchall("SELECT * FROM quote_items WHERE quote_id=?", (quote_id,))

    def update_quote_status(self, quote_id: int, status: str) -> None:
        self._execute("UPDATE quotes SET status=? WHERE id=?", (status, quote_id))

    def delete_quote(self, quote_id: int) -> None:
        self._execute("DELETE FROM quotes WHERE id=?", (quote_id,))

    # ═══════════════════════════════════════════════
    # INVOICES
    # ═══════════════════════════════════════════════

    def convert_quote_to_invoice(self, quote_id: int, invoice_date: str, due_date: str) -> int:
        quote = self.get_quote(quote_id)
        items = self.get_quote_items(quote_id)
        if not quote:
            raise ValueError("Quote not found")
        serial = self.next_serial("INV", "invoices")
        cur = self._execute(
            "INSERT INTO invoices (serial,quote_id,client_id,invoice_date,due_date,status,total,notes) VALUES (?,?,?,?,?,?,?,?)",
            (serial, quote_id, quote["client_id"], invoice_date, due_date, "unpaid", quote["total"], quote["notes"])
        )
        inv_id = cur.lastrowid
        for item in items:
            self._execute(
                "INSERT INTO invoice_items (invoice_id,description,quantity,unit_price,tax_rate,amount) VALUES (?,?,?,?,?,?)",
                (inv_id, item["description"], item["quantity"], item["unit_price"], item["tax_rate"], item["amount"])
            )
        self.update_quote_status(quote_id, "converted")
        return inv_id

    def add_invoice(self, client_id: int, invoice_date: str, due_date: str,
                    items: List[Dict], notes: str = "") -> int:
        serial = self.next_serial("INV", "invoices")
        total  = sum(i["amount"] for i in items)
        cur    = self._execute(
            "INSERT INTO invoices (serial,client_id,invoice_date,due_date,status,total,notes) VALUES (?,?,?,?,?,?,?)",
            (serial, client_id, invoice_date, due_date, "unpaid", total, notes)
        )
        inv_id = cur.lastrowid
        for item in items:
            self._execute(
                "INSERT INTO invoice_items (invoice_id,description,quantity,unit_price,tax_rate,amount) VALUES (?,?,?,?,?,?)",
                (inv_id, item["description"], item["quantity"], item["unit_price"], item.get("tax_rate", 0), item["amount"])
            )
        return inv_id

    def get_invoices(self, client_id: int = None) -> List[sqlite3.Row]:
        if client_id:
            return self._fetchall(
                "SELECT i.*,c.name as client_name FROM invoices i LEFT JOIN clients c ON i.client_id=c.id WHERE i.client_id=? ORDER BY i.invoice_date DESC",
                (client_id,)
            )
        return self._fetchall(
            "SELECT i.*,c.name as client_name FROM invoices i LEFT JOIN clients c ON i.client_id=c.id ORDER BY i.invoice_date DESC"
        )

    def get_invoice(self, inv_id: int) -> Optional[sqlite3.Row]:
        return self._fetchone("SELECT * FROM invoices WHERE id=?", (inv_id,))

    def get_invoice_items(self, inv_id: int) -> List[sqlite3.Row]:
        return self._fetchall("SELECT * FROM invoice_items WHERE invoice_id=?", (inv_id,))

    def settle_invoice(self, inv_id: int, paid_amount: float) -> None:
        inv = self.get_invoice(inv_id)
        if not inv:
            return
        total_paid = inv["paid_amount"] + paid_amount
        status = "paid" if total_paid >= inv["total"] else "partial"
        self._execute(
            "UPDATE invoices SET paid_amount=?, status=? WHERE id=?",
            (total_paid, status, inv_id)
        )
        # Auto-create finance revenue entry
        self._execute(
            "INSERT INTO finance (entry_date,category,source,ref_id,description,amount) VALUES (?,?,?,?,?,?)",
            (date.today().isoformat(), "revenue", "invoice", inv_id, f"تسوية فاتورة {inv['serial']}", paid_amount)
        )

    def delete_invoice(self, inv_id: int) -> None:
        self._execute("DELETE FROM invoices WHERE id=?", (inv_id,))

    # ═══════════════════════════════════════════════
    # DRIVERS & TRIPS
    # ═══════════════════════════════════════════════

    def add_driver(self, name: str, phone: str, license_num: str, notes: str = "") -> int:
        cur = self._execute(
            "INSERT INTO drivers (name,phone,license,notes) VALUES (?,?,?,?)",
            (name, phone, license_num, notes)
        )
        return cur.lastrowid

    def get_drivers(self, active_only: bool = True) -> List[sqlite3.Row]:
        sql = "SELECT * FROM drivers"
        if active_only:
            sql += " WHERE active=1"
        return self._fetchall(sql + " ORDER BY name")

    def get_driver(self, driver_id: int) -> Optional[sqlite3.Row]:
        return self._fetchone("SELECT * FROM drivers WHERE id=?", (driver_id,))

    def update_driver(self, driver_id: int, **fields) -> None:
        sets = ", ".join(f"{k}=?" for k in fields)
        self._execute(f"UPDATE drivers SET {sets} WHERE id=?", (*fields.values(), driver_id))

    def delete_driver(self, driver_id: int) -> None:
        self._execute("UPDATE drivers SET active=0 WHERE id=?", (driver_id,))

    def add_trip(self, driver_id: int, trip_date: str, destination: str, price: float, notes: str = "") -> int:
        cur = self._execute(
            "INSERT INTO trips (driver_id,trip_date,destination,price,notes) VALUES (?,?,?,?,?)",
            (driver_id, trip_date, destination, price, notes)
        )
        trip_id = cur.lastrowid
        drv = self.get_driver(driver_id)
        self._execute(
            "INSERT INTO finance (entry_date,category,source,ref_id,description,amount) VALUES (?,?,?,?,?,?)",
            (trip_date, "expense", "trip", trip_id, f"رحلة - {drv['name'] if drv else ''} - {destination}", price)
        )
        return trip_id

    def get_trips(self, driver_id: int = None) -> List[sqlite3.Row]:
        if driver_id:
            return self._fetchall(
                "SELECT t.*,d.name as driver_name FROM trips t JOIN drivers d ON t.driver_id=d.id WHERE t.driver_id=? ORDER BY t.trip_date DESC",
                (driver_id,)
            )
        return self._fetchall(
            "SELECT t.*,d.name as driver_name FROM trips t JOIN drivers d ON t.driver_id=d.id ORDER BY t.trip_date DESC"
        )

    def delete_trip(self, trip_id: int) -> None:
        self._execute("DELETE FROM trips WHERE id=?", (trip_id,))

    # ═══════════════════════════════════════════════
    # PROJECTS
    # ═══════════════════════════════════════════════

    def add_project(self, name: str, owner: str, start_date: str, end_date: str = "", notes: str = "") -> int:
        cur = self._execute(
            "INSERT INTO projects (name,owner,start_date,end_date,notes) VALUES (?,?,?,?,?)",
            (name, owner, start_date, end_date, notes)
        )
        return cur.lastrowid

    def get_projects(self) -> List[sqlite3.Row]:
        return self._fetchall("SELECT * FROM projects ORDER BY start_date DESC")

    def get_project(self, proj_id: int) -> Optional[sqlite3.Row]:
        return self._fetchone("SELECT * FROM projects WHERE id=?", (proj_id,))

    def update_project(self, proj_id: int, **fields) -> None:
        sets = ", ".join(f"{k}=?" for k in fields)
        self._execute(f"UPDATE projects SET {sets} WHERE id=?", (*fields.values(), proj_id))

    def delete_project(self, proj_id: int) -> None:
        self._execute("DELETE FROM projects WHERE id=?", (proj_id,))

    def add_project_material(self, proj_id: int, description: str, quantity: float,
                              unit_price: float, entry_date: str) -> int:
        amount = quantity * unit_price
        cur = self._execute(
            "INSERT INTO project_materials (project_id,description,quantity,unit_price,amount,entry_date) VALUES (?,?,?,?,?,?)",
            (proj_id, description, quantity, unit_price, amount, entry_date)
        )
        mat_id = cur.lastrowid
        proj = self.get_project(proj_id)
        self._execute(
            "UPDATE projects SET total_cost = total_cost + ? WHERE id=?", (amount, proj_id)
        )
        self._execute(
            "INSERT INTO finance (entry_date,category,source,ref_id,description,amount) VALUES (?,?,?,?,?,?)",
            (entry_date, "expense", "project", proj_id, f"مواد خام - {proj['name'] if proj else ''} - {description}", amount)
        )
        return mat_id

    def get_project_materials(self, proj_id: int) -> List[sqlite3.Row]:
        return self._fetchall("SELECT * FROM project_materials WHERE project_id=? ORDER BY entry_date", (proj_id,))

    def delete_project_material(self, mat_id: int) -> None:
        self._execute("DELETE FROM project_materials WHERE id=?", (mat_id,))

    # ═══════════════════════════════════════════════
    # FINANCE
    # ═══════════════════════════════════════════════

    def add_finance_entry(self, entry_date: str, category: str, source: str,
                          description: str, amount: float) -> int:
        cur = self._execute(
            "INSERT INTO finance (entry_date,category,source,description,amount) VALUES (?,?,?,?,?)",
            (entry_date, category, source, description, amount)
        )
        return cur.lastrowid

    def get_finance(self, category: str = None, month: str = None) -> List[sqlite3.Row]:
        conditions = []
        params = []
        if category:
            conditions.append("category=?")
            params.append(category)
        if month:
            conditions.append("entry_date LIKE ?")
            params.append(f"{month}%")
        sql = "SELECT * FROM finance"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY entry_date DESC"
        return self._fetchall(sql, tuple(params))

    def get_finance_summary(self, month: str = None) -> Dict[str, float]:
        params = []
        where  = ""
        if month:
            where  = "WHERE entry_date LIKE ?"
            params = [f"{month}%"]
        revenues = self._fetchone(f"SELECT SUM(amount) as t FROM finance {where} AND category='revenue'" if month else "SELECT SUM(amount) as t FROM finance WHERE category='revenue'", tuple(params))
        expenses = self._fetchone(f"SELECT SUM(amount) as t FROM finance {where} AND category='expense'" if month else "SELECT SUM(amount) as t FROM finance WHERE category='expense'", tuple(params))
        rev = revenues["t"] or 0.0
        exp = expenses["t"] or 0.0
        return {"revenues": rev, "expenses": exp, "profit": rev - exp}

    def delete_finance_entry(self, entry_id: int) -> None:
        self._execute("DELETE FROM finance WHERE id=?", (entry_id,))
