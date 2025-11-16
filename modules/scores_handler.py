from typing import Tuple

# cálculo da distância a partir das coordenadas
from geopy.distance import geodesic

# Constantes de pontuação e limiares (thresholds)
# (<qtde_de_pontos>, <threshold>, <mensagem ao usuário>)
SCORE_DISTANCE_THRESHOLDS = [
    (10, 5000, "🎯 Acertou em cheio! Parabéns!"),
    (50, 4000, "🎉 Muito perto! Excelente!"),
    (100, 3000, "👏 Bem perto! Bom trabalho!"),
    (300, 2000, "👍 Razoavelmente perto!"),
    (600, 1000, "😅 Um pouco longe..."),
    (1000, 500, "😬 Bem longe..."),
    (float('inf'), 100, "😔 Muito longe...")
]  # os limiares estao em km

SCORE_YEAR_THRESHOLDS = [
    (0, 5000, "🎯 Ano exato! Perfeito!"),
    (2, 4000, "🎉 Muito próximo! Ótimo!"),
    (5, 3000, "👏 Bem próximo! Legal!"),
    (10, 2000, "👍 Razoavelmente perto!"),
    (20, 1000, "😅 Um pouco longe..."),
    (30, 500, "😬 Bem longe..."),
    (float('inf'), 100, "😔 Muito longe...")
]


def calculate_distance_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """
    Calcula a distância em km entre dois pontos usando coordenadas

    Args:
        lat1, lon1: Coordenadas do primeiro ponto
        lat2, lon2: Coordenadas do segundo ponto

    Returns:
        float: Distância em km
    """
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    return geodesic(point1, point2).kilometers


def calculate_location_score(distance_km: float) -> Tuple[int, str]:
    """
    Calcula a pontuação baseada na distância do chute

    Args:
        distance_km: Distância em quilômetros entre o chute e o local correto

    Returns:
        tuple: (pontos, mensagem_feedback)
    """
    for threshold, score, message in SCORE_DISTANCE_THRESHOLDS:
        if distance_km <= threshold:
            return score, message

    # Fallback em caso de erro
    return 100, "😔 Muito longe..."


def calculate_year_score(year_guess: int, correct_year: int) -> Tuple[int, str]:
    """
    Calcula a pontuação baseada na diferença de anos

    Args:
        year_guess: Ano do chute do jogador
        correct_year: Ano correto da foto

    Returns:
        tuple: (pontos, mensagem_feedback)
    """
    difference = abs(year_guess - correct_year)

    for threshold, score, message in SCORE_YEAR_THRESHOLDS:
        if difference <= threshold:
            return score, message

    # Fallback em caso de erro
    return 100, "😔 Muito longe..."


def calculate_total_score(
    guess_lat: float,
    guess_lon: float,
    correct_lat: float,
    correct_lon: float,
    guess_year: int,
    correct_year: int
) -> Tuple[int, int, int, float]:
    """
    Calcula todas as pontuações de uma rodada

    Args:
        guess_lat, guess_lon: Coordenadas do chute
        correct_lat, correct_lon: Coordenadas corretas
        guess_year: Ano chutado
        correct_year: Ano correto

    Returns:
        tuple: (location_score, year_score, total_score, distance_km)
    """
    distance_km = calculate_distance_km(
        guess_lat, guess_lon, correct_lat, correct_lon)
    location_score, _ = calculate_location_score(distance_km)
    year_score, _ = calculate_year_score(guess_year, correct_year)
    total_score = location_score + year_score

    return location_score, year_score, total_score, distance_km
