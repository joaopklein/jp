import streamlit as st
import pandas as pd
import os
import plotly.express as px


def process_csv(file_path):
    df = pd.read_csv(file_path)
    
    # Verifique e exiba as colunas do arquivo
    st.write("Colunas do CSV:", df.columns)

    df['Data/Hora'] = pd.to_datetime(df['Data/Hora'])
    df['Consumo em kWh'] = pd.to_numeric(df['Consumo em kWh'], errors='coerce')
    df['Custo Total'] = pd.to_numeric(df['Custo Total'], errors='coerce')
    
    # Criar uma coluna de data sem a hora
    df['Data'] = df['Data/Hora'].dt.date
    return df


# Função para gerar os gráficos
def generate_graphs(df):
    # Gráfico de consumo total por dia
    consumo_diario = df.groupby('Data')['Consumo em kWh'].sum().reset_index()
    fig_consumo_diario = px.bar(consumo_diario, x='Data', y='Consumo em kWh', title='Consumo Total por Dia')

    # Gráfico de consumo médio por hora
    df['Hora'] = df['Data/Hora'].dt.hour
    consumo_hora = df.groupby('Hora')['Consumo em kWh'].mean().reset_index()
    fig_consumo_hora = px.line(consumo_hora, x='Hora', y='Consumo em kWh', title='Consumo Médio por Hora')

    # Gráfico de pizza (pico vs. noturno)
    pico = df[(df['Hora'] >= 18) | (df['Hora'] <= 6)]  # Definindo pico entre 18h e 6h
    noturno = df[(df['Hora'] > 6) & (df['Hora'] < 18)]
    consumo_pico = pico['Consumo em kWh'].sum()
    consumo_noturno = noturno['Consumo em kWh'].sum()

    fig_pizza = px.pie(names=['Pico', 'Noturno'], values=[consumo_pico, consumo_noturno],
                       title='Distribuição de Consumo (Pico x Noturno)')

    return fig_consumo_diario, fig_consumo_hora, fig_pizza


# Título do aplicativo
st.title("Análise de Consumo de Energia Residencial")

# Formulário para upload do arquivo CSV
uploaded_file = st.file_uploader("Carregue o arquivo CSV", type=["csv"])

# Verificar se o arquivo foi carregado
if uploaded_file is not None:
    # Processar o arquivo
    df = process_csv(uploaded_file)

    # Gerar os gráficos
    fig_consumo_diario, fig_consumo_hora, fig_pizza = generate_graphs(df)

    # Exibir os gráficos
    st.subheader("Consumo Total por Dia")
    st.plotly_chart(fig_consumo_diario)

    st.subheader("Consumo Médio por Hora")
    st.plotly_chart(fig_consumo_hora)

    st.subheader("Distribuição de Consumo (Pico x Noturno)")
    st.plotly_chart(fig_pizza)
