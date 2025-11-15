"""
Módulo ranking: Gerencia o sistema de rankings dos jogadores
"""

import json
import os
from typing import List

from classes.player import Player

RANKING_FILE = 'data/rankings.json'


def load_rankings() -> List[Player]:
    """
    Carrega os rankings do arquivo JSON.

    Returns:
        List[Player]: Lista de jogadores ordenada por pontuação
    """
    if not os.path.exists(RANKING_FILE):
        return []

    try:
        with open(RANKING_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            players = [Player.from_dict(p) for p in data]
            return sorted(players, key=lambda x: x.total_score, reverse=True)
    except Exception as e:
        print(f"Erro ao carregar rankings: {e}")
        return []


def save_rankings(players: List[Player]):
    """
    Salva os rankings no arquivo JSON.

    Args:
        players: Lista de jogadores a serem salvos
    """
    # Criar diretório se não existir
    os.makedirs('data', exist_ok=True)

    try:
        with open(RANKING_FILE, 'w', encoding='utf-8') as f:
            data = [p.to_dict() for p in players]
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar rankings: {e}")


def add_player_score(player_name: str, score: int):
    """
    Adiciona ou atualiza a pontuação de um jogador no ranking.

    Args:
        player_name: Nome do jogador
        score: Pontuação do jogo atual
    """
    players = load_rankings()

    # Procurar jogador existente
    existing_player = None
    for player in players:
        if player.name.lower() == player_name.lower():
            existing_player = player
            break

    if existing_player:
        # Atualizar jogador existente
        existing_player.add_game_score(score)
    else:
        # Criar novo jogador
        new_player = Player(name=player_name)
        new_player.add_game_score(score)
        players.append(new_player)

    # Salvar rankings atualizados
    save_rankings(players)


def get_top_players(limit: int = 10) -> List[Player]:
    """
    Retorna os top N jogadores.

    Args:
        limit: Número máximo de jogadores a retornar

    Returns:
        List[Player]: Top jogadores ordenados por pontuação
    """
    players = load_rankings()
    return players[:limit]


def get_player_rank(player_name: str) -> int:
    """
    Retorna a posição de um jogador no ranking.

    Args:
        player_name: Nome do jogador

    Returns:
        int: Posição no ranking (1-indexed), ou 0 se não encontrado
    """
    players = load_rankings()

    for i, player in enumerate(players, 1):
        if player.name.lower() == player_name.lower():
            return i

    return 0
