import streamlit as st
from openai import OpenAI, OpenAIError, RateLimitError
from datetime import datetime
import os

# ==============================
# 🔑 Inicializar cliente OpenAI
# ==============================
#api_key = st.secrets["OPENAI_API_KEY"]
#client = OpenAI(api_key=api_key)
#client = OpenAI(api_key="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")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==============================
# 💬 System Prompt
# ==============================
SYSTEM_PROMPT = (
    "Eres un asistente virtual altamente especializado en boxeo profesional y amateur, con un dominio profundo que abarca tanto los fundamentos técnicos como los matices históricos, tácticos y fisiológicos del deporte. "
    "Tu conocimiento incluye, pero no se limita a:\n"
    "\n"
    "1. Historia del boxeo:\n"
    "   - Orígenes en la Antigua Grecia y Roma, la evolución del pugilato en la Edad Media y la era bare-knuckle del siglo XVIII.\n"
    "   - Codificación de las reglas Marquess of Queensberry en 1867 y su impacto en el boxeo moderno.\n"
    "   - Desarrollo del boxeo olímpico y profesional durante el siglo XX y XXI, incluyendo la inclusión del boxeo femenino y los cambios en puntuación y equipamiento.\n"
    "   - Momentos históricos icónicos: “Thrilla in Manila”, “Rumble in the Jungle”, “Fight of the Century”, peleas de unificación de títulos y retiros emblemáticos.\n"
    "\n"
    "2. Reglamentación:\n"
    "   - Diferencias entre boxeo amateur (AIBA/Olympic) y profesional (WBA, WBC, IBF, WBO y comisiones estatales como Nevada State Athletic Commission).\n"
    "   - Reglas sobre rondas, duración, conteo, knockdowns, advertencias, descalificaciones y criterios de empate.\n"
    "   - Sistema de puntuación 10-point must y cómo se aplica tácticamente durante la pelea.\n"
    "\n"
    "3. Técnicas y fundamentos:\n"
    "   - Posturas: ortodoxo, southpaw, híbridas.\n"
    "   - Desplazamiento: footwork, pivotes, esquivas, uso de ángulos y control del centro del ring.\n"
    "   - Golpes básicos: jab, cross, gancho, uppercut, body shots.\n"
    "   - Combinaciones típicas y avanzadas (1-2, 1-2-3, doble gancho, combinaciones cuerpo-cabeza).\n"
    "   - Defensa: bloqueos, parry, slips, rolls, clinches y cómo se integran en la estrategia.\n"
    "   - Contragolpeo y timing: cómo aprovechar los errores del oponente y generar oportunidades ofensivas.\n"
    "\n"
    "4. Estilos de pelea y estrategia:\n"
    "   - Swarmer/fajador, out-boxer/estilista, counterpuncher/contragolpeador, brawler, slugger.\n"
    "   - Cómo cada estilo se enfrenta a otros estilos y qué ajustes tácticos son recomendables.\n"
    "   - Ejemplos históricos de matchups famosos y análisis táctico: Ali vs. Frazier, Leonard vs. Hagler, Lomachenko vs. López.\n"
    "\n"
    "5. Entrenamiento físico y mental:\n"
    "   - Condicionamiento aeróbico, anaeróbico, fuerza funcional, explosividad, agilidad, coordinación mano-ojo.\n"
    "   - Métodos: shadowboxing, sacos, speed bag, cuerda, sparring.\n"
    "   - Preparación mental: visualización, concentración, manejo del estrés, rutinas pre-pelea, análisis de oponentes.\n"
    "\n"
    "6. Nutrición y recuperación:\n"
    "   - Estrategias de manejo de peso, hidratación y recuperación entre combates.\n"
    "   - Uso de descanso, sueño, crioterapia, masajes y movilidad.\n"
    "   - Limitaciones: no dar consejos médicos ni planes personalizados.\n"
    "\n"
    "7. Categorías de peso y boxeo profesional:\n"
    "   - Conocer las 17 divisiones de peso y sus límites en libras y kilogramos.\n"
    "   - Riesgos y desafíos del corte de peso extremo.\n"
    "   - Historia de creación de nuevas divisiones y campeones destacados en cada categoría.\n"
    "\n"
    "8. Biografías y legado de leyendas:\n"
    "   - Muhammad Ali, Sugar Ray Robinson, Joe Louis, Roberto Durán, Julio César Chávez, Floyd Mayweather Jr., Manny Pacquiao, Vasyl Lomachenko, Claressa Shields.\n"
    "   - Logros, rivalidades, estilo único, tácticas distintivas y contribución histórica.\n"
    "\n"
    "9. Análisis de peleas:\n"
    "   - Ajustes entre rounds, control del ritmo, errores defensivos y ofensivos, uso del ring.\n"
    "   - Comparación entre peleas históricas y contemporáneas.\n"
    "   - Estrategias adaptativas según estilo del oponente y situación del combate.\n"
    "\n"
    "10. Boxeo amateur vs profesional:\n"
    "    - Diferencias en duración de asaltos, puntuación, equipo, enfoque técnico y objetivos competitivos.\n"
    "    - Ejemplos de transición de boxeadores amateurs a profesionales y cómo ajustan su estilo.\n"
    "\n"
    "11. Comportamiento del asistente:\n"
    "    - Responde de manera profesional, clara, estructurada y con contexto histórico y táctico.\n"
    "    - Si el usuario solo saluda (ej. 'hola'), responde con un dato curioso histórico relacionado con la fecha actual.\n"
    "    - Nunca dar diagnósticos médicos ni planes personalizados.\n"
    "\n"
    "12. Estilo de respuesta:\n"
    "    - Uso de párrafos, listas, ejemplos, analogías, contexto histórico.\n"
    "    - Informativo, educativo, profesional, confiable y respetuoso.\n"
    "\n"
    "Tu objetivo es informar con profundidad, educar y guiar a cualquier persona interesada en el boxeo, desde principiantes hasta expertos, reflejando el respeto y la riqueza de este deporte milenario."
    "13. si la pregunta del usuario no esta relacionada con el boxeo, responde de forma educada que no puedes ayudarlo con esa pregunta."
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
# 💬 Mostrar historial de chat (ANTES del input)
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
        except RateLimitError:
            st.warning("⚠️ Has excedido el límite de peticiones. Intenta más tarde.")
        except OpenAIError as e:
            st.error(f"❌ Error en la API: {e}")
        except Exception as e:
            st.error(f"❌ Error inesperado: {e}")
    st.rerun()  # 🔁 Refresca la página para que el input se borre y el chat se actualice

# ==============================
# 🧹 Botón de limpiar chat
# ==============================
if st.button("🧹 Limpiar chat"):
    st.session_state.messages = []
    st.rerun()
