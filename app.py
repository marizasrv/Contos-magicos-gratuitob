import streamlit as st
from huggingface_hub import InferenceClient
from io import BytesIO
import random
import unicodedata

# ==========================================
# CONFIGURACAO
# ==========================================

st.set_page_config(
    page_title="Contos Magicos IA",
    page_icon="✨",
    layout="centered"
)

st.title("✨ Contos Magicos IA")
st.write("Crie historias infantis com imagens para cada cena.")

# ==========================================
# TOKEN DO HUGGING FACE
# ==========================================

try:
    HF_TOKEN = str(st.secrets["HF_TOKEN"]).strip()
except Exception:
    st.error("HF_TOKEN nao foi encontrado nos Secrets do Streamlit.")
    st.stop()

# Verifica se a chave tem caracteres que nao deveriam existir
try:
    HF_TOKEN.encode("ascii")
except UnicodeEncodeError:
    st.error(
        "A chave HF_TOKEN salva no Streamlit tem um caractere invalido. "
        "Voce precisara copiar novamente a chave completa do Hugging Face."
    )
    st.stop()

if not HF_TOKEN.startswith("hf_"):
    st.error(
        "A chave HF_TOKEN parece estar incompleta. "
        "Ela deve comecar com hf_."
    )
    st.stop()

# ==========================================
# CLIENTE HUGGING FACE
# ==========================================

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
    texto = texto.replace("‘", "'")
    texto = texto.replace("’", "'")

    texto = unicodedata.normalize("NFKD", texto)

    texto = texto.encode(
        "ascii",
        "ignore"
    ).decode("ascii")

    return texto

# ==========================================
# CRIAR HISTORIA
# ==========================================

def criar_historia(personagem, tema, quantidade):

    introducoes = [
        f"Era uma vez {personagem}, uma crianca muito curiosa.",
        f"Em um lugar magico vivia {personagem}.",
        f"Certa manha, {personagem} descobriu que algo extraordinario estava para acontecer."
    ]

    acontecimentos = [
        "Uma luz misteriosa apareceu entre as arvores.",
        "Uma pequena fada surgiu trazendo uma mensagem secreta.",
        "Uma porta magica apareceu onde antes nao havia nada.",
        "Um animal encantado pediu ajuda.",
        "Um caminho brilhante surgiu no meio da floresta.",
        "Um castelo escondido apareceu entre as nuvens.",
        "Um espelho magico comecou a brilhar.",
        "Uma estrela caiu bem perto do personagem.",
        "Uma chave dourada apareceu misteriosamente.",
        "Uma voz suave chamou de dentro da floresta."
    ]

    desafios = [
        "Para continuar a aventura, era preciso encontrar uma chave encantada.",
        "O caminho estava protegido por um enigma magico.",
        "Uma ponte desapareceu e era necessario descobrir outra passagem.",
        "Um feitico havia escondido o caminho de volta.",
        "O personagem precisava ajudar um novo amigo antes de continuar."
    ]

    finais = [
        "Depois de uma grande aventura, tudo terminou bem e uma nova amizade nasceu.",
        "O misterio foi resolvido e todos comemoraram felizes.",
        "A magia voltou ao reino e todos viveram uma noite inesquecivel.",
        "O personagem voltou para casa levando uma lembranca magica daquela aventura."
    ]

    cenas = []

    for numero in range(quantidade):

        if numero == 0:
            texto = (
                random.choice(introducoes)
                + " "
                + f"A aventura comecou com o tema: {tema}."
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

def gerar_imagem(personagem, tipo, tema, numero, cena):

    personagem_limpo = limpar_texto(personagem)
    tipo_limpo = limpar_texto(tipo)
    tema_limpo = limpar_texto(tema)
    cena_limpa = limpar_texto(cena)

    prompt = (
        "Children's fairy tale illustration. "
        f"Main character: {personagem_limpo}. "
        f"Story type: {tipo_limpo}. "
        f"Story theme: {tema_limpo}. "
        f"Scene number: {numero}. "
        f"Scene description: {cena_limpa}. "
        "Cute young child. "
        "Magical fantasy world. "
        "Beautiful colorful storybook illustration. "
        "Cinematic lighting. "
        "Family friendly. "
        "Consistent character design. "
        "Landscape composition. "
        "No text. "
        "No letters. "
        "No captions. "
        "No watermark."
    )

    # Garantia final: o prompt enviado sera somente ASCII
    prompt = prompt.encode(
        "ascii",
        "ignore"
    ).decode("ascii")

    imagem = client.text_to_image(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell"
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

tipo = st.selectbox(
    "Escolha o tipo de historia",
    [
        "Aventura magica",
        "Conto de fadas",
        "Misterio infantil",
        "Fantasia",
        "Historia encantada"
    ]
)

tema = st.text_input(
    "Tema da historia",
    value="Luna e o espelho magico"
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
    "✨ Criar historia e imagens",
    use_container_width=True
):

    if not personagem.strip():
        st.warning("Digite o nome do personagem.")

    elif not tema.strip():
        st.warning("Digite o tema da historia.")

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

        for numero, cena in enumerate(cenas, start=1):

            st.markdown("---")
            st.subheader(f"🎬 Cena {numero}")
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
                        tipo,
                        tema,
                        numero,
                        cena
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

                    st.download_button(
                        label=f"⬇️ Baixar imagem da cena {numero}",
                        data=buffer.getvalue(),
                        file_name=f"cena_{numero}.png",
                        mime="image/png",
                        key=f"imagem_{numero}"
                    )

                except Exception as erro:

                    st.error(
                        f"Nao foi possivel gerar a imagem da cena {numero}."
                    )

                    st.code(str(erro))

        st.markdown("---")

        st.download_button(
            label="📖 Baixar historia completa",
            data=historia_completa,
            file_name="conto_magico.txt",
            mime="text/plain"
        )

st.markdown("---")
st.caption("✨ Contos Magicos IA")
