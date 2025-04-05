import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Chatbot Musical con Gemini", page_icon="🎵")
st.title("🎵 MelodyBot Tu Experto Musical")

# Configuración de la API Key (REEMPLAZA CON TU CLAVE REAL)
GEMINI_API_KEY = "AIzaSyD2GFUHiwfcrxiirFtpsf4OhN3kKP7Ipqo"
genai.configure(api_key=GEMINI_API_KEY)

# Selección del modelo
modelo_musical = "gemini-1.5-flash"

# Inicializar historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola amante de la música! 🎶 Soy tu experto musical personal. "
                       "Pregúntame sobre:\n\n"
                       "• Tus artistas favoritos 🎤\n"
                       "• Letras de canciones 📝\n"
                       "• Recomendaciones musicales 🎧\n"
                       "• Historia de bandas 🎸\n"
                       "• Géneros musicales 🎼\n\n"
                       "¿De qué artista o canción quieres hablar hoy?"
        }
    ]

# Mostrar historial del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if pregunta := st.chat_input("Sobre qué cantante quieres hablar o conocer hoy?..."):
    # Agregar pregunta al historial
    st.session_state.messages.append({"role": "user", "content": pregunta})
    
    # Mostrar pregunta del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    # Generar respuesta
    with st.chat_message("assistant"):
        try:
            # Crear modelo
            model = genai.GenerativeModel(modelo_musical)

            # Generar respuesta con una mejor instrucción
            respuesta = model.generate_content(f"Dime información sobre el artista {pregunta}. "
                                               "Incluye datos de su carrera, éxitos y curiosidades.", stream=False)

            # Extraer el texto de la respuesta
            respuesta_texto = respuesta.text if hasattr(respuesta, 'text') else "No pude obtener información sobre este artista."

            # Mostrar la respuesta en la interfaz
            st.markdown(respuesta_texto)

            # Agregar la respuesta al historial
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})

        except Exception as e:
            st.error("¡Vaya! Hubo un error al procesar tu pregunta musical. Inténtalo de nuevo más tarde.")
            st.session_state.messages.append(
                {"role": "assistant", "content": "Disculpa, no pude responder. ¿Podrías intentarlo de nuevo?"}
            )
