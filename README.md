# BOAT GAME

Boat Game est un bot discord qui permet aux utilisateurs de jouer, de parier et de gérer un compte bancaire fictif.

## Installation

Pour pouvoir utiliser ce bot, il vous foudra lancer les installations suivantes :

```bash
pip install discord.py # Librairie discord.
pip install python-dotenv # Pour la récupération des variables depuis le .env.
pip install mysql-connector-python # Pour la connexion à la base de données.
```
La création d'un fichier .env est également nécessaire afin d'y mettre le **TOKEN** de votre bot et les informations de votre base de données. (N'oublier pas d'ajouter le fichier à un **.gitignore**)

```bash
# RENSEIGNER LE TOKEN CI-APRES :
TOKEN=VOTRE_TOKEN

# INFORMATION DE CONNEXION A LA BD
DBHOST=bdHostHere
DBUSRNAME=dbUsernameHere
DBMDP=dbPwdHere
DBNAME=dbNameHere
```
Enfin pour la base de données, veuillez importer le fichier **creation_bd_boat_game.sql** dans mysql afin d'instancier la base de données, ses tables ainsi qu'un utilisateur nommé *BoatGame*. Pensez à changer le mot de passe du nouvel utilisateur.

## Commandes & évènements disponibles

Ci-dessous la liste des évènements disponibles :
 - *on_ready* : Indique que le bot est prêt.

Ci-dessous la liste des commandes disponibles (préfix : "!") :
 - *clear* : Efface un certain nombre de message dans le chat.
 - *setAccount* : Permet la création d'un compte dans la base de données dédié.
 - *getInfo* | *recap* : Permet la récupération des informations de l'utilisateur qui lance la commande.
 - *deposit* : Permet de déposer de l'argent vers son compte.
 - *draw* | *tirer* : Permet de retirer de l'argent depuis son compte.

## License

[© 2024 C-Lilian](https://github.com/C-Lilian)