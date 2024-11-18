# Async Func for Get Data from API:
async def fetch_api_data(response, url):
    try:
        if response.status == 200:
            print(f"[SUCCESS] Datos obtenidos correctamente de {url}.")
            return await response.json()
        print(f"[ERROR] No se pudo obtener los datos de {url}. Código de error: {response.status}")
    except Exception as e:
        print(f"[ERROR] Excepción al obtener datos de {url}: {e}")
    return None