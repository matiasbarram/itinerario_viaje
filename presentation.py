import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import folium
from folium import plugins
from typing import List, Dict

def crear_itinerario():
    """Genera el itinerario final"""
    return [
        # Base en Trento
        {"lugar": "Milán", "lat": 45.6301, "lon": 8.7255, "fecha": "13 Abril", "dia": "13", "categoria": "Llegada"},
        {"lugar": "Trento", "lat": 46.0748, "lon": 11.1217, "fecha": "13-18 Abril", "dia": "13-18", "categoria": "Base Trento", "nota": "Alojamiento con amiga"},
        
        # Provesano y Venecia
        {"lugar": "Provesano", "lat": 46.1947, "lon": 12.8801, "fecha": "19-20 Abril", "dia": "19-20", "categoria": "Provesano"},
        {"lugar": "Venecia", "lat": 45.4408, "lon": 12.3155, "fecha": "19 Abril", "dia": "19", "categoria": "Excursión"},
        
        # Vuelta a Trento
        {"lugar": "Trento", "lat": 46.0748, "lon": 11.1217, "fecha": "21 Abril", "dia": "21", "categoria": "Base Trento"},
        
        # Roma
        {"lugar": "Roma", "lat": 41.9028, "lon": 12.4964, "fecha": "22-25 Abril", "dia": "22-25", "categoria": "Roma"},
        
        # Ruta Roma-Trento (opciones a definir)
        {"lugar": "Orvieto", "lat": 42.7185, "lon": 12.1111, "fecha": "26 Abril", "dia": "26", "categoria": "Por definir", "nota": "Opción sugerida"},
        {"lugar": "Siena", "lat": 43.3188, "lon": 11.3305, "fecha": "27 Abril", "dia": "27", "categoria": "Por definir", "nota": "Opción sugerida"},
        {"lugar": "Florencia", "lat": 43.7696, "lon": 11.2558, "fecha": "28 Abril", "dia": "28", "categoria": "Por definir", "nota": "Opción sugerida"},
        {"lugar": "Bologna", "lat": 44.4949, "lon": 11.3426, "fecha": "29 Abril", "dia": "29", "categoria": "Por definir", "nota": "Opción sugerida"},
        {"lugar": "Trento", "lat": 46.0748, "lon": 11.1217, "fecha": "30 Abril", "dia": "30", "categoria": "Base Trento", "nota": "Alojamiento con amiga"},
        
        # Final en Milán
        {"lugar": "Milán", "lat": 45.6301, "lon": 8.7255, "fecha": "1-2 Mayo", "dia": "1-2", "categoria": "Final"}
    ]

def get_colores():
    """Obtiene los colores para las categorías"""
    return {
        "Llegada": "#1e40af",      # azul oscuro
        "Base Trento": "#2563eb",  # azul
        "Provesano": "#7c3aed",    # violeta
        "Excursión": "#059669",    # verde esmeralda
        "Roma": "#dc2626",         # rojo
        "Por definir": "#9ca3af",  # gris claro (para rutas tentativas)
        "Final": "#475569"         # gris
    }

def get_conexiones():
    """Obtiene las conexiones entre regiones"""
    return [
        {"inicio": "Milán", "fin": "Trento", "tipo": "Tren", "color": "#94a3b8"},
        {"inicio": "Trento", "fin": "Provesano", "tipo": "Auto", "color": "#94a3b8"},
        {"inicio": "Provesano", "fin": "Venecia", "tipo": "Tren", "color": "#94a3b8"},
        {"inicio": "Trento", "fin": "Roma", "tipo": "Tren", "color": "#94a3b8"},
        {"inicio": "Roma", "fin": "Orvieto", "tipo": "Auto", "color": "#94a3b8"}
    ]

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
        <p style="margin-bottom: 10px;"><strong>Etapas:</strong></p>
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

def crear_mapa(itinerario: List[Dict], colores: Dict[str, str], conexiones: List[Dict]):
    """Crea un mapa con el itinerario especificado y lo retorna"""
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
    
    return mapa

