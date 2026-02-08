# Arquivo 1: app_saude_streamlit.py
import streamlit as st
import json
from datetime import datetime

ARQUIVO = "pacientes.json"

# Funções para carregar e salvar pacientes
def carregar_pacientes():
    try:
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    except:
        return []

def salvar_pacientes(pacientes):
    with open(ARQUIVO, "w") as f:
        json.dump(pacientes, f, indent=4)

# Funções de classificação
def classificar_imc(IMC):
    if IMC < 18.5: return "Magreza"
    elif IMC < 25: return "Eutrófico"
    elif IMC < 30: return "Sobrepeso"
    elif IMC < 35: return "Obesidade Grau I"
    elif IMC < 40: return "Obesidade Grau II"
    else: return "Obesidade Grau III"

def classificar_pressao(sistolica, diastolica):
    if sistolica < 120 and diastolica < 80: return "Pressão normal"
    elif 120 <= sistolica < 130 and diastolica < 80: return "Elevada"
    elif 130 <= sistolica < 140 or 80 <= diastolica < 90: return "Hipertensão Grau I"
    elif 140 <= sistolica < 180 or 90 <= diastolica < 120: return "Hipertensão Grau II"
    else: return "Hipertensão Grave"

def classificar_glicemia(glicemia):
    if glicemia < 100: return "Normal"
    elif glicemia < 126: return "Alterada"
    else: return "Diabetes"

# Funções para registrar dados
def registrar_imc(paciente):
    peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f")
    altura = st.number_input("Altura (m)", min_value=0.0, format="%.2f")
    if st.button("Registrar IMC"):
        if peso > 0 and altura > 0:
            IMC = peso / (altura*altura)
            classificacao = classificar_imc(IMC)
            paciente['historico_imc'].append({
                "peso": peso,
                "altura": altura,
                "IMC": IMC,
                "classificacao_imc": classificacao,
                "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            salvar_pacientes(pacientes)
            st.success(f"IMC registrado: {IMC:.2f} ({classificacao})")
        else:
            st.error("Valores inválidos.")

def registrar_pressao(paciente):
    sistolica = st.number_input("Pressão sistólica", min_value=0)
    diastolica = st.number_input("Pressão diastólica", min_value=0)
    comentario = st.text_input("Comentário breve (opcional)")
    if st.button("Registrar Pressão"):
        classificacao = classificar_pressao(sistolica, diastolica)
        paciente['historico_pressao'].append({
            "sistolica": sistolica,
            "diastolica": diastolica,
            "classificacao_pa": classificacao,
            "comentario": comentario,
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        salvar_pacientes(pacientes)
        st.success(f"Pressão registrada: {sistolica}/{diastolica} mmHg ({classificacao})")

def registrar_glicemia(paciente):
    glicemia = st.number_input("Glicemia (mg/dL)", min_value=0.0, format="%.2f")
    comentario = st.text_input("Comentário breve (opcional)")
    if st.button("Registrar Glicemia"):
        classificacao = classificar_glicemia(glicemia)
        paciente['historico_glicemia'].append({
            "glicemia": glicemia,
            "classificacao_glicemia": classificacao,
            "comentario": comentario,
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        salvar_pacientes(pacientes)
        st.success(f"Glicemia registrada: {glicemia} mg/dL ({classificacao})")

# Exibir histórico
def exibir_historico(paciente):
    st.subheader(f"Histórico de {paciente['perfil']['nome']}")
    st.markdown("**IMC:**")
    for r in paciente['historico_imc']:
        st.write(f"{r['data_hora']} - {r['peso']}kg, {r['altura']}m, IMC: {r['IMC']:.2f} ({r['classificacao_imc']})")
    st.markdown("**Pressão:**")
    for r in paciente['historico_pressao']:
        comentario = f" | {r['comentario']}" if r['comentario'] else ""
        st.write(f"{r['data_hora']} - {r['sistolica']}/{r['diastolica']} mmHg ({r['classificacao_pa']}){comentario}")
    st.markdown("**Glicemia:**")
    for r in paciente['historico_glicemia']:
        comentario = f" | {r['comentario']}" if r['comentario'] else ""
        st.write(f"{r['data_hora']} - {r['glicemia']} mg/dL ({r['classificacao_glicemia']}){comentario}")

# App principal
st.title("Protótipo Saúde")
pacientes = carregar_pacientes()
menu = ["Login Paciente", "Login Profissional", "Criar Paciente"]
opcao = st.sidebar.selectbox("Menu", menu)

if opcao == "Criar Paciente":
    st.subheader("Cadastro de Paciente")
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=0)
    sexo = st.text_input("Sexo")
    raca = st.text_input("Raça")
    residencia = st.text_input("Local de residência")
    nascimento = st.text_input("Local de nascimento")
    profissao = st.text_input("Profissão")
    outros = st.text_input("Outras informações (opcional)")
    senha = st.text_input("Senha", type="password")
    if st.button("Criar Paciente"):
        perfil = {"nome": nome, "idade": idade, "sexo": sexo, "raca": raca,
                  "residencia": residencia, "nascimento": nascimento,
                  "profissao": profissao, "outros": outros}
        paciente = {"perfil": perfil, "senha": senha, "historico_imc": [], "historico_pressao": [], "historico_glicemia": []}
        pacientes.append(paciente)
        salvar_pacientes(pacientes)
        st.success(f"Paciente {nome} criado com sucesso!")

elif opcao == "Login Paciente":
    st.subheader("Login Paciente")
    nome = st.text_input("Nome do paciente")
    senha = st.text_input("Senha", type="password")
    paciente_logado = None
    if st.button("Login"):
        for p in pacientes:
            if p['perfil']['nome'] == nome and p['senha'] == senha:
                paciente_logado = p
                break
        if paciente_logado:
            st.success(f"Bem-vindo(a), {nome}!")
            aba = st.radio("Escolha uma ação:", ["Registrar IMC", "Registrar Pressão", "Registrar Glicemia", "Ver histórico"])
            if aba == "Registrar IMC":
                registrar_imc(paciente_logado)
            elif aba == "Registrar Pressão":
                registrar_pressao(paciente_logado)
            elif aba == "Registrar Glicemia":
                registrar_glicemia(paciente_logado)
            elif aba == "Ver histórico":
                exibir_historico(paciente_logado)
        else:
            st.error("Nome ou senha incorretos.")

elif opcao == "Login Profissional":
    st.subheader("Login Profissional")
    senha = st.text_input("Senha do profissional", type="password")
    if st.button("Login"):
        if senha == "apeiron":
            st.success("Login profissional bem-sucedido!")
            for p in pacientes:
                st.markdown(f"### {p['perfil']['nome']}")
                exibir_historico(p)
        else:
            st.error("Senha incorreta.")
