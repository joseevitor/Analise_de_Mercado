# DELETE SELECT E UPDATE SÃO NECESSARIOS, INSERT TBM PARA FAZER O CRUD NO BANCO DE DADOS

import streamlit as st
import requests 
import pandas as pd 
import plotly.express as px

st.set_page_config(layout= 'wide')

def format_number(value, prefix = ''):
    for unity in ['', 'mil']:
        if value <1000:
            return f'{prefix} {value:.2f} {unity}'
        value /= 1000
    return f'{prefix} {value:.2f} milhões'

st.title("Análise de Mercado")
# st.write("Projeto da disciplina")

url = 'https://labdados.com/produtos'
response = requests.get(url)
data = pd.DataFrame.from_dict(response.json())
data['Data da Compra'] = pd.to_datetime(data['Data da Compra'], format = '%d/%m/%Y')

## table
receita_estados = data.groupby('Local da compra')[['Preço']].sum()
receita_estados = data.drop_duplicates(subset= 'Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending = False)

receita_mensal = data.set_index('Data da Compra').groupby(pd.Grouper(freq='ME'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name()
#receita_mensal['']

## Graphics
fig_mapa_receita = px.scatter_geo(receita_estados,
                                    lat = 'lat',
                                    lon = 'lon',
                                    scope = 'south america',
                                    size = 'Preço',
                                    template = 'seaborn',
                                    hover_name = 'Local da compra',
                                    hover_data = {'lat': False, 'lon': False},
                                    title = 'Receita por estado')

fig_receita_mensal = px.line(receita_mensal,
                            x = 'Mes',
                            y = 'Preço',
                            markers = True,
                            range_y = (0, receita_mensal.max()),
                            color = 'Ano',
                            line_dash = 'Ano',
                            title = 'Receita mensal')

fig_receita_mensal.update_layout(yaxis_title = 'Receita')


# View on streamlit
coluna1, coluna2 = st.columns(2)
with coluna1:
    st.metric('Receita', format_number(data['Preço'].sum(), 'R$'))
    st.plotly_chart(fig_mapa_receita, use_container_width= True)
with coluna2:
    st.metric('Quantidade de vendas', format_number(data.shape[0]))
    st.plotly_chart(fig_receita_mensal, use_container_width= True)

st.dataframe(data)