def crear_presentacion():
    st.title("🌍 Itinerario Final: Italia 2025")
    st.subheader("13 Abril - 2 Mayo 2025")

    # Introducción
    st.write("""
    Itinerario definitivo para el viaje de 20 días por Italia, con bases principales en Trento y Roma.
    """)

    def mostrar_tabla_alojamiento(itinerario: List[Dict]):
        """Muestra una tabla con los enlaces de alojamiento para 1 y 3 personas"""
        # Crear DataFrame con los datos de alojamiento
        data = []
        for item in itinerario:
            # Excluir excursiones de un día, Trento, Provesano y opciones por definir
            if (item["categoria"] not in ["Excursión", "Base Trento", "Por definir", "Provesano"]):
                url_1p = get_booking_links(item["lugar"], item["fecha"], 1)
                url_3p = get_booking_links(item["lugar"], item["fecha"], 3)
                data.append({
                    "Ciudad": item["lugar"],
                    "Fechas": item["fecha"],
                    "Booking (1 persona)": f"[Reservar]({url_1p})",
                    "Booking (3 personas)": f"[Reservar]({url_3p})",
                    "Notas": item.get("nota", "")})
        
        df = pd.DataFrame(data)
        st.markdown("**🏨 Enlaces de Reserva por Ciudad:**")
        st.write(df.to_markdown(index=False), unsafe_allow_html=True)

    # Función para generar enlaces de Booking
    def get_booking_links(ciudad: str, fecha: str, personas: int) -> str:
        # Diccionario para convertir meses de español a inglés
        meses_es_en = {
            'Abril': 'April',
            'Mayo': 'May'
        }
        
        # Convertir la fecha a formato inglés
        for mes_es, mes_en in meses_es_en.items():
            fecha = fecha.replace(mes_es, mes_en)
        
        # Si la fecha tiene un rango (e.g., "14-15 April"), tomar solo el primer número
        dia = fecha.split()[0].split('-')[0]
        mes = fecha.split()[1]
        
        # Convertir fecha a formato booking (checkpoint-in)
        fecha_obj = pd.to_datetime(f"2025 {dia} {mes}", format="%Y %d %B")
        fecha_checkout = fecha_obj + pd.Timedelta(days=1)
        
        checkin = fecha_obj.strftime("%Y-%m-%d")
        checkout = fecha_checkout.strftime("%Y-%m-%d")
        
        # Diccionario de áreas recomendadas por ciudad
        areas_recomendadas = {
            "Milán": "Porta Nuova;-121726",
            "Trento": "Centro histórico;-130793",
            "Venecia": "San Marco;-129524",
            "Roma": "Centro Storico;-126693",
            "Florencia": "Duomo;-125977",
            "Bologna": "Centro;-126699",
            "Verona": "Città Antica;-130437",
            "Siena": "Terzo di Camollia;-130368",
            "Orvieto": "Centro Storico;-130129"
        }
        
        area_param = f"&ss={areas_recomendadas.get(ciudad, '')}" if ciudad in areas_recomendadas else f"&ss={ciudad}"
        
        base_url = f"https://www.booking.com/searchresults.es.html?selected_currency=EUR&checkin={checkin}&checkout={checkout}&group_adults={personas}&no_rooms=1&order=popularity"
        url = base_url + area_param
        
        return url

    # Crear y mostrar mapa
    itinerario = crear_itinerario()
    colores = get_colores()
    conexiones = get_conexiones()
    mapa = crear_mapa(itinerario, colores, conexiones)
    folium_static(mapa)
    
    # Notas y consideraciones
    st.subheader("📝 Notas Importantes")
    st.markdown("""
    **Sobre el alojamiento:**
    * En Trento nos quedamos con Lozana
    * Solo necesitamos reservar:
        - Roma (22-25 Abril)
        - Ciudades del recorrido de regreso (por definir)
        - Milán (última noche)

    **Sobre los traslados:**
    * Milán -> Trento: Auto con Nicola y Lozana
    * Trento es base de operaciones para la primera parte
    * Casa padres de Nicola -> Venecia: Se puede hacer en el día
    * Roma -> Norte: Ruta por definir, pero el 30 debemos estar en Trento

    **Puntos a definir:**
    * Excursiones desde Trento (13-18 Abril)
    * Ruta de regreso Roma -> Trento (26-29 Abril)
        - Opción Arte: más ciudad y cultura
        - Opción Costa: más naturaleza y mar
    * Tiempo en Milán al final (1-2 Mayo)

    **Recordatorios:**
    * El 30 de Abril hay que estar en Trento
    * Las fechas 26-29 son flexibles según la ruta que elijamos
    * Es importante reservar Roma con tiempo
    """)

    # Sección de alojamiento recomendado
    st.subheader("🏨 Alojamiento Recomendado")
    mostrar_tabla_alojamiento(itinerario)
    
    st.info("""
    💡 **Tips de alojamiento:**
    - En Trento, el centro histórico es la mejor opción para la base principal
    - En Provesano, buscar opciones de agroturismo o B&B locales
    - En Roma, el Centro Storico te permite caminar a todos los sitios principales
    - Para las ciudades de la ruta de retorno, priorizar ubicaciones céntricas
    """)

if __name__ == "__main__":
    crear_presentacion()