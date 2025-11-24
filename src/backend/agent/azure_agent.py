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
    """Plugin wrapping our MCP tools for Semantic Kernel."""

    @kernel_function(
        name="analyze_alert", description="Analyze an Azure Monitor alert by ID."
    )
    def analyze_alert_wrapper(
        self, alert_id: Annotated[str, "The ID of the alert to analyze"]
    ) -> str:
        return mcp_client.execute("analyze_alert", alert_id=alert_id)

    @kernel_function(
        name="get_resource_config",
        description="Get the configuration of an Azure resource.",
    )
    def get_resource_config_wrapper(
        self, resource_id: Annotated[str, "The ID of the resource"]
    ) -> str:
        return mcp_client.execute("get_resource_config", resource_id=resource_id)

    @kernel_function(
        name="generate_fix",
        description="Generate a fix for a specific issue type and resource type.",
    )
    def generate_fix_wrapper(
        self,
        issue_type: Annotated[str, "The type of issue (e.g., 'High CPU')"],
        resource_type: Annotated[str, "The type of resource"],
    ) -> str:
        return mcp_client.execute(
            "generate_fix", issue_type=issue_type, resource_type=resource_type
        )


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
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="AzureOpsAgent",
        instructions="You are an AI assistant that helps with Azure Operations. Use the available tools to analyze alerts and suggest fixes.",
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )
    return agent


async def run_agent(query: str):
    kernel = await get_agent()
    agent = await get_chat_agent(kernel)

    # Execute the agent
    final_response = []
    async for response in agent.invoke(query):
        if response.content:
            final_response.append(response.content)

    return "".join(final_response)
