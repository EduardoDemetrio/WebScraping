import pandas as pd
from datetime import datetime
import streamlit as st
from collections import Counter

### VAMOS PEGAR O ARQUIVO JSON

df = pd.read_json('C:/Users/edude/OneDrive/Documentos/GitHub/WebScraping/Webscraping-MercadoLivre/ColetaDados/data.jsonl', lines=True)

df_final = pd.DataFrame(df)
### VAMOS ADICIONAR COLUNA DE SOURCE E ID
df_final['_source'] = "https://lista.mercadolivre.com.br/iphone"

df_final.insert(0, 'ID', range(1, len(df_final)+1))

### INDEXANDO UMA DATA DE COLETA
df_final['_data_coleta'] = datetime.now()

### TRATANDO OS DADOS
df_final['valor_antigo'] = df_final['valor_antigo'].fillna(0).astype(float)
df_final['Valor_atual'] = df_final['Valor_atual'].fillna(0).astype(float)
df_final['avaliacao'] = df_final['avaliacao'].fillna(0).astype(float)
df_final['Quantidade de avaliação'] = df_final['Quantidade de avaliação'].str.replace('(','').str.replace(')','').fillna(0)
df_final['Quantidade de avaliação'] = df_final['Quantidade de avaliação'].astype(int)


def aux_analise(df):
    out = df.isna().sum().reset_index().rename(columns={'index':'Variavel',0:'Contagem_NA'})
    col = df.dtypes.reset_index().rename(columns={'index':'Variavel',0:'Tipo'})

    out = pd.merge(out,col, on='Variavel', how = 'inner')

    col=df.nunique().reset_index().rename(columns={'index':'Variavel',0:'Dado Unico'})

    out = pd.merge(out,col, on='Variavel', how = 'inner')

    col=[]
    for linha in range(0, out.shape[0]):
        for linhas in range(0, out.shape[0]):
            variavel = linhas
        var = out.iloc[linha]['Variavel']
        out_ = df_final[var].value_counts().index.to_list()[0:variavel]
        col.append(out_)
    out['Analise'] = col

    out['Identificador'] = out['Tipo'].apply(lambda x: 1 if x=='object' else 0)

    qtds =[]
    for linha in range(0, out.shape[0]):
        if out['Identificador'][linha] ==1:
            var = out['Variavel'].iloc[linha]
            varial = Counter(df[var])
            qtds.append(varial)
        else: 
            qtds.append(0)


    out['Qtds'] = qtds

    out = out.drop(columns={'Identificador'})
    return out 

def extrair_modelo(texto):
    palavra = 'iPhone'
    if palavra in texto:
        start = texto.find(palavra)
        end = start + len(palavra) + 3  # 6 caracteres de "iPhone" + 3 caracteres
        return texto[start:end]
    return ''


def extrair_valor(texto):
    try:
        valor = int(texto.split(' ')[1])
        return valor
    except (IndexError, ValueError):
        return 0



df_final['modelo'] = df_final['brand'].apply(extrair_modelo)
df_final['Valor_parcelamento'] = df_final['Parcelamento'].apply(extrair_valor)*10


tabela_resumo = aux_analise(df_final)

print(tabela_resumo)

# print(df_final)


st.title('Pesquisa de Mercado - Celular - Iphone')

### VAMOS CRIAR AQUI OS DASHBOARD

### CRIANDO UM FILTRO DE MODELOS
opcoes_modelos = ['Todos'] +list(df_final['modelo'].unique())

selecao = st.sidebar.selectbox("Modelos", opcoes_modelos)

if selecao != 'Todos':
    df_filtered = df_final[df_final['modelo']==selecao]
else:
    df_filtered= df_final


### KPI

st.subheader('KPIs principais do negócio')
col1,col2 = st.columns([2,2])

## QUANTIDADE TOTAL DE CASOS
total_itens = df_filtered.shape[0]
col1.metric(label="Número total de itens", value=total_itens ,delta_color="off")

## VALOR MAIS EM CONTA ENCONTRADO
em_conta = df_filtered['Valor_atual'].min().astype(float)
col2.metric(label="Valor mais em conta encontrado no mercado livre", value=em_conta ,delta_color="off")

## VALOR MÉDIO EM CASOS PARCELADOS
em_conta = df_filtered['Valor_atual'].mean().__round__(2)
col1.metric(label="Preço médio (R$)", value=em_conta ,delta_color="off")

## DATA DA ÚLTIMA EXTRAÇÃO DOS DADOS
data_ult_extract = df_filtered['avaliacao'].mean().__round__(2)
col2.metric(label="Média de avaliação da divulgação", value=data_ult_extract ,delta_color="off")


st.subheader('Gráficos e tabelas - Qt. por categoria')
col1p,col2p = st.columns([4,2])

## QUANTIDADE POR IPHONE "CATEGORIA"
iphone_catg = df_filtered['modelo'].value_counts().sort_values(ascending=False)
col1p.bar_chart(iphone_catg)
col2p.write(iphone_catg)


st.subheader('Gráficos e tabelas - Média por categoria')
col1m,col2m = st.columns([4,2])
## QUANTIDADE POR IPHONE "CATEGORIA"
iphone_median = df_filtered.groupby('modelo')['Valor_atual'].mean().sort_values(ascending=False)
col1m.bar_chart(iphone_median)
col2m.write(iphone_median)



st.subheader('Base de dados')
st.write(df_filtered)

### CRIAÇÃO DE BOTÃO
col1b,col2b = st.columns([0.15,1])

### botão do link do git
col1b.link_button("Git Hub", "https://github.com/EduardoDemetrio")

### botão do csv da base
csv = df_filtered.to_csv(index=False)

col2b.download_button(
    label="Baixar CSV",
    data= csv,
    file_name='dados_filtrados.csv',
    mime='text/csv'
)