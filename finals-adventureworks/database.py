"""
database.py — DB 연결 설정
SQLite + pandas 기반 AdventureWorks CRM
"""

import sqlite3
import pandas as pd

DB_FILE = "adventureworks.db"


def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """FastAPI 의존성 주입용"""
    conn = get_conn()
    try:
        yield conn
    finally:
        conn.close()


def create_tables():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            SalesOrderLineKey    INTEGER,
            CustomerKey          INTEGER,
            ProductKey           INTEGER,
            SalesTerritoryKey    INTEGER,
            "Order Quantity"     INTEGER,
            "Unit Price"         REAL,
            "Sales Amount"       REAL,
            "Total Product Cost" REAL,
            "Country-Region"     TEXT,
            Region               TEXT,
            Category             TEXT,
            Subcategory          TEXT,
            Color                TEXT,
            Customer             TEXT,
            City                 TEXT,
            "State-Province"     TEXT,
            Date                 TEXT,
            month_num            INTEGER,
            year_num             INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS customer_features (
            CustomerKey              INTEGER PRIMARY KEY,
            last_purchase            TEXT,
            first_purchase           TEXT,
            total_orders             INTEGER,
            total_spend              REAL,
            avg_spend                REAL,
            max_spend                REAL,
            min_spend                REAL,
            Recency                  INTEGER,
            tenure_days              INTEGER,
            avg_days_between_orders  REAL,
            loyalty_decay_rate       REAL,
            churn_risk_score         REAL,
            is_churn_risk            INTEGER,
            buys_bikes               INTEGER,
            buys_accessories         INTEGER,
            product_affinity         TEXT,
            R_score                  INTEGER,
            F_score                  INTEGER,
            M_score                  INTEGER,
            RFM_score                INTEGER,
            RFM_segment              TEXT,
            CLV                      REAL,
            CLV_tier                 TEXT,
            will_buy_next_quarter    INTEGER,
            next_purchase_amount     REAL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            ProductKey    INTEGER,
            Product       TEXT,
            Category      TEXT,
            Subcategory   TEXT,
            Color         TEXT,
            "List Price"  REAL,
            "Standard Cost" REAL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            CustomerKey      INTEGER,
            Customer         TEXT,
            City             TEXT,
            "State-Province" TEXT,
            "Country-Region" TEXT,
            "Postal Code"    TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Tables ready")


def insert_dataframe(table_name: str, df: pd.DataFrame):
    conn = sqlite3.connect(DB_FILE)
    try:
        existing_cols = pd.read_sql(f'SELECT * FROM "{table_name}" LIMIT 0', conn).columns.tolist()
        cols = [c for c in df.columns if c in existing_cols]
        df[cols].to_sql(table_name, conn, if_exists="replace", index=False, chunksize=500)
        print(f"   Saved {len(df):,} rows → '{table_name}'")
    except Exception as e:
        print(f"   ⚠️ Error: {e}")
    finally:
        conn.close()
