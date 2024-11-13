import pandas as pd
import streamlit as st

def process_csv(file_path):
    try:
        # Carregar o CSV
        df = pd.read_csv(file_path)
        
        # Exibir as colunas do CSV
        st.write("Colunas do CSV:", df.columns)

        # Verificar se as colunas essenciais existem no CSV
        required_columns = ['Data/Hora', 'Consumo em kWh', 'Custo Total']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Erro: Colunas ausentes no arquivo CSV: {', '.join(missing_columns)}")
            return None  # Retorna None se faltarem colunas essenciais

        # Remover espaços extras nas colunas
        df.columns = df.columns.str.strip()
        
        # Converter a coluna 'Data/Hora' para o formato datetime
        df['Data/Hora'] = pd.to_datetime(df['Data/Hora'], errors='coerce')
        
        # Converter 'Consumo em kWh' e 'Custo Total' para numérico, com erro como NaN
        df['Consumo em kWh'] = pd.to_numeric(df['Consumo em kWh'], errors='coerce')
        df['Custo Total'] = pd.to_numeric(df['Custo Total'], errors='coerce')
        
        # Verificar se há valores ausentes nas colunas críticas
        if df['Consumo em kWh'].isna().any():
            st.warning("Há valores ausentes na coluna 'Consumo em kWh'. Alguns dados podem não ser processados corretamente.")
        
        if df['Custo Total'].isna().any():
            st.warning("Há valores ausentes na coluna 'Custo Total'. Alguns dados podem não ser processados corretamente.")
        
        # Criar uma coluna de data sem a hora
        df['Data'] = df['Data/Hora'].dt.date
        
        # Exibir as primeiras linhas do DataFrame após o processamento
        st.write("Primeiras linhas do DataFrame processado:", df.head())
        
        return df
    
    except Exception as e:
        st.error(f"Erro ao processar o arquivo CSV: {e}")
        return None
