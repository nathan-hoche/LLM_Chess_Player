from fastmcp import Client
import asyncio
from colorama import Fore

from user import UserInteraction
from llm import LLMInteraction

class Processor:
    def __init__(self):
        self.client = Client("http://127.0.0.1:8000/mcp")
        self.user_interaction = UserInteraction(self.client)
        self.llm_interaction = LLMInteraction(self.client)
    
    async def call_tool(self, tool_name: str, **kwargs):
        async with self.client:
            result = await self.client.call_tool(tool_name, **kwargs)
            return result

    async def main(self):
        async with self.client:
            tools = await self.client.list_tools()
            print(Fore.LIGHTBLACK_EX + f"Available tools: {tools}" + Fore.RESET)
            if await self.user_interaction.user_turn():
                print(Fore.GREEN + "Your turn was successful!" + Fore.RESET)
            if await self.llm_interaction.llm_turn():
                print(Fore.GREEN + "LLM's turn was successful!" + Fore.RESET)

pc = Processor()
asyncio.run(pc.main())

asyncio.run(pc.main())