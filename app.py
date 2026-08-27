import streamlit as st
from huggingface_hub import InferenceClient
from io import BytesIO
import random

st.set_page_config(
    page_title="Contos Mágicos IA",
    page_icon="✨",
    layout="centered"
)

st.title("✨ Contos Mágicos IA")
st.write("Crie histórias infantis com imagens para cada cena.")

# Chave guardada nos Secrets do Streamlit
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except Exception:
    st.error("A chave HF_TOKEN não foi encontrada nos Secrets do Streamlit.")
    st.stop()

client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN
)

nome = st.text_input(
    "Nome do personagem principal",
    placeholder="Exemplo: Luna"
)

tipo = st.selectbox(
    "Escolha o tipo de história",
    [
        "Conto de fadas",
        "Aventura mágica",
        "Mistério infantil",
        "Conto sombrio infantil",
        "História para dormir"
    ]
)

tema = st.text_input(
    "Tema da história",
    placeholder="Exemplo: Luna e o espelho mágico"
)

numero_cenas = st.slider(
    "Quantidade de cenas",
    min_value=5,
    max_value=12,
    value=8
)

def criar_historia(personagem, tema_historia, estilo, quantidade):
    lugares = [
        "uma floresta encantada",
        "um castelo escondido entre as nuvens",
        "uma vila iluminada pela lua",
        "um jardim cheio de flores mágicas",
        "uma montanha onde vivem pequenas fadas"
    ]

    amigos = [
        "uma pequena fada",
        "um coelhinho falante",
        "uma estrela brilhante",
        "um dragãozinho amigável",
        "uma coruja sábia"
    ]

    lugar = tema_historia if tema_historia else random.choice(lugares)
    amigo = random.choice(amigos)

    cenas = [
        f"Era uma vez {personagem}, uma criança curiosa que vivia perto de {lugar}.",
        f"Certa noite, {personagem} viu uma luz misteriosa brilhando ao longe.",
        f"No caminho, {personagem} encontrou {amigo}, que decidiu acompanhar a aventura.",
        f"Juntos descobriram uma passagem secreta para um mundo cheio de magia.",
        f"{personagem} encontrou um objeto mágico escondido entre árvores brilhantes.",
        f"Um pequeno desafio apareceu, mas {personagem} decidiu enfrentá-lo com coragem.",
        f"Com a ajuda de {amigo}, o mistério começou a ser resolvido.",
        f"A magia voltou a iluminar todo o lugar.",
        f"{personagem} percebeu que amizade e coragem eram a verdadeira magia.",
        f"Depois da aventura, {personagem} voltou feliz para casa. Fim."
    ]

    while len(cenas) < quantidade:
        cenas.insert(
            -1,
            f"{personagem} continuou explorando o mundo encantado e encontrou uma nova surpresa."
        )

    return cenas[:quantidade]


def gerar_imagem(def gerar_imagem(cena, personagem):
    cena = cena.replace("…", "...").replace("—", "-").replace("–", "-")
    personagem = personagem.replace("…", "...").replace("—", "-").replace("–", "-")

    prompt = (
        f"Children's fairy tale illustration. "
        f"Main character: {personagem}, a cute young child. "
        f"Scene: {cena}. "
    )

    imagem = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-schnell",
        width=1024,
        height=576
    )

    return imagem, prompt


if st.button("✨ Criar história e imagens", use_container_width=True):

    if not nome:
        st.warning("Digite o nome do personagem principal.")

    else:
        cenas = criar_historia(
            nome,
            tema,
            tipo,
            numero_cenas
        )

        st.success("História criada! Agora vamos gerar as imagens.")

        historia_completa = ""

        for i, cena in enumerate(cenas, 1):

            st.subheader(f"🎬 Cena {i}")
            st.write(cena)

            historia_completa += f"Cena {i}\n{cena}\n\n"

            with st.spinner(f"🎨 Criando imagem da cena {i}..."):

                try:
                    imagem, prompt = gerar_imagem(cena, nome)

                    st.image(
                        imagem,
                        caption=f"Cena {i}",
                        use_container_width=True
                    )

                    buffer = BytesIO()
                    imagem.save(buffer, format="PNG")
                    dados_imagem = buffer.getvalue()

                    st.download_button(
                        f"📥 Baixar imagem da cena {i}",
                        data=dados_imagem,
                        file_name=f"cena_{i}.png",
                        mime="image/png",
                        key=f"download_{i}"
                    )

                    with st.expander("🎨 Ver prompt da imagem"):
                        st.write(prompt)

                except Exception as erro:
                    st.error(
                        f"Não foi possível gerar a imagem da cena {i}."
                    )
                    st.caption(str(erro))

        st.download_button(
            "📖 Baixar história completa",
            historia_completa,
            file_name="conto_magico.txt",
            mime="text/plain",
            use_container_width=True
        )

st.divider()
st.caption("✨ Contos Mágicos IA")
