import os
from typing import Annotated

from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import kernel_function
from services.mcp_client import MCPClient

load_dotenv()
mcp_client = MCPClient()


class AzureOpsPlugin:
    """Plugin wrapping the MCP tools for Semantic Kernel."""

    @kernel_function(
        name="analyze_alert", description="Analyze an Azure Monitor alert by ID."
    )
    async def analyze_alert_wrapper(
        self, alert_id: Annotated[str, "The ID of the alert to analyze"]
    ) -> str:
        return await mcp_client.execute("analyze_alert", alert_id=alert_id)

    @kernel_function(
        name="get_resource_config",
        description="Get the configuration of an Azure resource.",
    )
    async def get_resource_config_wrapper(
        self, resource_id: Annotated[str, "The ID of the resource"]
    ) -> str:
        return await mcp_client.execute("get_resource_config", resource_id=resource_id)

    @kernel_function(
        name="generate_fix",
        description="Generate a fix for a specific issue type and resource type.",
    )
    async def generate_fix_wrapper(
        self,
        issue_type: Annotated[str, "The type of issue (e.g., 'High CPU')"],
        resource_type: Annotated[str, "The type of resource"],
    ) -> str:
        return await mcp_client.execute(
            "generate_fix", issue_type=issue_type, resource_type=resource_type
        )

    @kernel_function(
        name="get_all_logs",
        description="Get all recent Azure Monitor logs/alerts. Use this to summarize alerts or get an overview.",
    )
    async def get_all_logs_wrapper(self) -> str:
        return await mcp_client.execute("get_all_logs")

    @kernel_function(
        name="get_all_resource_configs",
        description="Get all Azure resource configurations. Use this to get an overview of all resources.",
    )
    async def get_all_resource_configs_wrapper(self) -> str:
        return await mcp_client.execute("get_all_resource_configs")


async def get_agent() -> Kernel:
    kernel = Kernel()

    service_id = "default"
    try:
        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
                deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4"),
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
                api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            )
        )
    except Exception as e:
        print(f"Warning: Could not configure Azure OpenAI: {e}")

    kernel.add_plugin(AzureOpsPlugin(), plugin_name="AzureOps")

    return kernel


async def get_chat_agent(kernel: Kernel) -> ChatCompletionAgent:
    tools = await mcp_client.list_tools()
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="AzureOpsAgent",
        instructions=f"""You are an AI assistant that helps with Azure Operations.

You have access to the following tools:
{tools}

When users ask to "summarize logs" or "show all alerts", use the get_all_logs tool.
When users ask about "all resources" or "resource overview", use the get_all_resource_configs tool.""",
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )
    return agent


async def run_agent(query: str):
    kernel = await get_agent()
    agent = await get_chat_agent(kernel)

    final_response = []
    async for response_item in agent.invoke(query):
        if hasattr(response_item, "message") and response_item.message:
            message = response_item.message

            if hasattr(message, "content") and message.content:
                final_response.append(str(message.content))

        elif hasattr(response_item, "content") and response_item.content:
            final_response.append(str(response_item.content))

    return "".join(final_response)
