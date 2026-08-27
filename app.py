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
    "Crie historias infantis completas para videos do YouTube."
)


# ==========================================
# TOKEN HUGGING FACE
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
# CRIAR HISTORIA
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
        f"Depois da aventura, {personagem} voltou para casa levando uma lembranca magica e uma historia que jamais esqueceria."
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
# CRIAR FALA
# ==========================================

def criar_fala(personagem, numero):

    falas = [
        f"{personagem}: Que lugar lindo! O que sera que vou encontrar aqui?",
        f"{personagem}: Eu nao vou desistir. Preciso descobrir esse misterio!",
        f"{personagem}: Uau! Isso parece realmente magico!",
        f"{personagem}: Vou seguir em frente. Tenho certeza de que existe algo especial aqui.",
        f"{personagem}: Nao tenha medo. Eu vou ajudar voce!",
        f"{personagem}: Acho que estou cada vez mais perto de descobrir o segredo.",
        f"{personagem}: Conseguimos! Que aventura maravilhosa!"
    ]

    return falas[(numero - 1) % len(falas)]


# ==========================================
# MOVIMENTO PARA VIDEO
# ==========================================

def criar_movimento(numero):

    movimentos = [
        "Zoom lento em direcao a personagem enquanto as folhas se movimentam suavemente.",
        "Camera avanca lentamente pela floresta enquanto pequenas luzes magicas aparecem.",
        "Movimento suave da camera da esquerda para a direita, mostrando o ambiente encantado.",
        "A personagem caminha lentamente enquanto a camera acompanha seu movimento.",
        "Camera aproxima lentamente do objeto magico enquanto ele comeca a brilhar.",
        "Pequeno movimento cinematografico ao redor da personagem.",
        "Camera se afasta lentamente mostrando toda a floresta magica."
    ]

    return movimentos[(numero - 1) % len(movimentos)]


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
    descricao_limpa = limpar_texto(descricao_personagem)

    prompt = (
        "Children's animated fairy tale illustration. "
        f"Main character named {personagem_limpo}. "
        f"Character appearance: {descricao_limpa}. "
        "IMPORTANT: keep exactly the same character appearance, "
        "same hairstyle, same hair color, same eye color, "
        "same face, same dress, same shoes and same age "
        "in every scene. "
        f"Story theme: {tema_limpo}. "
        f"Scene {numero}: {cena_limpa}. "
        "Beautiful magical fairy tale environment. "
        "Cute young child character. "
        "Child friendly illustration. "
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
        "different shoes, adult woman, teenager, "
        "old person, extra fingers, extra arms, "
        "duplicate person, deformed face, "
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
# GERAR CAPA
# ==========================================

def gerar_capa(
    personagem,
    tema,
    descricao_personagem
):

    personagem_limpo = limpar_texto(personagem)
    tema_limpo = limpar_texto(tema)
    descricao_limpa = limpar_texto(descricao_personagem)

    prompt = (
        "Beautiful children's fairy tale YouTube thumbnail illustration. "
        f"Main character named {personagem_limpo}. "
        f"Character appearance: {descricao_limpa}. "
        f"Story theme: {tema_limpo}. "
        "The same young child character from the story. "
        "Character in the center of the image. "
        "Magical enchanted forest. "
        "Glowing magical lights. "
        "Fantasy castle in the distance. "
        "Colorful cinematic lighting. "
        "Cute animated children's movie style. "
        "Highly detailed storybook illustration. "
        "Wide landscape 16:9 YouTube thumbnail. "
        "Leave some empty space for adding a title later. "
        "No text. No letters. No watermark."
    )

    negative_prompt = (
        "adult woman, teenager, different character, "
        "different hairstyle, different dress, "
        "deformed face, extra arms, extra fingers, "
        "text, letters, watermark, logo"
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
    value=5
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
            "Historia criada! Agora vamos gerar as imagens."
        )

        historia_completa = ""
        roteiro_completo = ""

        imagens_zip = BytesIO()

        with zipfile.ZipFile(
            imagens_zip,
            "w",
            zipfile.ZIP_DEFLATED
        ) as arquivo_zip:

            # ==================================
            # CAPA
            # ==================================

            st.markdown("---")
            st.header("🖼️ Capa do YouTube")

            with st.spinner(
                "Criando a capa..."
            ):

                try:

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
                        label="⬇️ Baixar capa do YouTube",
                        data=dados_capa,
                        file_name="capa_youtube.png",
                        mime="image/png",
                        key="baixar_capa"
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

                st.subheader(
                    f"🎬 Cena {numero}"
                )

                # NARRACAO

                st.markdown("### 🎙️ Narradora")

                st.write(cena)

                # FALA

                fala = criar_fala(
                    personagem,
                    numero
                )

                st.markdown("### 💬 Fala")

                st.write(fala)

                # MOVIMENTO

                movimento = criar_movimento(
                    numero
                )

                st.markdown("### 🎥 Movimento para o video")

                st.write(movimento)

                # SALVAR ROTEIRO

                historia_completa += (
                    f"CENA {numero}\n"
                    f"{cena}\n\n"
                )

                roteiro_completo += (
                    f"CENA {numero}\n\n"
                    f"NARRADORA:\n"
                    f"{cena}\n\n"
                    f"FALA:\n"
                    f"{fala}\n\n"
                    f"MOVIMENTO:\n"
                    f"{movimento}\n\n"
                    "--------------------\n\n"
                )

                # IMAGEM

                with st.spinner(
                    f"Gerando imagem da cena {numero}..."
                ):

                    try:

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

                        dados = buffer.getvalue()

                        arquivo_zip.writestr(
                            f"cena_{numero}.png",
                            dados
                        )

                        st.download_button(
                            label=(
                                f"⬇️ Baixar imagem "
                                f"da cena {numero}"
                            ),
                            data=dados,
                            file_name=(
                                f"cena_{numero}.png"
                            ),
                            mime="image/png",
                            key=f"imagem_{numero}"
                        )

                    except Exception as erro:

                        st.error(
                            f"Nao foi possivel gerar "
                            f"a imagem da cena {numero}."
                        )

                        st.code(str(erro))


        # ======================================
        # DOWNLOADS
        # ======================================

        st.markdown("---")

        st.header("📥 Baixar seu projeto")

        imagens_zip.seek(0)

        st.download_button(
            label="📦 Baixar capa + todas as imagens",
            data=imagens_zip.getvalue(),
            file_name="conto_magico_imagens.zip",
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
            label="🎬 Baixar roteiro completo",
            data=roteiro_completo,
            file_name="roteiro_video.txt",
            mime="text/plain",
            use_container_width=True
        )


# ==========================================
# RODAPE
# ==========================================

st.markdown("---")

st.caption(
    "✨ Contos Magicos IA"
)
