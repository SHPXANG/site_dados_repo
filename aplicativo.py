import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão Financeira - Parceiro", layout="wide")

# --- ESTILO CSS (UI/UX) ---
def apply_custom_style():
    st.markdown("""
        <style>
        /* Animação suave para os cartões */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .stMetric {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            animation: fadeIn 0.6s ease-out;
            border-bottom: 4px solid #007BFF;
        }
        /* Botão de atualizar personalizado */
        .stButton>button {
            border-radius: 20px;
            background-color: #007BFF;
            color: white;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #0056b3;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE CONEXÃO E CARREGAMENTO (CACHE DE 5 HORAS) ---
@st.cache_data(ttl=18000)
def get_data(empresa_selecionada):
    # Puxa os dados das variáveis de ambiente
    USER = st.secrets["user"]
    PASSWORD = st.secrets["password"]
    HOST = st.secrets["host"]
    PORT = st.secrets["port"]
    DBNAME = st.secrets["dbname"]
    
    db_url = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    engine = create_engine(db_url)
    
    # Nome da tabela conforme o teu script de carga
    nome_tabela = f'"tabela_{empresa_selecionada}"'
    query = f"SELECT * FROM {nome_tabela}"
    
    df = pd.read_sql(query, engine)
    
    # Tratamento de tipos
    df['Vencimento'] = pd.to_datetime(df['Vencimento'])
    df['Valor'] = df['Valor'].astype(float)
    return df

# --- TELA DE LOGIN ---
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🚀 Login Dash board Corporativo - Login")
        with st.form("login_form"):
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")
            
            if submit:
                if usuario == st.secrets["LOGIN_USER"] and senha == st.secrets["LOGIN_PASS"]:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Credenciais inválidas")
        return False
    return True

# --- CONTEÚDO PRINCIPAL ---
def main():
    apply_custom_style()
    
    st.sidebar.header("⚙️ Configurações")
    # Primeira página por padrão: Shoptan
    empresa = st.sidebar.selectbox("Selecione a Empresa", ["Shoptan", "Xangai"])
    
    if st.sidebar.button("🔄 Atualizar Dados Manualmente"):
        st.cache_data.clear()
        st.rerun()

    try:
        df = get_data(empresa)
        
        # --- CÁLCULO DE MÉTRICAS ---
        hoje = pd.Timestamp.now().normalize()
        # Valor total a receber
        total_receber = df['Valor'].sum()
        # Quantidade em aberto (todos do DF, pois o teu script já filtra os pagos)
        qtd_aberto = len(df)
        # Vencidos: Data de vencimento menor que hoje
        vencidos_df = df[df['Vencimento'] < hoje]
        qtd_vencidos = len(vencidos_df)

        # --- EXIBIÇÃO DE CARTÕES (KPIs) ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Valor a Receber", f"R$ {total_receber:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        with col2:
            st.metric("Boletos em Aberto", f"{qtd_aberto}")
        with col3:
            st.metric("Boletos Vencidos QTD", f"{qtd_vencidos}")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- GRÁFICO DE BARRAS HORIZONTAL ---
        st.subheader("💰 Soma de Valor por Processo")
        # Agrupamento conforme pedido
        chart_data = df.groupby("Processo")["Valor"].sum().sort_values(ascending=True).reset_index()
        st.bar_chart(data=chart_data, x="Processo", y="Valor", horizontal=True)

        # --- TABELA DE DADOS ---
        st.subheader("📋 Lista de Documentos Detalhada")
        # Formatando a exibição da tabela
        df_display = df[['Processo', 'numero_do_documento', 'Valor', 'Vencimento']].copy()
        df_display['Vencimento'] = df_display['Vencimento'].dt.strftime('%d/%m/%Y')
        
        st.dataframe(
            df_display, 
            use_container_width=True, 
            hide_index=True
        )

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        st.info("Verifique se as tabelas existem no banco e se as credenciais estão corretas.")

# Iniciar aplicação
if login():
    main()
