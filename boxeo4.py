import streamlit as st
from openai import OpenAI
from datetime import datetime
import os

# ==============================
# 🔑 Inicializar cliente OpenAI
# ==============================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==============================
# 💬 System Prompt
# ==============================
SYSTEM_PROMPT = (
    "Eres un asistente virtual altamente especializado en boxeo profesional y amateur, con un dominio profundo que abarca tanto los fundamentos técnicos como los matices históricos, tácticos y fisiológicos del deporte. "
    "Tu conocimiento incluye, pero no se limita a:\n"
    "\n"
    "1. Historia del boxeo.\n"
    "2. Reglamentación.\n"
    "3. Técnicas y fundamentos.\n"
    "4. Estilos de pelea y estrategia.\n"
    "5. Entrenamiento físico y mental.\n"
    "6. Nutrición y recuperación.\n"
    "7. Categorías de peso y boxeo profesional.\n"
    "8. Biografías y legado de leyendas.\n"
    "9. Análisis de peleas.\n"
    "10. Boxeo amateur vs profesional.\n"
    "11. Comportamiento del asistente: responde de manera profesional, clara, estructurada y con contexto histórico y táctico. "
    "Si el usuario solo saluda (ej. 'hola'), responde con un dato curioso histórico relacionado con la fecha actual. "
    "12. Estilo de respuesta: informativo, educativo, profesional y respetuoso.\n"
    "13. Si la pregunta del usuario no está relacionada con el boxeo, responde educadamente que no puedes ayudar con esa pregunta."
)

# ==============================
# 🧠 Inicializar historial de chat
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# 🎨 Configuración visual
# ==============================
st.set_page_config(page_title="Asistente experto en Boxeo", page_icon="🏆", layout="centered")

st.markdown("""
<style>
body {
    background-color: #000000;
    color: #ffffff;
}
.main {
    background-color: #111111;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.6);
}
.stTextInput input {
    border-radius: 15px !important;
    border: 2px solid #ffcc00 !important;
    padding: 12px !important;
    background-color: #333333;
    color: #ffffff;
}
.stButton button {
    background-color: #ffcc00;
    color: #000000;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}
.stButton button:hover {
    background-color: #ffaa00;
    cursor: pointer;
}
h1, h2, h3, h4, h5, h6 {
    color: #ffcc00;
}
.chat-message {
    padding: 10px 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    max-width: 90%;
}
.user-message {
    background-color: #2a2a2a;
    margin-left: auto;
    text-align: right;
    color: #ffffff;
}
.bot-message {
    background-color: #3a3a3a;
    margin-right: auto;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🏆 Box AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#cccccc;'>Pregunta lo que quieras saber sobre boxeo.</p>", unsafe_allow_html=True)

# ==============================
# 📋 Barra lateral
# ==============================
st.sidebar.title("📚 Temas rápidos")
queries = {
    "🥊 Top 10 boxeadores con más Ko's": "Lista de los 10 boxeadores con más nocauts en la historia del boxeo profesional, con número aproximado de KOs y contexto histórico.",
    "🏅 Grandes campeones invictos": "¿Quiénes son los boxeadores más destacados que se retiraron invictos? Incluye récords y divisiones de peso.",
    "🧠 Estilos de pelea en el boxeo": "Explica los principales estilos de boxeo, tácticas para cada uno y estrategias para ganar.",
    "⚖️ Categorías de peso actuales (profesional)": "Lista completa de las 17 divisiones de peso en el boxeo profesional, con límites en libras, kilogramos y el máximo campeón de esa categoría.",
    "📅 ¿Qué pasó hoy en el boxeo?": f"Evento histórico o nacimiento de un campeón ocurrido el {datetime.now().strftime('%d de %B')}."
}

for label, query in queries.items():
    if st.sidebar.button(label):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.spinner("Pensando..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}] + 
                              [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                answer = response.choices[0].message.content.strip()
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"❌ Error: {e}")
        st.rerun()

# ==============================
# 💬 Mostrar historial de chat
# ==============================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message bot-message">{msg["content"]}</div>', unsafe_allow_html=True)

# ==============================
# 📥 Entrada del usuario
# ==============================
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Escribe tu pregunta aquí:")
    submit_button = st.form_submit_button("Enviar")

if submit_button and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    with st.spinner("Pensando..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + 
                          [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            answer = response.choices[0].message.content.strip()
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"❌ Error: {e}")
    st.rerun()  # Refresca para limpiar el input y mostrar respuesta

# ==============================
# 🧹 Botón de limpiar chat
# ==============================
if st.button("🧹 Limpiar chat"):
    st.session_state.messages = []
    st.rerun()
