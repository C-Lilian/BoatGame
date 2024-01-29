import mysql.connector
import dotenv, os
import discord
from discord.ext import commands

mydb = mysql.connector.connect(
  host = os.getenv("DBHOST"),
  user=os.getenv("DBUSRNAME"),
  password=os.getenv("DBMDP"),
  database=os.getenv("DBNAME")
)


class DatabaseCmd(commands.Cog):
  """ Class of database command.
  
  Attributes :
    commands.Cog : ...
  """
  
  def __init__(self, bot : commands.Bot) -> None:
    """ Init Bot class """
    self.bot = bot
  
  @commands.command(brief="Permet la création d'un compte.",description="Inscription dans la base de données avec les données personnelles.")
  async def setAccount(self, ctx : commands.Context) -> discord.Message:
    """ Allow or not users to set an account.
    
    Attributes :
      self : ...
      ctx : Context of the commands.
    """
    cursor = mydb.cursor(buffered=True, dictionary=True)
    # PRÉPARATION DE LA REQUÊTE.
    sql = "INSERT INTO bg_users (BG_ID_DISCORD, BG_BANK_ACCOUNT, BG_ON_MYSELF) VALUES (%s, %s, %s)"
    val = (ctx.author.id, 100, 100)
    
    # GESTION DE LA REQUÊTE.
    try:
      cursor.execute(sql, val)
      mydb.commit()
      cursor.close()
    except mysql.connector.IntegrityError as err:
      raise commands.CommandInvokeError("Une erreur d'intégrité a eut lieu.")
    else:
      info_embed = discord.Embed(
        title=f"Félicitation {ctx.author.name} !",
        description="Votre compte à bien été créé.",
        color=discord.Color.dark_blue()
      )
      return await ctx.send(embed=info_embed)
    
    return
  
  
  @setAccount.error
  async def setAccount_error(self, ctx : commands.Context, error : commands.CommandError):
    """ Help with error handling.
    
    Attributes :
      self : ...
      ctx : Context of the commands.
      error : The error received.
    """
    
    if isinstance(error, commands.CommandInvokeError):
      return await ctx.send("Vous possédez déjà un compte.")
    
    raise error


async def setup(bot : commands.Bot) -> None:
  """ Adding the Cog to the Bot.
  
  Attributes :
    bot : Bot who receive the Cog.
  """
  await bot.add_cog(DatabaseCmd(bot))