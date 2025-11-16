import json
from typing import List, Optional, Tuple

import streamlit as st

from classes.photo import Photo
from modules import map_handler, ranking_handler, scores_handler

# Constantes
PHOTOS_FILE = 'data/photos.json'
MIN_YEAR = 1800
MAX_YEAR = 2025
DEFAULT_YEAR = 2020


def load_photos() -> List[Photo]:
    """Carrega as fotos do arquivo JSON"""
    try:
        with open(PHOTOS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Photo.from_dict(p) for p in data]
    except FileNotFoundError:
        st.error(f"Arquivo {PHOTOS_FILE} não encontrado.")
        return []
    except json.JSONDecodeError:
        st.error(f"Erro ao decodificar JSON do arquivo {PHOTOS_FILE}")
        return []
    except Exception as e:
        st.error(f"Erro ao carregar fotos: {e}")
        return []


def initialize_session_state() -> None:
    """Inicializa todas as variáveis de sessão necessárias"""
    defaults = {
        'current_photo_index': 0,  # não é o id da foto
        'total_score': 0,
        'guess_made': False,
        'guess_coords': None,
        'guess_year': None,
        'game_finished': False,
        'photos': None,
        'map_zoom': None,
        'map_center': None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            # Seta os atributos de session_state
            st.session_state[key] = value

    # Carrega fotos se ainda não foram carregadas
    if st.session_state.photos is None:
        st.session_state.photos = load_photos()


def reset_game() -> None:
    """Reinicia o jogo resetando todas as variáveis relevantes"""
    st.session_state.current_photo_index = 0
    st.session_state.total_score = 0
    st.session_state.guess_made = False
    st.session_state.guess_coords = None
    st.session_state.guess_year = None
    st.session_state.game_finished = False
    st.session_state.map_zoom = None
    st.session_state.map_center = None


def apply_image_style() -> None:
    """Aplica CSS para remover bordas arredondadas das imagens"""
    st.markdown(
        """
        <style>
        img {
            border-radius: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def display_photo_info(photo: Photo, show_answer: bool = False) -> None:
    """
    Exibe informações da foto

    Args:
        photo: Objeto Photo a ser exibido
        show_answer: Se True, mostra descrição e ano correto
    """
    # só vai mostrar dados sobre a foto se o usuário já tiver feito o chute
    if show_answer:
        st.header(
            f":blue[{photo.description}] :green-background[:green[{photo.year}]]"
        )

    apply_image_style()
    st.image(photo.url)
    st.caption(f"© {photo.photographer}")


def display_round_header() -> None:
    """Exibe cabeçalho com informações da rodada atual"""
    current_round = st.session_state.current_photo_index + 1
    total_rounds = len(st.session_state.photos)
    current_score = st.session_state.total_score

    st.markdown(
        f"**Rodada:** {current_round}/{total_rounds} | "
        f"**Pontuação:** {current_score}"
    )


def handle_guess_input(photo: Photo) -> Tuple[Optional[int], Optional[Tuple[float, float]]]:
    """
    Gerencia entrada de chute do usuário (ano e localização)

    Args:
        photo: Foto atual

    Returns:
        Tupla com (ano_chutado, coordenadas_chutadas)
    """
    ################# ANO #################
    st.markdown("Em que **ano** você acha que a foto foi tirada?")
    year_guess = st.number_input(
        "Ano",
        min_value=MIN_YEAR,
        max_value=MAX_YEAR,
        value=DEFAULT_YEAR,
        step=1,
        key=f"year_input_{photo.id}",
        label_visibility='collapsed'
    )

    ################# LOCAL #################
    st.markdown("Em que **local** você acha que a foto foi tirada?")

    # Se for a primeira foto, ensina como fazer o chute
    if st.session_state.current_photo_index == 0:
        st.warning("⚠️ Apenas UM clique permitido, escolha bem o local.")

    # Criar mapa padrão do Brasil (sempre do zero, sem zoom salvo)
    m = map_handler.create_brazil_map()

    # Se já existe um chute confirmado, adicionar marcador
    if st.session_state.guess_coords:
        lat, lon = st.session_state.guess_coords
        map_handler.add_marker_to_map(
            m, lat, lon, "Seu chute", "blue", "hand-point-up"
        )

    # Exibir mapa e capturar APENAS clique (sem zoom/center)
    map_data = map_handler.display_interactive_map(
        m,
        key=f"map_{photo.id}"
    )

    # Processar APENAS o clique (se houver)
    if map_data and map_data.get('last_clicked'):
        clicked_lat = map_data['last_clicked']['lat']
        clicked_lon = map_data['last_clicked']['lng']

        # Salvar coordenadas do chute
        st.session_state.guess_coords = (clicked_lat, clicked_lon)
        st.rerun()  # Força atualização para mostrar o marcador

    return year_guess, st.session_state.guess_coords


def display_year_result(
    guess_year: int,
    photo: Photo,
    year_score: int,
    year_msg: str


) -> None:
    """Exibe resultado do chute de ano"""
    year_diff = abs(guess_year - photo.year)

    st.write("---")
    st.write("**:green-background[:green[Ano]]**")
    st.write(year_msg)
    st.write(f"**🔵 Você chutou:** {guess_year}")
    st.write(f"**🟢 Correto:** {photo.year}")
    st.write(f"**Diferença:** {year_diff} anos")
    st.write(f"**Pontos:** {year_score}")


def display_location_result(
    guess_coords: Tuple[float, float],
    photo: Photo,
    distance: float,
    location_score: int,
    location_msg: str
) -> None:
    """Exibe resultado do chute de localização"""
    guess_lat, guess_lon = guess_coords

    st.write("---")
    st.write("**:blue-background[:blue[Localização]]**")
    st.write(location_msg)
    st.write(f"**🔵 Você chutou:** ({guess_lat:.3f}, {guess_lon:.3f})")
    st.write(f"**🟢 Correto:** ({photo.latitude:.3f}, {photo.longitude:.3f})")
    st.write(f"**Diferença:** {distance:.1f} km de distância")
    st.write(f"**Pontos:** {location_score}")


def show_result(photo: Photo) -> None:
    """
    Mostra o resultado do chute com pontuações e mapa

    Args:
        photo: Foto atual
    """
    guess_lat, guess_lon = st.session_state.guess_coords
    guess_year = st.session_state.guess_year

    # Calcular distância
    distance = scores_handler.calculate_distance_km(
        guess_lat, guess_lon, photo.latitude, photo.longitude
    )

    # Calcular pontuações
    location_score, location_msg = scores_handler.calculate_location_score(
        distance)
    year_score, year_msg = scores_handler.calculate_year_score(
        guess_year, photo.year)
    total_round_score = location_score + year_score

    # Mostrar resultados
    display_year_result(guess_year, photo, year_score, year_msg)
    display_location_result((guess_lat, guess_lon),
                            photo, distance, location_score, location_msg)

    # Mapa com resultado
    result_map = map_handler.create_result_map(
        guess_lat, guess_lon, photo.latitude, photo.longitude
    )
    st.write("Seu chute _versus_ o local correto:")
    map_handler.display_interactive_map(
        result_map,
        key=f"result_map_{photo.id}"
    )

    # Total da rodada
    st.write("---")
    st.markdown(f"**Total de pontos nesta rodada:** {total_round_score}")
    st.markdown(
        f"**Total de pontos acumulados:** {st.session_state.total_score}")

    # Botões de navegação
    show_navigation_buttons(photo)


def show_navigation_buttons(photo: Photo) -> None:
    """
    Mostra botões de navegação (próxima foto ou finalizar)

    Args:
        photo: Foto atual
    """
    is_last_photo = st.session_state.current_photo_index >= len(
        st.session_state.photos) - 1

    if not is_last_photo:
        if st.button(
            "Próxima foto",
            type="primary",
            key=f"next_{photo.id}",
            use_container_width=True
        ):
            advance_to_next_photo()
    else:
        if st.button(
            "Ver resultado final",
            type="primary",
            key=f"finish_{photo.id}",
            use_container_width=True
        ):
            st.session_state.game_finished = True
            st.rerun()


def advance_to_next_photo() -> None:
    """Avança para a próxima foto resetando variáveis de chute"""
    st.session_state.current_photo_index += 1
    st.session_state.guess_made = False
    st.session_state.guess_coords = None
    st.session_state.guess_year = None
    st.session_state.map_zoom = None
    st.session_state.map_center = None
    st.rerun()


def show_photo_screen(photo: Photo) -> None:
    """
    Tela principal de jogo com foto e interface de chute

    Args:
        photo: Foto atual a ser exibida
    """
    col1, col2 = st.columns([1, 1])

    with col1:
        display_round_header()
        display_photo_info(photo, show_answer=st.session_state.guess_made)

    with col2:
        if not st.session_state.guess_made:
            year_guess, guess_coords = handle_guess_input(photo)

            # Botão de submissão só aparece se houver coordenadas
            if guess_coords:
                if st.button(
                    "Enviar chute",
                    type="primary",
                    key=f"confirm_{photo.id}",
                    use_container_width=True
                ):
                    submit_guess(year_guess, guess_coords)
        else:
            show_result(photo)


def submit_guess(year_guess: int, guess_coords: Tuple[float, float]) -> None:
    """
    Submete o chute do usuário e calcula pontuação

    Args:
        year_guess: Ano chutado
        guess_coords: Coordenadas chutadas
    """
    photo = st.session_state.photos[st.session_state.current_photo_index]

    # Calcular pontuações
    distance = scores_handler.calculate_distance_km(
        guess_coords[0], guess_coords[1],
        photo.latitude, photo.longitude
    )
    location_score, _ = scores_handler.calculate_location_score(distance)
    year_score, _ = scores_handler.calculate_year_score(year_guess, photo.year)
    total_round_score = location_score + year_score

    # Salvar chute e atualizar pontuação
    st.session_state.guess_coords = guess_coords
    st.session_state.guess_year = year_guess
    st.session_state.guess_made = True
    st.session_state.total_score += total_round_score

    st.rerun()


def handle_ranking_submission(player_name: str) -> None:
    """
    Processa submissão de nome para o ranking

    Args:
        player_name: Nome do jogador
    """
    if player_name and player_name.strip():
        ranking_handler.add_player_score(
            player_name.strip(),
            st.session_state.total_score
        )
        st.success(f"🎊 {player_name} adicionado ao ranking!")

        player_rank = ranking_handler.get_player_rank(player_name.strip())
        if player_rank > 0:
            st.info(f"🏆 Posição: #{player_rank}")
    else:
        st.error("❌ Por favor, digite um nome válido!")


def display_ranking(limit: int = 10) -> None:
    """
    Exibe o ranking de jogadores

    Args:
        limit: Número máximo de jogadores a exibir
    """
    st.write("---")
    st.markdown("**🏆 Ranking de jogadores**")

    top_players = ranking_handler.get_top_players(limit)

    if top_players:
        for i, player in enumerate(top_players, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            st.write(
                f"{medal} **{player.name}** - {player.total_score} pontos "
                f"({player.games_played} jogos)"
            )
    else:
        st.info("Nenhum jogador no ranking ainda. Seja o primeiro!")


def show_final_screen() -> None:
    """Tela final com pontuação total e ranking"""
    st.balloons()

    col1, col2 = st.columns(2)

    with col1:
        st.write("---")
        st.success(
            f"**🏆 Sua pontuação final:** {st.session_state.total_score} pontos"
        )
        st.write("---")

        # Entrada no ranking
        st.markdown("**🏅 Quer entrar no ranking?**")
        st.markdown("Digite seu nome:")

        player_name = st.text_input(
            "Nome do jogador",
            placeholder="Seu nome aqui",
            key="player_name_input",
            label_visibility='collapsed'
        )

        if st.button("Entrar no ranking", type="primary", use_container_width=True):
            handle_ranking_submission(player_name)

        # Exibir ranking
        display_ranking()

        # Botão jogar novamente
        if st.button("🔄 Jogar novamente", type="primary", use_container_width=True):
            reset_game()
            st.rerun()


def main() -> None:
    """Função principal da aplicação"""
    # Configuração da página
    st.set_page_config(
        page_title="Brasil Guessr",
        page_icon="🇧🇷",
        layout="wide"
    )

    # Inicialização
    initialize_session_state()

    st.title("🇧🇷 Brasil Guessr")

    # Verificar se há fotos carregadas
    if not st.session_state.photos:
        st.error("Nenhuma foto encontrada.")
        return

    # Fluxo do jogo
    if not st.session_state.game_finished:
        current_photo = st.session_state.photos[st.session_state.current_photo_index]
        show_photo_screen(current_photo)
    else:
        show_final_screen()


if __name__ == "__main__":
    main()
