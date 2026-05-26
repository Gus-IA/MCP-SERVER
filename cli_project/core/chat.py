from mcp_client import MCPClient
from core.tools import ToolManager
from core.openai_service import OpenAIService


class Chat:
    def __init__(self, llm_service: OpenAIService, clients: dict[str, MCPClient]):
        self.llm_service: OpenAIService = llm_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[dict] = []

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})

    async def run(
        self,
        query: str,
    ) -> str:
        final_text_response = ""

        await self._process_query(query)

        while True:
            tools = await ToolManager.get_all_tools(self.clients)
            completion = self.llm_service.chat(
                messages=self.messages,
                tools=tools if tools else None,
            )

            choice = completion.choices[0]
            assistant_msg = choice.message
            tool_calls_raw = assistant_msg.tool_calls or []
            tool_calls_serialized = []
            for tc in tool_calls_raw:
                if hasattr(tc, "model_dump"):
                    tool_calls_serialized.append(tc.model_dump())
                elif isinstance(tc, dict):
                    tool_calls_serialized.append(tc)
                else:
                    # Best-effort fallback to keep messages JSON-like.
                    tool_calls_serialized.append(
                        {
                            "id": getattr(tc, "id", None),
                            "type": getattr(tc, "type", "function"),
                            "function": {
                                "name": getattr(getattr(tc, "function", None), "name", None),
                                "arguments": getattr(getattr(tc, "function", None), "arguments", None),
                            },
                        }
                    )

            assistant_message_dict = {"role": "assistant", "content": assistant_msg.content}
            if tool_calls_serialized:
                assistant_message_dict["tool_calls"] = tool_calls_serialized
            self.messages.append(assistant_message_dict)

            if tool_calls_raw:
                assistant_text = self.llm_service.assistant_text(assistant_msg)
                if assistant_text.strip():
                    print(assistant_text)

                tool_result_messages = await ToolManager.execute_tool_requests(
                    self.clients, tool_calls_raw
                )
                self.messages += tool_result_messages
            else:
                final_text_response = self.llm_service.assistant_text(assistant_msg)
                break

        return final_text_response
