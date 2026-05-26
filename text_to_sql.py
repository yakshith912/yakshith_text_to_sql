import os
import re
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_API_KEY  = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
DEPLOYMENT_NAME       = os.getenv("DEPLOYMENT_NAME", "gpt-4")
API_VERSION           = os.getenv("API_VERSION", "2024-12-01-preview")

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT", "")
AZURE_SEARCH_KEY      = os.getenv("AZURE_SEARCH_KEY", "")
INDEX_NAME            = os.getenv("INDEX_NAME", "aaitech-index")

# ── Lazy clients ─────────────────────────────────────────────────────────────
_openai_client = None
_search_client = None

def _is_placeholder(val: str) -> bool:
    return not val or "your_" in val.lower() or val.strip() == ""

def get_openai_client():
    global _openai_client
    if _openai_client is None:
        if _is_placeholder(AZURE_OPENAI_API_KEY) or _is_placeholder(AZURE_OPENAI_ENDPOINT):
            return None
        from openai import AzureOpenAI
        _openai_client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version=API_VERSION
        )
    return _openai_client

def get_search_client():
    global _search_client
    if _search_client is None:
        if _is_placeholder(AZURE_SEARCH_ENDPOINT) or _is_placeholder(AZURE_SEARCH_KEY):
            return None
        from azure.search.documents import SearchClient
        from azure.core.credentials import AzureKeyCredential
        _search_client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=INDEX_NAME,
            credential=AzureKeyCredential(AZURE_SEARCH_KEY)
        )
    return _search_client

# ── Fallback schema ───────────────────────────────────────────────────────────
FALLBACK_SCHEMA = (
    "Table: customers     - Columns: customer_id, company_name, contact_name, city, country\n"
    "Table: orders        - Columns: order_id, customer_id, order_date, ship_city, freight\n"
    "Table: order_details - Columns: order_id, product_id, quantity, unit_price\n"
    "Table: products      - Columns: product_id, product_name, supplier_id, category, unit_price\n"
    "Table: suppliers     - Columns: supplier_id, company_name, contact_name, city, country\n"
)

# ── Keyword SQL map ───────────────────────────────────────────────────────────
KEYWORD_SQL_MAP = [

    # ── company names ─────────────────────────────────────────────────────
    (r"company.?name|list.*compan|all.*compan|compan.*list|compan.*name",
     "SELECT 'Customer' AS type, company_name, city, country FROM customers "
     "UNION SELECT 'Supplier' AS type, company_name, city, country FROM suppliers "
     "ORDER BY type, company_name"),
    (r"customer.*company|company.*customer",
     "SELECT company_name, contact_name, city, country FROM customers ORDER BY company_name"),
    (r"supplier.*company|company.*supplier",
     "SELECT company_name, contact_name, city, country FROM suppliers ORDER BY company_name"),

    # ── customers ─────────────────────────────────────────────────────────
    (r"how many customers",
     "SELECT COUNT(*) AS total_customers FROM customers"),
    (r"customers?\s+from\s+(\w+)",
     "SELECT * FROM customers WHERE country = '{1}'"),
    (r"customers?\s+by\s+country|customers?\s+per\s+country",
     "SELECT country, COUNT(*) AS total FROM customers GROUP BY country ORDER BY total DESC"),
    (r"customers?\s+by\s+city|customers?\s+per\s+city",
     "SELECT city, COUNT(*) AS total FROM customers GROUP BY city ORDER BY total DESC"),

    # ── suppliers ─────────────────────────────────────────────────────────
    (r"how many suppliers",
     "SELECT COUNT(*) AS total_suppliers FROM suppliers"),
    (r"suppliers?\s+from\s+(\w+)",
     "SELECT * FROM suppliers WHERE country = '{1}'"),
    (r"supplier.*most products|most products.*supplier",
     "SELECT s.company_name, COUNT(p.product_id) AS total_products "
     "FROM suppliers s JOIN products p ON s.supplier_id = p.supplier_id "
     "GROUP BY s.company_name ORDER BY total_products DESC LIMIT 10"),
    (r"supplier",
     "SELECT * FROM suppliers LIMIT 100"),

    # ── products ──────────────────────────────────────────────────────────
    (r"how many products",
     "SELECT COUNT(*) AS total_products FROM products"),
    (r"expensive products|top.*products|products.*price|highest.*price",
     "SELECT product_name, category, unit_price FROM products ORDER BY unit_price DESC LIMIT 10"),
    (r"cheap.*products|lowest.*price",
     "SELECT product_name, category, unit_price FROM products ORDER BY unit_price ASC LIMIT 10"),
    (r"products?\s+in\s+(beverages|condiments|seafood|produce|meat)",
     "SELECT * FROM products WHERE LOWER(category) = '{1}'"),
    (r"products?\s+by\s+category|products?\s+per\s+category",
     "SELECT category, COUNT(*) AS total FROM products GROUP BY category ORDER BY total DESC"),
    (r"beverages",
     "SELECT * FROM products WHERE category = 'Beverages'"),
    (r"condiments",
     "SELECT * FROM products WHERE category = 'Condiments'"),
    (r"seafood",
     "SELECT * FROM products WHERE category = 'Seafood'"),
    (r"produce",
     "SELECT * FROM products WHERE category = 'Produce'"),
    (r"product",
     "SELECT * FROM products LIMIT 100"),

    # ── orders ────────────────────────────────────────────────────────────
    (r"how many orders",
     "SELECT COUNT(*) AS total_orders FROM orders"),
    (r"orders?\s+by\s+country|orders?\s+per\s+country",
     "SELECT c.country, COUNT(o.order_id) AS orders "
     "FROM customers c JOIN orders o ON c.customer_id = o.customer_id "
     "GROUP BY c.country ORDER BY orders DESC"),
    (r"total freight|shipping cost|freight cost",
     "SELECT c.country, ROUND(SUM(o.freight),2) AS total_freight "
     "FROM customers c JOIN orders o ON c.customer_id = o.customer_id "
     "GROUP BY c.country ORDER BY total_freight DESC"),
    (r"recent orders|latest orders",
     "SELECT o.order_id, c.company_name, o.order_date, o.freight "
     "FROM orders o JOIN customers c ON o.customer_id = c.customer_id "
     "ORDER BY o.order_date DESC LIMIT 10"),
    (r"order.?detail|order.?item",
     "SELECT od.order_id, p.product_name, od.quantity, od.unit_price, "
     "ROUND(od.quantity*od.unit_price,2) AS line_total "
     "FROM order_details od JOIN products p ON od.product_id = p.product_id LIMIT 100"),
    (r"orders?.*customer|customer.*orders?",
     "SELECT o.order_id, c.company_name, c.country, o.order_date, o.ship_city, o.freight "
     "FROM orders o JOIN customers c ON o.customer_id = c.customer_id "
     "ORDER BY o.order_date DESC LIMIT 100"),
    (r"order",
     "SELECT o.order_id, c.company_name, c.country, o.order_date, o.ship_city, o.freight "
     "FROM orders o JOIN customers c ON o.customer_id = c.customer_id "
     "ORDER BY o.order_date DESC LIMIT 100"),
    (r"customer",
     "SELECT * FROM customers LIMIT 100"),

    # ── revenue / sales ───────────────────────────────────────────────────
    (r"revenue\s+by\s+product|revenue\s+per\s+product|top.*revenue",
     "SELECT p.product_name, ROUND(SUM(od.quantity * od.unit_price),2) AS revenue "
     "FROM products p JOIN order_details od ON p.product_id = od.product_id "
     "GROUP BY p.product_name ORDER BY revenue DESC LIMIT 10"),
    (r"revenue|total sales|overall sales",
     "SELECT p.category, ROUND(SUM(od.quantity * od.unit_price),2) AS revenue "
     "FROM products p JOIN order_details od ON p.product_id = od.product_id "
     "GROUP BY p.category ORDER BY revenue DESC"),
]


