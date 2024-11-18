# Libs / Configs
import os
import json
from config.constants import CONFIG_FILE

# Func for Load Config from JSON Files:
def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"[INFO] {CONFIG_FILE} no encontrado. Creando uno nuevo.")
        config = {"channel_id": None, "message_id": None}
        save_config(config)
        return config
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = json.load(file)
            channel_id = config.get("channel_id")
            config["channel_id"] = int(channel_id) if channel_id else None
            message_id = config.get("message_id")
            config["message_id"] = int(message_id) if message_id else None
            print(f"[INFO] {CONFIG_FILE} cargado: {config}")
            return config
    except (json.JSONDecodeError, ValueError) as e:
        print(f"[ERROR] Error al decodificar {CONFIG_FILE}: {e}")
    except Exception as e:
        print(f"[ERROR] Error al cargar {CONFIG_FILE}: {e}")
    return {"channel_id": None, "message_id": None}

# Func for Save Config:
def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)
        print(f"[INFO] {CONFIG_FILE} guardado: {config}")
    except Exception as e:
        print(f"[ERROR] Error al guardar {CONFIG_FILE}: {e}")