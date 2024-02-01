import mysql.connector
import dotenv, os
import discord
import datetime
import random
from discord.ext import commands

mydb = mysql.connector.connect(
  host = os.getenv("DBHOST"),
  user=os.getenv("DBUSRNAME"),
  password=os.getenv("DBMDP"),
  database=os.getenv("DBNAME")
)


class GameCmd(commands.Cog):
  """ Class of game command.
  
  Attributes :
    commands.Cog : ...
  """
  
  def __init__(self, bot : commands.Bot) -> None:
    """ Init Bot class """
    self.bot = bot
  
  
  # BET GAME
  @commands.command(brief="Parier une certaines somme.",description="Parier une somme donnée qui si vous avez bon sera multiplié aléatoirement entre 1.1 et 10.")
  async def betGame(self, ctx : commands.Context, nbrBet : int, amount : int = 1) -> discord.Message:
    """ User bet some money and try to win more.
    
    Attributes :
      self : ...
      ctx : Context of the commands.
      nbrBet : Number on which you bet.
      amount : Amount bet with a minimum of 1.
    """
    
    # VÉRIFICATION DES CONDITIONS DU PARI.
    cursor = mydb.cursor(buffered=True, dictionary=True)
    sql = f"SELECT BG_BANK_ACCOUNT, BG_ON_MYSELF FROM bg_users WHERE BG_ID_DISCORD = {ctx.author.id}"
    
    # GESTION DE LA REQUÊTE.
    cursor.execute(sql)
    row_count = cursor.rowcount
    
    bgBankAccount = 0
    bgOnMyself = 0
    
    if row_count <= 0:
      raise commands.CommandInvokeError("Aucun compte lié.")
    if row_count > 0:
      # RÉCUPÉRATION DES VARIABLES.
      row = cursor.fetchone()
      bgBankAccount = row['BG_BANK_ACCOUNT']
      bgOnMyself = row['BG_ON_MYSELF']
      
      if amount > bgOnMyself:
        if amount > bgOnMyself + bgBankAccount:
          return await ctx.send("Vous n'avez pas assez sur vous.")
        return await ctx.send("Vous avez misé plus que ce que vous possédez.")
    
    # FERMETURE DU CURSEUR
    cursor.close()
    
    if nbrBet > 100 or nbrBet <= 0:
      return await ctx.send("Vous devez miser un nombre entre 1 et 100.")
    
    
    # ON LANCE LE PARI.
    winningNbr = random.randint(1, 100)
    finalNbr = 0
    winner = False
    
    if winningNbr == nbrBet:
      winner = True
      finalNbr = round(amount * random.uniform(1.1, 10), 2)
    else:
      finalNbr = round(finalNbr - amount, 2)
    
    
    # MISE À JOUR DANS LA BASE DE DONNÉES.
    cursor = mydb.cursor(buffered=True, dictionary=True)
    sql = "UPDATE bg_users SET BG_ON_MYSELF = BG_ON_MYSELF + (%s) WHERE BG_ID_DISCORD = %s"
    val = (finalNbr, ctx.author.id)
    
    try:
      # EXÉCUTION DE LA REQUÊTE
      cursor.execute(sql, val)
      mydb.commit()
      cursor.close()
      
    except mysql.connector.errors.ProgrammingError as err:
      # GESTION DES ERREURS
      raise commands.CommandInvokeError("Problème de paramètre.")
      
    else:
      # PRÉPARATION DE L'EMBED
      if winner:
        titre = f"Pari réussi, bravo {ctx.author.name} !"
        description = f"Vous venez de gagné {finalNbr}€ !"
        couleur = discord.Color.green()
      else:
        titre = f"Pari raté, désolé {ctx.author.name} !"
        description = f"Vous avez perdu {amount}€..."
        couleur = discord.Color.red()
      
      info_embed = discord.Embed(title=titre, description=description, color=couleur)
      info_embed.set_footer(text='© BoatGame')
      info_embed.timestamp = datetime.datetime.now()
      
      # ON RETOURNE LE MESSAGE FINAL.
      return await ctx.send(embed=info_embed)
    
    return
  
  @betGame.error
  async def betGame_error(self, ctx : commands.Context, error : commands.CommandError):
    """ Help with error handling.
    
    Attributes :
      self : ...
      ctx : Context of the commands.
      error : The error received.
    """
    
    if isinstance(error, commands.CommandInvokeError):
      return await ctx.send("Problème de compte ou de requête.")
    
    raise error


async def setup(bot : commands.Bot) -> None:
  """ Adding the Cog to the Bot.
  
  Attributes :
    bot : Bot who receive the Cog.
  """
  await bot.add_cog(GameCmd(bot))