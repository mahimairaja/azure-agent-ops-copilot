import json
from pathlib import Path

# Constants
DATA_DIR = Path(__file__).parent.parent.parent / "data"
LOGS_FILE = DATA_DIR / "logs.json"
CONFIGS_FILE = DATA_DIR / "configs.json"
TEMPLATES_DIR = DATA_DIR / "templates"


def analyze_alert_logic(alert_id: str) -> str:
    """
    Analyze an Azure Monitor alert by ID.
    Returns the alert details and potential root cause.
    """
    try:
        if not LOGS_FILE.exists():
            return "Error: Logs file not found."

        with open(LOGS_FILE, "r") as f:
            logs = json.load(f)

        alert = next((log for log in logs if log["id"] == alert_id), None)
        if not alert:
            return f"Error: Alert {alert_id} not found."

        return f"Alert Analysis:\nID: {alert['id']}\nSeverity: {alert['severity']}\nResource: {alert['resource_id']}\nDescription: {alert['description']}\nMetric Value: {alert['properties'].get('metric_value')}"
    except Exception as e:
        return f"Error analyzing alert: {str(e)}"


def get_resource_config_logic(resource_id: str) -> str:
    """
    Get the configuration of an Azure resource.
    Supports both full resource IDs and short names (e.g., 'vm-01').
    """
    try:
        if not CONFIGS_FILE.exists():
            return "Error: Configs file not found."

        with open(CONFIGS_FILE, "r") as f:
            configs = json.load(f)

        # Try exact match first
        config = next((c for c in configs if c["resource_id"] == resource_id), None)

        # If no exact match, try matching the end of the resource_id (for short names)
        if not config:
            config = next(
                (c for c in configs if c["resource_id"].endswith(f"/{resource_id}")),
                None,
            )

        if not config:
            return f"Error: Resource {resource_id} not found."

        return json.dumps(config, indent=2)
    except Exception as e:
        return f"Error reading config: {str(e)}"


def generate_fix_logic(issue_type: str, resource_type: str) -> str:
    """
    Generate a fix for a specific issue type and resource type.
    Returns a Bicep or CLI snippet.
    """
    # Normalize inputs for better matching
    issue_lower = issue_type.lower()
    resource_lower = resource_type.lower().replace(" ", "")

    # VM CPU/Performance issues
    if "cpu" in issue_lower and (
        "vm" in resource_lower or "virtualmachine" in resource_lower
    ):
        template_path = TEMPLATES_DIR / "vm_resize.bicep"
        if template_path.exists():
            return template_path.read_text()

    # SQL Database issues
    if "dtu" in issue_lower or "sql" in issue_lower or "database" in resource_lower:
        template_path = TEMPLATES_DIR / "sql_scale.sh"
        if template_path.exists():
            return template_path.read_text()

    return "No specific fix template found for this issue. Please investigate manually."
