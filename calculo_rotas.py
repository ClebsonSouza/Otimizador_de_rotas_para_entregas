#pip install pyexcel
#pip install pyexcel-xls

import pyexcel as p
import pandas as pd
import streamlit as st
from io import BytesIO
import re
from math import radians, sin, cos, sqrt, atan2
import networkx as nx
from networkx.algorithms.approximation import traveling_salesman_problem
import time


#dir_modelos = r'C:\Users\User\Desktop\Codigos'

def remove_illegal_characters(df):
    df = df.applymap(lambda x: re.sub(r'[\000-\010]|[\013-\014]|[\016-\037]', '', str(x)) if isinstance(x, str) else x)
    return df

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6378.1  # Raio da Terra em km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return (R * c) * 1.82

def process_data(df):

    if df.shape[0] < 2:
            raise ValueError("O DataFrame precisa conter pelo menos dois pontos (inicial e um intermediário).")

    pontos = [(row['Local'], row['Lat'], row['Long']) for _, row in df.iterrows()]
    nomes = [p[0] for p in pontos]
    coord_map = {p[0]: (p[1], p[2]) for p in pontos}

    # Criar grafo completo com distâncias haversine como pesos
    G = nx.Graph()
    for i in range(len(pontos)):
        for j in range(i + 1, len(pontos)):
            nome_a, lat_a, lon_a = pontos[i]
            nome_b, lat_b, lon_b = pontos[j]
            dist = haversine_distance(lat_a, lon_a, lat_b, lon_b)
            G.add_edge(nome_a, nome_b, weight=dist)

    # Resolver TSP com heurística aproximada (sem ponto fixo suportado diretamente)
    ciclo = traveling_salesman_problem(G, cycle=True)

    # Reorganizar para iniciar e terminar no ponto_inicial
    ponto_inicial = nomes[0]
    if ciclo[0] != ponto_inicial:
        idx = ciclo.index(ponto_inicial)
        ciclo = ciclo[idx:] + ciclo[1:idx+1]

    # Construir roteiro detalhado
    roteiro = []
    distancia_total = 0
    for i in range(len(ciclo) - 1):
        a, b = ciclo[i], ciclo[i + 1]
        d = haversine_distance(coord_map[a][0], coord_map[a][1], coord_map[b][0], coord_map[b][1])
        roteiro.append((a, b, round(d, 2)))
        distancia_total += d

    return round(distancia_total, 2), roteiro


# Função para autenticação com múltiplos usuários
def autenticar_usuario(usuario, senha):
    # Dicionário com usuários e suas respectivas senhas
    credenciais = {        
        "teste": "4321",
        # Adicione mais usuários aqui
    }
    
    # Verifica se o usuário está no dicionário e se a senha está correta
    if usuario in credenciais and credenciais[usuario] == senha:
        return True
    else:
        return False

# Verifica se o usuário já está autenticado
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
    

