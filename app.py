import json

import streamlit as st

from classes.photo import Photo
from modules import game_handler, map_handler, ranking_handler

# Configuração da página
st.set_page_config(
    page_title="Brasil Guessr 🇧🇷",
    page_icon="🇧🇷",
    layout="wide"
)


def load_photos():
    """Carrega as fotos do arquivo JSON"""
    try:
        with open('data/photos.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Photo.from_dict(p) for p in data]
    except Exception as e:
        st.error(f"Erro ao carregar fotos: {e}")
        return []


def initialize_session_state():
    """Inicializa variáveis de sessão"""
    if 'current_photo_index' not in st.session_state:
        st.session_state.current_photo_index = 0

    if 'total_score' not in st.session_state:
        st.session_state.total_score = 0

    if 'guess_made' not in st.session_state:
        st.session_state.guess_made = False

    if 'guess_coords' not in st.session_state:
        st.session_state.guess_coords = None

    if 'guess_year' not in st.session_state:
        st.session_state.guess_year = None

    if 'game_finished' not in st.session_state:
        st.session_state.game_finished = False

    if 'photos' not in st.session_state:
        st.session_state.photos = load_photos()


def reset_game():
    """Reinicia o jogo"""
    st.session_state.current_photo_index = 0
    st.session_state.total_score = 0
    st.session_state.guess_made = False
    st.session_state.guess_coords = None
    st.session_state.guess_year = None
    st.session_state.game_finished = False


def show_photo_screen(photo: Photo):
    """Tela de exibição da foto e captura de chute"""

    # Exibir foto
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"**Rodada:** {st.session_state.current_photo_index + 1}/{len(st.session_state.photos)} | **Pontuação:** {st.session_state.total_score}")

        if st.session_state.guess_made:
            st.header(f":red[{photo.description}] :blue[{photo.year}.]")

        # Tirando as bordas arredondadas para combinar com o mapa
        st.markdown(
            """
            <style>
            img {
                border-radius: 0 !important;
            }
            </style>
            """,
            unsafe_allow_html=True)
        st.image(photo.url)
        st.caption(f"© {photo.photographer}")

    with col2:
        if not st.session_state.guess_made:
            st.markdown("Em que **ano** você acha que a foto foi tirada?")
            year_guess = st.number_input(
                "Em que **ano** você acha que a foto foi tirada?",
                min_value=1900,
                max_value=2025,
                value=2020,
                step=1,
                key=f"year_input_{photo.id}",
                label_visibility='collapsed'
            )
            st.markdown("Em que **local** você acha que a foto foi tirada?")
            st.warning("⚠️ Apenas UM clique é permitido!")

            # Criar e exibir mapa
            m = map_handler.create_brazil_map()
            map_data = map_handler.display_interactive_map(
                m, key=f"map_{photo.id}")

            # Capturar clique no mapa
            if map_data and map_data.get('last_clicked'):
                clicked_lat = map_data['last_clicked']['lat']
                clicked_lon = map_data['last_clicked']['lng']

                if st.button("Enviar chute", type="primary", key=f"confirm_{photo.id}"):
                    st.session_state.guess_coords = (clicked_lat, clicked_lon)
                    st.session_state.guess_year = year_guess
                    st.session_state.guess_made = True
                    st.rerun()

        else:
            # Mostrar resultado
            show_result(photo)


