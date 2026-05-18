import requests
import json

# --- CONFIGURACIÓN ---
# API Key proporcionada por el usuario
API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImJhNDcxZDA1N2Y0MDQ1M2VhODRmNzdlYWQ2YjY2YTQzIiwiaCI6Im11cm11cjY0In0=" 
URL_BASE = "https://api.openrouteservice.org/geocode/search"
URL_RUTA = "https://api.openrouteservice.org/v2/directions/driving-car"

def obtener_coordenadas(ciudad):
    """Obtiene latitud y longitud de una ciudad usando la API de Geocoding."""
    params = {"api_key": API_KEY, "text": ciudad, "size": 1}
    try:
        r = requests.get(URL_BASE, params=params, timeout=10)
        if r.status_code == 200:
            datos = r.json()
            if 'features' in datos and len(datos['features']) > 0:
                coords = datos['features'][0]['geometry']['coordinates']
                return coords  # Retorna [longitud, latitud]
        return None
    except Exception:
        return None

def calcular_ruta():
    print("\n" + "="*60)
    print("SISTEMA DE NAVEGACIÓN: VICENTE COMIGUAL")
    print("="*60)
    
    while True:
        try:
            # Requerimiento: Solicitar Ciudad Origen y Ciudad Destino
            origen = input("\nIngrese Ciudad de Origen (o 'q' para salir): ").strip()
            if origen.lower() == 'q': 
                print("Saliendo del programa de navegación...")
                break
            
            destino = input("Ingrese Ciudad de Destino (o 'q' para salir): ").strip()
            if destino.lower() == 'q': 
                print("Saliendo del programa de navegación...")
                break

            if not origen or not destino:
                print("[!] Error: Los campos no pueden estar vacíos.")
                continue

            # 1. Obtener coordenadas
            print(f"[*] Consultando coordenadas para la ruta {origen} -> {destino}...")
            coord_org = obtener_coordenadas(origen)
            coord_des = obtener_coordenadas(destino)

            if coord_org and coord_des:
                # 2. Consultar la ruta mediante API Directions
                headers = {
                    'Authorization': API_KEY,
                    'Content-Type': 'application/json'
                }
                body = {"coordinates": [coord_org, coord_des]}
                res = requests.post(URL_RUTA, json=body, headers=headers, timeout=15)
                
                if res.status_code == 200:
                    data = res.json()
                    
                    # Requerimiento: Obtener distancia en km y duración
                    distancia_km = data['routes'][0]['summary']['distance'] / 1000
                    duracion_seg = data['routes'][0]['summary']['duration']
                    
                    # Requerimiento: Conversión a horas, minutos y segundos
                    horas = int(duracion_seg // 3600)
                    minutos = int((duracion_seg % 3600) // 60)
                    segundos = int(duracion_seg % 60)
                    
                    # Requerimiento: Cálculo de combustible (Consumo promedio 12km/L)
                    consumo_litros = distancia_km / 12

                    # --- SALIDA DE DATOS Y NARRATIVA ---
                    print("\n" + "·" * 60)
                    print(f"NARRATIVA DEL VIAJE")
                    print(f"Usted iniciará su viaje desde la ciudad de {origen.title()}, ")
                    print(f"atravesando la ruta principal para llegar finalmente a {destino.title()}.")
                    print(f"Este trayecto requiere una planificación logística cuidadosa debido a ")
                    print(f"la distancia y el tiempo estimado de conducción.")
                    print("-" * 60)
                    
                    # Requerimiento: Mostrar valores con dos decimales
                    print(f"DISTANCIA TOTAL: {distancia_km:.2f} Kilómetros")
                    print(f"TIEMPO ESTIMADO: {horas:02d} Horas, {minutos:02d} Minutos y {segundos:02d} Segundos")
                    print(f"COMBUSTIBLE ESTIMADO: {consumo_litros:.2f} Litros (Basado en 12 km/L)")
                    print("·" * 60)
                else:
                    print(f"[!] Error de API ({res.status_code}): No se pudo calcular el trayecto.")
            else:
                print("[!] No se encontraron coordenadas válidas para las ciudades ingresadas.")
        
        except EOFError:
            print("\n[!] Error de entrada. Ejecute el script en la Terminal de VS Code.")
            break
        except Exception as e:
            print(f"[!] Ocurrió un error inesperado: {e}")
            break

if __name__ == "__main__":
    calcular_ruta()