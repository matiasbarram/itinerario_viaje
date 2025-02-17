import folium
from folium import plugins

# Datos del itinerario actualizado
itinerario = [
    {"lugar": "Milán", "lat": 45.6301, "lon": 8.7255, "fecha": "13 Abril", "dia": "13", "categoria": "Norte de Italia"},
    {"lugar": "Trento", "lat": 46.0748, "lon": 11.1217, "fecha": "14-15 Abril", "dia": "14-15", "categoria": "Norte de Italia"},
    {"lugar": "Sirmione", "lat": 45.5000, "lon": 10.6056, "fecha": "16 Abril", "dia": "16", "categoria": "Norte de Italia"},
    {"lugar": "Verona", "lat": 45.4384, "lon": 10.9916, "fecha": "17 Abril", "dia": "17", "categoria": "Norte de Italia"},
    {"lugar": "Venecia", "lat": 45.4408, "lon": 12.3155, "fecha": "18-19 Abril", "dia": "18-19", "categoria": "Norte de Italia"},
    {"lugar": "Provesano", "lat": 46.1947, "lon": 12.8801, "fecha": "20 Abril", "dia": "20", "categoria": "Norte de Italia"},
    {"lugar": "Roma", "lat": 41.9028, "lon": 12.4964, "fecha": "21-24 Abril", "dia": "21-24", "categoria": "Centro-Sur"},
    {"lugar": "Nápoles", "lat": 40.8518, "lon": 14.2681, "fecha": "25-27 Abril", "dia": "25-27", "categoria": "Centro-Sur"},
    {"lugar": "Costa Amalfitana", "lat": 40.6333, "lon": 14.6029, "fecha": "28 Abril", "dia": "28", "categoria": "Centro-Sur"},
    {"lugar": "Florencia", "lat": 43.7696, "lon": 11.2558, "fecha": "29-30 Abril", "dia": "29-30", "categoria": "Centro-Sur"},
    {"lugar": "Trento", "lat": 46.0748, "lon": 11.1217, "fecha": "1 Mayo", "dia": "1", "categoria": "Regreso"},
    {"lugar": "Milán (Aeropuerto)", "lat": 45.6301, "lon": 8.7255, "fecha": "2 Mayo", "dia": "2", "categoria": "Regreso"}
]

# Colores para las diferentes categorías
colores = {
    "Norte de Italia": "blue",
    "Centro-Sur": "green",
    "Regreso": "black"
}

# Conexiones entre regiones
conexiones = [
    {
        "inicio": "Provesano",
        "fin": "Roma",
        "tipo": "Tren",
        "color": "brown"
    },
    {
        "inicio": "Florencia",
        "fin": "Trento",
        "tipo": "Tren",
        "color": "brown"
    }
]
# Crear el mapa centrado en Italia
mapa = folium.Map(location=[44.4968, 12.5568], zoom_start=6)

# Crear feature groups para cada categoría
grupos = {categoria: folium.FeatureGroup(name=categoria) for categoria in colores.keys()}

# Añadir marcadores y conectar puntos por categoría
for categoria in colores.keys():
    puntos = [(item["lat"], item["lon"]) for item in itinerario if item["categoria"] == categoria]
    
    # Añadir marcadores
    for item in [i for i in itinerario if i["categoria"] == categoria]:
        icono = folium.DivIcon(
            html=f'<div style="background-color: {colores[categoria]}; color: white; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 11px;">{item["dia"]}</div>'
        )
        
        folium.Marker(
            [item["lat"], item["lon"]],
            popup=f"<b>{item['lugar']}</b><br>{item['fecha']}",
            icon=icono
        ).add_to(grupos[categoria])
    
    # Conectar puntos de la misma categoría
    if len(puntos) > 1:
        folium.PolyLine(
            puntos,
            weight=2,
            color=colores[categoria],
            opacity=0.8
        ).add_to(grupos[categoria])

# Añadir conexiones entre regiones
for conexion in conexiones:
    inicio = next(item for item in itinerario if item["lugar"] == conexion["inicio"])
    fin = next(item for item in itinerario if item["lugar"] == conexion["fin"])
    
    folium.PolyLine(
        [(inicio["lat"], inicio["lon"]), (fin["lat"], fin["lon"])],
        weight=2,
        color=conexion["color"],
        opacity=0.8,
        dash_array="5",
        popup=f"{conexion['tipo']}"
    ).add_to(mapa)

# Añadir los grupos al mapa
# Añadir leyenda
leyenda_html = '''
     <div style="position: fixed; 
                bottom: 50px; 
                left: 50px; 
                width: 150px;
                height: 360;
                z-index: 1000;
                background-color: white;
                padding: 10px;
                border: 2px solid grey;
                border-radius: 5px;
                font-size: 14px;">
        <p style="margin-bottom: 10px;"><strong>Regiones:</strong></p>
        <p style="margin: 5px; color: blue;">⬤ Norte de Italia</p>
        <p style="margin: 5px; color: red;">⬤ Croacia</p>
        <p style="margin: 5px; color: green;">⬤ Sur de Italia</p>
        <p style="margin: 5px; color: black;">⬤ Regreso</p>
        <p style="margin-top: 10px;"><strong>Conexiones:</strong></p>
        <p style="margin: 5px; color: purple;">- - - Auto/Bus</p>
        <p style="margin: 5px; color: orange;">- - - Avión</p>
        <p style="margin: 5px; color: brown;">- - - Tren</p>
     </div>
     '''
mapa.get_root().html.add_child(folium.Element(leyenda_html))

# Añadir los grupos al mapa
for grupo in grupos.values():
    grupo.add_to(mapa)

# Añadir control de capas
folium.LayerControl().add_to(mapa)

# Guardar el mapa
mapa.save("itinerario_viaje_conexiones.html")