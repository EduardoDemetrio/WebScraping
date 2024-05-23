import pandas as pd
from datetime import datetime 
import sqlite3

### VAMOS PEGAR O ARQUIVO JSON

df = pd.read_json('C:/Users/edude/OneDrive/Documentos/GitHub/WebScraping/Webscraping-MercadoLivre/ColetaDados/data.jsonl', lines=True)

df = pd.DataFrame(df)
### VAMOS ADICIONAR COLUNA DE SOURCE E ID
df['_source'] = "https://lista.mercadolivre.com.br/iphone"

df.insert(0, 'ID', range(1, len(df)+1))

### INDEXANDO UMA DATA DE COLETA
df['_data_coleta'] = datetime.now()

### TRATANDO OS DADOS
df['valor_antigo'] = df['valor_antigo'].fillna(0).astype(float)
df['Valor_atual'] = df['Valor_atual'].fillna(0).astype(float)
df['avaliacao'] = df['avaliacao'].fillna(0).astype(float)
df['Quantidade de avaliação'] = df['Quantidade de avaliação'].str.replace('(','').str.replace(')','').fillna(0)
df['Quantidade de avaliação'] = df['Quantidade de avaliação'].astype(int)
print(df) 

# ### CRIANDO UMA CONEXAO COM SQLITE
# conexao = sqlite3.connect('../data/quotes.db')

# ### SALVANDO DATAFRAME NO BANCO DE DADOS SQLITE
# df.to_sql('mercadoLivre_iphone_itens',conexao, if_exists=='replace', index=False)

# conexao.close()


