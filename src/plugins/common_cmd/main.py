import discord
from discord.ext import commands


class CommonCmd(commands.Cog):
  """ Class of common command who can be useful.
  
  Attributes :
    commands.Cog : ...
  """
  
  
  def __init__(self, bot : commands.Bot) -> None:
    """ Init Bot class """
    self.bot = bot
  
  
  @commands.command(brief="Permet d'effacer un certains nombres de message.",description="Permet d'effacer un nombre de message important avec une limite à 100.")
  async def clear(self, ctx : commands.Context, amount : int) -> discord.Message:
    """ Helper to clear the code.
    
    Attributes :
      self : ...
      ctx : Context of the commands.
      amount : Number of messages to clear.
    """
    # GESTION DES ERREURS :
    if not isinstance(amount, int) or amount <= 0 or amount > 100:
      raise commands.BadArgument("La quantité de message à supprimé doit être un entier strictement positif et inférieur à 100.")
    
    if isinstance(ctx.author, discord.User) and ctx.guild is None:
      raise commands.NoPrivateMessage("Vous ne pouvez pas utiliser cette commande en message privé.")
    
    if isinstance(ctx.channel, discord.TextChannel):
      raise commands.CommandInvokeError("Vous devez appeler cette commande depuis un salon textuel.")
    
    if ctx.author.guild_permissions.manage_messages:
      raise commands.CommandInvokeError("Vous n'avez pas les permissions pour cette commande.")
    
    # TRAITEMENT DE LA FONCTION
    await ctx.channel.purge(limit=amount+1)
    
    return await ctx.send(f"{amount} messages on été supprimés.")
  
  
  @clear.error
  async def clear_error(self, ctx : commands.Context, error : commands.CommandError):
    """ Help with error handling.
    
    Attributes :
      self : ...
      ctx : Context of the commands.
      error : The error received.
    """
    
    if isinstance(error, commands.NoPrivateMessage):
      return await ctx.send("Le channel utilisé est incorrect.")
    
    if isinstance(error, commands.BadArgument):
      return await ctx.send("Un arguement est incorrect.")
    
    if isinstance(error, commands.CommandInvokeError):
      return await ctx.send("Le channel utilisé est incorrect.")
    
    if isinstance(error, commands.MissingPermissions):
      return await ctx.send("Les permissions sont insuffisantes.")
    
    raise error


async def setup(bot : commands.Bot) -> None:
  """ Adding the Cog to the Bot.
  
  Attributes :
    bot : Bot who receive the Cog.
  """
  await bot.add_cog(CommonCmd(bot))