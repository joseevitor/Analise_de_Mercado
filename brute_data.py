import streamlit as st
import requests 
import pandas as pd

st.title('DADOS BRUTOS')

url = 'https://labdados.com/produtos'

response = requests.get(url)
data = pd.DataFrame.from_dict(response.json())
data['Data da Compra'] = pd.to_datetime(data['Data da Compra'], format = '%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(data.columns), list(data.columns))

st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do produto'):
    products = st.multiselect('Selecione os produtos', data['Produto'].unique(), data['Produto'].unique())
with st.sidebar.expander('Preço do produto'):
    price = st.slider('Selecione o preço', 0, 5000, (0, 5000))
with st.sidebar.expander('Data da Compra'):
    date_of_purchase = st.date_input('Selecione a data', (data['Data da Compra'].min(), data['Data da Compra'].max()))
st.dataframe(data)