import streamlit as st
import random

st.set_page_config(
    page_title="Contos Mágicos IA Grátis",
    page_icon="🪄",
    layout="centered"
)

st.title("🪄 Contos Mágicos IA Grátis")
st.write("Crie histórias infantis e cenas para vídeos gratuitamente.")

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
    placeholder="Exemplo: uma floresta encantada"
)

numero_cenas = st.slider(
    "Quantidade de cenas",
    min_value=5,
    max_value=12,
    value=8
)

def criar_historia(personagem, tema_historia, estilo, cenas):
    lugares = [
        "uma floresta encantada",
        "um castelo escondido entre as nuvens",
        "uma vila iluminada pela lua",
        "um jardim cheio de flores mágicas",
        "uma montanha onde viviam pequenas fadas"
    ]

    amigos = [
        "uma pequena fada",
        "um coelhinho falante",
        "uma estrela brilhante",
        "um dragãozinho amigável",
        "uma coruja sábia"
    ]

    objeto = [
        "uma chave dourada",
        "um cristal luminoso",
        "um livro encantado",
        "uma pequena lanterna mágica",
        "uma coroa de estrelas"
    ]

    lugar = tema_historia if tema_historia else random.choice(lugares)
    amigo = random.choice(amigos)
    item = random.choice(objeto)

    historia = []

    historia.append(
        f"Era uma vez {personagem}, uma criança muito curiosa que vivia perto de {lugar}."
    )

    historia.append(
        f"Certa noite, {personagem} percebeu uma luz misteriosa brilhando ao longe e decidiu descobrir de onde ela vinha."
    )

    historia.append(
        f"No caminho, encontrou {amigo}, que contou que algo mágico havia acontecido naquele lugar."
    )

    historia.append(
        f"Juntos, eles encontraram {item}, mas para descobrir seu segredo precisariam seguir um caminho cheio de magia e pequenas surpresas."
    )

    historia.append(
        f"{personagem} sentiu um pouco de medo, mas continuou avançando com coragem."
    )

    historia.append(
        f"Depois de atravessar o caminho encantado, descobriram que {item} poderia devolver a luz e a alegria ao lugar."
    )

    historia.append(
        f"{personagem} usou sua bondade e inteligência para resolver o mistério."
    )

    historia.append(
        f"Quando tudo terminou, o lugar voltou a brilhar e todos comemoraram."
    )

    historia.append(
        f"{personagem} voltou para casa levando uma lembrança daquela aventura e sabendo que a verdadeira magia estava na coragem e na amizade."
    )

    historia.append(
        "E assim terminou mais uma aventura mágica. Fim."
    )

    return historia[:cenas]


if st.button("✨ Criar história", use_container_width=True):

    if not nome:
        st.warning("Digite o nome do personagem.")
    else:
        cenas = criar_historia(
            nome,
            tema,
            tipo,
            numero_cenas
        )

        st.success("História criada!")

        historia_completa = ""

        for i, cena in enumerate(cenas, 1):

            st.subheader(f"🎬 Cena {i}")
            st.write(cena)

            prompt = (
                f"Ilustração infantil cinematográfica, personagem chamado {nome}, "
                f"{cena}, cenário mágico, conto de fadas, iluminação suave, "
                f"cores encantadoras, alta qualidade, formato 16:9, "
                f"sem texto e sem legendas."
            )

            with st.expander("🎨 Prompt para imagem/vídeo"):
                st.code(prompt)

            historia_completa += f"Cena {i}\n{cena}\n\n"

        st.download_button(
            "📥 Baixar história",
            historia_completa,
            file_name="conto_magico.txt",
            mime="text/plain",
            use_container_width=True
        )


st.divider()

st.write("💜 Feito para criar contos e preparar cenas para vídeos.")
st.caption("Não precisa de chave da OpenAI.")
