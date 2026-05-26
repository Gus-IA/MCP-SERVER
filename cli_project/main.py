import asyncio
import sys
import os
from dotenv import load_dotenv
from contextlib import AsyncExitStack

from mcp_client import MCPClient
from core.openai_service import OpenAIService

from core.cli_chat import CliChat
from core.cli import CliApp

load_dotenv()

# LLM Config (OpenAI-compatible; supports Groq)
llm_provider = os.getenv("LLM_PROVIDER", "openai")
llm_model = os.getenv("LLM_MODEL", os.getenv("OPENAI_MODEL", ""))
llm_api_key = os.getenv("LLM_API_KEY", "").strip()
openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
groq_api_key = os.getenv("GROQ_API_KEY", "").strip()

# Fallback: si la clave está en OPENAI_API_KEY pero parece de Groq (gsk_...)
if not llm_api_key and not groq_api_key and openai_api_key.startswith("gsk_"):
    groq_api_key = openai_api_key
elif not llm_api_key:
    llm_api_key = openai_api_key


assert llm_model, "Error: LLM_MODEL (o OPENAI_MODEL) cannot be empty. Update .env"
if (llm_provider or "").lower() == "groq":
    assert (llm_api_key or groq_api_key), (
        "Error: GROQ_API_KEY (o LLM_API_KEY) cannot be empty. Update .env"
    )
else:
    assert llm_api_key, (
        "Error: OPENAI_API_KEY (o LLM_API_KEY) cannot be empty. Update .env"
    )


async def main():
    llm_service = OpenAIService(model=llm_model)

    server_scripts = sys.argv[1:]
    clients = {}

    command, args = (
        ("uv", ["run", "mcp_server.py"])
        if os.getenv("USE_UV", "0") == "1"
        else ("python", ["mcp_server.py"])
    )

    async with AsyncExitStack() as stack:
        doc_client = await stack.enter_async_context(
            MCPClient(command=command, args=args)
        )
        clients["doc_client"] = doc_client

        for i, server_script in enumerate(server_scripts):
            client_id = f"client_{i}_{server_script}"
            client = await stack.enter_async_context(
                MCPClient(command="uv", args=["run", server_script])
            )
            clients[client_id] = client

        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            llm_service=llm_service,
        )

        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
