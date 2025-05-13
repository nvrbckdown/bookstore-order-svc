from datetime import datetime
from typing import Any, Dict

def serialize_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB document to JSON serializable format"""
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
    return doc