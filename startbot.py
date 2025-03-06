import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from connect import connect
import random
import asyncio


load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')

# Intents nécessaires pour interagir avec les membres du serveur.
intents = discord.Intents.default()
intents.message_content = True

# Création du bot avec un préfixe slash (/) pour les commandes.
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.command()
async def stats(ctx, pronom: str):
    """
    Commande pour afficher les statistiques calculées d'un pilote.
    Utilisation : /stats [pronom pilote]
    """
    try:
        # Vérifier si le pilote existe
        if pronom.upper() not in stats_globaux:
            await ctx.send(f"❌ Le pilote '{pronom}' n'existe pas.")
            return

        # Récupérer les stats du pilote
        pilote_stats = stats_globaux[pronom.upper()]
        stats_values = list(pilote_stats.values())  # Convertir en liste pour gérer l'ordre

        # Calcul de Force et Agression
        force = round(sum(stats_values[:4]) / 4)  # Moyenne des 4 premières stats
        agression = round(sum(stats_values[4:]) / 3)  # Moyenne des 3 dernières stats

        # Créer un embed pour afficher les stats
        embed = discord.Embed(title=f"📊 Stats calculées de {pronom.upper()}", color=0x00ff00)
        embed.add_field(name="💪 Force", value=str(force), inline=True)
        embed.add_field(name="🔥 Agression", value=str(agression), inline=True)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Une erreur est survenue : {e}")


# Stockage des statistiques par utilisateur
user_stats = {}

# Stockage des statistiques par utilisateur et dernière utilisation
user_last_command_date = {}

