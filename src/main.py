from fastmcp import Client
import asyncio
from colorama import Fore

class Processor:
    def __init__(self):
        self.client = Client("http://127.0.0.1:8000/mcp")
    
    async def main(self):
        async with self.client:
            tools = await self.client.list_tools()
            print(Fore.LIGHTBLACK_EX + f"Available tools: {tools}" + Fore.RESET)

pc = Processor()
asyncio.run(pc.main())
