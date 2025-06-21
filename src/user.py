from colorama import Fore

class UserInteraction:
    def __init__(self, client):
        self.client = client
    
    async def call_tool(self, tool_name: str, **kwargs):
        async with self.client:
            result = await self.client.call_tool(tool_name, kwargs)
            return result[0].text
    
    async def user_turn(self) -> bool:
        print("====================== User's Turn ====================")
        print(f"{Fore.BLUE}Board:\n{Fore.RESET}{await self.call_tool("get_board")}\n")
        possible_moves = await self.call_tool("get_legal_moves")
        print(f"{Fore.BLUE}Possible moves: {Fore.RESET} {possible_moves}")
        while True:
            decision = input(f"{Fore.BLUE}Enter your move in standard algebraic notation (e.g., e4, Nf3): {Fore.RESET}")
            result = await self.call_tool("make_move", san_move=decision)
            if f"Move {decision} has been made" in result:
                break
            print(f"{Fore.RED}{result}{Fore.RESET}")
        print(f"{Fore.GREEN}{result}{Fore.RESET}")

        print("====================== End of Turn ====================")
        game_status = await self.call_tool("check_game_status")
        if not game_status.startswith("The game is ongoing"):
            print(game_status)
            return False
        return True