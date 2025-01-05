import os
from dotenv import load_dotenv
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

# Stockage des statistiques par utilisateur
user_stats = {}

# Initialisation des statistiques globales pour chaque pronom
stats_globaux = {
    "KIM": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "PRY": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "MED": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "NIA": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "KOV": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "AIE": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "MAK": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "ROS": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "LFE": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "TFE": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "CON": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "DIA": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "HUL": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "BEL": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "PRO": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "NUN": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "BIL": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "NIT": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "END": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
    "THE": {"con": 80.0, "tra": 79.0, "men": 78.5, "réa": 77.5, "pré": 78.0, "nst": 79.5, "ene": 80.0},
}

@bot.command()
async def amélioration(ctx, option: int, pronom: str, *categories):
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
            return

        # Afficher les statistiques mises à jour
        embed = discord.Embed(title=f"Statistiques mises à jour pour {pronom.capitalize()}", color=0x00ffcc)
        for key, value in stats.items():
            embed.add_field(name=key, value=f"{value:.1f}", inline=False)
        await ctx.send(embed=embed)

    except ValueError:
        await ctx.send("Une erreur est survenue. Assurez-vous que toutes les données fournies sont correctes.")



@bot.command()
async def aide(ctx):
    """
    Commande pour afficher l'aide sur les commandes disponibles.
    """
    embed = discord.Embed(title="Aide des Commandes", color=0x00ffcc)
    embed.add_field(name="/crée", value="Génère deux stats : Force et Agression, avec des valeurs aléatoires entre 77 et 80.", inline=False)
    embed.add_field(name="/amélioration [option] [pronom pilote ex: Aiello -> AIE] [mettre les noms des stats a améliorer]", value="Améliore les statistiques selon l'option choisie :\n\n1. +0.1 pour 4 stats\n2. +0.2 pour 2 stats\n3. +0.2 pour 1 stat et +0.1 pour 2 stats\n4. +0.3 pour 1 stat et +0.1 pour 1 stat\n5. +0.4 pour 1 stat\n\nExemple : /up 1 78.0 79.5 80.0 77.5", inline=False)

    await ctx.send(embed=embed)

connect()
# Démarrage du bot.
bot.run(BOT_TOKEN)
