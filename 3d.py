import geopandas as gpd
import pydeck as pdk
import numpy as np

# Leer tu capa
grilla = gpd.read_file("C:/Repos/Scrape Toc Toc Propiedades/grilla_con_datos.shp")
grilla = grilla.to_crs("EPSG:4326")
grilla = grilla.dropna(subset=['UF/M2_mean'])

# Función para colores basada en rangos específicos
def get_color(value):
    if value <= 16:
        return [255, 245, 240, 220]  # #fff5f0
    elif value <= 43:
        return [252, 190, 165, 220]  # #fcbea5
    elif value <= 68:
        return [251, 112, 80, 220]   # #fb7050
    elif value <= 126:
        return [211, 32, 32, 220]    # #d32020
    else:  # > 126
        return [103, 0, 13, 220]     # #67000d

min_uf = grilla['UF/M2_mean'].min()
max_uf = grilla['UF/M2_mean'].max()

# ALTURA PROPORCIONAL con raíz cuadrada
percentil_95 = grilla['UF/M2_mean'].quantile(0.95)
grilla['altura_sqrt'] = np.sqrt(grilla['UF/M2_mean'] / percentil_95) * 100

print(f"Rango de valores: {min_uf:.2f} - {max_uf:.2f} UF/M²")

data = []
for idx, row in grilla.iterrows():
    coords = list(row.geometry.exterior.coords)
    polygon = [[c[0], c[1]] for c in coords[:-1]]
    
    uf_value = row['UF/M2_mean']
    color = get_color(uf_value)
    
    data.append({
        'polygon': polygon,
        'elevation': row['altura_sqrt'],  # ALTURA PROPORCIONAL
        'uf_m2': round(uf_value, 2),
        'color': color
    })

layer = pdk.Layer(
    'PolygonLayer',
    data,
    get_polygon='polygon',
    get_elevation='elevation',
    get_fill_color='color',
    pickable=True,
    extruded=True,
    wireframe=False,
    elevation_scale=8  # Ajusta si quieres más/menos altura
)

center_lat = grilla.geometry.centroid.y.mean()
center_lon = grilla.geometry.centroid.x.mean()

view_state = pdk.ViewState(
    latitude=center_lat,
    longitude=center_lon,
    zoom=11.5,
    pitch=50,
    bearing=-10
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={'html': '<b>UF/M²:</b> {uf_m2}', 'style': {'color': 'white'}},
    map_style='https://basemaps.cartocdn.com/gl/positron-gl-style/style.json'
)

r.to_html('C:/Jupyter/Scrape Toc Toc Propiedades/mapa_3d.html')
print("✓ Mapa con colores por rangos y altura proporcional")