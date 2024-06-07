import pandas as pd
from datetime import datetime 

### VAMOS PEGAR O ARQUIVO JSON

df = pd.read_json('C:/Users/edude/OneDrive/Documentos/GitHub/WebScraping/Webscraping-MercadoLivre/project-MercadoLivre/data.jsonl', lines=True)

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