# Initialisation des statistiques globales pour chaque pronom
stats_globaux = {
    "KIM": {"con": 90.4, "tra": 89.8, "men": 90.0, "réa": 90.0, "pré": 90.0, "nst": 90.4, "ene": 89.5},
    "BIA": {"con": 85.0, "tra": 85.0, "men": 85.1, "réa": 85.0, "pré": 85.3, "nst": 85.0, "ene": 85.0},
    "WIL": {"con": 81.8, "tra": 89.6, "men": 81.0, "réa": 82.0, "pré": 83.4, "nst": 81.0, "ene": 82.0},
    "NIA": {"con": 90.2, "tra": 87.0, "men": 87.0, "réa": 85.8, "pré": 85.8, "nst": 85.4, "ene": 85.4},
    "KOV": {"con": 91.0, "tra": 91.0, "men": 91.0, "réa": 91.0, "pré": 90.6, "nst": 90.0, "ene": 90.0},
    "AIE": {"con": 90.0, "tra": 99.6, "men": 90.0, "réa": 87.2, "pré": 85.0, "nst": 86.0, "ene": 85.0},
    "PAI": {"con": 84.4, "tra": 84.2, "men": 84.4, "réa": 84.2, "pré": 84.3, "nst": 84.3, "ene": 84.4},
    "ROS": {"con": 90.4, "tra": 91.0, "men": 90.0, "réa": 90.0, "pré": 90.0, "nst": 90.0, "ene": 90.0},
    "LFE": {"con": 89.0, "tra": 91.0, "men": 89.0, "réa": 88.4, "pré": 88.2, "nst": 88.0, "ene": 88.2},
    "TFE": {"con": 88.8, "tra": 94.0, "men": 87.8, "réa": 87.2, "pré": 94.2, "nst": 89.2, "ene": 88.2},
    "CON": {"con": 89.0, "tra": 88.0, "men": 88.2, "réa": 88.0, "pré": 88.0, "nst": 88.0, "ene": 89.0},
    "GAI": {"con": 81.0, "tra": 97.8, "men": 81.5, "réa": 82.5, "pré": 83.0, "nst": 81.0, "ene": 82.0},
    "HUL": {"con": 89.1, "tra": 86.8, "men": 87.3, "réa": 87.2, "pré": 88.1, "nst": 86.3, "ene": 88.0},
    "BEL": {"con": 88.0, "tra": 88.2, "men": 88.2, "réa": 88.0, "pré": 87.8, "nst": 87.0, "ene": 87.6},
    "PRO": {"con": 85.0, "tra": 84.0, "men": 86.0, "réa": 85.0, "pré": 84.4, "nst": 84.0, "ene": 83.4},
    "NUN": {"con": 85.0, "tra": 85.2, "men": 85.0, "réa": 85.2, "pré": 85.2, "nst": 85.2, "ene": 85.0},
    "BIL": {"con": 86.6, "tra": 86.4, "men": 85.8, "réa": 86.0, "pré": 85.4, "nst": 86.2, "ene": 86.2},
    "NIT": {"con": 83.2, "tra": 89.6, "men": 82.0, "réa": 82.0, "pré": 83.4, "nst": 82.0, "ene": 83.6},
    "DIA": {"con": 88.0, "tra": 89.8, "men": 88.0, "réa": 85.0, "pré": 84.0, "nst": 84.0, "ene": 84.0},
    "THE": {"con": 88.7, "tra": 90.0, "men": 87.0, "réa": 87.0, "pré": 88.0, "nst": 86.0, "ene": 87.0},
    "GRO": {"con": 83.0, "tra": 85.0, "men": 82.0, "réa": 86.0, "pré": 83.0, "nst": 85.0, "ene": 84.0},
}
# Dictionnaire des noms et prénoms6
noms_prenoms = {
    "KIM": ("Hae Won", "Kim", "Femme", "Formula One"),
    "PRY": ("Andreas", "Pryviat", "Homme", "Formula One"),
    "WIL": ("Leclerc", "Wilveur", "Homme", "Formula One"),
    "NIA": ("Lewis", "Niamate", "Homme", "Formula One"),
    "KOV": ("Riin", "Kovac", "Homme", "Formula One"),
    "AIE": ("Allessandro", "Aiello", "Homme", "Formula One"),
    "PAI": ("Oscar", "Paistra", "Homme", "Formula One"),
    "ROS": ("Oscar", "Rosberg", "Homme", "Formula One"),
    "LFE": ("Luis", "Fernand", "Homme", "Formula One"),
    "TFE": ("Tom", "Fernandez", "Homme", "Formula One"),
    "CON": ("Noah", "Connor", "Homme", "Formula One"),
    "GAI": ("Gabriele", "Aiello", "Homme", "Formula One"),
    "HUL": ("Justin", "Huler", "Homme", "Formula One"),
    "BEL": ("Marc-Antoine", "Belmondini", "Homme", "Formula One"),
    "PRO": ("Alain", "Proviste", "Homme", "Formula One"),
    "NUN": ("Rio", "Nuno", "Homme", "Formula One"),
    "BIL": ("Jakie", "Biloutte", "Homme", "Formula One"),
    "NIT": ("Trivality", "Nitrox", "Homme", "Formula One"),
    "DIA": ("Zach", "Diaz", "Homme", "Formula One"),
    "THE": ("Tome", "Théo", "Homme", "Formula One"),
    "GRO": ("Alex", "Groël", "Homme", "Formula One"),
}
# Variable pour suivre l'état de la commande /up
up_bloque = False

@bot.command()
async def bloquerup(ctx):
    """
    Active ou désactive la commande /up.
    Seuls les administrateurs peuvent l'utiliser.
    """
    global up_bloque

    # Vérifier si l'utilisateur est administrateur
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Vous n'avez pas la permission d'utiliser cette commande.")
        return

    # Inverser l'état de la commande /up
    up_bloque = not up_bloque

    if up_bloque:
        await ctx.send("🚫 La commande `/up` est maintenant **désactivée**.")
    else:
        await ctx.send("✅ La commande `/up` est maintenant **activée**.")

