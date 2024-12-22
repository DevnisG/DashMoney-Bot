# Libs / Runner (Main)
import os
import discord
from discord.ext import commands
from manager.data_manager import load_local_data
from commands.bot_commands import setup_commands
from config.message_formatter import format_message
from manager.config_manager import load_config, save_config
from commands.bot_tasks import setup_tasks  

# Discord Config:
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True 
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

# Task On_Ready Event run Bot at the start:
@bot.event
async def on_ready():
    print(f"[INFO] Bot iniciado como {bot.user}")
    setup_tasks(bot)  
    config = load_config()
    if config.get("channel_id"):
        channel = bot.get_channel(config["channel_id"])
        if channel:
            print(f"[INFO] Canal encontrado: {channel.name} ({channel.id})")
            if config.get("message_id"):
                try:
                    await channel.fetch_message(config["message_id"])
                    print(f"[INFO] Mensaje de dashboard encontrado: {config['message_id']}")
                except discord.NotFound:
                    print("[WARNING] Mensaje de dashboard no encontrado. Creando uno nuevo.")
            else:
                print("[INFO] No hay mensaje de dashboard configurado. Creando uno nuevo.")
            if not config.get("message_id"):
                data = load_local_data()
                embed = format_message(data)
                try:
                    message = await channel.send(embed=embed)
                    config["message_id"] = message.id
                    save_config(config)
                except Exception as e:
                    print(f"[ERROR] Error al enviar o fijar el mensaje: {e}")
        else:
            print("[ERROR] No se pudo encontrar el canal configurado.")
    else:
        print("[WARNING] No hay canal configurado. Usa el comando !set_channel para configurarlo.")

# Func for `on_guild_join`:
@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                "¡Hola a todos! Soy DashMoney-bot, desarrollado por @Devnis. "
                "Usa `@dolar set_channel` para configurar mi canal de interacción."
            )
            print(f"[INFO] Bot unido al servidor: {guild.name} (ID: {guild.id})")
            break

# Main Func read DISCORD_TOKEN from env:
def main():
    DOLAR_DISCORD_TOKEN = os.getenv('DOLAR_DISCORD_TOKEN')
    if not DOLAR_DISCORD_TOKEN:
        print(f"[INFO] Token de Discord no encontrado. Por favor, configura la variable de entorno DISCORD_TOKEN.")
    setup_commands(bot)
    bot.run(DOLAR_DISCORD_TOKEN)

# Runner:
if __name__ == "__main__":
    main()
