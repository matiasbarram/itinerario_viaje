import folium
from folium import plugins
from typing import List, Dict

def crear_itinerario_plan_a():
    """Genera el itinerario del Plan A: Italia + Croacia"""
    return [
        {"lugar": "Milán", "lat": 45.6301, "lon": 8.7255, "fecha": "13 Abril", "dia": "13", "categoria": "Norte de Italia"},
        {"lugar": "Trento", "lat": 46.0748, "lon": 11.1217, "fecha": "14-15 Abril", "dia": "14-15", "categoria": "Norte de Italia"},
        {"lugar": "Sirmione", "lat": 45.5000, "lon": 10.6056, "fecha": "16 Abril", "dia": "16", "categoria": "Norte de Italia"},
        {"lugar": "Verona", "lat": 45.4384, "lon": 10.9916, "fecha": "17 Abril", "dia": "17", "categoria": "Norte de Italia"},
        {"lugar": "Venecia", "lat": 45.4408, "lon": 12.3155, "fecha": "18-19 Abril", "dia": "18-19", "categoria": "Norte de Italia"},
        {"lugar": "Provesano", "lat": 46.1947, "lon": 12.8801, "fecha": "20 Abril", "dia": "20", "categoria": "Norte de Italia"},
        {"lugar": "Rovinj", "lat": 45.0812, "lon": 13.6387, "fecha": "21 Abril", "dia": "21", "categoria": "Croacia"},
        {"lugar": "Lagos Plitvice", "lat": 44.8654, "lon": 15.5820, "fecha": "22 Abril", "dia": "22", "categoria": "Croacia"},
        {"lugar": "Split", "lat": 43.5081, "lon": 16.4402, "fecha": "23 Abril", "dia": "23", "categoria": "Croacia"},
        {"lugar": "Dubrovnik", "lat": 42.6507, "lon": 18.0944, "fecha": "24 Abril", "dia": "24", "categoria": "Croacia"},
        {"lugar": "Roma", "lat": 41.9028, "lon": 12.4964, "fecha": "25-27 Abril", "dia": "25-27", "categoria": "Sur de Italia"},
        {"lugar": "Nápoles", "lat": 40.8518, "lon": 14.2681, "fecha": "28-29 Abril", "dia": "28-29", "categoria": "Sur de Italia"},
        {"lugar": "Florencia", "lat": 43.7696, "lon": 11.2558, "fecha": "30 Abril", "dia": "30", "categoria": "Sur de Italia"},
        {"lugar": "Trento", "lat": 46.0748, "lon": 11.1217, "fecha": "1 Mayo", "dia": "1", "categoria": "Regreso"},
        {"lugar": "Milán (Aeropuerto)", "lat": 45.6301, "lon": 8.7255, "fecha": "2 Mayo", "dia": "2", "categoria": "Regreso"}
    ]

