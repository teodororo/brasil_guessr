class Player:
    """
    Representa um jogador do Brasil Guessr.

    Attributes:
        name (str): Nome do jogador
        total_score (int): Pontuação total acumulada
        games_played (int): Número de jogos jogados
    """

    def __init__(self, name: str, total_score: int = 0, games_played: int = 0):
        self.name = name
        self.total_score = total_score
        self.games_played = games_played

    @property
    def average_score(self) -> float:
        """Calcula a pontuação média do jogador"""
        if self.games_played == 0:
            return 0
        return self.total_score / self.games_played

    @classmethod
    def from_dict(cls, data: dict):
        """Cria uma instância de Player a partir de um dicionário"""
        return cls(
            name=data['name'],
            total_score=data.get('total_score', 0),
            games_played=data.get('games_played', 0)
        )

    def to_dict(self) -> dict:
        """Converte o jogador para dicionário"""
        return {
            'name': self.name,
            'total_score': self.total_score,
            'games_played': self.games_played
        }

    def add_game_score(self, score: int):
        """Adiciona pontuação de um novo jogo"""
        self.total_score += score
        self.games_played += 1
