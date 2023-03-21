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

st.set_page_config(page_title='Visão Empresa', page_icon='', layout='wide')

# --------------Funções---------------#
def country_maps(df1):
    cols6 = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
    linhas = (df1['Road_traffic_density'] != 'NaN') & (df1['City'] != 'NaN')
    group6 = ['City', 'Road_traffic_density']

    df6 = df1.loc[linhas, cols6].groupby(group6).median().reset_index()

    map_ = folium.Map(zoom_start=11)

    for index, location_info in df6.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
                       location_info['Delivery_location_longitude']],
                      popup=location_info[['City', 'Road_traffic_density']]).add_to(map_)

    folium_static(map_, width=1024, height=600)


def order_share_by_week(df1):
    # Agrupando os dados
    cols5_a = ['ID', 'week_of_year']
    cols5_b = ['Delivery_person_ID', 'week_of_year']

    df5_aux1 = df1.loc[:, cols5_a].groupby('week_of_year').count().reset_index()
    df5_aux2 = df1.loc[:, cols5_b].groupby('week_of_year').nunique().reset_index()

    df5_aux = pd.merge(df5_aux1, df5_aux2, how='inner')

    df5_aux['order_by_deliver'] = df5_aux['ID'] / df5_aux['Delivery_person_ID']

    # Plotando Gráfico
    fig = px.line(df5_aux, x='week_of_year', y='order_by_deliver')
    return fig


def order_by_week(df1):
    # Criar uma nova coluna semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    # Agrupando os dados
    cols2 = ['ID', 'week_of_year']
    qtde_semana = df1.loc[:, cols2].groupby('week_of_year').count().reset_index()
    # Plotando o Gráfico
    fig = px.line(qtde_semana, x='week_of_year', y='ID')

    return fig


def traffic_order_city(df1):
    # Agrupando os Dados
    cols4 = ['ID', 'Road_traffic_density', 'City']
    group = ['City', 'Road_traffic_density']
    # linhas = (df1['Road_traffic_density'] != 'NaN') & (df1['City'] != 'NaN')

    df4_aux = df1.loc[:, cols4].groupby(group).count().reset_index()

    # Plotando o gráfico
    fig = px.scatter(df4_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    return fig



def traffic_order_share(df1):
    # Agrupando os dados
    cols3 = ['ID', 'Road_traffic_density']
    # linhas = df1['Road_traffic_density'] != 'NaN'
    df1_aux = df1.loc[:, cols3].groupby('Road_traffic_density').count().reset_index()

    # Criar uma nova coluna e calcular o percentual (Total de Cada ID / Soma total)
    df1_aux['entregas_perc'] = df1_aux['ID'] / df1_aux['ID'].sum()

    # Exibindo Gráfico
    fig = px.pie(df1_aux, values='entregas_perc', names='Road_traffic_density')

    return fig


# Função Plotar Gráfico Barras coluna [ID, Order Date]
def order_metric(df1):
    cols1 = ['ID', 'Order_Date']
    qtde = df1.loc[:, cols1].groupby('Order_Date').count().reset_index()

    # Plotando o Gráfico
    fig = px.bar(qtde, x='Order_Date', y='ID')

    return fig


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

# -----------Inicio da Estrutura lógica do código--------------------------- #
# Import Dataset
df = pd.read_csv('train.csv')
# ----------------

# Limpando os dados
df1 = clean_code(df)
# -------------------


###############################
# Barra Lateral no Streamlit
# executar o arquivo digite no terminal dentro da pasta onde se localiza o arquivo ->
# streamlit run 'nome_do_arquivo.py'
###############################

st.header('MarketPlace - Visão Cliente')

image = Image.open('image_delivery.jpg')
st.sidebar.image(image, width=300, caption='Fast Delivery')

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fast Delivery in Town')
st.sidebar.markdown("""___""")

st.sidebar.markdown('## Selecione uma Data Limite')
data_slider = st.sidebar.slider('Até qual Valor?',
                                value=pd.datetime(2022, 4, 14),
                                min_value=pd.datetime(2022, 2, 11),
                                max_value=pd.datetime(2022, 4, 6),
                                format='DD-MM-YYYY')

st.sidebar.markdown("""___""")

traffic_options = st.sidebar.multiselect('Quais as condições do transito',
                                         ['Low', 'Medium', 'High', 'Jam'],
                                         default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Comunidade DS')

# Filtros no DataFrame
linhas_selecionadas = df1['Order_Date'] < data_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

###############################
# Layout no Streamlit
# executar o arquivo digite no terminal dentro da pasta onde se localiza o arquivo ->
# streamlit run 'nome_do_arquivo.py'
###############################

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        # Criando os Dados
        fig = order_metric(df1)
        st.markdown('# Orders by Day')
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            fig = traffic_order_share(df1)
            st.header('Traffic Order Share')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.header('Traffic Order City')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)


with tab2:
    with st.container():
        st.markdown('# Order by Week')
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)


    with st.container():
        st.markdown('# Order Share by Week')
        fig = order_share_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)


with tab3:
    st.markdown('# Country Maps')
    country_maps(df1)
