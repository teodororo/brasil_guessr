class Photo:
    """
    Attributes:
        id (int): ID único da foto
        url (str): URL da imagem
        photographer (str): Nome do fotógrafo
        latitude (float): Latitude onde a foto foi tirada
        longitude (float): Longitude onde a foto foi tirada
        year (int): Ano em que a foto foi tirada
        description (str): Descrição breve da foto
    """

    def __init__(self, id: int, url: str, photographer: str,
                 latitude: float, longitude: float, year: int,
                 description: str):
        self.id = id
        self.url = url
        self.photographer = photographer
        self.latitude = latitude
        self.longitude = longitude
        self.year = year
        self.description = description

    @classmethod
    def from_dict(cls, data: dict):
        """Cria uma instância de Photo a partir de um dicionário"""
        return cls(
            id=data['id'],
            url=data['url'],
            photographer=data['photographer'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            year=data['year'],
            description=data['description'],
        )
