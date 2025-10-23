import requests
import pandas as pd
import time

def scrape_toctoc():
    url = "https://www.toctoc.com/api/mapa/GetProps"
    
    # Headers EXACTOS desde tu navegador (actualizados) / SE CAMBIA COOKIE, REFERER, X-ACCES-TOKEN
    headers = {
        "authority": "www.toctoc.com",
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.5",
        "content-type": "application/json",
        "cookie": "D67DD356796A31797828FBD03642BABF6|1ee50ec241c299f1413e18c6ae09163a",  # COOKIE SE CAMBIA
        "origin": "https://www.toctoc.com",
        "referer": "https://www.toctoc.com/resultados/mapa/compra/casa/?moneda=2&precioDesde=0&precioHasta=0&dormitoriosDesde=&dormitoriosHasta=&banosDesde=0&banosHasta=0&estado=0&disponibilidadEntrega=&numeroDeDiasTocToc=0&superficieDesdeUtil=0&superficieHastaUtil=0&superficieDesdeConstruida=0&superficieHastaConstruida=0&superficieDesdeTerraza=0&superficieHastaTerraza=0&superficieDesdeTerreno=0&superficieHastaTerreno=0&ordenarPor=0&pagina=1&paginaInterna=1&zoom=11.960719324099083&idZonaHomogenea=0&atributos=&texto=Vitacura,%20Santiago&viewport=-33.42715410566527,-70.64753120229197,-33.31976392125945,-70.51717200069167&idPoligono=19&publicador=0&temporalidad=0",  # ESTE SE CAMBIA A LA NUEVA BUSQUEDA Y PARAMETROS
        "sec-ch-ua": '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "x-access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjE4MS40My4xNDguMjUwIiwiaWF0IjoxNzU5OTM2NzUyLCJleHAiOjE3NjA1NDE1NTJ9.ykXekAFNnmlxoFsfTQiJjDEY8dq_xDmyob6Cg_wSxi8"  # ACTUALIZAR TOKEN 
    }

        # PAYLOAD COMPLETO Y CORRECTO
    payload_template = {
        "region": "metropolitana",
        "comuna": "",
        "barrio": "",
        "poi": "",
        "tipoVista": "mapa",
        "operacion": 1, # 2 es arriendo, 1 compra
        "atributos": [],
        "banosDesde": 0,
        "banosHasta": 0,
        "busqueda": "Las Condes, Santiago", # CAMBIAR NOMBRE
        "disponibilidadEntrega": "",
        "dormitoriosDesde": 0,
        "dormitoriosHasta": 0,
        "estado": 0,
        "idPoligono": 17, # POLIGONO COMUNA 17 las condes, 57 puente alto, 32 la reina, 19 vitacura, 18 lo barnechea
        "idZonaHomogenea": 0,
        "limite": 1500,
        "moneda": 2,
        "numeroDeDiasTocToc": 0,
        "ordenarPor": 0,
        "pagina": 1,
        "paginaInterna": 1,
        "precioDesde": 0,
        "precioHasta": 0,
        "publicador": 0,
        "santander": False,
        "superficieDesdeConstruida": 0,
        "superficieDesdeTerraza": 0,
        "superficieDesdeTerreno": 0,
        "superficieDesdeUtil": 0,
        "superficieHastaConstruida": 0,
        "superficieHastaTerraza": 0,
        "superficieHastaTerreno": 0,
        "superficieHastaUtil": 0,
        "temporalidad": 0,
        "tipoPropiedad": "terreno", #DEPARTAMENTO, CASA, terreno
        "viewport": "-33.7,-70.8,-33.3,-70.4",
        "zoom": 10
    }

    session = requests.Session()
    all_propiedades = []
    pagina = 1

    while True:
        print(f"Obteniendo página {pagina}...")
        payload = payload_template.copy()  # <--- ESTA LÍNEA DEBE USAR payload_template DEFINIDO ARRIBA
        payload["pagina"] = pagina
        
        response = session.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            print(f"Error en página {pagina}: {response.status_code}")
            break
        
        data = response.json()
        propiedades = data["resultados"]["Propiedades"]
        
        if not propiedades:
            print("No hay más propiedades.")
            break
        
        all_propiedades.extend(propiedades)
        print(f"Propiedades obtenidas: {len(propiedades)} (Total: {len(all_propiedades)})")
        
        total_resultados = data["resultados"].get("totalResultados", 0)
        if len(all_propiedades) >= total_resultados and total_resultados > 0:
            print("Se alcanzó el total de propiedades.")
            break
        
        pagina += 1
        time.sleep(2)
    
    if all_propiedades:
        df = pd.DataFrame(all_propiedades)
        df.to_csv("propiedades_compraLCterreno.csv", index=False)
        print(f"✅ ¡Éxito! {len(df)} propiedades guardadas.")
    else:
        print("⚠️ No se encontraron propiedades.")

# Ejecutar
scrape_toctoc()