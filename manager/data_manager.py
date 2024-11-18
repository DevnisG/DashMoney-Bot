# Libs / Data Managers
import os
import json
from config.constants import DATA_FILE

# Func for Load Data:
def load_local_data():
    if not os.path.exists(DATA_FILE):
        print(f"[INFO] {DATA_FILE} no encontrado. Creando uno nuevo.")
        data = {"values": [], "state": {}}
        save_local_data(data)
        return data
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            data.setdefault("values", [])
            data.setdefault("state", {})
            print(f"[INFO] {DATA_FILE} cargado: {data}")
            return data
    except (json.JSONDecodeError, ValueError) as e:
        print(f"[ERROR] Error al decodificar {DATA_FILE}: {e}")
    except Exception as e:
        print(f"[ERROR] Error al cargar {DATA_FILE}: {e}")
    return {"values": [], "state": {}}

# Func for Save Data:
def save_local_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        print(f"[INFO] {DATA_FILE} guardado.")
    except Exception as e:
        print(f"[ERROR] Error al guardar {DATA_FILE}: {e}")