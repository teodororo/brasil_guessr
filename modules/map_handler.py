import folium
from streamlit_folium import st_folium


def create_brazil_map(center_lat: float = -14.235, center_lon: float = -51.9253,
                      zoom: int = 4):
    """
    Cria um mapa do Brasil usando Folium.

    Args:
        center_lat: Latitude central do mapa (padrão: centro do Brasil)
        center_lon: Longitude central do mapa (padrão: centro do Brasil)
        zoom: Nível de zoom inicial

    Returns:
        folium.Map: Mapa criado
    """
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles='OpenStreetMap'
    )
    return m


def display_interactive_map(m: folium.Map, key: str = "map"):
    """
    Exibe um mapa interativo no Streamlit e captura cliques.

    Args:
        m: Mapa Folium a ser exibido
        key: Chave única para o componente Streamlit

    Returns:
        dict: Dados do mapa incluindo último clique
    """
    map_data = st_folium(
        m,
        width=700,
        height=500,
        key=key
    )
    return map_data


def add_marker_to_map(m: folium.Map, lat: float, lon: float,
                      popup_text: str = "Local", color: str = "red",
                      icon: str = "info-sign"):
    """
    Adiciona um marcador ao mapa.

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


def create_result_map(guess_lat: float, guess_lon: float,
                      correct_lat: float, correct_lon: float):
    """
    Cria um mapa mostrando o chute do jogador e o local correto.

    Args:
        guess_lat, guess_lon: Coordenadas do chute
        correct_lat, correct_lon: Coordenadas corretas

    Returns:
        folium.Map: Mapa com ambos os marcadores
    """
    # Calcular o centro entre os dois pontos
    center_lat = (guess_lat + correct_lat) / 2
    center_lon = (guess_lon + correct_lon) / 2

    m = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    # Marcador do chute (azul)
    add_marker_to_map(m, guess_lat, guess_lon,
                      "Seu chute", "blue", "hand-point-up")

    # Marcador correto (verde)
    add_marker_to_map(m, correct_lat, correct_lon,
                      "Local correto", "green", "star")

    # Linha conectando os dois pontos
    folium.PolyLine(
        locations=[[guess_lat, guess_lon], [correct_lat, correct_lon]],
        color='red',
        weight=2,
        opacity=0.8
    ).add_to(m)

    return m
