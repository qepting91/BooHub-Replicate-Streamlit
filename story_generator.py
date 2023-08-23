import os
import replicate
import streamlit as st

def generate_story(starting_phrase, artist_role='Dark Romanticism'):
    """
    Generate a story based on the user's starting phrase and selected style
    """
    role_prompt = {
        'Dark Romanticism': "You are an encapsulating storyteller, weaving captivating tales of dark romanticism, akin to Edgar Allan Poe.",
        'Horror': "You are the king of horror, skilled in crafting tales of dark fantasy, science fiction, psychological suspense, and horror, in the style of Stephen King."
    }
    prompt = role_prompt[artist_role] + " " + starting_phrase

    response = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
                             input={"prompt": prompt, "temperature": 0.1, "top_p": 0.9, "max_length": 512, "repetition_penalty": 1})
    return response

def app():
    with st.sidebar:
        st.title('Story provided by LLAMA 2')
        if 'REPLICATE_API_TOKEN' in st.secrets:
            st.success('API key already provided!', icon='🎃')
            replicate_api = st.secrets['REPLICATE_API_TOKEN']
        else:
            replicate_api = st.text_input('Enter Replicate API token:', type='password')
            if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
                st.warning('Please enter your credentials!', icon='⚠️')
            else:
                st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Creepster&display=swap');
    body {
        font-family: 'Creepster', cursive;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title('Spooky Story Generator')
    starting_phrase = st.text_input('Enter a starting phrase for your story')
    artist_role = st.selectbox('Choose a style for your story', ['Dark Romanticism', 'Horror'])

    if st.button('Generate'):
        # Use your story generation model here
        st.write("Generating your spooky story. Please wait...")
        story = generate_story(starting_phrase, artist_role=artist_role)
        st.write(f"Your story starts with '{starting_phrase}'. Here is how it unfolds...")
        st.write(story)

if __name__ == "__main__":
    app()