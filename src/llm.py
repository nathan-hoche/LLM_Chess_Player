from ollama import chat
from colorama import Fore


def format_tools(tools):
    """Convert MCP tools for ollama compatibility."""
    return [
        {
            'name': tool.name,
            'description': tool.description,
            'parameters': {
                'type': 'object',
                'properties': {
                    key: {
                        'type': param["type"],
                        'description': param["title"],
                    } for key, param in tool.inputSchema['properties'].items()
                },
                'required': tool.inputSchema.get('required', [])
            }
        } for tool in tools
    ]

class LLMInteraction:
    def __init__(self, client):
        self.client = client
        self.tools = None
    
    async def call_tool(self, tool_name: str, **kwargs):
        async with self.client:
            result = await self.client.call_tool(tool_name, kwargs)
            return result[0].text
    
    async def llm_turn(self) -> bool:
        if not self.tools:
            self.tools = format_tools(await self.client.list_tools())
            print(Fore.LIGHTBLACK_EX + f"Available tools: {self.tools}" + Fore.RESET)
        print("====================== LLM's Turn ====================")
        print(f"{Fore.BLUE}Board:\n{Fore.RESET}{await self.call_tool("get_board")}\n")
        possible_moves = await self.call_tool("get_legal_moves")
        print(f"{Fore.BLUE}Possible moves: {Fore.RESET} {possible_moves}")
        

        messages = [
            {'role': 'user', 'content': 'describe your tools'}
        ]

        # Run chat with streaming and tool support
        stream = chat(
            model='qwen3:0.6b',
            messages=messages,
            tools=self.tools,
            stream=True
        )

        for chunk in stream:
            # Print the streamed content as it arrives
            print(chunk.message.content, end='', flush=True)
            # If the model calls a tool, print the tool call details
            if chunk.message.tool_calls:
                print(chunk.message.tool_calls)


        print("====================== End of Turn ====================")
        game_status = await self.call_tool("check_game_status")
        if not game_status.startswith("The game is ongoing"):
            print(game_status)
            return False
        return True