@bot.command()
async def up(ctx, option: int, pronom: str, *categories):
    """
    Commande pour améliorer les statistiques des pilotes.
    """
    global up_bloque

    # Vérifier si la commande est bloquée
    if up_bloque:
        await ctx.send("❌ La commande `/up` est actuellement désactivée.")
        return

    # (Le reste du code de la commande /up reste inchangé)
    user_id = ctx.author.id
    current_date = datetime.now().date()

    # Rôles qui permettent des utilisations illimitées
    roles_with_no_limit = ["Staff du serveur"]

    # Vérification si l'utilisateur a un rôle spécial
    has_no_limit = any(role.name in roles_with_no_limit for role in ctx.author.roles)

    # Si l'utilisateur n'a pas un rôle spécial, limiter à une utilisation par jour
    if not has_no_limit:
        if user_id in user_last_command_date and user_last_command_date[user_id] == current_date:
            await ctx.send("Vous avez déjà utilisé la commande /up aujourd'hui. Revenez demain !")
            return

    # Vérification si le pronom existe
    pronom = pronom.upper()
    if pronom not in stats_globaux:
        await ctx.send(f"Le pronom {pronom} n'existe pas. Veuillez en choisir un parmi : {', '.join(stats_globaux.keys())}.")
        return

    stats = stats_globaux[pronom]

    # Vérification des catégories spécifiées
    for category in categories:
        category = category.lower()
        if category not in stats:
            await ctx.send(f"La catégorie {category} n'existe pas pour {pronom}. Veuillez choisir parmi : {', '.join(stats.keys())}.")
            return

    try:
        # (Le code de gestion des options reste le même ici)
        # Gestion des modifications des statistiques en fonction des options...

        # Met à jour la date d'utilisation de la commande si l'utilisateur n'a pas un rôle spécial
        if not has_no_limit:
            user_last_command_date[user_id] = current_date

    except ValueError:
        await ctx.send("Une erreur est survenue. Assurez-vous que toutes les données fournies sont correctes.")
        return

    try:
        # Gestion des options d'amélioration
        if option == 1 and len(categories) >= 4:
            for category in categories[:4]:
                if stats[category] + 0.1 > 100:
                    await ctx.send(f"La statistique {category.upper()} ne peut pas dépasser 100. Action annulée.")
                    return
                stats[category] += 0.1
                # Met à jour la date d'utilisation de la commande
                user_last_command_date[user_id] = current_date
        elif option == 2 and len(categories) >= 2:
            for category in categories[:2]:
                if stats[category] + 0.2 > 100:
                    await ctx.send(f"La statistique {category.upper()} ne peut pas dépasser 100. Action annulée.")
                    return
                stats[category] += 0.2
                # Met à jour la date d'utilisation de la commande
                user_last_command_date[user_id] = current_date
        elif option == 3 and len(categories) >= 3:
            if stats[categories[0]] + 0.2 > 100:
                await ctx.send(f"La statistique {categories[0].upper()} ne peut pas dépasser 100. Action annulée.")
                return
            stats[categories[0]] += 0.2
            for category in categories[1:3]:
                if stats[category] + 0.1 > 100:
                    await ctx.send(f"La statistique {category.upper()} ne peut pas dépasser 100. Action annulée.")
                    return
                stats[category] += 0.1
                # Met à jour la date d'utilisation de la commande
                user_last_command_date[user_id] = current_date
        elif option == 4 and len(categories) >= 2:
            if stats[categories[0]] + 0.3 > 100:
                await ctx.send(f"La statistique {categories[0].upper()} ne peut pas dépasser 100. Action annulée.")
                return
            stats[categories[0]] += 0.3
            if stats[categories[1]] + 0.1 > 100:
                await ctx.send(f"La statistique {categories[1].upper()} ne peut pas dépasser 100. Action annulée.")
                return
            stats[categories[1]] += 0.1
            # Met à jour la date d'utilisation de la commande
            user_last_command_date[user_id] = current_date
        elif option == 5 and len(categories) >= 1:
            if stats[categories[0]] + 0.4 > 100:
                await ctx.send(f"La statistique {categories[0].upper()} ne peut pas dépasser 100. Action annulée.")
                return
            stats[categories[0]] += 0.4
            # Met à jour la date d'utilisation de la commande
            user_last_command_date[user_id] = current_date
        else:
            await ctx.send("Option ou nombre de catégories invalides. Veuillez vérifier votre commande.")

    except ValueError:
        await ctx.send("Une erreur est survenue. Assurez-vous que toutes les données fournies sont correctes.")

    # Récupération du prénom et du nom
    if pronom in noms_prenoms:
        prenom, nom, sex, catégorie = noms_prenoms[pronom]
    else:
        prenom, nom, sex, catégorie = "Inconnu", "Inconnu"

    # Récupération des stats
    stats = stats_globaux[pronom]
    note_generale = sum(stats.values()) / len(stats.values())

    fiche_message = f"""
# **DRIVER FICHE**

Nom pilote : {prenom} {nom}
Sexe : {sex}
Catégorie : {catégorie}

--------------------------

┌
          {round(note_generale)}          NOTE
                     générale
└

╭→     CON                    {stats['con']}    ┐
┊       concentration
┊
┊→     TRA                    {stats['tra']}
┊       trajectoire                   ┘
╰

╭→     MEN                    {stats['men']}       ┐
┊       mentalité
┊
┊→     RÉA                    {stats['réa']} 
┊       réaction
┊
┊→     PRÉ                   {stats['pré']}
┊       précision                         ┘
╰

╭
┊→       NST                    {stats['nst']}
┊         no stress
┊
┊→       ENE                    {stats['ene']}
┊         energie
╰
  ***OFFICIAL STATS***

------------------------------------------
Besoin d’aide ? Merci de faire la commande /aide
"""
    await ctx.send(fiche_message)