def crear_itinerario_plan_b():
    """Genera el itinerario del Plan B: Solo Italia"""
    return [
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
    

def get_conexiones_plan_a():
    """Obtiene las conexiones entre regiones para el Plan A"""
    return [
        {"inicio": "Provesano", "fin": "Rovinj", "tipo": "Auto/Bus", "color": "purple"},
        {"inicio": "Dubrovnik", "fin": "Roma", "tipo": "Avión", "color": "orange"},
        {"inicio": "Florencia", "fin": "Trento", "tipo": "Tren", "color": "brown"}
    ]

def get_conexiones_plan_b():
    """Obtiene las conexiones entre regiones para el Plan B"""
    return [
        {"inicio": "Provesano", "fin": "Roma", "tipo": "Tren", "color": "brown"},
        {"inicio": "Florencia", "fin": "Trento", "tipo": "Tren", "color": "brown"}
    ]

def get_colores_plan_a():
    """Obtiene los colores para las categorías del Plan A"""
    return {
        "Norte de Italia": "blue",
        "Croacia": "red",
        "Sur de Italia": "green",
        "Regreso": "black"
    }

def get_colores_plan_b():
    """Obtiene los colores para las categorías del Plan B"""
    return {
        "Norte de Italia": "blue",
        "Centro-Sur": "green",
        "Regreso": "black"
    }

def crear_leyenda(colores: Dict[str, str], conexiones: List[Dict]) -> str:
    """Crea el HTML para la leyenda del mapa"""
    leyenda_html = '''
     <div style="position: fixed; 
                bottom: 50px; 
                left: 50px; 
                width: 150px;
                z-index: 1000;
                background-color: white;
                padding: 10px;
                border: 2px solid grey;
                border-radius: 5px;
                font-size: 14px;">
        <p style="margin-bottom: 10px;"><strong>Regiones:</strong></p>
    '''
    
    # Agregar regiones
    for categoria, color in colores.items():
        leyenda_html += f'<p style="margin: 5px; color: {color};">⬤ {categoria}</p>'
    
    # Agregar conexiones
    leyenda_html += '<p style="margin-top: 10px;"><strong>Conexiones:</strong></p>'
    tipos_conexiones = set((conexion["tipo"], conexion["color"]) for conexion in conexiones)
    for tipo, color in tipos_conexiones:
        leyenda_html += f'<p style="margin: 5px; color: {color};">- - - {tipo}</p>'
    
    leyenda_html += '</div>'
    return leyenda_html

def crear_mapa(itinerario: List[Dict], colores: Dict[str, str], conexiones: List[Dict], nombre_archivo: str):
    """
    Crea un mapa con el itinerario especificado
    
    Args:
        itinerario: Lista de diccionarios con la información de cada lugar
        colores: Diccionario con los colores para cada categoría
        conexiones: Lista de diccionarios con las conexiones entre regiones
        nombre_archivo: Nombre del archivo HTML a generar
    """
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
    
    # Añadir leyenda
    leyenda_html = crear_leyenda(colores, conexiones)
    mapa.get_root().html.add_child(folium.Element(leyenda_html))
    
    # Añadir los grupos al mapa
    for grupo in grupos.values():
        grupo.add_to(mapa)
    
    # Añadir control de capas
    folium.LayerControl().add_to(mapa)
    
    # Guardar el mapa
    mapa.save(nombre_archivo)

# Ejemplo de uso
def crear_plan_a():
    """Crea el mapa para el Plan A"""
    itinerario = crear_itinerario_plan_a()
    colores = get_colores_plan_a()
    conexiones = get_conexiones_plan_a()
    crear_mapa(itinerario, colores, conexiones, "itinerario_plan_a.html")

def crear_plan_b():
    """Crea el mapa para el Plan B"""
    itinerario = crear_itinerario_plan_b()
    colores = get_colores_plan_b()
    conexiones = get_conexiones_plan_b()
    crear_mapa(itinerario, colores, conexiones, "itinerario_plan_b.html")

def crear_itinerario_plan_c():
    """Genera el itinerario del Plan C: Norte de Italia + Toscana"""
    return [
        {"lugar": "Milán", "lat": 45.6301, "lon": 8.7255, "fecha": "13 Abril", "dia": "13", "categoria": "Norte de Italia"},
        {"lugar": "Trento", "lat": 46.0748, "lon": 11.1217, "fecha": "14-15 Abril", "dia": "14-15", "categoria": "Norte de Italia"},
        {"lugar": "Sirmione", "lat": 45.5000, "lon": 10.6056, "fecha": "16 Abril", "dia": "16", "categoria": "Norte de Italia"},
        {"lugar": "Verona", "lat": 45.4384, "lon": 10.9916, "fecha": "17 Abril", "dia": "17", "categoria": "Norte de Italia"},
        {"lugar": "Venecia", "lat": 45.4408, "lon": 12.3155, "fecha": "18-19 Abril", "dia": "18-19", "categoria": "Norte de Italia"},
        {"lugar": "Provesano", "lat": 46.1947, "lon": 12.8801, "fecha": "20 Abril", "dia": "20", "categoria": "Norte de Italia"},
        {"lugar": "Como", "lat": 45.8081, "lon": 9.0852, "fecha": "21-22 Abril", "dia": "21-22", "categoria": "Lagos"},
        {"lugar": "Bellagio", "lat": 45.9864, "lon": 9.2618, "fecha": "23 Abril", "dia": "23", "categoria": "Lagos"},
        {"lugar": "Florencia", "lat": 43.7696, "lon": 11.2558, "fecha": "24-26 Abril", "dia": "24-26", "categoria": "Toscana"},
        {"lugar": "Siena", "lat": 43.3188, "lon": 11.3305, "fecha": "27-28 Abril", "dia": "27-28", "categoria": "Toscana"},
        {"lugar": "San Gimignano", "lat": 43.4684, "lon": 11.0409, "fecha": "29 Abril", "dia": "29", "categoria": "Toscana"},
        {"lugar": "Pisa", "lat": 43.7228, "lon": 10.4017, "fecha": "30 Abril", "dia": "30", "categoria": "Toscana"},
        {"lugar": "Trento", "lat": 46.0748, "lon": 11.1217, "fecha": "1 Mayo", "dia": "1", "categoria": "Regreso"},
        {"lugar": "Milán (Aeropuerto)", "lat": 45.6301, "lon": 8.7255, "fecha": "2 Mayo", "dia": "2", "categoria": "Regreso"}
    ]

def get_colores_plan_c():
    """Obtiene los colores para las categorías del Plan C"""
    return {
        "Norte de Italia": "blue",
        "Lagos": "purple",
        "Toscana": "green",
        "Regreso": "black"
    }

def get_conexiones_plan_c():
    """Obtiene las conexiones entre regiones para el Plan C"""
    return [
        {"inicio": "Provesano", "fin": "Como", "tipo": "Tren", "color": "brown"},
        {"inicio": "Bellagio", "fin": "Florencia", "tipo": "Tren", "color": "brown"},
        {"inicio": "Pisa", "fin": "Trento", "tipo": "Tren", "color": "brown"}
    ]

def crear_plan_c():
    """Crea el mapa para el Plan C"""
    itinerario = crear_itinerario_plan_c()
    colores = get_colores_plan_c()
    conexiones = get_conexiones_plan_c()
    crear_mapa(itinerario, colores, conexiones, "itinerario_plan_c.html")

def crear_itinerario_plan_d():
    """Genera el itinerario del Plan D: Norte de Italia + Croacia con regreso gradual"""
    return [
        {"lugar": "Milán", "lat": 45.6301, "lon": 8.7255, "fecha": "13 Abril", "dia": "13", "categoria": "Norte de Italia"},
        {"lugar": "Trento", "lat": 46.0748, "lon": 11.1217, "fecha": "14-15 Abril", "dia": "14-15", "categoria": "Norte de Italia"},
        {"lugar": "Sirmione", "lat": 45.5000, "lon": 10.6056, "fecha": "16 Abril", "dia": "16", "categoria": "Norte de Italia"},
        {"lugar": "Verona", "lat": 45.4384, "lon": 10.9916, "fecha": "17 Abril", "dia": "17", "categoria": "Norte de Italia"},
        {"lugar": "Venecia", "lat": 45.4408, "lon": 12.3155, "fecha": "18-19 Abril", "dia": "18-19", "categoria": "Norte de Italia"},
        {"lugar": "Provesano", "lat": 46.1947, "lon": 12.8801, "fecha": "20 Abril", "dia": "20", "categoria": "Norte de Italia"},
        {"lugar": "Trieste", "lat": 45.6495, "lon": 13.7768, "fecha": "21 Abril", "dia": "21", "categoria": "Norte de Italia"},
        {"lugar": "Rovinj", "lat": 45.0812, "lon": 13.6387, "fecha": "22-23 Abril", "dia": "22-23", "categoria": "Croacia"},
        {"lugar": "Lagos Plitvice", "lat": 44.8654, "lon": 15.5820, "fecha": "24-25 Abril", "dia": "24-25", "categoria": "Croacia"},
        {"lugar": "Split", "lat": 43.5081, "lon": 16.4402, "fecha": "26-27 Abril", "dia": "26-27", "categoria": "Croacia"},
        {"lugar": "Dubrovnik", "lat": 42.6507, "lon": 18.0944, "fecha": "28-29 Abril", "dia": "28-29", "categoria": "Croacia"},
        {"lugar": "Zagreb", "lat": 45.8150, "lon": 15.9819, "fecha": "30 Abril", "dia": "30", "categoria": "Regreso"},
        {"lugar": "Trento", "lat": 46.0748, "lon": 11.1217, "fecha": "1 Mayo", "dia": "1", "categoria": "Regreso"},
        {"lugar": "Milán (Aeropuerto)", "lat": 45.6301, "lon": 8.7255, "fecha": "2 Mayo", "dia": "2", "categoria": "Regreso"}
    ]

def get_conexiones_plan_d():
    """Obtiene las conexiones entre regiones para el Plan D"""
    return [
        {"inicio": "Provesano", "fin": "Trieste", "tipo": "Auto", "color": "purple"},
        {"inicio": "Dubrovnik", "fin": "Zagreb", "tipo": "Auto", "color": "purple"},
        {"inicio": "Zagreb", "fin": "Trento", "tipo": "Auto", "color": "purple"}
    ]

def get_colores_plan_d():
    """Obtiene los colores para las categorías del Plan D"""
    return {
        "Norte de Italia": "blue",
        "Croacia": "red",
        "Regreso": "black"
    }


def crear_plan_d():
    """Crea el mapa para el Plan C"""
    itinerario = crear_itinerario_plan_d()
    colores = get_colores_plan_d()
    conexiones = get_conexiones_plan_d()
    crear_mapa(itinerario, colores, conexiones, "itinerario_plan_d.html")


def crear_itinerario_plan_e():
    """Genera el itinerario del Plan E: Norte de Italia + Lagos + Roma"""
    return [
        {"lugar": "Milán", "lat": 45.6301, "lon": 8.7255, "fecha": "13 Abril", "dia": "13", "categoria": "Norte de Italia"},
        {"lugar": "Trento", "lat": 46.0748, "lon": 11.1217, "fecha": "14-15 Abril", "dia": "14-15", "categoria": "Norte de Italia"},
        {"lugar": "Sirmione", "lat": 45.5000, "lon": 10.6056, "fecha": "16 Abril", "dia": "16", "categoria": "Norte de Italia"},
        {"lugar": "Verona", "lat": 45.4384, "lon": 10.9916, "fecha": "17 Abril", "dia": "17", "categoria": "Norte de Italia"},
        {"lugar": "Venecia", "lat": 45.4408, "lon": 12.3155, "fecha": "18-19 Abril", "dia": "18-19", "categoria": "Norte de Italia"},
        {"lugar": "Provesano", "lat": 46.1947, "lon": 12.8801, "fecha": "20 Abril", "dia": "20", "categoria": "Norte de Italia"},
        {"lugar": "Como", "lat": 45.8081, "lon": 9.0852, "fecha": "21-22 Abril", "dia": "21-22", "categoria": "Lagos"},
        {"lugar": "Bellagio", "lat": 45.9864, "lon": 9.2618, "fecha": "23 Abril", "dia": "23", "categoria": "Lagos"},
        {"lugar": "Roma", "lat": 41.9028, "lon": 12.4964, "fecha": "24-28 Abril", "dia": "24-28", "categoria": "Roma"},
        {"lugar": "Orvieto", "lat": 42.7185, "lon": 12.1111, "fecha": "29 Abril", "dia": "29", "categoria": "Roma"},
        {"lugar": "Ostia Antica", "lat": 41.7556, "lon": 12.2883, "fecha": "30 Abril", "dia": "30", "categoria": "Roma"},
        {"lugar": "Trento", "lat": 46.0748, "lon": 11.1217, "fecha": "1 Mayo", "dia": "1", "categoria": "Regreso"},
        {"lugar": "Milán (Aeropuerto)", "lat": 45.6301, "lon": 8.7255, "fecha": "2 Mayo", "dia": "2", "categoria": "Regreso"}
    ]

def get_colores_plan_e():
    """Obtiene los colores para las categorías del Plan E"""
    return {
        "Norte de Italia": "blue",
        "Lagos": "purple",
        "Roma": "red",
        "Regreso": "black"
    }

def get_conexiones_plan_e():
    """Obtiene las conexiones entre regiones para el Plan E"""
    return [
        {"inicio": "Provesano", "fin": "Como", "tipo": "Tren", "color": "brown"},
        {"inicio": "Bellagio", "fin": "Roma", "tipo": "Tren", "color": "brown"},
        {"inicio": "Ostia Antica", "fin": "Trento", "tipo": "Tren", "color": "brown"}
    ]

def crear_plan_e():
    """Crea el mapa para el Plan E"""
    itinerario = crear_itinerario_plan_e()
    colores = get_colores_plan_e()
    conexiones = get_conexiones_plan_e()
    crear_mapa(itinerario, colores, conexiones, "itinerario_plan_e.html")

# Para crear los mapas:
crear_plan_a()
crear_plan_b()
crear_plan_c()
crear_plan_d()
crear_plan_e()