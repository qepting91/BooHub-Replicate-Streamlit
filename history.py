import streamlit as st
import os
import replicate
from streamlit_extras.stoggle import stoggle


# Replicate Credentials
if 'REPLICATE_API_TOKEN' in st.secrets:
    replicate_api = st.secrets['REPLICATE_API_TOKEN']
else:
    replicate_api = st.text_input('Enter Replicate API token:', type='password')
    if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
        st.warning('Please enter your credentials!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')
os.environ['REPLICATE_API_TOKEN'] = replicate_api


def generate_response(prompt, user_input):
    full_prompt = prompt + " " + user_input
    response = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
                             input={"prompt": full_prompt, "temperature": 0.1, "top_p": 0.9, "max_length": 512, "repetition_penalty": 1})
    return response

def app():
    st.title("The spoookiest time of the year!")
    st.subheader("👻🎃💀")

    st.markdown("## History of Halloween")
    # Add a checkbox to show or hide the history section
    stoggle(
        "Show the History of Halloween!",
        """'<iframe src="https://blogs.loc.gov/headlinesandheroes/2021/10/the-origins-of-halloween-traditions/" width="100%" height="450"></iframe>', unsafe_allow_html=True)"""
    
    )
    st.markdown("---")  # Add horizontal line for separation
    st.markdown("## Halloween Recipe and Decoration Generator")
    # Dropdown menu for user to select recipe or decoration
    option = st.selectbox('What would you like help with?', ['Halloween Recipe', 'DIY Halloween Decoration'])
    user_prompt = st.text_input('Enter more specifics (optional)')

    if st.button('Get Ideas'):
        if option == 'Halloween Recipe':
            system_prompt = "You are an expert chef who specializes in creating fun and spooky Halloween recipes."
            with st.spinner("Cooking up the recipe..."):
                response = generate_response(system_prompt, user_prompt)
                st.write(response)
        else:
            system_prompt = "You are a skilled craftsman with a knack for DIY Halloween decorations."
            with st.spinner("Searching the craft box..."):
                response = generate_response(system_prompt, user_prompt)
                st.write(response)

app()