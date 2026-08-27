import streamlit as st
from huggingface_hub import InferenceClient
from io import BytesIO
import random
import re

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Contos Mágicos IA",
    page_icon="✨",
    layout="centered"
)

st.title("✨ Contos Mágicos IA")
st.write("Crie histórias infantis mágicas com cenas e imagens.")

# ==========================================
# PEGAR TOKEN DO HUGGING FACE
# ==========================================

try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except Exception:
    st.error(
        "A chave HF_TOKEN não foi encontrada nos Secrets do Streamlit."
    )
    st.stop()

# ==========================================
# CLIENTE HUGGING FACE
# ==========================================

client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)

# ==========================================
# FUNÇÃO PARA GERAR IMAGEM
# ==========================================

def gerar_imagem(descricao):

    # Evita caracteres que podem causar problemas
    descricao_limpa = descricao.replace("•", "-")
    descricao_limpa = descricao.replace("—", "-")
    descricao_limpa = descricao.replace("–", "-")
    descricao_limpa = descricao.replace("…", "...")

    prompt = f"""
Children's fairy tale illustration.
Cute child character.
Magical fantasy environment.
Colorful cinematic lighting.
Family friendly.
No text.
No letters.
No watermark.
YouTube story illustration.

Scene:
{descricao_limpa}
"""

    try:

        imagem = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-schnell"
        )

        return imagem

    except Exception as erro:

        st.warning("Não foi possível gerar esta imagem.")
        st.caption(str(erro))

        return None


# ==========================================
# FUNÇÃO PARA CRIAR HISTÓRIA
# ==========================================

def criar_historia(personagem, tipo, tema, quantidade):

    introducoes = [
        f"Era uma vez {personagem}, uma criança muito curiosa.",
        f"Em um lugar mágico vivia {personagem}.",
        f"Certa manhã, {personagem} descobriu que algo extraordinário estava para acontecer."
    ]

    acontecimentos = [
        "Uma luz misteriosa apareceu entre as árvores.",
        "Uma pequena fada surgiu trazendo uma mensagem secreta.",
        "Uma porta mágica apareceu onde antes não havia nada.",
        "Um animal encantado pediu ajuda.",
        "Um caminho brilhante surgiu no meio da floresta.",
        "Um castelo escondido apareceu entre as nuvens.",
        "Um espelho mágico começou a brilhar.",
        "Uma estrela caiu bem perto do personagem.",
        "Uma chave dourada apareceu misteriosamente.",
        "Uma voz suave chamou de dentro da floresta."
    ]

    desafios = [
        "Para continuar a aventura, era preciso encontrar uma chave encantada.",
        "O caminho estava protegido por um enigma mágico.",
        "Uma ponte desapareceu e era necessário descobrir outra passagem.",
        "Um feitiço havia escondido o caminho de volta.",
        "O personagem precisava ajudar um novo amigo antes de continuar."
    ]

    finais = [
        "Depois de uma grande aventura, tudo terminou bem e uma nova amizade nasceu.",
        "O mistério foi resolvido e todos comemoraram felizes.",
        "A magia voltou ao reino e todos viveram uma noite inesquecível.",
        "O personagem voltou para casa levando uma lembrança mágica daquela aventura."
    ]

    cenas = []

    for numero in range(quantidade):

        if numero == 0:

            texto = (
                random.choice(introducoes)
                + " "
                + f"A aventura começou com o tema: {tema}."
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
# FORMULÁRIO
# ==========================================

st.subheader("🧚 Crie sua história")

personagem = st.text_input(
    "Nome do personagem principal",
    value="Luna"
)

tipo = st.selectbox(
    "Escolha o tipo de história",
    [
        "Aventura mágica",
        "Conto de fadas",
        "Mistério infantil",
        "Fantasia",
        "História encantada"
    ]
)

tema = st.text_input(
    "Tema da história",
    value="Luna e o espelho mágico"
)

quantidade = st.slider(
    "Quantidade de cenas",
    min_value=3,
    max_value=12,
    value=6
)

# ==========================================
# BOTÃO
# ==========================================

if st.button(
    "✨ Criar história e imagens",
    use_container_width=True
):

    if not personagem.strip():

        st.warning("Digite o nome do personagem.")

    elif not tema.strip():

        st.warning("Digite o tema da história.")

    else:

        with st.spinner("Criando sua história..."):

            cenas = criar_historia(
                personagem,
                tipo,
                tema,
                quantidade
            )

        st.success(
            "História criada! Agora vamos gerar as imagens."
        )

        historia_completa = ""

        # ==================================
        # MOSTRAR CENAS
        # ==================================

        for numero, cena in enumerate(cenas, start=1):

            st.markdown("---")

            st.subheader(f"🎬 Cena {numero}")

            st.write(cena)

            historia_completa += (
                f"CENA {numero}\n"
                f"{cena}\n\n"
            )

            # ==============================
            # GERAR IMAGEM
            # ==============================

            with st.spinner(
                f"Gerando imagem da cena {numero}..."
            ):

                imagem = gerar_imagem(
                    f"""
                    Character: {personagem}.
                    Story type: {tipo}.
                    Story theme: {tema}.
                    Scene number: {numero}.
                    Scene description: {cena}.
                    """
                )

            if imagem is not None:

                st.image(
                    imagem,
                    caption=f"Cena {numero}",
                    use_container_width=True
                )

                # ==========================
                # DOWNLOAD DA IMAGEM
                # ==========================

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
                    key=f"download_imagem_{numero}"
                )

        # ==================================
        # DOWNLOAD DA HISTÓRIA
        # ==================================

        st.markdown("---")

        st.subheader("📖 História completa")

        st.download_button(
            label="⬇️ Baixar história",
            data=historia_completa.encode("utf-8"),
            file_name="conto_magico.txt",
            mime="text/plain"
        )

        st.success(
            "✨ História finalizada!"
        )


# ==========================================
# RODAPÉ
# ==========================================

st.markdown("---")

st.caption(
    "✨ Contos Mágicos IA - Criador de histórias infantis"
)
