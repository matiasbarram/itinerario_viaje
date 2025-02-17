import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import folium
from folium import plugins
from typing import List, Dict


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

def crear_mapa(itinerario: List[Dict], colores: Dict[str, str], conexiones: List[Dict]):
    """
    Crea un mapa con el itinerario especificado y lo retorna
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
    
    return mapa

def crear_presentacion():
    st.title("🌍 Planes de Viaje: Italia y Croacia")
    st.subheader("Abril-Mayo 2025")

    # Introducción
    st.write("""
    Exploraremos 4 diferentes planes para nuestro viaje de 18 días. 
    Cada plan tiene sus propias ventajas y enfoque único.
    """)

    # Selector de planes
    plan = st.selectbox(
        "Selecciona un plan para ver detalles:",
        ["Plan A: Italia + Croacia Completo", 
         "Plan B: Solo Italia", 
         "Plan C: Norte de Italia + Toscana",
         "Plan D: Norte de Italia + Croacia con regreso por Zagreb"]
    )

    def mostrar_tabla_alojamiento(itinerario: List[Dict]):
        """Muestra una tabla con los enlaces de alojamiento para 1 y 3 personas"""
        # Crear DataFrame con los datos de alojamiento
        data = []
        for item in itinerario:
            if item["categoria"] not in ["Regreso"]:
                url_1p = get_booking_links(item["lugar"], item["fecha"], 1)
                url_3p = get_booking_links(item["lugar"], item["fecha"], 3)
                data.append({
                    "Ciudad": item["lugar"],
                    "Fechas": item["fecha"],
                    "Booking (1 persona)": f"[Reservar]({url_1p})",
                    "Booking (3 personas)": f"[Reservar]({url_3p})"
                })
        
        df = pd.DataFrame(data)
        st.markdown("**🏨 Enlaces de Reserva por Ciudad:**")
        st.write(df.to_markdown(index=False), unsafe_allow_html=True)

    # Función para generar enlaces de Booking
    def get_booking_links(ciudad: str, fecha: str, personas: int) -> str:
        # Diccionario para convertir meses de español a inglés
        meses_es_en = {
            'Enero': 'January', 'Febrero': 'February', 'Marzo': 'March',
            'Abril': 'April', 'Mayo': 'May', 'Junio': 'June',
            'Julio': 'July', 'Agosto': 'August', 'Septiembre': 'September',
            'Octubre': 'October', 'Noviembre': 'November', 'Diciembre': 'December'
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
            "Milán": "Porta Nuova;-121726", # Área moderna y bien conectada
            "Trento": "Centro histórico;-130793",
            "Venecia": "San Marco;-129524", # Centro histórico
            "Roma": "Centro Storico;-126693", # Centro histórico
            "Florencia": "Duomo;-125977", # Centro histórico
            "Split": "Centro histórico;-127514",
            "Dubrovnik": "Old Town;-127241", # Ciudad amurallada
            "Zagreb": "Lower Town;-128739", # Centro
            "Rovinj": "Centro;-127466",
            "Siena": "Terzo di Camollia;-130368",
            "Verona": "Città Antica;-130437",
            "Como": "Como City Centre;-125932",
            "Nápoles": "Historical Center;-127198"
        }
        
        area_param = f"&ss={areas_recomendadas.get(ciudad, '')}" if ciudad in areas_recomendadas else f"&ss={ciudad}"
        
        base_url = f"https://www.booking.com/searchresults.es.html?selected_currency=EUR&checkin={checkin}&checkout={checkout}&group_adults={personas}&no_rooms=1&order=popularity"
        url = base_url + area_param
        
        return url

    # Mostrar detalles según el plan seleccionado
    if plan == "Plan A: Italia + Croacia Completo":
        st.markdown("""
        ### 🎯 Plan A: La ruta completa
        **Características principales:**
        - Norte de Italia (6 días)
        - Croacia (6 días)
        - Sur de Italia (6 días)
        
        **Ventajas:**
        - ✅ Cubre todos los destinos principales
        - ✅ Balance entre Italia y Croacia
        - ✅ Incluye Roma y la Costa Amalfitana
        
        **Desventajas:**
        - ⚠️ Ritmo más intenso
        - ⚠️ Más tiempo en traslados
        - ⚠️ Mayor costo en transportes
        """)
        
        # Crear y mostrar mapa del Plan A
        itinerario = crear_itinerario_plan_a()
        colores = get_colores_plan_a()
        conexiones = get_conexiones_plan_a()
        mapa = crear_mapa(itinerario, colores, conexiones)
        folium_static(mapa)
        
        # Sección de alojamiento recomendado
        st.subheader("🏨 Alojamiento Recomendado")
        mostrar_tabla_alojamiento(itinerario)  
      
        st.info("""
        💡 **Tips de alojamiento:**
        - En Venecia, el área de San Marco es más cara pero vale la pena por la experiencia
        - En Roma, el Centro Storico te permite caminar a todos los sitios principales
        - En Split y Dubrovnik, quedarse dentro del casco histórico mejora mucho la experiencia
        - En Milán, el área de Porta Nuova ofrece buena conexión y precios más moderados
        """)
        
        
    elif plan == "Plan B: Solo Italia":
        st.markdown("""
        ### 🎯 Plan B: Italia en profundidad
        **Características principales:**
        - Norte de Italia (6 días)
        - Roma (4 días)
        - Florencia y Toscana (4 días)
        - Costa Amalfitana (4 días)
        
        **Ventajas:**
        - ✅ Experiencia más profunda de Italia
        - ✅ Menos traslados largos
        - ✅ Más tiempo en cada ciudad
        
        **Desventajas:**
        - ⚠️ No conocer Croacia
        - ⚠️ Mayor costo en alojamiento
        """)
        
        # Crear y mostrar mapa del Plan B
        itinerario = crear_itinerario_plan_b()
        colores = get_colores_plan_b()
        conexiones = get_conexiones_plan_b()
        mapa = crear_mapa(itinerario, colores, conexiones)
        folium_static(mapa)

        # Sección de alojamiento recomendado
        st.subheader("🏨 Alojamiento Recomendado")
        mostrar_tabla_alojamiento(itinerario)
        
        st.info("""
        💡 **Tips de alojamiento Plan B:**
        - En Roma, elige el Centro Storico para estar cerca de todo
        - En Florencia, el área del Duomo es perfecta para turismo
        - En Nápoles, el Centro Histórico tiene el mejor ambiente
        - Para la Costa Amalfitana, Positano o Sorrento son excelentes bases
        """)

    elif plan == "Plan C: Norte de Italia + Toscana":
        st.markdown("""
        ### 🎯 Plan C: La Toscana y los Lagos
        **Características principales:**
        - Norte de Italia (7 días)
        - Región de Lagos (3 días)
        - Toscana (8 días)
        
        **Ventajas:**
        - ✅ Ritmo más relajado
        - ✅ Italia más auténtica
        - ✅ Pueblos pequeños
        - ✅ Mejor gastronomía local
        
        **Desventajas:**
        - ⚠️ No visitar Roma
        - ⚠️ No conocer Croacia
        """)
        
        # Crear y mostrar mapa del Plan C
        itinerario = crear_itinerario_plan_c()
        colores = get_colores_plan_c()
        conexiones = get_conexiones_plan_c()
        mapa = crear_mapa(itinerario, colores, conexiones)
        folium_static(mapa)

        # Sección de alojamiento recomendado
        st.subheader("🏨 Alojamiento Recomendado")
        mostrar_tabla_alojamiento(itinerario)
        
        st.info("""
        💡 **Tips de alojamiento Plan C:**
        - En Como, el centro histórico ofrece las mejores vistas al lago
        - En Siena, el Terzo di Camollia es tranquilo y auténtico
        - En San Gimignano, intenta alojarte dentro de las murallas
        - En Bellagio, busca hoteles con vista al lago
        """)

    else:  # Plan D

        st.markdown("""
        ### 🎯 Plan D: Norte de Italia + Croacia con regreso gradual
        **Características principales:**
        - Norte de Italia (7 días)
        - Croacia (8 días)
        - Regreso vía Zagreb (3 días)
        
        **Ventajas:**
        - ✅ Viaje en auto con amigos
        - ✅ Conocer Zagreb
        - ✅ Más tiempo en cada lugar
        - ✅ Ritmo más relajado en Croacia
        
        **Desventajas:**
        - ⚠️ No visitar Roma
        - ⚠️ No ver Costa Amalfitana
        """)
        
        # Crear y mostrar mapa del Plan D
        itinerario = crear_itinerario_plan_d()
        colores = get_colores_plan_d()
        conexiones = get_conexiones_plan_d()
        mapa = crear_mapa(itinerario, colores, conexiones)
        folium_static(mapa)

        # Sección de alojamiento recomendado
        st.subheader("🏨 Alojamiento Recomendado")
        mostrar_tabla_alojamiento(itinerario)
        
        st.info("""
        💡 **Tips de alojamiento Plan D:**
        - En Rovinj, busca alojamiento en el casco antiguo con vista al mar
        - En Split, el Palacio de Diocleciano es la mejor zona
        - En Zagreb, Lower Town ofrece mejor relación calidad-precio
        - En Plitvice, alójate cerca del Parque Nacional para entrar temprano
        """)


    # Recomendación final
    st.subheader("🌟 Recomendación Personal")
    st.write("""
    Basado en nuestras conversaciones, el Plan C o D serían los más recomendados porque:
    - Permiten un ritmo más relajado
    - Se ajustan mejor al presupuesto
    - Ofrecen una experiencia más auténtica
    - Tienen mejor logística de transporte
    """)

# Importar todas las funciones auxiliares del archivo original
from planes import (
    crear_itinerario_plan_a, get_colores_plan_a, get_conexiones_plan_a,
    crear_itinerario_plan_b, get_colores_plan_b, get_conexiones_plan_b,
    crear_itinerario_plan_c, get_colores_plan_c, get_conexiones_plan_c,
    crear_itinerario_plan_d, get_colores_plan_d, get_conexiones_plan_d
)

if __name__ == "__main__":
    crear_presentacion()