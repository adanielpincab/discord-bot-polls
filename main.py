import discord
from discord.ext import commands
import matplotlib.pyplot as plt

import secrets

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

polls = {
    "test": {  # Nombre de la encuesta
        "options": ["option1", "option2"],  # Lista de opciones iniciales
        "votes": [4, 7],
        "finished": False  # Estado de la encuesta
    }
}

# Turn on bot message
@bot.event
async def on_ready():
    print(f"Encendido! {bot.user}")

# Create new poll
@bot.command()
async def create(ctx, poll_name: str):
    if poll_name in polls:
        await ctx.send(f"Ya existe una encuesta con el nombre '{poll_name}'.")
    else:
        polls[poll_name] = {"options": [], "finished": False}
        await ctx.send(f"Encuesta '{poll_name}' creada exitosamente.")

# Add to poll
@bot.command()
async def add(ctx, poll_name: str, *, option: str):
    if poll_name not in polls:
        polls[poll_name] = {"options": [], "finished": False}
    
    if polls[poll_name]["finished"]:
        await ctx.send(f"La encuesta '{poll_name}' ya ha sido finalizada.")
    else:
        polls[poll_name]["options"].append(option)
        await ctx.send(f"Opción añadida a la encuesta '{poll_name}': {option}")

# Remove from poll
@bot.command()
async def remove(ctx, poll_name: str, position: int):
    if poll_name not in polls:
        await ctx.send(f"No existe una encuesta llamada '{poll_name}'.")
    elif polls[poll_name]["finished"]:
        await ctx.send(f"La encuesta '{poll_name}' ya ha sido finalizada.")
    else:
        try:
            removed_option = polls[poll_name]["options"].pop(position - 1)
            await ctx.send(f"Opción eliminada de la encuesta '{poll_name}': {removed_option}")
        except IndexError:
            await ctx.send(f"La posición {position} no es válida en la encuesta '{poll_name}'.")

# Finish poll
async def finish(ctx, poll_name: str):
    if poll_name not in polls:
        await ctx.send(f"No existe una encuesta llamada '{poll_name}'.")
    elif polls[poll_name]["finished"]:
        await ctx.send(f"La encuesta '{poll_name}' ya ha sido finalizada.")
    else:
        polls[poll_name]["finished"] = True
        results = "\n".join([f"{i+1}. {option}" for i, option in enumerate(polls[poll_name]["options"])])
        await ctx.send(f"Encuesta '{poll_name}' finalizada. Resultados:\n{results}")

# List poll
@bot.command()
async def list(ctx, poll_name: str):
    if poll_name not in polls:
        await ctx.send(f"No existe una encuesta llamada '{poll_name}'. Usa el comando `$create {poll_name}` para crearla primero.")
    elif polls[poll_name]["finished"]:
        await ctx.send(f"La encuesta '{poll_name}' ya ha sido finalizada. Usa `$finish {poll_name}` para ver los resultados.")
    else:
        if len(polls[poll_name]["options"]) == 0:
            await ctx.send(f"La encuesta '{poll_name}' no tiene opciones añadidas todavía.")
        else:
            options = "\n".join([f"{i+1}. {option}" for i, option in enumerate(polls[poll_name]["options"])])
            await ctx.send(f"Opciones de la encuesta '{poll_name}':\n{options}")

@bot.command()
async def show1(ctx):
    # Crear la gráfica de tarta
    plt.figure(figsize=(8, 8))  # Tamaño de la figura (opcional)
    plt.pie(polls["test"]["votes"], labels=polls["test"]["options"], autopct='%1.1f%%', colors=['skyblue', 'orange'])

    # Añadir título
    plt.title(f'Gráfico de Tarta - Encuesta: TEST')

    # Mostrar la gráfica
    plt.show()



bot.run(secrets.TOKEN)



# si creamos una encuesta que ha sido finalizada, ¿crear otra de cero y borrar anterior? ¿se reabre la encuesta con sus opciones?