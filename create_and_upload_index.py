import os
from pathlib import Path
from typing import List
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT", "")
KEY = os.getenv("AZURE_SEARCH_KEY", "")
INDEX_NAME = os.getenv("INDEX_NAME", "aaitech-index")
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "aaitech_vector_schema_info.csv"


def _import_azure_search_clients():
    try:
        from azure.search.documents.indexes import SearchIndexClient
        from azure.search.documents import SearchClient
        from azure.core.credentials import AzureKeyCredential
        return SearchIndexClient, SearchClient, AzureKeyCredential
    except ImportError as exc:
        raise RuntimeError(
            "The azure-search-documents and azure-core packages are required to create the Azure Search index. "
            "Install them with `pip install azure-search-documents azure-core`."
        ) from exc


def _import_index_models():
    try:
        from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
        return SearchIndex, SimpleField, SearchableField
    except ImportError as exc:
        raise RuntimeError(
            "The azure-search-documents package is required to create the Azure Search index models. "
            "Install it with `pip install azure-search-documents`."
        ) from exc


def _is_placeholder(value: str) -> bool:
    return not value or "your_" in value.lower() or value.strip() == ""


def get_index_client():
    if _is_placeholder(ENDPOINT) or _is_placeholder(KEY):
        raise RuntimeError("Azure Search endpoint and key must be configured in the .env file.")
    SearchIndexClient, _, AzureKeyCredential = _import_azure_search_clients()
    return SearchIndexClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))


def get_search_client():
    if _is_placeholder(ENDPOINT) or _is_placeholder(KEY):
        raise RuntimeError("Azure Search endpoint and key must be configured in the .env file.")
    _, SearchClient, AzureKeyCredential = _import_azure_search_clients()
    return SearchClient(endpoint=ENDPOINT, index_name=INDEX_NAME, credential=AzureKeyCredential(KEY))


def ensure_index(client):
    SearchIndex, SimpleField, SearchableField = _import_index_models()
    existing = [idx.name for idx in client.list_indexes()]
    if INDEX_NAME in existing:
        print(f"Deleting existing index '{INDEX_NAME}'...")
        client.delete_index(INDEX_NAME)

    fields = [
        SimpleField(name="id", type="Edm.String", key=True, searchable=False),
        SearchableField(name="type", type="Edm.String", sortable=True, analyzer_name="standard.lucene"),
        SearchableField(name="name", type="Edm.String", sortable=True, analyzer_name="standard.lucene"),
        SearchableField(name="description", type="Edm.String", sortable=True, analyzer_name="standard.lucene"),
        SearchableField(name="columns", type="Edm.String", sortable=True, analyzer_name="standard.lucene"),
    ]
    index = SearchIndex(name=INDEX_NAME, fields=fields)
    client.create_index(index)
    print(f"Created index: {INDEX_NAME}")


def load_documents(path: Path) -> List[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {path}")

    df = pd.read_csv(path)
    df = df.fillna("")
    documents = []
    for _, row in df.iterrows():
        documents.append({
            "id": str(row["id"]),
            "type": str(row["type"]),
            "name": str(row["name"]),
            "description": str(row["description"]),
            "columns": str(row["columns"]),
        })
    return documents


def upload_documents(client, documents: List[dict]) -> None:
    if not documents:
        print("No documents to upload.")
        return

    result = client.upload_documents(documents=documents)
    uploaded = sum(1 for item in result if getattr(item, "succeeded", False) or getattr(item, "status_code", 200) == 201)
    print(f"[✓] Uploaded {uploaded} documents.")


def main() -> None:
    index_client = get_index_client()
    ensure_index(index_client)
    search_client = get_search_client()
    documents = load_documents(DATA_FILE)
    upload_documents(search_client, documents)


if __name__ == "__main__":
    main()