def show_result(photo: Photo):
    """Mostra o resultado do chute"""

    guess_lat, guess_lon = st.session_state.guess_coords
    guess_year = st.session_state.guess_year

    # Calcular distância
    distance = game_handler.calculate_distance_km(
        guess_lat, guess_lon, photo.latitude, photo.longitude
    )

    # Calcular pontuações
    location_score, location_msg = game_handler.calculate_location_score(
        distance)
    year_score, year_msg = game_handler.calculate_year_score(
        guess_year, photo.year)
    total_round_score = location_score + year_score

    # Atualizar pontuação total
    st.session_state.total_score += total_round_score

    # Exibir resultados
    st.subheader("🎯 RESULTADO")

    # Informações da foto
    st.info(f"**{photo.description}**")

    # Resultado de localização
    st.write("---")
    st.write("**LOCALIZAÇÃO:**")
    st.write(location_msg)
    st.write(game_handler.get_distance_message(distance))
    st.write(f"🎯 Pontos de localização: **{location_score}**")

    # Resultado de ano
    st.write("---")
    st.write("**ANO:**")
    st.write(year_msg)
    year_diff = abs(guess_year - photo.year)
    st.write(
        f"Você chutou: {guess_year} | Correto: {photo.year} | Diferença: {year_diff} anos")
    st.write(f"📅 Pontos de ano: **{year_score}**")

    # Total da rodada
    st.write("---")
    st.success(f"✨ **TOTAL DA RODADA: {total_round_score} pontos**")
    st.info(
        f"💯 **PONTUAÇÃO ACUMULADA: {st.session_state.total_score} pontos**")

    # Mapa com resultado
    result_map = map_handler.create_result_map(
        guess_lat, guess_lon, photo.latitude, photo.longitude
    )
    st.write("Seu chute e o local correto:")
    map_handler.display_interactive_map(
        result_map, key=f"result_map_{photo.id}")

    # Botão para próxima foto
    if st.session_state.current_photo_index < len(st.session_state.photos) - 1:
        if st.button("Próxima foto", type="primary", key=f"next_{photo.id}"):
            st.session_state.current_photo_index += 1
            st.session_state.guess_made = False
            st.session_state.guess_coords = None
            st.session_state.guess_year = None
            st.rerun()
    else:
        if st.button("Ver resultado final", type="primary", key=f"finish_{photo.id}"):
            st.session_state.game_finished = True
            st.rerun()


def show_final_screen():
    """Tela final com pontuação total e opção de entrar no ranking"""

    st.balloons()

    st.header(f"🏆 Sua pontuação final: {st.session_state.total_score} pontos")

    # Calcular média por foto
    avg_per_photo = st.session_state.total_score / len(st.session_state.photos)
    st.write(f"📊 Média por foto: {avg_per_photo:.0f} pontos")

    st.write("---")

    # Opção de entrar no ranking
    st.subheader("🏅 Quer entrar no ranking?")

    col1, col2 = st.columns(2)

    with col1:
        player_name = st.text_input(
            "Digite seu nome:",
            placeholder="Seu nome aqui",
            key="player_name_input"
        )

        if st.button("✅ ENTRAR NO RANKING", type="primary"):
            if player_name and player_name.strip():
                ranking_handler.add_player_score(
                    player_name.strip(), st.session_state.total_score)
                st.success(f"🎊 {player_name} adicionado ao ranking!")
                player_rank = ranking_handler.get_player_rank(
                    player_name.strip())
                if player_rank > 0:
                    st.info(f"🏆 Sua posição: #{player_rank}")
            else:
                st.error("❌ Por favor, digite um nome válido!")

    with col2:
        if st.button("🔄 JOGAR NOVAMENTE"):
            reset_game()
            st.rerun()

    # Mostrar ranking
    st.write("---")
    st.subheader("🏆 TOP 10 RANKING")

    top_players = ranking_handler.get_top_players(10)

    if top_players:
        for i, player in enumerate(top_players, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            st.write(
                f"{medal} **{player.name}** - {player.total_score} pontos ({player.games_played} jogos)")
    else:
        st.info("Nenhum jogador no ranking ainda. Seja o primeiro!")


def main():
    """Função principal da aplicação"""

    initialize_session_state()

    # Título principal
    st.title("🇧🇷 Brasil Guessr")

    # Verificar se há fotos
    if not st.session_state.photos:
        st.error("Nenhuma foto encontrada.")
        return

    # Lógica do jogo
    if not st.session_state.game_finished:
        current_photo = st.session_state.photos[st.session_state.current_photo_index]
        show_photo_screen(current_photo)
    else:
        show_final_screen()


if __name__ == "__main__":
    main()
