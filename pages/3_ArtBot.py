# Lab 3: Chatbot page
# TODO: Rename this file to fit your page. Keep the number at the front.
#
# A chatbot built with Pydantic AI (see the Pydantic AI pages on Canvas).
# It should:
#   - use a Pydantic AI Agent with instructions that fit your project's theme (no tools yet)
#   - use Streamlit's chat elements: st.chat_message and st.chat_input
#   - remember the conversation (message_history, saved in st.session_state)
#   - use try/except so an error shows a message instead of crashing the page
#   - stay on theme, without using any API or external data
#
# Your Gemini API key goes in .streamlit/secrets.toml as GOOGLE_API_KEY.

import streamlit as st
from pydantic_ai import Agent
from google import genai
from pydantic_ai.models.google import GoogleModel

st.title("Meet Artbot")
st.subheader("Ask him anything about any questions you have regarding the Art Institure of Chicago!")
model = GoogleModel("gemini-3.1-flash-lite")
agent = Agent(model=model)
agent = Agent(
    model="gemini-3.1-flash-lite",
    instructions=(
        "You are a friendly assistant for The Art Institute of Chicago. "
        "Only talk about The Art Institute of Chicago. "
        "The classification titles you should know about are: "
        "oil on canvas, oil on panel, painting, palladium print."
    ),
)


gemini_key = "AQ.Ab8RN6J1HdM_ITHvyp5unXEW9Juww4q2rEmmAdRd4BbBSXO40A"
genai.Client(api_key=gemini_key)

from pydantic_ai.models.fallback import FallbackModel

##agent = Agent(
##    "google:gemini-2.5-flash-lite",
##    FallbackModel("google:gemini-3.1-flash-lite"),
##    instructions="...",
##)

st.chat_message("assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.text(message["content"])
prompt = st.chat_input("Ask me anything ~~~~~ ")
if prompt:
    with st.chat_message("user"):
        st.text(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    try:
        art_prompt = f"""You are Artbot, a friendly assistant who knows all about
        the Art Institute of Chicago and the classification titles it gives to its artworks. You cannot look
        up live data, so answer from general knowledge in under 5 sentences and say when you're not sure. Only talk
        about the Art Institute of Chicago, its artworks, and the classification titles such as oil on panel, oil on canvas,
        painting, and palladium print. You may only need to introduce yourself once unless asked to inroduce yourself again. 
        user input: {prompt}"""
        #personality
        art_response = agent.run_sync(art_prompt).output
        with st.chat_message("assistant"):
            st.text(art_response)
            st.session_state.messages.append({"role": "assistant", "content": art_response})
    except Exception as e:
        print("Something went wrong")
        print(e)
                        
