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

st.set_page_config(page_title='Visão Entregadores', page_icon='', layout='wide')

# --------------Funções---------------#
#######################################
# ------------------------------------#

def top_delivers(df1, top_asc):
    cols7 = ['Delivery_person_ID', 'Time_taken(min)', 'City']
    linhas = df1['Time_taken(min)'] != 'NaN'
    group = ['City', 'Delivery_person_ID']
    sort = ['City', 'Time_taken(min)']

    # Agrupamento
    df7 = df1.loc[linhas, cols7].groupby(group).max().sort_values(sort, ascending=top_asc).reset_index()

    # Filtrando as Listas
    df7_aux1 = df7.loc[df7['City'] == 'Metropolitian', :].head(10)
    df7_aux2 = df7.loc[df7['City'] == 'Urban', :].head(10)
    df7_aux3 = df7.loc[df7['City'] == 'Semi-Urban', :].head(10)

    # Concatenando as Listas
    df7_aux4 = pd.concat([df7_aux1, df7_aux2, df7_aux3]).reset_index(drop=True)

    return df7_aux4


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

st.header('MarketPlace - Visão Entregadores')

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
        st.title('Overall Metrics')
        col1, col2, col3, col4 = st.columns(4, gap='large')

        with col1:
            # Maior idade dos entregadores
            # st.subheader('Maior de idade')
            maior_idade = df1['Delivery_person_Age'].max()
            col1.metric('Maior idade', maior_idade)

        with col2:
            # Menor idade dos entregadores
            # st.subheader('Menor de idade')
            menor_idade = df1['Delivery_person_Age'].min()
            col2.metric('Menor idade', menor_idade)

        with col3:
            # Melhor condição de Veículos
            # st.subheader('Melhor condição Veículos')
            melhor_cond = df1['Vehicle_condition'].max()
            col3.metric('Melhor condição', melhor_cond)

        with col4:
            # Pior condição de Veículos
            # st.subheader('Pior condição Veículos')
            pior_cond = df1['Vehicle_condition'].min()
            col4.metric('Pior condição', pior_cond)

    with st.container():
        st.markdown("""---""")
        col1, col2 = st.columns(2, gap='large')
        with col1:
            st.subheader('Avaliações médias por Entregador')
            cols3 = ['Delivery_person_ID', 'Delivery_person_Ratings']
            aval_media = df1.loc[:, cols3].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(aval_media)

        with col2:
            st.subheader('Avaliações médias por Trânsito')
            # Outra Forma fazendo Média e Desvio juntos numa mesma Função. Utilizando função de Agregação
            cols4 = ['Delivery_person_Ratings', 'Road_traffic_density']
            linhas = df1['Road_traffic_density'] != 'NaN'
            dv_med = df1.loc[linhas, cols4].groupby('Road_traffic_density').agg(
                {'Delivery_person_Ratings': ['mean', 'std']})
            dv_med.columns = ['Delivery_mean', 'Delivery_std']
            st.dataframe(dv_med)

            st.subheader('Avaliações médias por Clima')
            # Outra Forma fazendo Média e Desvio juntos numa mesma Função. Utilizando função de Agregação
            cols5 = ['Delivery_person_Ratings', 'Weatherconditions']
            linhas = df1['Weatherconditions'] != 'conditions NaN'
            med_dvp = df1.loc[linhas, cols5].groupby('Weatherconditions').agg(
                {'Delivery_person_Ratings': ['mean', 'std']})
            med_dvp.columns = ['Rating_mean', 'Rating_std']
            med_dvp = med_dvp.reset_index()
            st.dataframe(med_dvp)

    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de Entrega')
        col1, col2 = st.columns(2, gap='large')
        with col1:
            st.markdown('##### Top Entregadores mais rápidos')
            df6_aux4 = top_delivers(df1, top_asc=True)
            st.dataframe(df6_aux4)

        with col2:
            st.markdown('##### Top Entregadores mais lentos')
            df7_aux4 = top_delivers(df1, top_asc=False)
            st.dataframe(df7_aux4)