import streamlit as st
import boto3
from utils import *
from invoke_model_converse_stream_api import stream_conversation

# Page configuration
st.set_page_config(
    page_title='ChatLab',
    page_icon='🚀',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Maiin title whit animation
st.title('🚀 ChatLab')
st.subheader('Your AI Conversation Partner')

# Session state initialization
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'region' not in st.session_state:
    st.session_state['region'] = 'us-east-1'
if 'provider' not in st.session_state:
    st.session_state['provider'] = 'Anthropic'

# Enhandce sider
with st.sidebar:
    st.html('<header>⚙️ Model Configuration</header>')
    st.html("<hr style='border: 2px solid red'>")

    # Region selection with better styling
    regions = get_available_regions()
    # print(regions)
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_region = st.selectbox(
            label="AWS Region Selection",  # Added explicit label
            options=regions,
            index=regions.index(st.session_state['region'])
        )

    all_model_summaries = get_model_summaries(
        region=selected_region, provider='Anthropic')
    print(f"Modelos: {all_model_summaries}")

    providers = get_unique_providers(all_model_summaries)
    st.html("<h4>🤖 Model Selection</h4>")

    selected_provider = st.selectbox(
        label='Model Provider Selection',
        options=providers,
        help="IMPORTANT: We're limiting to Anthropic models, as some models may not support streaming or System Messages. Add your own logic to add more Providers; e.g. Amazon, Meta, AI21, etc.",
        index=providers.index(
            st.session_state['provider']) if st.session_state['provider'] in providers else 0
    )

    provider_models = [
        model for model in filter_models(all_model_summaries)
        if model['providerName'] == selected_provider
        and model['responseStreamingSupported'] == True
    ]

    default_model_index = next((idx for idx, model in enumerate(provider_models)
                                if 'haiku' in model['modelId'].lower()), 0)

    if provider_models:
        selected_model = st.selectbox(
            label="Model Selection",  # Added explicit label
            options=[model['modelName'] for model in provider_models],
            index=default_model_index
        )
        # print("provider_models:{}".format(selected_model))
        selected_model_id = next(
            model['modelId'] for model in provider_models
            if model['modelName'] == selected_model
        )
    else:
        st.error("❌ No compatible models found")
        selected_model_id = None
