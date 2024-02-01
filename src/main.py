import discord
from discord.ext import commands

import dotenv, os

class BoatGame(commands.Bot):
  """ The Boat Game 
  
  Attributes :
    ...
  """
  
  
  def __init__(self) -> None:
    """ Init Bot """
    super().__init__(command_prefix="!", intents=discord.Intents.all())
  
  
  async def setup_hook(self) -> None:
    """ Setup the different extension and other... """
    await self.load_extension("plugins.common_cmd.main")
    await self.load_extension("plugins.database_cmd.main")
    await self.load_extension("plugins.game_cmd.main")
    await self.tree.sync()
  
  
  async def on_ready(self) -> None:
    """ Indicates when the Bot is ready """
    print("Je suis en ligne !")


def main() -> None:
  """ Function main """
  dotenv.load_dotenv()
  
  TOKEN = os.getenv("TOKEN")
  
  if TOKEN is None:
    raise ValueError("Votre TOKEN n'est pas défini.")
  
  bot = BoatGame()
  bot.run(token=TOKEN)


if __name__ == "__main__":
  main()