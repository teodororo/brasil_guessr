from geopy.distance import geodesic


def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distância em quilômetros entre dois pontos usando coordenadas.

    Args:
        lat1, lon1: Coordenadas do primeiro ponto
        lat2, lon2: Coordenadas do segundo ponto

    Returns:
        float: Distância em quilômetros
    """
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    return geodesic(point1, point2).kilometers


def calculate_location_score(distance_km: float) -> tuple[int, str]:
    """
    Calcula a pontuação baseada na distância do chute.

    Args:
        distance_km: Distância em quilômetros entre o chute e o local correto

    Returns:
        tuple: (pontos, mensagem_feedback)
    """
    # Pontuação máxima: 5000 pontos
    # Distância em km determina a pontuação

    if distance_km < 10:
        return 5000, "🎯 ACERTOU EM CHEIO! Incrível!"
    elif distance_km < 50:
        return 4000, "🎉 MUITO PERTO! Excelente chute!"
    elif distance_km < 100:
        return 3000, "👏 BEM PERTO! Bom trabalho!"
    elif distance_km < 300:
        return 2000, "👍 RAZOAVELMENTE PERTO! Não está mal!"
    elif distance_km < 600:
        return 1000, "😅 UM POUCO LONGE... Mas ainda vale!"
    elif distance_km < 1000:
        return 500, "😬 LONGE... Quase não deu!"
    else:
        return 100, "🌎 MUITO LONGE! Mas não desista!"


def calculate_year_score(year_guess: int, correct_year: int) -> tuple[int, str]:
    """
    Calcula a pontuação baseada na diferença de anos.

    Args:
        year_guess: Ano do chute do jogador
        correct_year: Ano correto da foto

    Returns:
        tuple: (pontos, mensagem_feedback)
    """
    # Pontuação máxima: 5000 pontos
    difference = abs(year_guess - correct_year)

    if difference == 0:
        return 5000, "📅 ANO EXATO! Perfeito!"
    elif difference <= 2:
        return 4000, "📅 MUITO PRÓXIMO! Ótimo!"
    elif difference <= 5:
        return 3000, "📅 BEM PRÓXIMO! Legal!"
    elif difference <= 10:
        return 2000, "📅 RELATIVAMENTE PERTO!"
    elif difference <= 20:
        return 1000, "📅 UM POUCO LONGE..."
    elif difference <= 30:
        return 500, "📅 BEM LONGE..."
    else:
        return 100, "📅 MUITO LONGE DO ANO!"


def get_distance_message(distance_km: float) -> str:
    """
    Retorna uma mensagem descritiva sobre a distância.

    Args:
        distance_km: Distância em quilômetros

    Returns:
        str: Mensagem descritiva
    """
    if distance_km < 1:
        return f"Você estava a apenas {int(distance_km * 1000)} metros!"
    else:
        return f"Você estava a {distance_km:.1f} km de distância."
