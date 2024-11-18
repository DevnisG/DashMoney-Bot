# Libs / Tasks.
import aiohttp
import discord
from discord.ext import tasks
from manager.api_manager import fetch_api_data
from config.message_formatter import format_message
from manager.config_manager import load_config, save_config
from manager.data_manager import load_local_data, save_local_data
from config.constants import DOLLAR_API_VALUES, DOLLAR_API_STATE

# Var for Checking Global Task:
tasks_started = False

# Async Func for Updating Dashboard MSG:
async def perform_dashboard_update(bot):
    print("[INFO] Ejecutando tarea de actualización del dashboard...")
    config = load_config()
    data = load_local_data()

    channel_id = config.get("channel_id")
    message_id = config.get("message_id")

    if not channel_id or not message_id:
        print("[WARNING] Canal o mensaje no configurado. Esperando configuración...")
        return

    channel = bot.get_channel(channel_id)
    if not channel:
        print("[ERROR] No se encontró el canal configurado.")
        return

    try:
        message = await channel.fetch_message(message_id)
    except discord.NotFound:
        print("[ERROR] No se encontró el mensaje configurado. Reiniciando configuración.")
        config["message_id"] = None
        save_config(config)
        return
    except Exception as e:
        print(f"[ERROR] Error al obtener el mensaje: {e}")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(DOLLAR_API_VALUES) as response:
            api_values = await fetch_api_data(response, DOLLAR_API_VALUES)
        async with session.get(DOLLAR_API_STATE) as response:
            api_state = await fetch_api_data(response, DOLLAR_API_STATE)

    data_changed = False

    if api_values and api_values != data.get("values"):
        print(f"[UPDATE] Actualización detectada en 'values'")
        data["values"] = api_values
        save_local_data(data)
        data_changed = True

    if api_state and api_state.get("estado") != data.get("state", {}).get("estado"):
        print(f"[UPDATE] Actualización detectada en 'state'")
        data["state"] = api_state
        save_local_data(data)
        data_changed = True

    if data_changed:
        embed = format_message(data)
        try:
            await message.edit(embed=embed)
            print("[INFO] Mensaje del dashboard actualizado.")
        except Exception as e:
            print(f"[ERROR] Error al editar el mensaje: {e}")
    else:
        print("[INFO] Sin cambios detectados en los datos.")

# Task Loop Every (5 Hours)
@tasks.loop(hours=5)
async def update_dashboard_loop(bot):
    await perform_dashboard_update(bot)

# Func for Setup Tasks:
def setup_tasks(bot):
    global tasks_started
    if not tasks_started:
        if not update_dashboard_loop.is_running():
            update_dashboard_loop.start(bot)
            print("[INFO] Bucle de actualización del dashboard iniciado.")
        bot.loop.create_task(perform_dashboard_update(bot))
        tasks_started = True
        print("[INFO] Tarea de actualización del dashboard ejecutada una vez al inicio.")
