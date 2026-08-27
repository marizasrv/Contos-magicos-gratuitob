import streamlit as st
from huggingface_hub import InferenceClient
from io import BytesIO
import random
import unicodedata
import zipfile


# ==========================================
# CONFIGURACAO
# ==========================================

st.set_page_config(
    page_title="Contos Magicos IA",
    page_icon="✨",
    layout="centered"
)

st.title("✨ Contos Magicos IA")
st.write(
    "Crie historias infantis completas com imagens, "
    "narracao e falas para videos do YouTube."
)


# ==========================================
# TOKEN
# ==========================================

try:
    HF_TOKEN = str(st.secrets["HF_TOKEN"]).strip()
except Exception:
    st.error("HF_TOKEN nao foi encontrado nos Secrets.")
    st.stop()

if not HF_TOKEN.startswith("hf_"):
    st.error("A chave HF_TOKEN parece invalida.")
    st.stop()


client = InferenceClient(
    provider="auto",
    token=HF_TOKEN
)


# ==========================================
# LIMPAR TEXTO
# ==========================================

def limpar_texto(texto):

    texto = str(texto)

    texto = texto.replace("…", "...")
    texto = texto.replace("—", "-")
    texto = texto.replace("–", "-")
    texto = texto.replace("“", '"')
    texto = texto.replace("”", '"')
    texto = texto.replace("’", "'")

    texto = unicodedata.normalize(
        "NFKD",
        texto
    )

    texto = texto.encode(
        "ascii",
        "ignore"
    ).decode("ascii")

    return texto


# ==========================================
# HISTORIA
# ==========================================

def criar_historia(personagem, tema, quantidade):

    acontecimentos = [
        f"{personagem} viu uma luz misteriosa aparecer entre as arvores.",
        f"Uma pequena fada apareceu diante de {personagem} com uma mensagem secreta.",
        f"{personagem} encontrou uma porta magica escondida entre as flores.",
        f"Um coelhinho encantado apareceu e pediu ajuda para {personagem}.",
        f"Um caminho brilhante surgiu diante de {personagem}.",
        f"{personagem} viu um castelo magico surgir por tras das nuvens.",
        f"Um espelho encantado comecou a brilhar diante de {personagem}.",
        f"Uma estrela brilhante caiu perto de {personagem}.",
        f"{personagem} encontrou uma pequena chave dourada entre as folhas."
    ]

    desafios = [
        f"Para continuar a aventura, {personagem} precisava resolver um enigma magico.",
        f"Uma ponte encantada havia desaparecido e {personagem} precisava encontrar outro caminho.",
        f"Um feitico escondia o caminho correto, mas {personagem} decidiu continuar.",
        f"{personagem} encontrou um novo amigo que precisava de ajuda.",
        f"Uma grande porta encantada so poderia ser aberta com coragem."
    ]

    finais = [
        f"{personagem} resolveu o misterio e todos comemoraram felizes.",
        f"A magia voltou ao reino e {personagem} percebeu que sua coragem havia salvado aquele lugar.",
        f"Depois da aventura, {personagem} voltou para casa levando uma lembranca magica."
    ]

    cenas = []

    for numero in range(quantidade):

        if numero == 0:

            texto = (
                f"Era uma vez {personagem}, "
                f"uma menina curiosa que entrou em uma floresta encantada. "
                f"A aventura comecou com o tema: {tema}."
            )

        elif numero == quantidade - 1:

            texto = random.choice(finais)

        elif numero % 3 == 0:

            texto = random.choice(desafios)

        else:

            texto = random.choice(acontecimentos)

        cenas.append(texto)

    return cenas


# ==========================================
# FALAS
# ==========================================

def criar_fala(personagem, numero):

    falas = [
        f"{personagem}: Que lugar lindo! O que sera que existe aqui?",
        f"{personagem}: Eu vou descobrir esse misterio!",
        f"{personagem}: Uau! Isso parece magico!",
        f"{personagem}: Nao vou desistir. Vou continuar.",
        f"{personagem}: Nao tenha medo. Eu vou ajudar voce!",
        f"{personagem}: Acho que estou perto de descobrir o segredo.",
        f"{personagem}: Conseguimos! Que aventura maravilhosa!"
    ]

    return falas[(numero - 1) % len(falas)]


# ==========================================
# MOVIMENTO
# ==========================================

def criar_movimento(numero):

    movimentos = [
        "Zoom lento em direcao a personagem enquanto as folhas se movimentam.",
        "Camera avanca lentamente pela floresta com pequenas luzes magicas.",
        "Camera se move suavemente da esquerda para a direita.",
        "A personagem caminha enquanto a camera acompanha seu movimento.",
        "Camera aproxima lentamente do objeto magico enquanto ele brilha.",
        "Movimento cinematografico suave ao redor da personagem.",
        "Camera se afasta mostrando toda a floresta encantada."
    ]

    return movimentos[(numero - 1) % len(movimentos)]


