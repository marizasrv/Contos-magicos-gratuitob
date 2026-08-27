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
    "Crie historias infantis com imagens em formato YouTube."
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
        "Uma luz misteriosa apareceu entre as arvores.",
        "Uma pequena fada apareceu com uma mensagem secreta.",
        "Uma porta magica surgiu entre as flores.",
        "Um coelhinho encantado pediu ajuda.",
        "Um caminho brilhante apareceu na floresta.",
        "Um castelo surgiu por tras das nuvens.",
        "Um espelho magico comecou a brilhar.",
        "Uma estrela caiu perto da personagem.",
        "Uma chave dourada apareceu entre as folhas."
    ]

    desafios = [
        "Para continuar, era preciso resolver um enigma.",
        "Uma ponte magica havia desaparecido.",
        "Um feitico escondia o caminho correto.",
        "A personagem precisava ajudar um novo amigo.",
        "Uma porta encantada so abriria com coragem."
    ]

    finais = [
        "O misterio foi resolvido e todos comemoraram felizes.",
        "A magia voltou ao reino e todos ficaram felizes.",
        "Depois da aventura, a personagem voltou para casa com uma lembranca magica."
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
# GERAR IMAGEM
# ==========================================

def gerar_imagem(
    personagem,
    tema,
    numero,
    cena,
    descricao_personagem
):

    personagem = limpar_texto(personagem)
    tema = limpar_texto(tema)
    cena = limpar_texto(cena)
    descricao_personagem = limpar_texto(
        descricao_personagem
    )

    prompt = (
        "Children's animated fairy tale illustration. "
        f"Main character named {personagem}. "
        f"Character appearance: {descricao_personagem}. "
        "IMPORTANT: keep exactly the same character appearance, "
        "same hairstyle, same hair color, same face, "
        "same dress and same age in every scene. "
        f"Story theme: {tema}. "
        f"Scene {numero}: {cena}. "
        "Beautiful magical forest environment. "
        "Cute child friendly illustration. "
        "Cinematic lighting. "
        "Detailed storybook art. "
        "Wide landscape shot. "
        "YouTube video composition. "
        "No text. No letters. No captions."
    )

    negative_prompt = (
        "different character, different hairstyle, "
        "different dress, adult woman, teenager, "
        "extra fingers, extra arms, duplicate person, "
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
    "✨ Criar historia e imagens",
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
            "Historia criada! Gerando imagens..."
        )

        historia_completa = ""

        imagens_zip = BytesIO()

        with zipfile.ZipFile(
            imagens_zip,
            "w",
            zipfile.ZIP_DEFLATED
        ) as arquivo_zip:

            for numero, cena in enumerate(
                cenas,
                start=1
            ):

                st.markdown("---")

                st.subheader(
                    f"🎬 Cena {numero}"
                )

                st.write(cena)

                historia_completa += (
                    f"CENA {numero}\n"
                    f"{cena}\n\n"
                )

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


        st.markdown("---")

        imagens_zip.seek(0)

        st.download_button(
            label="📦 Baixar todas as imagens",
            data=imagens_zip.getvalue(),
            file_name="imagens_contos_magicos.zip",
            mime="application/zip",
            use_container_width=True
        )

        st.download_button(
            label="📖 Baixar historia completa",
            data=historia_completa,
            file_name="conto_magico.txt",
            mime="text/plain",
            use_container_width=True
        )


st.markdown("---")

st.caption(
    "✨ Contos Magicos IA"
)
