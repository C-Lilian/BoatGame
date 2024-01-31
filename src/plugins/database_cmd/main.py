import mysql.connector
import dotenv, os
import discord
import datetime
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
      info_embed.set_footer(text='© BoatGame')
      info_embed.timestamp = datetime.datetime.now()
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
  
  
  @commands.command(brief="Récupération d'informations.",description="Permet à l'utilisateur qui lance la commande de récupérer ses informations.",aliases=['recap'])
  async def getInfo(self, ctx : commands.Context) -> discord.Message:
    """ Get your own information
    
    Attributes :
      self : ...
      ctx : Context of the commands.
    """
    cursor = mydb.cursor(buffered=True, dictionary=True)
    #PRÉPARATION DE LA REQUÊTE.
    sql = f"SELECT BG_BANK_ACCOUNT, BG_ON_MYSELF FROM bg_users WHERE BG_ID_DISCORD = {ctx.author.id}"
    
    #GESTION DE LA REQUÊTE.
    cursor.execute(sql)
    row_count = cursor.rowcount
    
    if row_count > 0:
      # RÉCUPÉRATION DES VARIABLES.
      row = cursor.fetchone()
      bgBankAccount = row['BG_BANK_ACCOUNT']
      bgOnMyself = row['BG_ON_MYSELF']
      
      # FERMETURE DU CURSEUR
      cursor.close()
      
      # PRÉPARATION DE L'EMBED
      titre = f"Voici vos informations {ctx.author.name} :"
      info_embed = discord.Embed(title=titre, color=discord.Color.dark_blue())
      info_embed.add_field(name="Tout solde :",value=f"{bgBankAccount+bgOnMyself}€",inline=False)
      info_embed.add_field(name="Sur votre compte :",value=f"{bgBankAccount}€",inline=False)
      info_embed.add_field(name="Sur vous :",value=f"{bgOnMyself}€",inline=False)
      info_embed.set_footer(text='© BoatGame')
      info_embed.timestamp = datetime.datetime.now()
      
      # ON RETOURNE LE MESSAGE FINAL.
      return await ctx.send(embed=info_embed)
      
    else:
      # ON RÉCUPÈRE L'ERREUR
      raise commands.CommandInvokeError("Aucun compte lié.")
    
    return
  
  @getInfo.error
  async def getInfo_error(self, ctx : commands.Context, error : commands.CommandError):
    """ Help with error handling.
    
    Attributes :
      self : ...
      ctx : Context of the commands.
      error : The error received.
    """
    
    if isinstance(error, commands.CommandInvokeError):
      return await ctx.send("Aucun compte n'est associé à votre identifiant.")
    
    raise error
  
  
  @commands.command(brief="Récupération d'informations.",description="Permet à l'utilisateur qui lance la commande de récupérer ses informations.")
  async def deposit(self, ctx : commands.Context, toDeposit : int) -> discord.Message:
    """ Deposit on your bank account
    
    Attributes :
      self : ...
      ctx : Context of the commands.
      toDeposit ; Monney to deposit.
    """
    
    cursor = mydb.cursor(buffered=True, dictionary=True)
    
    # PRÉPARATION DE LA REQUÊTE.
    sql = f"SELECT BG_ON_MYSELF FROM bg_users WHERE BG_ID_DISCORD = {ctx.author.id}"
    
    # ON VÉRIFIE QUE LE COMPTE EXISTE.
    cursor.execute(sql)
    row_count = cursor.rowcount
    
    if row_count > 0:
      # RÉCUPÉRATION DES VARIABLES.
      row = cursor.fetchone()
      bgOnMyself = row['BG_ON_MYSELF']
      
      # FERMETURE DU CURSEUR
      cursor.close()
      
      if bgOnMyself < toDeposit:
        return await ctx.send("Vous possédez moins que ce que vous voulez poser.")
      
    else:
      # ON RÉCUPÈRE L'ERREUR
      raise commands.CommandInvokeError("Aucun compte lié.")
    
    
    cursor = mydb.cursor(buffered=True, dictionary=True)
    
    #PRÉPARATION DE LA REQUÊTE.
    sql = "UPDATE bg_users SET BG_BANK_ACCOUNT = BG_BANK_ACCOUNT + %s, BG_ON_MYSELF = BG_ON_MYSELF - %s WHERE BG_ID_DISCORD = %s"
    val = (toDeposit, toDeposit, ctx.author.id)
    
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
      titre = f"Dépôt sur votre compte, {ctx.author.name} :"
      info_embed = discord.Embed(title=titre, description=f"Vous venez de réaliser un dépôt de {toDeposit}€ sur votre compte.", color=discord.Color.dark_blue())
      info_embed.set_footer(text='© BoatGame')
      info_embed.timestamp = datetime.datetime.now()
      
      # ON RETOURNE LE MESSAGE FINAL.
      return await ctx.send(embed=info_embed)
    
    return
  
  @deposit.error
  async def deposit_error(self, ctx : commands.Context, error : commands.CommandError):
    """ Help with error handling.
    
    Attributes :
      self : ...
      ctx : Context of the commands.
      error : The error received.
    """
    
    if isinstance(error, commands.CommandInvokeError):
      return await ctx.send("Une erreur s'est produite lors du dépôt.")
    
    raise error


async def setup(bot : commands.Bot) -> None:
  """ Adding the Cog to the Bot.
  
  Attributes :
    bot : Bot who receive the Cog.
  """
  await bot.add_cog(DatabaseCmd(bot))