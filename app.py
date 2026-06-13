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
regioes = ['Brasil', 'Centro-Oeste', 'Nordeste', 'Norte', 'Noroeste', 'Sul', 'Sudeste']

st.sidebar.title('Filtros') 
regiao = st.sidebar.selectbox('Região', regioes)

if regiao =='Brasil':
    regiao = ''

all_years = st.sidebar.checkbox('Dados de todo o período', value = True)
if all_years:
    year = ''
else:
    year = st.sidebar.slider('Ano', 2020, 2023)

query_string = {'regiao': regiao.lower(), 'year':year}
response = requests.get(url, params=query_string)
data = pd.DataFrame.from_dict(response.json())
data['Data da Compra'] = pd.to_datetime(data['Data da Compra'], format = '%d/%m/%Y')

sellers_filter = st.sidebar.multiselect('Sellers', data['Vendedor'].unique())
if sellers_filter:
    data = data[data['Vendedor'].isin(sellers_filter)]

### revenue tables
receita_estados = data.groupby('Local da compra')[['Preço']].sum()
receita_estados = data.drop_duplicates(subset= 'Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending = False)

receita_mensal = data.set_index('Data da Compra').groupby(pd.Grouper(freq='ME'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name()

receita_categorias = data.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending = False)

### Sales quantity tables
sales_by_state = pd.DataFrame(data.groupby('Local da compra')['Preço'].count())
sales_by_state = data.drop_duplicates(subset = 'Local da compra')[['Local da compra', 'lat', 'lon']].merge(sales_by_state, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending= False)

# Sales by cathegory
sales_by_cathegory = pd.DataFrame(data.groupby('Categoria do Produto')['Preço'].count().sort_values(ascending=False))


## Sales by month
sales_by_month = pd.DataFrame(data.set_index('Data da Compra').groupby(pd.Grouper(freq = 'ME'))['Preço'].count()).reset_index()
sales_by_month['Ano'] = sales_by_month['Data da Compra'].dt.year
sales_by_month['Mes'] = sales_by_month['Data da Compra'].dt.month_name()

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

fig_sales_map = px.scatter_geo(sales_by_state,
                               lat = 'lat',
                               lon = 'lon',
                               scope = 'south america',
                               #fitbounds = 'locations',
                               template = 'seaborn',
                               size = 'Preço',
                               hover_name = 'Local da compra',
                               hover_data = {'lat':False, 'lon':False},
                               title = 'Vendas por estado',
                               )

fig_sales_by_month = px.line(sales_by_month,
                             x = 'Mes',
                             y = 'Preço',
                             markers = True,
                             range_y = (0, sales_by_month.max()),
                             color = 'Ano',
                             line_dash = 'Ano',
                             title = 'Quantidade de vendas mensal')
fig_sales_by_month.update_layout(yaxis_title='Quantidade de vendas')

# Quantidade de vendas por categoria de produto
fig_sales_by_state = px.bar(sales_by_state.head(),
                            x = 'Local da compra',
                            y = 'Preço',
                            text_auto = True,
                            title = 'Top 5 estados')
fig_sales_by_state.update_layout(yaxis_title='Quantidade de Vendas')

# Graphics about the sales by cathegory of the products
fig_sales_by_cathegory = px.bar(sales_by_cathegory,
                                text_auto = True,
                                title = 'Vendas por categoria')
fig_sales_by_cathegory.update_layout(showlegend=False, yaxis_title='Quantidade de vendas')

# View on streamlit
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(['Receita', 'Quantidade de vendas', 'Setores', 'Fornecedores', 'Cadastro', 'Assistente', 'Beneficiários', 'Produtos em vencimento'])

with tab1:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', format_number(data['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_receita, use_container_width= True)
     #   st.plotly_chart(fig_receita_estados, use_container_width= True)

    with coluna2:
        st.metric('Quantidade de vendas', format_number(data.shape[0]))
        st.plotly_chart(fig_receita_mensal, use_container_width= True)
      #  st.plotly_chart(fig, use_container_width= True)

with tab2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
     #   st.metric('Receita', format_number(data['Preço'].sum(), 'R$'))
      #  st.plotly_chart(fig_sales_map, use_container_width = True)
       # st.plotly_chart(fig_sales_by_state, use_container_width = True)


        sales_by_month = pd.DataFrame(data.set_index('Data da Compra').groupby(pd.Grouper(freq = 'ME'))['Preço'].count()).reset_index()
        sales_by_month['Ano'] = sales_by_month['Data da Compra'].dt.year
        sales_by_month['Mes'] = sales_by_month['Data da Compra'].dt.month
    with coluna2:
        st.metric('Quantidade de vendas', format_number(data.shape[0]))
      #  st.plotly_chart(fig_sales_by_month, use_container_width = True)
      #  st.plotly_chart(fig_sales_by_cathegory, use_container_width = True)
with tab3:
    sellers_qtt = st.number_input('Quantidade de vendedores', 2, 10, 5)
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita', format_number(data['Preço'].sum(), 'R$'))
        fig_receita_vendedores = px.bar(sellers[['sum']].sort_values('sum', ascending=False).head(sellers_qtt),
                                        x = 'sum',
                                        y = sellers[['sum']].sort_values('sum', ascending=False).head(sellers_qtt).index,
                                        text_auto = True,
                                        title = f'Top {sellers_qtt} sellers (receita)'
        )
        st.plotly_chart(fig_receita_vendedores)
    with coluna2:
        st.metric('Quantidade de vendas', format_number(data.shape[0]))
        fig_vendas_vendedores = px.bar(sellers[['count']].sort_values('count', ascending=False).head(sellers_qtt),
                                        x = 'count',
                                        y = sellers[['count']].sort_values('count', ascending=False).head(sellers_qtt).index,
                                        text_auto = True,
                                        title = f'Top {sellers_qtt} sellers (receita)'
        )
        st.plotly_chart(fig_vendas_vendedores)

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
