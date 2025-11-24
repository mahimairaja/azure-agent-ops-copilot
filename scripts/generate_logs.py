import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

# Ensure data directory exists
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

LOGS_FILE = DATA_DIR / "logs.json"

RESOURCE_IDS = [
    "/subscriptions/sub-1/resourceGroups/rg-1/providers/Microsoft.Compute/virtualMachines/vm-01",
    "/subscriptions/sub-1/resourceGroups/rg-1/providers/Microsoft.Sql/servers/sql-01/databases/db-01",
    "/subscriptions/sub-1/resourceGroups/rg-1/providers/Microsoft.Web/sites/app-01",
]

ALERT_DESCRIPTIONS = [
    "High CPU usage detected (95%)",
    "Disk space low (5% remaining)",
    "SQL Database DTU usage high (90%)",
    "App Service response time high (>2s)",
]


def generate_logs(count: int = 10):
    logs: List[Dict[str, Any]] = []
    for i in range(count):
        resource_id = random.choice(RESOURCE_IDS)
        description = random.choice(ALERT_DESCRIPTIONS)

        # Determine severity based on description
        severity = "Warning"
        if "95%" in description or "5%" in description:
            severity = "Critical"

        log = {
            "id": f"alert-{i + 1:03d}",
            "severity": severity,
            "resource_id": resource_id,
            "description": description,
            "created_at": (
                datetime.now() - timedelta(minutes=random.randint(1, 60))
            ).isoformat(),
            "status": "New",
            "properties": {"metric_value": random.randint(80, 100), "threshold": 80},
        }
        logs.append(log)

    with open(LOGS_FILE, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"Generated {count} logs in {LOGS_FILE}")


if __name__ == "__main__":
    generate_logs()
