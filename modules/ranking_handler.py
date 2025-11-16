import json
import os
from pathlib import Path
from typing import List, Optional

from classes.player import Player

RANKING_FILE = 'data/rankings.json'


def ensure_data_directory() -> None:
    """Garante que o diretório de dados existe"""
    Path('data').mkdir(parents=True, exist_ok=True)


def load_rankings() -> List[Player]:
    """
    Carrega os rankings do arquivo JSON

    Returns:
        List[Player]: Lista de jogadores ordenada por pontuação (decrescente)
    """
    if not os.path.exists(RANKING_FILE):
        return []

    try:
        with open(RANKING_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            players = [Player.from_dict(p) for p in data]
            return sorted(players, key=lambda x: x.total_score, reverse=True)
    except json.JSONDecodeError:
        print(f"Erro: Arquivo {RANKING_FILE} contém JSON inválido")
        return []
    except Exception as e:
        print(f"Erro ao carregar rankings: {e}")
        return []


def save_rankings(players: List[Player]) -> bool:
    """
    Salva os rankings no arquivo JSON

    Args:
        players: Lista de jogadores a serem salvos

    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    ensure_data_directory()

    try:
        with open(RANKING_FILE, 'w', encoding='utf-8') as f:
            data = [p.to_dict() for p in players]
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar rankings: {e}")
        return False


def find_player_by_name(players: List[Player], player_name: str) -> Optional[Player]:
    """
    Busca um jogador na lista pelo nome (case-insensitive)

    Args:
        players: Lista de jogadores
        player_name: Nome a buscar

    Returns:
        Player ou None se não encontrado
    """
    normalized_name = player_name.lower().strip()
    for player in players:
        if player.name.lower().strip() == normalized_name:
            return player
    return None


def add_player_score(player_name: str, score: int) -> bool:
    """
    Adiciona ou atualiza a pontuação de um jogador no ranking

    Args:
        player_name: Nome do jogador
        score: Pontuação do jogo atual

    Returns:
        bool: True se a operação foi bem-sucedida
    """
    if not player_name or not player_name.strip():
        return False

    players = load_rankings()
    existing_player = find_player_by_name(players, player_name)

    if existing_player:
        # Atualizar jogador existente
        existing_player.add_game_score(score)
    else:
        # Criar novo jogador
        new_player = Player(name=player_name.strip())
        new_player.add_game_score(score)
        players.append(new_player)

    # Salvar rankings atualizados
    return save_rankings(players)


def get_top_players(limit: int = 10) -> List[Player]:
    """
    Retorna os top N jogadores

    Args:
        limit: Número máximo de jogadores a retornar

    Returns:
        List[Player]: Top jogadores ordenados por pontuação
    """
    players = load_rankings()
    return players[:limit]


def get_player_rank(player_name: str) -> int:
    """
    Retorna a posição de um jogador no ranking

    Args:
        player_name: Nome do jogador

    Returns:
        int: Posição no ranking (1-indexed), ou 0 se não encontrado
    """
    if not player_name or not player_name.strip():
        return 0

    players = load_rankings()
    normalized_name = player_name.lower().strip()

    for i, player in enumerate(players, 1):
        if player.name.lower().strip() == normalized_name:
            return i

    return 0


def get_player_stats(player_name: str) -> Optional[Player]:
    """
    Retorna as estatísticas completas de um jogador

    Args:
        player_name: Nome do jogador

    Returns:
        Player ou None se não encontrado
    """
    if not player_name or not player_name.strip():
        return None

    players = load_rankings()
    return find_player_by_name(players, player_name)


def clear_rankings() -> bool:
    """
    Limpa todos os rankings (para testes)

    Returns:
        bool: True se limpou com sucesso
    """
    try:
        if os.path.exists(RANKING_FILE):
            os.remove(RANKING_FILE)
        return True
    except Exception as e:
        print(f"Erro ao limpar rankings: {e}")
        return False