# Tela de login com formulário para permitir envio com "Enter"
if not st.session_state['autenticado']:
    st.title("Otimização de Rotas")
    
        
    # Formulário de login
    with st.form("login_form"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        
        # Botão de enviar (submit), que também é acionado ao pressionar "Enter"
        submit_button = st.form_submit_button("Entrar")
    
    # Verifica se o formulário foi enviado
    if submit_button:
        if autenticar_usuario(usuario, senha):
            st.session_state['autenticado'] = True  # Marca o estado de autenticação como verdadeiro

            st.success(f"Login bem-sucedido! Bem-vindo, {usuario}!")

            time.sleep(1)

            st.rerun()          
            
        else:
            st.error("Usuário ou senha incorretos.")  # Exibe erro se a autenticação falhar
else:    
    # Aplicação principal que é exibida após o login bem-sucedido
    st.sidebar.title("🚚 Aplicação de Otimização de Rotas")    

    st.sidebar.write("  Bem-vindo à ferramenta de otimização de rotas com base em coordenadas geográficas! \
                        Desenvolvida para ajudar no planejamento logístico de entregas, \
                         a aplicação calcula a menor rota possível entre diversos pontos, retornando ao ponto de origem.")

    st.sidebar.write("-------------------------------------")

    st.sidebar.write("📌 Funcionalidades principais:")

    st.sidebar.write(" - Leitura automatizada de planilhas com coordenadas")
    st.sidebar.write(" - Geração de rota otimizada")   
    st.sidebar.write(" - Estimativa de tempo e distância total")   
    st.sidebar.write("-------------------------------------")

    st.sidebar.warning('⚠️ Atenção: Esta versão está em modo de testes. Resultados podem sofrer ajustes e melhorias nas próximas atualizações.')

    # Estado inicial para as variáveis
    if 'reset' not in st.session_state:
        st.session_state['reset'] = 'Não'

    with st.container():
        st.title("Otimização de Rotas")        

        uploaded_file = st.file_uploader("Escolha o arquivo Excel no formato padrão:", type=["xlsx"])
        
        if uploaded_file is not None:            

            if uploaded_file is not None:
                result = pd.read_excel(uploaded_file)

            result = pd.DataFrame(result)

            result[['Lat', 'Long']] = result['Coordenadas'].str.split(',', expand=True)
            result['Lat'] = result['Lat'].str.strip().astype(float)
            result['Long'] = result['Long'].str.strip().astype(float)

            dist_total, roteiro = process_data(result)
            result = remove_illegal_characters(result)

            #st.dataframe(result.drop(columns = ['Lat', 'Long']))

            #st.table(result.drop(columns = ['Lat', 'Long']))

            st.success('Arquivo carregado com sucesso!!!!!!!')

            if st.button("Calcular rota"):

                with st.spinner("🕒 Calculando a melhor rota, aguarde..."):
                    # ⏳ Aqui vai o cálculo da rota
                    time.sleep(3)  # simula o tempo de processamento
                    

                # progress_bar = st.progress(0)
                # with st.spinner("🚀 Otimizando rota..."):
                #     for percent in range(1, 101):
                #         time.sleep(0.02)  # simula cálculo
                #         progress_bar.progress(percent)

                trecho_0 = []
                trecho_1 = []
                dist = []


                for trecho in roteiro:
                    trecho_0.append(trecho[0])
                    trecho_1.append(trecho[1])
                    dist.append(trecho[2])

                data = {'Início': trecho_0,
                        'Fim': trecho_1,
                        'Distância': dist,}              
                
                
                df_rota_otimizada = pd.DataFrame(data)

                qtd_entregas = len(df_rota_otimizada) -1

                dist_total = df_rota_otimizada['Distância'].sum()

                velocidade_media_kmh = 50

                df_rota_otimizada['Tempo Médio'] = round(df_rota_otimizada['Distância']/velocidade_media_kmh*60, 2)
                
                tempo_horas = dist_total / velocidade_media_kmh
                horas = int(tempo_horas)
                minutos = int((tempo_horas - horas) * 60)
                temp_total = f"{horas}h {minutos}min"                

                df_rota_otimizada['Distância'] = df_rota_otimizada['Distância'].apply(lambda x: str(x) + ' Km')

                df_rota_otimizada['Tempo Médio'] = df_rota_otimizada['Tempo Médio'].apply(lambda x: str(x) + ' Min')               
                

                col1, col2, col3, col_spacer2 = st.columns([0.7, 0.7, 0.7, 0.5])

                with col1:
                    st.markdown(f"""
                        <div style="background-color:#FF4B4B;padding:2px;border-radius:10px;text-align:center;color:white; max-width:150px; margin:left;">
                            <span style="font-size:16px;">📏Distância Total</span>
                            <p style="font-size:24px;font-weight:bold;margin:0;">{dist_total:.2f} km</p>
                        </div>
                        """, unsafe_allow_html=True)


                with col2:
                    st.markdown(f"""
                        <div style="background-color:#FF4B4B;padding:2px;border-radius:10px;text-align:center;color:white; max-width:150px; margin:left;">
                            <span style="font-size:16px;">📍Pontos Visitados</span>
                            <p style="font-size:24px;font-weight:bold;margin:0;">{qtd_entregas}</p>
                        </div>
                        """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                        <div style="background-color:#FF4B4B;padding:2px;border-radius:10px;text-align:center;color:white; max-width:150px; margin:left;">
                            <span style="font-size:16px;">⏱️Tempo Estimado</span>
                            <p style="font-size:24px;font-weight:bold;margin:0;">{temp_total}</p>
                        </div>
                        """, unsafe_allow_html=True)                    

                st.title("_________________________")                

                st.dataframe(df_rota_otimizada)

                #st.table(df_rota_otimizada)

                #AgGrid(df_rota_otimizada)

                # Cria um arquivo Excel em memória
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_rota_otimizada.to_excel(writer, index=False, sheet_name='melhor_rota')                    
                
                output.seek(0)                

                st.download_button(
                    label="📤Baixar planilha",
                    data=output,
                    file_name="melhor_rota.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                
                if st.button("Limpar"):
                    st.session_state['reset'] = False        
                    st.rerun() 

        else:
            st.warning("Faça o upload do arquivo!")

        if st.button("Sair"):
            st.session_state['autenticado'] = False  # Reseta o estado de autenticação
            st.rerun()  


####################################################################################
####################################################################################