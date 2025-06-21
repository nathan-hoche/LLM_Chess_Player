
class UserInteraction:
    def __init__(self, client):
        self.client = client
    
    async def call_tool(self, tool_name: str, **kwargs):
        async with self.client:
            result = await self.client.call_tool(tool_name, kwargs)
            return result[0].text
    
    async def user_turn(self) -> bool:
        print(await self.call_tool("get_board"))

        possible_moves = await self.call_tool("get_legal_moves")
        print(f"Possible moves: {possible_moves}")
        while True:
            decision = input("Enter your move in standard algebraic notation (e.g., e4, Nf3): ")
            if decision in possible_moves:
                break
            print(f"Invalid move: {decision}. Please try again.")
        result = await self.call_tool("make_move", san_move=decision)
        print(result)
        game_status = await self.call_tool("check_game_status")
        if not game_status.startswith("The game is ongoing"):
            print(game_status)
            return False
        return True