# ==========================================
# GERAR AUDIO
# ==========================================

def gerar_audio(texto):

    texto_limpo = limpar_texto(texto)

    audio = client.text_to_speech(
        text=texto_limpo
    )

    return audio


# ==========================================
# GERAR IMAGEM
# ==========================================

def gerar_imagem(
    personagem,
    tema,
    numero,
    cena,
    descricao_personagem
):

    personagem_limpo = limpar_texto(personagem)
    tema_limpo = limpar_texto(tema)
    cena_limpa = limpar_texto(cena)
    descricao_limpa = limpar_texto(
        descricao_personagem
    )

    prompt = (
        "Children's animated fairy tale illustration. "
        f"Main character named {personagem_limpo}. "
        f"Character appearance: {descricao_limpa}. "
        "IMPORTANT: keep exactly the same character appearance, "
        "same hairstyle, same hair color, same eyes, same face, "
        "same dress, same shoes and same age in every scene. "
        f"Story theme: {tema_limpo}. "
        f"Scene {numero}: {cena_limpa}. "
        "Beautiful magical fairy tale environment. "
        "Cute child friendly illustration. "
        "Colorful magical scenery. "
        "Cinematic lighting. "
        "Detailed animated storybook art. "
        "Wide landscape shot. "
        "16:9 YouTube video composition. "
        "No text. No letters. No captions. No watermark."
    )

    negative_prompt = (
        "different character, different hairstyle, "
        "different hair color, different dress, "
        "adult woman, teenager, extra fingers, "
        "extra arms, duplicate person, deformed face, "
        "text, letters, subtitles, watermark, logo"
    )

    imagem = client.text_to_image(
        prompt=prompt,
        negative_prompt=negative_prompt,
        model="black-forest-labs/FLUX.1-schnell",
        width=1024,
        height=576,
        seed=12345
    )

    return imagem


# ==========================================
# CAPA
# ==========================================

def gerar_capa(
    personagem,
    tema,
    descricao_personagem
):

    personagem_limpo = limpar_texto(personagem)
    tema_limpo = limpar_texto(tema)
    descricao_limpa = limpar_texto(
        descricao_personagem
    )

    prompt = (
        "Beautiful children's fairy tale YouTube thumbnail. "
        f"Main character named {personagem_limpo}. "
        f"Character appearance: {descricao_limpa}. "
        f"Story theme: {tema_limpo}. "
        "Same young child character from the story. "
        "Character centered in a magical enchanted forest. "
        "Glowing lights and fantasy castle. "
        "Colorful cinematic lighting. "
        "Animated children's movie style. "
        "Wide landscape 16:9 YouTube thumbnail. "
        "No text. No letters. No watermark."
    )

    imagem = client.text_to_image(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell",
        width=1024,
        height=576,
        seed=12345
    )

    return imagem


# ==========================================
# FORMULARIO
# ==========================================

st.subheader("🧚 Crie sua historia")

personagem = st.text_input(
    "Nome do personagem principal",
    value="Luna"
)

tema = st.text_input(
    "Tema da historia",
    value="Luna e o espelho magico"
)

descricao_personagem = st.text_area(
    "Como a personagem deve ser",
    value=(
        "A cute 7 year old girl, "
        "long dark brown hair, "
        "large brown eyes, "
        "yellow fairy tale dress, "
        "red shoes, "
        "round child face"
    )
)

quantidade = st.slider(
    "Quantidade de cenas",
    min_value=3,
    max_value=12,
    value=3
)


# ==========================================
# BOTAO
# ==========================================

