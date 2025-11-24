import json
from pathlib import Path

# Ensure data directory exists
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

CONFIGS_FILE = DATA_DIR / "configs.json"

CONFIGS = [
    {
        "resource_id": "/subscriptions/sub-1/resourceGroups/rg-1/providers/Microsoft.Compute/virtualMachines/vm-01",
        "type": "Microsoft.Compute/virtualMachines",
        "location": "eastus",
        "properties": {
            "hardwareProfile": {"vmSize": "Standard_D2s_v3"},
            "storageProfile": {"osDisk": {"osType": "Linux", "diskSizeGB": 30}},
        },
        "compliance_status": "Compliant",
    },
    {
        "resource_id": "/subscriptions/sub-1/resourceGroups/rg-1/providers/Microsoft.Sql/servers/sql-01/databases/db-01",
        "type": "Microsoft.Sql/servers/databases",
        "location": "eastus",
        "properties": {
            "sku": {"name": "Standard", "tier": "Standard", "capacity": 10},
            "maxSizeBytes": 2147483648,
        },
        "compliance_status": "NonCompliant",
    },
    {
        "resource_id": "/subscriptions/sub-1/resourceGroups/rg-1/providers/Microsoft.Web/sites/app-01",
        "type": "Microsoft.Web/sites",
        "location": "eastus",
        "properties": {
            "serverFarmId": "/subscriptions/sub-1/resourceGroups/rg-1/providers/Microsoft.Web/serverfarms/plan-01",
            "httpsOnly": False,
        },
        "compliance_status": "NonCompliant",
    },
]


def generate_configs():
    with open(CONFIGS_FILE, "w") as f:
        json.dump(CONFIGS, f, indent=2)

    print(f"Generated {len(CONFIGS)} configs in {CONFIGS_FILE}")


if __name__ == "__main__":
    generate_configs()
