import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.mcp.logic import (
    analyze_alert_logic,
    generate_fix_logic,
    get_resource_config_logic,
)


def test_analyze_alert():
    print("Testing analyze_alert_logic...")
    # Use a known ID from generation script logic (alert-001)
    result = analyze_alert_logic("alert-001")
    print(result)
    assert "Alert Analysis" in result
    assert "alert-001" in result


def test_get_resource_config():
    print("\nTesting get_resource_config_logic...")
    # Use a known ID from generation script
    resource_id = "/subscriptions/sub-1/resourceGroups/rg-1/providers/Microsoft.Compute/virtualMachines/vm-01"
    result = get_resource_config_logic(resource_id)
    print(result)
    assert "Standard_D2s_v3" in result


def test_generate_fix():
    print("\nTesting generate_fix_logic...")
    result = generate_fix_logic("High CPU", "Microsoft.Compute/virtualMachines")
    print(result)
    assert "vmSize" in result


if __name__ == "__main__":
    try:
        test_analyze_alert()
        test_get_resource_config()
        test_generate_fix()
        print("\nAll tests passed!")
    except Exception as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
