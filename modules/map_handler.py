from typing import Optional, Tuple

import folium
from streamlit_folium import st_folium

# Constantes
BRAZIL_CENTER_LAT = -14.235
BRAZIL_CENTER_LON = -51.9253
DEFAULT_ZOOM = 4
RESULT_MAP_ZOOM = 5
MAP_WIDTH = 500
MAP_HEIGHT = 300


def create_brazil_map(
    center_lat: float = BRAZIL_CENTER_LAT,
    center_lon: float = BRAZIL_CENTER_LON,
    zoom: int = DEFAULT_ZOOM
) -> folium.Map:
    """
    Cria um mapa do Brasil usando Folium

    Args:
        center_lat: Latitude central do mapa (padrão: centro do Brasil)
        center_lon: Longitude central do mapa (padrão: centro do Brasil)
        zoom: Nível de zoom inicial

    Returns:
        folium.Map: Mapa criado
    """
    return folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles='OpenStreetMap'  # existem outras alternativas de mapa
    )


def display_interactive_map(
    m: folium.Map,
    key: str = "map",
    width: int = MAP_WIDTH,
    height: int = MAP_HEIGHT
) -> Optional[dict]:
    """
    Exibe um mapa interativo no Streamlit e captura cliques

    Args:
        m: Mapa Folium a ser exibido
        key: Chave única para o componente Streamlit
        width: Largura do mapa em pixels
        height: Altura do mapa em pixels

    Returns:
        dict: Dados do mapa incluindo último clique, ou None se não houver dados
    """
    try:
        map_data = st_folium(
            m,
            width=width,
            height=height,
            key=key,
            returned_objects=["last_clicked"]  # APENAS clique, sem zoom/center
        )
        return map_data
    except Exception as e:
        print(f"Erro ao exibir mapa: {e}")
        return None


def add_marker_to_map(
    m: folium.Map,
    lat: float,
    lon: float,
    popup_text: str = "Local",
    color: str = "red",
    icon: str = "info-sign"
) -> None:
    """
    Adiciona um marcador ao mapa

    Args:
        m: Mapa Folium
        lat: Latitude do marcador
        lon: Longitude do marcador
        popup_text: Texto do popup
        color: Cor do marcador
        icon: Ícone do marcador
    """
    folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        icon=folium.Icon(color=color, icon=icon)
    ).add_to(m)


def add_line_between_points(
    m: folium.Map,
    point1: Tuple[float, float],
    point2: Tuple[float, float],
    color: str = 'red',
    weight: int = 2,
    opacity: float = 0.8
) -> None:
    """
    Adiciona uma linha conectando dois pontos no mapa

    Args:
        m: Mapa Folium
        point1: Tupla (lat, lon) do primeiro ponto
        point2: Tupla (lat, lon) do segundo ponto
        color: Cor da linha
        weight: Espessura da linha
        opacity: Opacidade da linha
    """
    folium.PolyLine(
        locations=[point1, point2],
        color=color,
        weight=weight,
        opacity=opacity
    ).add_to(m)


def calculate_map_center(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> Tuple[float, float]:
    """
    Calcula o ponto central entre duas coordenadas

    Args:
        lat1, lon1: Primeira coordenada
        lat2, lon2: Segunda coordenada

    Returns:
        Tupla com (latitude_central, longitude_central)
    """
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2
    return center_lat, center_lon


def create_result_map(
    guess_lat: float,
    guess_lon: float,
    correct_lat: float,
    correct_lon: float,
    zoom: int = RESULT_MAP_ZOOM
) -> folium.Map:
    """
    Cria um mapa mostrando o chute do jogador e o local correto

    Args:
        guess_lat, guess_lon: Coordenadas do chute
        correct_lat, correct_lon: Coordenadas corretas
        zoom: Nível de zoom do mapa (para melhorar a visualização)

    Returns:
        folium.Map: Mapa com ambos os marcadores e uma linha conectando-os
    """
    # Calcular o centro entre os dois pontos
    center_lat, center_lon = calculate_map_center(
        guess_lat, guess_lon, correct_lat, correct_lon
    )

    # Mapa centralizado
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)

    # Marcador do chute (azul)
    add_marker_to_map(
        m, guess_lat, guess_lon,
        "Seu chute", "blue", "hand-point-up"
    )

    # Marcador correto (verde)
    add_marker_to_map(
        m, correct_lat, correct_lon,
        "Local correto", "green", "star"
    )

    # Linha conectando os dois pontos
    add_line_between_points(
        m,
        (guess_lat, guess_lon),
        (correct_lat, correct_lon)
    )

    return m
