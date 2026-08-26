
import io, random, tempfile
from pathlib import Path
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Contos Mágicos IA Grátis", page_icon="✨", layout="wide")
st.title("✨ Contos Mágicos IA Grátis")
st.caption("Crie histórias, cenas ilustradas, narração e vídeo sem usar a API paga da OpenAI.")

for k,v in {"historia":None,"imagens":{},"audios":{},"video_path":None}.items():
    if k not in st.session_state: st.session_state[k]=v

with st.sidebar:
    formato = st.selectbox("Formato", ["YouTube 16:9","Shorts 9:16"])
    num_cenas = st.slider("Número de cenas", 4, 12, 8)
    usar_voz = st.toggle("Criar narração", value=True)

tema = st.text_input("🌟 Tema da história", placeholder="Ex.: Lili e a Floresta Encantada")
idade = st.selectbox("👧 Faixa etária", ["3–5 anos","6–8 anos","9–11 anos"])
estilo = st.selectbox("🎨 Estilo", ["Conto de fadas mágico","Aventura leve","Mistério infantil","Conto sombrio suave"])

def gerar_historia():
    nome = (tema.split()[0] if tema.strip() else "Lili").capitalize()
    locais = ["Bosque das Estrelas","Lago dos Sonhos","Ponte dos Vagalumes","Castelo de Cristal","Jardim das Nuvens"]
    cenas=[]
    for i in range(1,num_cenas+1):
        lugar = locais[(i-1)%len(locais)]
        if i==1:
            nar=f"Era uma vez {nome}, uma criança curiosa que encontrou uma luz misteriosa perto da floresta."
        elif i==num_cenas:
            nar=f"{nome} voltou para casa feliz e aprendeu que coragem e gentileza iluminam qualquer caminho."
        else:
            nar=f"{nome} chegou ao {lugar}, encontrou uma nova pista brilhante e continuou sua aventura com coragem."
        cenas.append({"numero":i,"titulo":f"Cena {i}","narracao":nar,"visual":f"{nome} em {lugar}, cenário mágico infantil"})
    return {"titulo":tema or f"{nome} e a Floresta Encantada","descricao":f"História infantil em estilo {estilo.lower()} para {idade}.","cenas":cenas}

def font(size,bold=False):
    paths=["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for p in paths:
        try:return ImageFont.truetype(p,size)
        except:pass
    return ImageFont.load_default()

def ilustrar(cena):
    W,H=(1280,720) if formato=="YouTube 16:9" else (720,1280)
    img=Image.new("RGB",(W,H),(40,45,90)); d=ImageDraw.Draw(img)
    random.seed(cena["numero"])
    for _ in range(70):
        x=random.randint(0,W-1); y=random.randint(0,int(H*.55)); r=random.randint(1,4)
        d.ellipse((x-r,y-r,x+r,y+r),fill=(255,245,190))
    d.ellipse((int(W*.72),int(H*.08),int(W*.9),int(H*.26)),fill=(255,238,170))
    d.ellipse((-W//4,int(H*.6),int(W*.8),int(H*1.15)),fill=(45,90,72))
    d.ellipse((int(W*.3),int(H*.63),int(W*1.25),int(H*1.2)),fill=(35,75,70))
    cx,cy=W//2,int(H*.55)
    d.ellipse((cx-55,cy-55,cx+55,cy+55),fill=(244,196,158))
    d.polygon([(cx-75,cy+55),(cx+75,cy+55),(cx+55,cy+180),(cx-55,cy+180)],fill=(130,100,220))
    d.rounded_rectangle((30,H-180,W-30,H-30),radius=24,fill=(10,10,25))
    d.text((60,H-160),cena["titulo"],font=font(34,True),fill="white")
    d.text((60,H-105),cena["visual"][:80],font=font(22),fill=(235,235,245))
    b=io.BytesIO(); img.save(b,format="PNG"); return b.getvalue()

def voz(cena):
    try:
        import asyncio, edge_tts
        async def run():
            c=edge_tts.Communicate(cena["narracao"], voice="pt-BR-FranciscaNeural", rate="-5%")
            chunks=[]
            async for ch in c.stream():
                if ch["type"]=="audio": chunks.append(ch["data"])
            return b"".join(chunks)
        loop=asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        data=loop.run_until_complete(run()); loop.close(); return data
    except:
        return None

def montar():
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
    work=Path(tempfile.mkdtemp(prefix="conto_gratis_")); clips=[]
    for c in st.session_state.historia["cenas"]:
        n=c["numero"]; ip=work/f"cena_{n}.png"; ip.write_bytes(st.session_state.imagens[n])
        aud=st.session_state.audios.get(n)
        if aud:
            ap=work/f"cena_{n}.mp3"; ap.write_bytes(aud)
            ac=AudioFileClip(str(ap)); clip=ImageClip(str(ip),duration=max(2.5,ac.duration)).with_audio(ac)
        else:
            clip=ImageClip(str(ip),duration=5)
        clips.append(clip)
    final=concatenate_videoclips(clips,method="compose")
    out=work/"conto_magico_gratis.mp4"
    final.write_videofile(str(out),fps=24,codec="libx264",audio_codec="aac",logger=None)
    final.close()
    for c in clips:c.close()
    return str(out)

if st.button("✨ CRIAR VÍDEO GRÁTIS", type="primary", use_container_width=True):
    if not tema.strip(): st.warning("Digite o tema da história.")
    else:
        st.session_state.historia=gerar_historia(); st.session_state.imagens={}; st.session_state.audios={}
        for c in st.session_state.historia["cenas"]:
            st.session_state.imagens[c["numero"]]=ilustrar(c)
            if usar_voz:
                a=voz(c)
                if a: st.session_state.audios[c["numero"]]=a
        with st.spinner("Montando vídeo..."):
            st.session_state.video_path=montar()

if st.session_state.historia:
    st.subheader(st.session_state.historia["titulo"])
    st.write(st.session_state.historia["descricao"])
    for c in st.session_state.historia["cenas"]:
        n=c["numero"]
        with st.expander(c["titulo"]):
            st.write(c["narracao"])
            st.image(st.session_state.imagens[n])
            if n in st.session_state.audios: st.audio(st.session_state.audios[n],format="audio/mp3")

if st.session_state.video_path:
    p=Path(st.session_state.video_path)
    if p.exists():
        data=p.read_bytes(); st.video(data)
        st.download_button("⬇️ BAIXAR VÍDEO MP4",data,file_name="conto_magico_gratis.mp4",mime="video/mp4",use_container_width=True)

st.caption("Sem OpenAI API. O roteiro e as ilustrações são locais; a voz gratuita depende de serviço externo.")
