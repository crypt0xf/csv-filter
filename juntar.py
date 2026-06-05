import pandas as pd
import glob

# Procura todos os arquivos CSV da pasta
arquivos = glob.glob("*.csv")

# Lê todos os CSVs
dfs = [pd.read_csv(arquivo, dtype=str) for arquivo in arquivos]

# Junta tudo
df_final = pd.concat(dfs, ignore_index=True)

# Salva o resultado
df_final.to_csv("arquivo_unificado.csv", index=False, encoding="utf-8-sig")

print(f"{len(arquivos)} arquivos unidos com sucesso.")