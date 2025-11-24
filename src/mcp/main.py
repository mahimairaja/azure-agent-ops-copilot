from fastmcp import FastMCP
from utils import (
    CONFIGS_FILE,
    LOGS_FILE,
    analyze_alert_logic,
    generate_fix_logic,
    get_resource_config_logic,
)

# Initialize FastMCP server
mcp = FastMCP("Azure Ops Copilot")

# --- Tools ---


@mcp.tool()
def analyze_alert(alert_id: str) -> str:
    """
    Analyze an Azure Monitor alert by ID.
    Returns the alert details and potential root cause.
    """
    return analyze_alert_logic(alert_id)


@mcp.tool()
def get_resource_config(resource_id: str) -> str:
    """
    Get the configuration of an Azure resource.
    """
    return get_resource_config_logic(resource_id)


@mcp.tool()
def generate_fix(issue_type: str, resource_type: str) -> str:
    """
    Generate a fix for a specific issue type and resource type.
    Returns a Bicep or CLI snippet.
    """
    return generate_fix_logic(issue_type, resource_type)


@mcp.tool()
def integration_placeholder(service_name: str, action: str) -> str:
    """
    Placeholder for future integrations (e.g., Jira, ServiceNow).
    """
    return (
        f"Integration with {service_name} for action '{action}' is not yet implemented."
    )


# --- Resources ---


@mcp.resource("azure://logs/recent")
def get_recent_logs() -> str:
    """Get the most recent Azure Monitor logs."""
    if LOGS_FILE.exists():
        return LOGS_FILE.read_text()
    return "[]"


@mcp.resource("azure://configs/all")
def get_all_configs() -> str:
    """Get all resource configurations."""
    if CONFIGS_FILE.exists():
        return CONFIGS_FILE.read_text()
    return "[]"


# --- Prompts ---


@mcp.prompt()
def analyze_issue(alert_id: str) -> str:
    """Create a prompt to analyze an issue based on an alert ID."""
    return f"""Please analyze the following alert and suggest remediation steps:
    Alert ID: {alert_id}

    1. Use the 'analyze_alert' tool to get details.
    2. Use the 'get_resource_config' tool to check the resource configuration.
    3. Use the 'generate_fix' tool if a fix is applicable.
    """


@mcp.prompt()
def suggest_fix(resource_id: str, issue: str) -> str:
    """Create a prompt to suggest a fix for a resource."""
    return f"""The resource {resource_id} is experiencing {issue}.
    Please generate a fix using the available templates.
    """


if __name__ == "__main__":
    mcp.run()
