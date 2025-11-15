# Brasil Guessr 🇧🇷

Jogo de adivinhação de localização e ano de fotos brasileiras baseado no [TimeGuessr](https://timeguessr.com/) e [GeoGuessr](https://www.geoguessr.com/).

Todas as imagens utilizadas são de domínio público ou sob a licença CC BY-NC-SA 2.0.



## Instalação

**1. Crie um ambiente virtual**
```bash
python -m venv brasil_guessr
```

**2. Ative o ambiente virtual**

- Windows
```bash
brasil_guessr\Scripts\activate
```

- Linux/MacOS
```bash
source brasil_guessr/bin/activate
```
**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

## Execução

```bash
streamlit run app.py
```

## Como contribuir com novas fotos

Submeta um PR editando o arquivo `data/photos.json` seguindo o formato:

```json
{
  "id": 1,
  "url": "URL_DA_FOTO",
  "photographer": "Nome do Fotógrafo(a)",
  "latitude": -3.1190,
  "longitude": -60.0217,
  "year": 2019,
  "description": "Teatro Amazonas em Manaus",
  "source": "Wikimedia Commons"
}
```