@bot.command()
async def fiche(ctx, pronom: str):
    """
    Affiche la fiche détaillée d'un pilote selon le pronom fourni.
    """
    pronom = pronom.upper()
    if pronom not in stats_globaux:
        await ctx.send(f"Le pronom {pronom} n'existe pas. Veuillez en choisir un parmi : {', '.join(stats_globaux.keys())}.")
        return

    # Récupération des informations du pilote
    if pronom in noms_prenoms:
        prenom, nom, sex, catégorie = noms_prenoms[pronom]
    else:
        prenom, nom, sex, catégorie = "Inconnu", "Inconnu", "Inconnu", "Inconnu"

    # Récupération des statistiques
    stats = stats_globaux[pronom]
    note_generale = sum(stats.values()) / len(stats.values())

    # Construction de la fiche
    fiche_message = f"""
# **DRIVER FICHE**

Nom pilote : {prenom} {nom}
Sexe : {sex}
Catégorie : {catégorie}

--------------------------

┌
          {round(note_generale)}          NOTE
                     générale
└

╭→     CON                    {stats['con']}    ┐
┊       concentration
┊
┊→     TRA                    {stats['tra']}
┊       trajectoire                   ┘
╰

╭→     MEN                    {stats['men']}       ┐
┊       mentalité
┊
┊→     RÉA                    {stats['réa']} 
┊       réaction
┊
┊→     PRÉ                   {stats['pré']}
┊       précision                         ┘
╰

╭
┊→       NST                    {stats['nst']}
┊         no stress
┊
┊→       ENE                    {stats['ene']}
┊         energie
╰
  ***OFFICIAL STATS***

------------------------------------------
Besoin d’aide ? Merci de faire la commande /aide
"""
    await ctx.send(fiche_message)

@bot.command()
async def aide(ctx):
    """
    Commande pour afficher l'aide sur les commandes disponibles.
    """
    aide_message = f'''**Comment fonctionnent les commandes /up ?**

Syntaxe :
`/up [option] [pronom pilote ex : Aiello -> AIE] [statistiques à améliorer en minuscules]`

Cette commande permet d'améliorer les statistiques d'un pilote en fonction de l'option choisie.

## *Options disponibles* :

1. **+0.1** sur **4 stats**

2. **+0.2** sur **2 stats**

3. **+0.2** sur **1 stat** et **+0.1** sur **2 stats**

4. **+0.3** sur **1 stat** et **+0.1** sur **1 stat**

5. **+0.4** sur **1 stat**

## *Exemple d'utilisation* :

`/up 2 AIE men tra`
Ici, les stats **men** et **tra** seront améliorées de **+0.2** chacune.

**Note** : Si des résultats affichent plusieurs chiffres après la virgule, ne prenez en compte que le **premier chiffre après la virgule.**'''

    await ctx.send(aide_message)

connect()
# Démarrage du bot.
bot.run(BOT_TOKEN)
