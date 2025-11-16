# Brasil Guessr 🇧🇷

Jogo de adivinhação de localização e ano de fotos brasileiras baseado no [TimeGuessr](https://timeguessr.com/) e [GeoGuessr](https://www.geoguessr.com/).

Todas as imagens utilizadas são de domínio público ou sob a licença CC BY-NC-SA 2.0.

## Jogue online em: [Brasil Guessr](https://brasilguessr.streamlit.app/)!

Aplicação hospedada gratuitamente no Streamlit Community. Acesse também via seção [Explore](https://share.streamlit.io/).

## Instalação

**1. Crie um ambiente virtual**
```bash
python -m venv venv
```

**2. Ative o ambiente virtual**

- Windows
```bash
venv\Scripts\activate
```

- Linux/MacOS
```bash
source venv/bin/activate
```
**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

## Execução

```bash
streamlit run app.py
```
## Aspectos tecnológicos do projeto

### Pontos positivos

- Interface 100% Python, sem necessidade de códigos .html ou .css.
- Possibilidade de acessar o website pelo celular.
- Possibilidade de hospedar o website gratuitamente no Streamlit Community ou GitHub Pages.
- As imagens não estão dentro do repositório, permitindo que ele escale sem gerar custos de armazenamento.
- Todas as imagens são de domínio público ou têm uma licença permissiva para uso não comercial.

### Pontos negativos

- Para renderizar o marcador do chute no mapa, a interface inteira é recarregada e isso é muito ruim para a experiência do usuário. Nem sempre o marcador do último chute é mostrado no mapa e dar muitos zooms trava tudo. O TimeGuessr permite o usuário poder mudar a posição do chute, mas o folium não é adequado para isso.
- Os rankings somem se o website for desativado por inatividade, o apropriado seria enviar os rankings via requests (API) para algum banco de dados.
- Como as imagens não foram baixadas (é feito um link ao website onde elas estão hospedadas), elas podem ficar indisponíveis se o host delas ficar indisponível.
- Como as imagens não foram baixadas, o usuário pode clicar com o botão direito, abri-las no website onde elas estão hospedadas e descobrir a resposta.

## Como contribuir com novas fotos

Submeta um PR editando o arquivo `data/photos.json` seguindo o formato:

```json
{
  "id": 1,
  "url": "url_da_foto",
  "photographer": "nome do fotógrafo(a)",
  "latitude": -3.1190,
  "longitude": -60.0217,
  "year": 2019,
  "description": "COP30 em Belém, Pará."
}
```
