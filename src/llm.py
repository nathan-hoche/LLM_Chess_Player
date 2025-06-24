from ollama import chat
from colorama import Fore


def format_tools(tools):
    """Convert MCP tools for ollama compatibility."""
    return [
        {
            'type': 'function',
            'function': {
                'name': tool.name,
                'description': tool.description,
                'parameters': {
                    'type': 'object',
                    'properties': {
                        key: {
                            'type': param["type"],
                            'description': param.get("description", ""),
                        } for key, param in tool.inputSchema['properties'].items()
                    },
                    'required': tool.inputSchema.get('required', [])
                }
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
        board = await self.call_tool("get_board")
        print(f"{Fore.BLUE}Board:\n{Fore.RESET}{board}\n")
        possible_moves = await self.call_tool("get_legal_moves")
        print(f"{Fore.BLUE}Possible moves: {Fore.RESET} {possible_moves}")
        
        messages = [
            {'role': 'system', 'content': 'You are a chess player. You can make moves, check the board, and get legal moves. You are the lower case player in this game.'},
            {'role': 'user', 'content': f'It\'s your turn to play. This is the current board state:\n{board}\n. Here are the legal moves you can make:\n{possible_moves}\nPlease call the tool "make_move" with your chosen move.'},
        ]

        # Run chat with streaming and tool support
        stream = chat(
            model='qwen3:0.6b',
            messages=messages,
            tools=self.tools,
            stream=True,
        )

        for chunk in stream:
            # Print the streamed content as it arrives
            print(chunk.message.content, end='', flush=True)
            # If the model calls a tool, print the tool call details
            if chunk.message.tool_calls:
                print(f"\n{Fore.YELLOW}LLM called tool: {chunk.message.tool_calls}{Fore.RESET}")
                if chunk.message.tool_calls[0].function.name == "make_move":
                    print(f"\n{Fore.GREEN}Call make_move with this args: {chunk.message.tool_calls[0].function.arguments}{Fore.RESET}")
                    result = await self.call_tool("make_move", **chunk.message.tool_calls[0].function.arguments)
                    print(f"{Fore.GREEN}Result of the move: {result}{Fore.RESET}")
                else:
                    print(f"\n{Fore.RED}LLM called an unexpected tool: {chunk.message.tool_calls[0].function.name}{Fore.RESET}")

        print("====================== End of Turn ====================")
        game_status = await self.call_tool("check_game_status")
        if not game_status.startswith("The game is ongoing") and not game_status.startswith("Check!"):
            print(game_status)
            return False
        return True