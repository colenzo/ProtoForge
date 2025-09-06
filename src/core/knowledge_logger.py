from datetime import datetime
from typing import Any, Dict, Optional
import uuid
import requests
import json
from src.core.lumen_analyzer import add_log_to_simulated_store

# Dashboard API endpoint for logs
DASHBOARD_LOG_URL = "http://localhost:8001/log"

async def log_to_knowledge_vault(event_type: str, data: Dict[str, Any], log_level: str = "INFO", source_agent: Optional[str] = None):
    """Simulates logging an event to the Knowledge Vault for Lumen Protocol consumption and sends to dashboard."""
    timestamp = datetime.now().isoformat()
    log_id = str(uuid.uuid4())
    log_entry = {
        "log_id": log_id,
        "timestamp": timestamp,
        "event_type": event_type,
        "log_level": log_level,
        "source_agent": source_agent,
        "data": data
    }
    print(f"[KNOWLEDGE_VAULT_LOG] {log_entry}")
    add_log_to_simulated_store(log_entry) # For Lumen Analyzer

    # Send log to dashboard (non-blocking)
    try:
        requests.post(DASHBOARD_LOG_URL, json=log_entry, timeout=0.1) # Short timeout to avoid blocking
    except requests.exceptions.RequestException as e:
        print(f"[KNOWLEDGE_LOGGER] Failed to send log to dashboard: {e}")
    
    # In a real implementation, this would write to a persistent database, file, or message queue
