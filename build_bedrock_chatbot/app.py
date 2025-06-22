import streamlit as st
import boto3
# from utils import *

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
# TODO: Trabajar La inicialización de variables

# Enhandce sider
with st.sidebar:
    st.html('<header>⚙️ Model Configuration</header>')
    st.html("<hr style='border: 2px solid red'>")

    # Region selection with better styling
