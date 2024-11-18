#Libs / Formatter
import discord
from datetime import datetime, timezone

# Func for Formatting Date & Time:
def format_date_time(date_str):
    try:
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return f"Fecha: {date_obj.strftime('%Y-%m-%d')} - Hora: {date_obj.strftime('%H:%M:%S')}"
    except ValueError as e:
        print(f"[ERROR] Error al formatear fecha: {e}")
    return "Fecha no disponible"

# Func for Formatting Data:
def format_message(data):
    values = data.get("values", [])
    state = data.get("state", {}).get("estado", "No disponible")
    embed = discord.Embed(title="📈 Dashboard de Cotizaciones del Dólar", color=0x00f999)
    embed.set_footer(text=f"Última actualización: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")

    if values:
        for item in values:
            nombre = item.get('nombre', 'Desconocido')
            if nombre.lower() in ['blue', 'oficial', 'tarjeta']:
                compra = item.get('compra', 'N/A')
                venta = item.get('venta', 'N/A')
                fecha = format_date_time(item.get('fechaActualizacion', datetime.now(timezone.utc).isoformat()))
                embed.add_field(name=nombre, value=f"🛒 Compra: {compra} | 💵  Venta: {venta}\n📅 {fecha}", inline=False)
    else:
        embed.add_field(name="Valores", value="No hay datos disponibles.", inline=False)

    embed.add_field(name="Estado de la API", value=state, inline=False)
    return embed

# Func for Formatting Data for All Values:
async def format_message_all(data):
    values = data.get("values", [])
    state = data.get("state", {}).get("estado", "No disponible")
    embed = discord.Embed(title="📈 Dashboard de Cotizaciones del Dólar", color=0x00f999)
    embed.set_footer(text=f"Última actualización: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")

    if values:
        for item in values:
            nombre = item.get('nombre', 'Desconocido')
            if nombre.lower() in ['blue', 'oficial', 'tarjeta','cripto','contadoconliqui','bolsa','mayorista']:
                compra = item.get('compra', 'N/A')
                venta = item.get('venta', 'N/A')
                fecha = format_date_time(item.get('fechaActualizacion', datetime.now(timezone.utc).isoformat()))
                embed.add_field(name=nombre, value=f"🛒 Compra: {compra} | 💵  Venta: {venta}\n📅 {fecha}", inline=False)
    else:
        embed.add_field(name="Valores", value="No hay datos disponibles.", inline=False)

    embed.add_field(name="Estado de la API", value=state, inline=False)
    return embed