import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from connect import connect
import random

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
async def crée(ctx):
    """
    Commande pour créer deux stats : Force et Agression.
    Les valeurs sont générées aléatoirement entre 77 et 80.
    """
    force = random.randint(77, 80)
    agression = random.randint(77, 80)

    # Crée un message avec les statistiques.
    embed = discord.Embed(title="Vos stats générées", color=0x00ff00)
    embed.add_field(name="Force", value=str(force), inline=False)
    embed.add_field(name="Agression", value=str(agression), inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def transformer(ctx, *notes):
    """
    Commande pour transformer des notes en stats.
    Les 4 premières notes sont utilisées pour calculer la moyenne de la Force (arrondie),
    et les 3 dernières pour calculer la moyenne de l'Agression (arrondie).
    """
    try:
        # Convertir les notes en liste d'entiers
        notes = list(map(int, notes))

        # Vérifier que 7 notes sont fournies
        if len(notes) != 7:
            await ctx.send("Veuillez fournir exactement 7 notes (4 pour Force, 3 pour Agression).")
            return

        # Calculer la moyenne pour Force et Agression
        force_notes = notes[:4]
        agression_notes = notes[4:]
        force = round(sum(force_notes) / len(force_notes))
        agression = round(sum(agression_notes) / len(agression_notes))

        # Créer un message avec les statistiques calculées
        embed = discord.Embed(title="Stats calculées", color=0x0000ff)
        embed.add_field(name="Force", value=str(force), inline=False)
        embed.add_field(name="Agression", value=str(agression), inline=False)

        await ctx.send(embed=embed)

    except ValueError:
        await ctx.send("Veuillez fournir uniquement des nombres entiers comme notes.")

# Stockage des statistiques par utilisateur
user_stats = {}

# Dictionnaire pour suivre les dernières utilisations de la commande par utilisateur
derniere_utilisation = {}

# Initialisation des statistiques globales pour chaque pronom
stats_globaux = {
    "KIM": {"con": 90.0, "tra": 88.2, "men": 88.4, "réa": 88.0, "pré": 88.0, "nst": 88.0, "ene": 88.3},
    "PRY": {"con": 84.8, "tra": 85.0, "men": 83.0, "réa": 85.0, "pré": 84.0, "nst": 85.0, "ene": 85.0},
    "MED": {"con": 88.0, "tra": 88.0, "men": 87.0, "réa": 88.0, "pré": 89.0, "nst": 87.0, "ene": 86.2},
    "NIA": {"con": 84.4, "tra": 84.2, "men": 84.2, "réa": 85.0, "pré": 84.0, "nst": 84.0, "ene": 84.0},
    "KOV": {"con": 89.0, "tra": 89.0, "men": 89.0, "réa": 89.0, "pré": 88.6, "nst": 88.0, "ene": 88.0},
    "AIE": {"con": 85.0, "tra": 90.0, "men": 89.6, "réa": 85.0, "pré": 85.0, "nst": 86.0, "ene": 85.0},
    "MAK": {"con": 85.0, "tra": 100.0, "men": 85.2, "réa": 85.0, "pré": 85.0, "nst": 86.0, "ene": 85.0},
    "ROS": {"con": 88.0, "tra": 88.0, "men": 87.6, "réa": 89.0, "pré": 88.0, "nst": 87.0, "ene": 87.2},
    "LFE": {"con": 88.2, "tra": 87.0, "men": 89.0, "réa": 88.4, "pré": 87.0, "nst": 88.0, "ene": 88.2},
    "TFE": {"con": 86.2, "tra": 90.4, "men": 85.6, "réa": 85.4, "pré": 90.6, "nst": 86.2, "ene": 86.0},
    "CON": {"con": 85.0, "tra": 86.0, "men": 87.0, "réa": 86.0, "pré": 86.0, "nst": 86.0, "ene": 86.2},
    "DIA": {"con": 84.0, "tra": 86.2, "men": 84.0, "réa": 85.0, "pré": 84.0, "nst": 84.0, "ene": 84.0},
    "HUL": {"con": 89.1, "tra": 85.0, "men": 85.5, "réa": 84.6, "pré": 88.1, "nst": 85.9, "ene": 85.0},
    "BEL": {"con": 86.4, "tra": 87.0, "men": 85.8, "réa": 85.6, "pré": 87.0, "nst": 83.8, "ene": 84.8},
    "PRO": {"con": 85.0, "tra": 84.0, "men": 86.0, "réa": 85.0, "pré": 84.4, "nst": 84.0, "ene": 83.4},
    "NUN": {"con": 83.4, "tra": 83.6, "men": 82.6, "réa": 82.2, "pré": 83.6, "nst": 83.6, "ene": 84.2},
    "BIL": {"con": 84.2, "tra": 83.6, "men": 84.2, "réa": 83.2, "pré": 83.0, "nst": 84.2, "ene": 83.4},
    "NIT": {"con": 82.0, "tra": 86.4, "men": 82.0, "réa": 82.0, "pré": 81.0, "nst": 82.0, "ene": 80.0},
    "END": {"con": 86.0, "tra": 90.0, "men": 86.0, "réa": 86.0, "pré": 86.4, "nst": 85.8, "ene": 85.4},
    "THE": {"con": 85.0, "tra": 86.0, "men": 85.2, "réa": 85.0, "pré": 85.0, "nst": 84.8, "ene": 85.0},
}
# Dictionnaire des noms et prénoms
noms_prenoms = {
    "KIM": ("Hae Won", "Kim", "Femme", ":1FORMULA:"),
    "PRY": ("Andreas", "Pryviat", "Homme", ":1FORMULA:"),
    "MED": ("Léo", "Medo", "Homme", ":1FORMULA:"),
    "NIA": ("Lewis", "Niamate", "Homme", ":1FORMULA:"),
    "KOV": ("Riin", "Kovac", "Homme", ":1FORMULA:"),
    "AIE": ("Allessandro", "Aiello", "Homme", ":1FORMULA~1:"),
    "MAK": ("Nicholas", "Makkinen", "Homme", ":1FORMULA:"),
    "ROS": ("Oscar", "Rosberg", "Homme", ":1FORMULA:"),
    "LFE": ("Luis", "Fernand", "Homme", ":1FORMULA:"),
    "TFE": ("Tom", "Fernandez", "Homme", ":1FORMULA:"),
    "CON": ("Noah", "Connor", "Homme", ":1FORMULA:"),
    "DIA": ("Zachary", "Diaz", "Homme", ":1FORMULA:"),
    "HUL": ("Justin", "Huler", "Homme", ":1FORMULA:"),
    "BEL": ("Marc-Antoine", "Belmondini", "Homme", ":1FORMULA:"),
    "PRO": ("Alain", "Proviste", "Homme", ":1FORMULA:"),
    "NUN": ("Rio", "Nuno", "Homme", ":1FORMULA:"),
    "BIL": ("Jakie", "Biloutte", "Homme", ":1FORMULA:"),
    "NIT": ("Trivality", "Nitrox", "Homme", ":1FORMULA:"),
    "END": ("Félix", "Ender", "Homme", ":1FORMULA:"),
    "THE": ("Tome", "Théo", "Homme", ":1FORMULA:"),
}

@bot.command()
async def amélioration(ctx, option: int, pronom: str, *categories):

    utilisateur_id = ctx.author.id
    maintenant = datetime.now()

    # Vérifier si l'utilisateur a déjà utilisé la commande aujourd'hui
    if utilisateur_id in derniere_utilisation:
        derniere_date = derniere_utilisation[utilisateur_id]
        if maintenant - derniere_date < timedelta(days=1):
            temps_restant = timedelta(days=1) - (maintenant - derniere_date)
            heures, secondes = divmod(temps_restant.total_seconds(), 3600)
            minutes, _ = divmod(secondes, 60)
            await ctx.send(
                f"Vous avez déjà utilisé cette commande aujourd'hui ! Vous pourrez réessayer dans {int(heures)}h {int(minutes)}m."
            )
            return

    # Enregistrer la date d'utilisation actuelle pour cet utilisateur
    derniere_utilisation[utilisateur_id] = maintenant
    
    """
    Améliore les statistiques d'un pronom spécifique selon l'option choisie.
    """
    pronom = pronom.upper()
    if pronom not in stats_globaux:
        await ctx.send(f"Le pronom {pronom} n'existe pas. Veuillez en choisir un parmi : {', '.join(stats_globaux.keys())}.")
        return

    stats = stats_globaux[pronom]

    for category in categories:
        category = category.lower()
        if category not in stats:
            await ctx.send(f"La catégorie {category} n'existe pas pour {pronom}. Veuillez choisir parmi : {', '.join(stats.keys())}.")
            return

    try:
        # Gestion des options d'amélioration
        if option == 1 and len(categories) >= 4:
            for category in categories[:4]:
                if stats[category] + 0.1 > 100:
                    await ctx.send(f"La statistique {category.upper()} ne peut pas dépasser 100. Action annulée.")
                    return
                stats[category] += 0.1
        elif option == 2 and len(categories) >= 2:
            for category in categories[:2]:
                if stats[category] + 0.2 > 100:
                    await ctx.send(f"La statistique {category.upper()} ne peut pas dépasser 100. Action annulée.")
                    return
                stats[category] += 0.2
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
        elif option == 4 and len(categories) >= 2:
            if stats[categories[0]] + 0.3 > 100:
                await ctx.send(f"La statistique {categories[0].upper()} ne peut pas dépasser 100. Action annulée.")
                return
            stats[categories[0]] += 0.3
            if stats[categories[1]] + 0.1 > 100:
                await ctx.send(f"La statistique {categories[1].upper()} ne peut pas dépasser 100. Action annulée.")
                return
            stats[categories[1]] += 0.1
        elif option == 5 and len(categories) >= 1:
            if stats[categories[0]] + 0.4 > 100:
                await ctx.send(f"La statistique {categories[0].upper()} ne peut pas dépasser 100. Action annulée.")
                return
            stats[categories[0]] += 0.4
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
    :Fia~1: :peflogo~1:
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
    embed = discord.Embed(title="Comment marche les up !", color=0x00ffcc)
    embed.add_field(name="/amélioration [option] [pronom pilote ex: Aiello -> AIE] [mettre les noms des stats a améliorer OBLIGATOIREMENT EN MINUSCULE]", value="Améliore les statistiques selon l'option choisie :\n\n1. +0.1 pour 4 stats\n2. +0.2 pour 2 stats\n3. +0.2 pour 1 stat et +0.1 pour 2 stats\n4. +0.3 pour 1 stat et +0.1 pour 1 stat\n5. +0.4 pour 1 stat\n\nExemple : /amélioration 2 AIE men tra", inline=False)

    await ctx.send(embed=embed)

connect()
# Démarrage du bot.
bot.run(BOT_TOKEN)
