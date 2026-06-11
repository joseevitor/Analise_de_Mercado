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

st.title("Análise de Mercado/ atlerar cadastro")
# st.write("Projeto da disciplina")

url = 'https://labdados.com/produtos'
response = requests.get(url)
data = pd.DataFrame.from_dict(response.json())
data['Data da Compra'] = pd.to_datetime(data['Data da Compra'], format = '%d/%m/%Y')

### revenue tables
receita_estados = data.groupby('Local da compra')[['Preço']].sum()
receita_estados = data.drop_duplicates(subset= 'Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending = False)

receita_mensal = data.set_index('Data da Compra').groupby(pd.Grouper(freq='ME'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name()

receita_categorias = data.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending = False)

### Sales quantity tables

### Sellers tables
sellers = pd.DataFrame(data.groupby('Vendedor')['Preço'].agg(['sum', 'count']))

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

fig_receita_estados = px.bar(receita_estados.head(),
                            x = 'Local da compra',
                            y = 'Preço',
                            text_auto = True,
                            title = 'Top estados (receita)')

fig_receita_estados.update_layout(yaxis_title = 'Receita')

fig_receita_categorias = px.bar(receita_categorias,
                                text_auto = True,
                                title = 'Receita por Categoria')

fig_receita_categorias.update_layout(yaxis_title = 'Receita')

# View on streamlit
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(['Receita', 'Quantidade de vendas', 'Setores', 'Fornecedores', 'Cadastro', 'Assistente', 'Beneficiários', 'Produtos em vencimento'])

# Cadastro teria de ser para funconarios e clientes, 
# seria necessário fazer os cadastros dos produtos???
# O cadastro ainda não foi definido e a dúvida será trada com o professor...
# De qualquer forma precisa existir um CRUD


with tab1:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', format_number(data['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_receita, use_container_width= True)
        st.plotly_chart(fig_receita_estados, use_container_width= True)

    with coluna2:
        st.metric('Quantidade de vendas', format_number(data.shape[0]))
        st.plotly_chart(fig_receita_mensal, use_container_width= True)
        st.plotly_chart(fig_receita_categorias, use_container_width= True)

with tab2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', format_number(data['Preço'].sum(), 'R$'))
        sales_by_state = pd.DataFrame(data.groupby('Local da compra')['Preço'].count())
        sales_by_state = data.drop_duplicates(subset = 'Local da compra', 'lat', 'lon')
    with coluna2:
        st.metric('Quantidade de vendas', format_number(data.shape[0]))

with tab3:
    sellers_qtt = st.number_input('Quantidade de vendedores', 2, 10, 5)
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', format_number(data['Preço'].sum(), 'R$'))
        #fig_receita_vendedores = px.bar(sellers[['sum']].sort_values('sum', ascending=False).head(sellers_qtt)
             #                           x = 'sum')
    with coluna2:
        st.metric('Quantidade de vendas', format_number(data.shape[0]))

with tab4:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', format_number(data['Preço'].sum(), 'R$'))

    with coluna2:
        st.metric('Quantidade de vendas', format_number(data.shape[0]))
   
with tab5:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', format_number(data['Preço'].sum(), 'R$'))

    with coluna2:
        st.metric('Quantidade de vendas', format_number(data.shape[0]))

with tab6:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', format_number(data['Preço'].sum(), 'R$'))

    with coluna2:
        st.metric('Quantidade de vendas', format_number(data.shape[0]))
   

with tab7:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', format_number(data['Preço'].sum(), 'R$'))

    with coluna2:
        st.metric('Quantidade de vendas', format_number(data.shape[0]))
   
with tab8:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', format_number(data['Preço'].sum(), 'R$'))

    with coluna2:
        st.metric('Quantidade de vendas', format_number(data.shape[0]))


st.dataframe(data)