if st.button(
    "✨ Criar historia completa",
    use_container_width=True
):

    if not personagem.strip():

        st.warning(
            "Digite o nome do personagem."
        )

    elif not tema.strip():

        st.warning(
            "Digite o tema da historia."
        )

    else:

        cenas = criar_historia(
            personagem,
            tema,
            quantidade
        )

        st.success(
            "Historia criada! Gerando seu projeto..."
        )

        historia_completa = ""
        roteiro_completo = ""

        arquivos_zip = BytesIO()

        with zipfile.ZipFile(
            arquivos_zip,
            "w",
            zipfile.ZIP_DEFLATED
        ) as arquivo_zip:

            # ==================================
            # CAPA
            # ==================================

            st.markdown("---")
            st.header("🖼️ Capa do YouTube")

            try:

                with st.spinner("Criando capa..."):

                    capa = gerar_capa(
                        personagem,
                        tema,
                        descricao_personagem
                    )

                st.image(
                    capa,
                    caption="Capa do video",
                    use_container_width=True
                )

                buffer_capa = BytesIO()

                capa.save(
                    buffer_capa,
                    format="PNG"
                )

                dados_capa = buffer_capa.getvalue()

                arquivo_zip.writestr(
                    "capa_youtube.png",
                    dados_capa
                )

                st.download_button(
                    "⬇️ Baixar capa do YouTube",
                    data=dados_capa,
                    file_name="capa_youtube.png",
                    mime="image/png"
                )

            except Exception as erro:

                st.warning(
                    "Nao foi possivel gerar a capa."
                )

                st.code(str(erro))


            # ==================================
            # CENAS
            # ==================================

            for numero, cena in enumerate(
                cenas,
                start=1
            ):

                st.markdown("---")
                st.header(f"🎬 Cena {numero}")

                # ==============================
                # NARRADORA
                # ==============================

                st.subheader("🎙️ Narradora")
                st.write(cena)

                try:

                    with st.spinner(
                        "Criando voz da narradora..."
                    ):

                        audio_narradora = gerar_audio(
                            cena
                        )

                    st.audio(
                        audio_narradora
                    )

                    arquivo_zip.writestr(
                        f"narradora_cena_{numero}.flac",
                        audio_narradora
                    )

                    st.download_button(
                        label=(
                            f"⬇️ Baixar narracao "
                            f"da cena {numero}"
                        ),
                        data=audio_narradora,
                        file_name=(
                            f"narradora_cena_{numero}.flac"
                        ),
                        mime="audio/flac",
                        key=f"narradora_{numero}"
                    )

                except Exception as erro:

                    st.warning(
                        "Nao foi possivel gerar "
                        "a voz da narradora."
                    )

                    st.caption(str(erro))


                # ==============================
                # FALA
                # ==============================

                fala = criar_fala(
                    personagem,
                    numero
                )

                st.subheader("💬 Personagem")
                st.write(fala)

                try:

                    with st.spinner(
                        "Criando voz da personagem..."
                    ):

                        audio_personagem = gerar_audio(
                            fala
                        )

                    st.audio(
                        audio_personagem
                    )

                    arquivo_zip.writestr(
                        f"fala_cena_{numero}.flac",
                        audio_personagem
                    )

                    st.download_button(
                        label=(
                            f"⬇️ Baixar fala "
                            f"da cena {numero}"
                        ),
                        data=audio_personagem,
                        file_name=(
                            f"fala_cena_{numero}.flac"
                        ),
                        mime="audio/flac",
                        key=f"fala_{numero}"
                    )

                except Exception as erro:

                    st.warning(
                        "Nao foi possivel gerar "
                        "a voz da personagem."
                    )

                    st.caption(str(erro))


                # ==============================
                # MOVIMENTO
                # ==============================

                movimento = criar_movimento(
                    numero
                )

                st.subheader(
                    "🎥 Movimento para video"
                )

                st.write(movimento)


                # ==============================
                # IMAGEM
                # ==============================

                try:

                    with st.spinner(
                        f"Gerando imagem da cena {numero}..."
                    ):

                        imagem = gerar_imagem(
                            personagem,
                            tema,
                            numero,
                            cena,
                            descricao_personagem
                        )

                    st.image(
                        imagem,
                        caption=f"Cena {numero}",
                        use_container_width=True
                    )

                    buffer = BytesIO()

                    imagem.save(
                        buffer,
                        format="PNG"
                    )

                    dados_imagem = buffer.getvalue()

                    arquivo_zip.writestr(
                        f"cena_{numero}.png",
                        dados_imagem
                    )

                    st.download_button(
                        label=(
                            f"⬇️ Baixar imagem "
                            f"da cena {numero}"
                        ),
                        data=dados_imagem,
                        file_name=f"cena_{numero}.png",
                        mime="image/png",
                        key=f"imagem_{numero}"
                    )

                except Exception as erro:

                    st.error(
                        f"Nao foi possivel gerar "
                        f"a imagem da cena {numero}."
                    )

                    st.code(str(erro))


                # ==============================
                # TEXTOS
                # ==============================

                historia_completa += (
                    f"CENA {numero}\n"
                    f"{cena}\n\n"
                )

                roteiro_completo += (
                    f"CENA {numero}\n\n"
                    f"NARRADORA:\n"
                    f"{cena}\n\n"
                    f"PERSONAGEM:\n"
                    f"{fala}\n\n"
                    f"MOVIMENTO:\n"
                    f"{movimento}\n\n"
                    "--------------------\n\n"
                )


        # ======================================
        # DOWNLOAD FINAL
        # ======================================

        st.markdown("---")
        st.header("📥 Baixar projeto")

        arquivos_zip.seek(0)

        st.download_button(
            label="📦 Baixar projeto completo",
            data=arquivos_zip.getvalue(),
            file_name="conto_magico_completo.zip",
            mime="application/zip",
            use_container_width=True
        )

        st.download_button(
            label="📖 Baixar historia",
            data=historia_completa,
            file_name="conto_magico.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.download_button(
            label="🎬 Baixar roteiro",
            data=roteiro_completo,
            file_name="roteiro_video.txt",
            mime="text/plain",
            use_container_width=True
        )


st.markdown("---")

st.caption(
    "✨ Contos Magicos IA"
)