def keyword_to_sql(question: str) -> Optional[str]:
    q = question.lower().strip()
    for pattern, sql_template in KEYWORD_SQL_MAP:
        m = re.search(pattern, q)
        if m:
            sql = sql_template
            for i, g in enumerate(m.groups(), 1):
                if g:
                    sql = sql.replace(f"{{{i}}}", g.capitalize())
            return sql
    return None


def search_index(query_text: str, top: int = 3) -> List[dict]:
    client = get_search_client()
    if client is None:
        return []
    try:
        return [r for r in client.search(query_text, top=top)]
    except Exception as e:
        print(f"Warning: Azure Search failed: {e}")
        return []


def build_schema_context(docs: list) -> str:
    if not docs:
        return ""
    return "\n".join(
        f"Table: {d.get('name','')}\nDescription: {d.get('description','')}\nColumns: {d.get('columns','')}\n"
        for d in docs
    )


def clean_sql(sql: str) -> str:
    lines = sql.strip().splitlines()
    return "\n".join(line for line in lines if not line.strip().startswith("```")).strip()


def question_to_sql(question: str) -> str:
    client = get_openai_client()

    # Azure OpenAI path
    if client is not None:
        search_results = search_index(question, top=3)
        context = build_schema_context(search_results) or FALLBACK_SCHEMA
        system_prompt = (
            "You are an expert SQL assistant converting natural language to MySQL queries.\n"
            "Available tables: customers, suppliers, products, orders, order_details\n\n"
            f"Schema:\n{context}\n"
            "Rules: Return ONLY the SQL. No markdown. Limit 100 rows unless specified.\n"
        )
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": question}
            ],
            temperature=0,
            max_tokens=300
        )
        return clean_sql(response.choices[0].message.content.strip())

    # Keyword fallback
    sql = keyword_to_sql(question)
    if sql:
        return sql

    raise ValueError(
        "Azure OpenAI is not configured. "
        "Try questions like: 'show customers', 'list company names', 'show orders', 'total revenue'. "
        "Or add your Azure keys to .env."
    )


if __name__ == "__main__":
    from database import execute_query
    tests = ["list all company names", "show customers", "show orders", "total revenue"]
    for q in tests:
        sql = question_to_sql(q)
        df = execute_query(sql)
        print(f"Q: {q}\nSQL: {sql}\nRows: {len(df)}\n{df}\n")
