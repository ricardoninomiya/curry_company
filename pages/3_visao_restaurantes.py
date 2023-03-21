# Bibliotecas
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
import re
import haversine
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Restaurantes', page_icon='', layout='wide')


# --------------Funções---------------#
#######################################
# ------------------------------------#

def distance(df1):
    # Biblioteca haversine para calcular distancia latitude e longitude
    cols2 = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude',
             'Delivery_location_longitude']

    df1['distance'] = df1.loc[:, cols2].apply(
        lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)

    media = np.round(df1['distance'].mean(), 2)
    return media


# Função Limpeza dos dados
def clean_code(df1):
    """ Esta função tem a responsabilidade de limpar o DataFrame
        Tipos de Limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços das variáveis de texto
        4. Formatação de colunas de data
        5. Limpeza da coluna de Tempo(Remoção do texto da variável numérica)

        Input: DataFrame
        Output: DataFrame
    """
    # Tratando a formatação das colunas
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'] != 'NaN '
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    df1['Delivery_person_Age'] = pd.to_numeric(df['Delivery_person_Age'], errors='coerce')
    df1['Delivery_person_Ratings'] = pd.to_numeric(df['Delivery_person_Age'], errors='coerce')
    df1['multiple_deliveries'] = df1['multiple_deliveries'] != 'NaN '
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    df1['Delivery_location_latitude'] = pd.to_numeric(df['Delivery_location_latitude'], errors='coerce')
    df1['Delivery_location_longitude'] = pd.to_numeric(df['Delivery_location_longitude'], errors='coerce')
    df1['Restaurant_latitude'] = pd.to_numeric(df['Restaurant_latitude'], errors='coerce')
    df1['Restaurant_longitude'] = pd.to_numeric(df['Restaurant_longitude'], errors='coerce')

    # Limpar os espacos vazios
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Time_Orderd'] = df1.loc[:, 'Time_Orderd'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    # Limpando a coluna Time_taken(min)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1


# Import Dataset
df = pd.read_csv('train.csv')

# Limpando os dados
df1 = clean_code(df)
# -------------------

###############################
# Barra Lateral no Streamlit
# executar o arquivo digite no terminal dentro da pasta onde se localiza o arquivo ->
# streamlit run 'nome_do_arquivo.py'
###############################

st.header('MarketPlace - Visão Restaurantes')

image = Image.open('image_delivery.JPG')
st.sidebar.image(image, width=300, caption='Fast Delivery')

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fast Delivery in Town')
st.sidebar.markdown("""___""")

st.sidebar.markdown('## Selecione uma Data Limite')
data_slider = st.sidebar.slider('Até qual Valor?',
                                value=pd.datetime(2022, 4, 13),
                                min_value=pd.datetime(2022, 2, 11),
                                max_value=pd.datetime(2022, 4, 6),
                                format='DD-MM-YYYY')

st.sidebar.markdown("""___""")

traffic_options = st.sidebar.multiselect('Quais as condições do transito',
                                         ['Low', 'Medium', 'High', 'Jam'],
                                         default=['Low', 'Medium', 'High', 'Jam'])

weather_options = st.sidebar.multiselect('Quais as condições do Clima',
                                         ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms',
                                          'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
                                         default=['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms',
                                                  'conditions Stormy', 'conditions Sunny', 'conditions Windy'])

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Comunidade DS')

# Filtros no DataFrame
linhas_selecionadas = df1['Order_Date'] < data_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Clima
linhas_selecionadas = df1['Weatherconditions'].isin(weather_options)
df1 = df1.loc[linhas_selecionadas, :]

###############################
# Layout no Streamlit
# executar o arquivo digite no terminal dentro da pasta onde se localiza o arquivo ->
# streamlit run 'nome_do_arquivo.py'
###############################

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Em Construção', 'Em Contrução'])

with tab1:
    with st.container():
        st.title('Overal Metrics')
        col1, col2 = st.columns(2, gap='large')

        with col1:
            qtde = df1['Delivery_person_ID'].nunique()
            col1.metric('Entregadores únicos', qtde)

        with col2:
            media = distance(df1)
            col2.metric('Média Restaurantes x Locais Entrega', media)


    with st.container():
        st.markdown("""---""")
        st.title('Tempo médio de entrega por cidade')
        cols3 = ['Time_taken(min)', 'City']
        linhas = df1['City'] != 'NaN'

        med_dvp3 = df1.loc[linhas, cols3].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
        med_dvp3.columns = ['Time_taken(min)_mean', 'Time_taken(min)_std']
        med_dvp3 = med_dvp3.reset_index()
        st.dataframe(med_dvp3)

    with st.container():
        st.markdown("""---""")
        st.title('O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido.')
        cols4 = ['Time_taken(min)', 'City', 'Type_of_order']
        groupy4 = ['City', 'Type_of_order']
        linhas = df1['City'] != 'NaN'

        med_dvp4 = df1.loc[linhas, cols4].groupby(groupy4).agg({'Time_taken(min)': ['mean', 'std']})
        med_dvp4.columns = ['Time_taken(min)_mean', 'Time_taken(min)_std']
        med_dvp4 = med_dvp4.reset_index()
        st.dataframe(med_dvp4)


    with st.container():
        st.markdown("""---""")
        st.title('O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.')
        cols5 = ['Time_taken(min)','City', 'Road_traffic_density']
        groupy5 = ['City', 'Road_traffic_density']
        linhas = (df1['Road_traffic_density'] != 'NaN') & (df1['City'] != 'NaN')

        med_dvp5 = df1.loc[linhas, cols5].groupby(groupy5).agg({'Time_taken(min)': ['mean', 'std']})
        med_dvp5.columns = ['Time_taken(min)_mean', 'Time_taken(min)_std']
        med_dvp5 = med_dvp5.reset_index()
        st.dataframe(med_dvp5)

    with st.container():
        st.markdown("""---""")
        st.title('O tempo médio de entrega durantes os Festivais.')
        cols6 = ['Festival', 'Time_taken(min)']
        linhas = df1['Festival'] == 'Yes'
        tmp_medio = df1.loc[linhas, cols6].groupby('Festival').mean().reset_index()
        st.dataframe(tmp_medio)



