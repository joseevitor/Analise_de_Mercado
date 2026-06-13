import streamlit as st
import requests 
import pandas as pd
import time

@st.cache_data
def csv_convert(df):
    return df.to_csv(index = False).encode('utf-8')

def success_message():
    success = st.success('Arquivo baixado com sucesso!', icon="✅")
    time.sleep(5)
    success.empty()

st.title('DADOS BRUTOS')

url = 'https://labdados.com/produtos'

response = requests.get(url)
data = pd.DataFrame.from_dict(response.json())
data['Data da Compra'] = pd.to_datetime(data['Data da Compra'], format = '%d/%m/%Y')

with st.expander('Colunas'):
    columns = st.multiselect('Selecione as colunas', list(data.columns), list(data.columns))

st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do produto'):
    products = st.multiselect('Selecione os produtos', data['Produto'].unique(), data['Produto'].unique())
with st.sidebar.expander('Preço do produto'):
    price = st.slider('Selecione o preço', 0, 5000, (0, 5000))
with st.sidebar.expander('Data da Compra'):
    date_of_purchase = st.date_input('Selecione a data', (data['Data da Compra'].min(), data['Data da Compra'].max()))
with st.sidebar.expander('Categoria do produto'):
    cathegory = st.multiselect('Selecione as categorias', data['Categoria do Produto'].unique(), data['Categoria do Produto'].unique())
with st.sidebar.expander('Frete da venda'):
    shipping = st.slider('Frete', 0,250, (0,250))
#with st.sidebar.expander('Data da compra'):
 #   data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))
with st.sidebar.expander('Vendedor'):
    sellers = st.multiselect('Selecione os vendedores', data['Vendedor'].unique(), data['Vendedor'].unique())
with st.sidebar.expander('Local da compra'):
    local_of_purchase = st.multiselect('Selecione o local da compra', data['Local da compra'].unique(), data['Local da compra'].unique())
with st.sidebar.expander('Avaliação da compra'):
    evaluation = st.slider('Selecione a avaliação da compra',1,5, value = (1,5))
with st.sidebar.expander('Tipo de pagamento'):
    payment_type = st.multiselect('Selecione o tipo de pagamento',data['Tipo de pagamento'].unique(), data['Tipo de pagamento'].unique())
with st.sidebar.expander('Quantidade de parcelas'):
    installments_qtt = st.slider('Selecione a quantidade de parcelas', 1, 24, (1,24))

query = '''
Produto in @products and \
`Categoria do Produto` in @cathegory and \
@price[0] <= Preço <= @price[1] and \
@date_of_purchase[0] <= `Data da Compra` <= @date_of_purchase[1] and \
@shipping[0] <= Frete <= @shipping[1] and \
Vendedor in @sellers and \
`Local da compra` in @local_of_purchase and \
@evaluation[0] <= `Avaliação da compra` <= @evaluation[1] and \
`Tipo de pagamento` in @payment_type and \
@installments_qtt[0] <= `Quantidade de parcelas` <= @installments_qtt[1]




'''

filtered_data = data.query(query)
filtered_data = filtered_data[columns]

st.dataframe(filtered_data)

st.markdown(f'A tabela possui :blue[{filtered_data.shape[0]}] linhas e :blue[{filtered_data.shape[1]}] colunas')

st.markdown('Escreva um nome para o arquivo')
column1, column2 = st.columns(2)
with column1:
    file_name = st.text_input('', label_visibility='collapsed', value='dados')
    file_name += '.csv'
with column2:
    st.download_button('Fazer o download da tabela em csv', data= csv_convert(filtered_data), file_name = file_name, mime='text/csv', on_click= success_message)
