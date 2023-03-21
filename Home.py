import streamlit as st
from PIL import Image

st.set_page_config(page_title='Home', page_icon='')

image = Image.open('image_delivery.jpg')

st.sidebar.image(image, width=150)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fast Delivery in Town')
st.sidebar.markdown("""___""")

st.write('# Curry Company Growth Dashboard')

st.markdown(
    """
        Growth Dashboard foi construido para acompanhar o crescimento dos Entregadores e Restaurantes.
        ### Como utilizar esse Growth Dashboard?
        - Visão Empresa:
            - Visão Gerencial: Métricas gerais de comportamento.
            - Visão Tática: Indicadores semanais de crescimento.
            - Visão Geográfica: Insights de Geolocalização.
        - Visão Entregador:
            - Acompanhamento dos indicadores semanais de crescimento.
        - Visão Restaurantes:
            - Indicadores semanais de crescimento dos restaurantes.
        ### Ask for help
        - Time de Data Science no Discord
            - ricardo_ninomiya#2135
    
    """

)