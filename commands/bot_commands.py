# Libs / Commands.
import json
import time
import discord
from discord.ext import commands
from datetime import datetime, timezone
from manager.data_manager import load_local_data
from commands.bot_tasks import perform_dashboard_update 
from manager.config_manager import load_config, save_config
from config.message_formatter import format_message, format_message_all, format_date_time

# Command for Set Channel:
def setup_commands(bot):
    @bot.command(name='set_channel')
    @commands.has_permissions(administrator=True)
    async def set_channel(ctx):
        try:
            await ctx.message.delete(delay=10) 
        except discord.Forbidden:
            await ctx.send("⚠️ No tengo permisos para eliminar mensajes del usuario.", delete_after=5)
            return
        
        config = load_config()
        config["channel_id"] = ctx.channel.id
        save_config(config)
        await ctx.send("📢 Canal configurado correctamente para el dashboard.", delete_after=10)
        print(f"[INFO] Canal configurado: {ctx.channel.id}")

        if not config.get("message_id"):
            data = load_local_data()
            embed = format_message(data)
            try:
                message = await ctx.send(embed=embed)
                config["message_id"] = message.id
                save_config(config)
                print(f"[INFO] Mensaje de dashboard enviado en el canal {ctx.channel.id}.")
            except Exception as e:
                print(f"[ERROR] Error al enviar el mensaje: {e}")

    # Command for Save Channel ID:
    @bot.command(name='channel_id')
    @commands.has_permissions(administrator=True)
    async def channel_id_command(ctx):
        try:
            await ctx.message.delete(delay=10)
        except discord.Forbidden:
            await ctx.send("⚠️ No tengo permisos para eliminar mensajes del usuario.", delete_after=5)
            return
        
        config = load_config()
        if config.get("channel_id"):
            message = await ctx.send(f"📢 Canal configurado: <#{config['channel_id']}> (ID: {config['channel_id']})", delete_after=10)
            print(f"[INFO] Comando 'channel_id' ejecutado.")
        else:
            message = await ctx.send("⚠️ No hay canal configurado. Usa el comando !set_channel para configurarlo.", delete_after=10)
            print(f"[INFO] Comando 'channel_id' ejecutado sin canal configurado.")

    # Command for send Dashboard with all Values:
    @bot.command(name='values')
    @commands.has_permissions(administrator=True)
    async def values_command(ctx):
        try:
            await ctx.message.delete(delay=5)  
        except discord.Forbidden:
            await ctx.send("⚠️ No tengo permisos para eliminar mensajes del usuario.", delete_after=5)
            return
        
        data = load_local_data()
        embed = await format_message_all(data)
        message = await ctx.send(embed=embed, delete_after=20)  
        print(f"[INFO] Comando 'values' ejecutado.")

    # Command for set a Specific Dollar Value:
    @bot.command(name='value')
    @commands.has_permissions(administrator=True)
    async def value_command(ctx, dolar_nombre: str):
        try:
            await ctx.message.delete(delay=10) 
        except discord.Forbidden:
            await ctx.send("⚠️ No tengo permisos para eliminar mensajes del usuario.", delete_after=5)
            return
        
        data = load_local_data()
        values = data.get("values", [])
        for item in values:
            if item.get('nombre', '').lower() == dolar_nombre.lower():
                compra = item.get('compra', 'N/A')
                venta = item.get('venta', 'N/A')
                fecha = format_date_time(item.get('fechaActualizacion', datetime.now(timezone.utc).isoformat()))

                message = await ctx.send(f"🛒 Compra: {compra} \n 💵 Venta: {venta} \n 📅 Fecha: {fecha}", delete_after=10)
                print(f"[INFO] Comando 'value' ejecutado para {dolar_nombre}.")
                return
            
        message = await ctx.send(f"⚠️ No se encontró información para el dólar: {dolar_nombre}", delete_after=10)
        print(f"[INFO] Comando 'value' ejecutado sin resultados para {dolar_nombre}.")

    # Command for force start update Dashboard:
    @bot.command(name='start_update')
    @commands.has_permissions(administrator=True)
    async def start_update_command(ctx):
        try:
            await ctx.message.delete(delay=10)  
        except discord.Forbidden:
            await ctx.send("⚠️ No tengo permisos para eliminar mensajes del usuario.", delete_after=5)
            return
        try:
            await perform_dashboard_update(bot)
            await ctx.send("🔄 Tarea de actualización del dashboard ejecutada manualmente.", delete_after=10)
            print("[INFO] Tarea de actualización del dashboard ejecutada manualmente.")
        except Exception as e:
            await ctx.send("⚠️ Ocurrió un error al ejecutar la actualización del dashboard.", delete_after=10)
            print(f"[ERROR] Error al ejecutar la actualización manual: {e}")

    # Command for calculate Taxes:
    @bot.command(name='taxes')
    @commands.has_permissions(administrator=True)
    async def taxes(ctx, value: float):
        try:
            await ctx.message.delete(delay=10) 
        except discord.Forbidden:
            await ctx.send("⚠️ No tengo permisos para eliminar mensajes del usuario.", delete_after=5)
            return
        try:
            with open('values.json', 'r') as file:
                data = json.load(file)
                dollar_card = data.get("compra", 1115) 
        except (FileNotFoundError, json.JSONDecodeError):
            await ctx.send("⚠️ No se pudo cargar el archivo de configuración. Verifica que 'values.json' existe y está en el formato correcto.", delete_after=10)
            return

        service_cost = value * dollar_card
        cntry_tax = service_cost * 0.30  # 30% TAX CNTRY
        iva = service_cost * 0.21  # 21% IVA
        total_taxes = cntry_tax + iva
        total_pesos = service_cost + total_taxes
        await ctx.send(
            f"💸 **Desglose de la Transacción:**\n"
            f"🛒 **Costo del Servicio:** {service_cost:.2f} ARS\n"
            f"🧾 **Impuesto PAIS (30%):** {cntry_tax:.2f} ARS\n"
            f"🧾 **Percepción IVA (21%):** {iva:.2f} ARS\n"
            f"💰 **Total a Pagar:** {total_pesos:.2f} ARS",
            delete_after=15
        )
        print(f"[INFO] Comando 'taxes' ejecutado para el valor {value} USD.")

    # Command for List of Available Commands:
    @bot.command(name='commands_list') 
    @commands.has_permissions(administrator=True)
    async def commands_list(ctx):
        try:
            await ctx.message.delete(delay=10)  
        except discord.Forbidden:
            await ctx.send("⚠️ No tengo permisos para eliminar mensajes del usuario.", delete_after=5)
            return
        command_list = [
            "1. @dolar ping: Responde 'Pong' si Dolar está online.",
            "2. @dolar values: Envía la lista de todas las divisas.",
            "3. @dolar value <nombre_del_dolar>: Te da información sobre ese cambio.",
            "4. @dolar taxes <valor_en_usd>: Te da el valor de un artículo con impuestos en el país.",
            "5. @dolar set_channel: (Solo administradores) Configura el canal actual para las notificaciones.",
            "NOTA: El Bot elimina los mensajes automaticamente, para mantener el canal lo mas limpio Posible."
        ]
        await ctx.send("Comandos disponibles para el bot:\n" + "\n".join(command_list), delete_after=10)  
        print("[INFO] Comando 'commands_list' ejecutado.")

    # Command for 'Ping' Test.
    @bot.command(name='ping')
    async def ping(ctx):
        try:
            await ctx.message.delete(delay=10)  
        except discord.Forbidden:
            await ctx.send("⚠️ No tengo permisos para eliminar mensajes del usuario.", delete_after=5)
            return
        start_time = time.time()
        message = await ctx.send("Pong!")
        end_time = time.time()
        latency = round((end_time - start_time) * 1000)
        await message.edit(content=f"Pong! Latencia: {latency}ms")
        await message.delete(delay=5)  
        print(f"[INFO] Comando 'ping' ejecutado. Latencia: {latency}ms")

    # Error Commands Manager:
    @set_channel.error
    @channel_id_command.error
    @values_command.error
    @value_command.error
    @start_update_command.error
    @taxes.error
    @commands_list.error

    async def command_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("⚠️ No tienes permisos para usar este comando.", delete_after=10)
        else:
            await ctx.send("⚠️ Ocurrió un error al procesar el comando.", delete_after=10)
            print(f"[ERROR] {error}")