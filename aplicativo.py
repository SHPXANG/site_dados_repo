import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="SHOPTAN XANGAI | Gestão Financeira",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
#  ESTILOS GLOBAIS
# ══════════════════════════════════════════════════════════════════
def inject_global_css():
    st.markdown("""
    <style>
    /* ── Google Fonts ─────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Reset & base ─────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Animações ────────────────────────────────────────────── */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(24px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse-border {
        0%   { box-shadow: 0 0 0 0 rgba(99,179,237,.45); }
        70%  { box-shadow: 0 0 0 10px rgba(99,179,237,0); }
        100% { box-shadow: 0 0 0 0 rgba(99,179,237,0); }
    }
    @keyframes shimmer {
        0%   { background-position: -1000px 0; }
        100% { background-position:  1000px 0; }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50%       { transform: translateY(-8px); }
    }
    @keyframes orb-move {
        0%,100% { transform: translate(0,0) scale(1); }
        33%      { transform: translate(60px,-40px) scale(1.08); }
        66%      { transform: translate(-40px,30px) scale(0.95); }
    }

    /* ══════════════════════════════════════════════════════════
       TELA DE LOGIN
    ══════════════════════════════════════════════════════════ */
    .login-bg {
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse at 20% 50%, rgba(0,82,165,.35) 0%, transparent 55%),
            radial-gradient(ellipse at 80% 20%, rgba(0,163,255,.22) 0%, transparent 50%),
            linear-gradient(135deg, #020c1b 0%, #0a1f3d 50%, #011427 100%);
        z-index: -10;
        overflow: hidden;
    }
    /* Grade de rotas oceânicas animada */
    .login-bg::before {
        content: '';
        position: absolute;
        inset: 0;
        background-image:
            linear-gradient(rgba(0,120,255,.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,120,255,.08) 1px, transparent 1px);
        background-size: 60px 60px;
        animation: float 8s ease-in-out infinite;
    }
    /* Orbs decorativos */
    .orb {
        position: fixed;
        border-radius: 50%;
        filter: blur(80px);
        opacity: .18;
        animation: orb-move 14s ease-in-out infinite;
        pointer-events: none;
        z-index: -5;
    }
    .orb-1 { width:500px; height:500px; background:#0052a5; top:-120px; left:-100px; animation-delay:0s; }
    .orb-2 { width:400px; height:400px; background:#00b4ff; bottom:-80px; right:-60px; animation-delay:4s; }
    .orb-3 { width:300px; height:300px; background:#0077ff; top:40%; right:20%; animation-delay:8s; }

    /* Ícone do navio animado no canto */
    .ship-deco {
        position: fixed;
        bottom: 32px;
        right: 40px;
        font-size: 80px;
        opacity: .12;
        animation: float 5s ease-in-out infinite;
        pointer-events: none;
        z-index: -1;
    }

    /* Card de login */
    .login-card {
        background: rgba(255,255,255,.06);
        backdrop-filter: blur(24px) saturate(180%);
        -webkit-backdrop-filter: blur(24px) saturate(180%);
        border: 1px solid rgba(255,255,255,.14);
        border-radius: 24px;
        padding: 48px 40px;
        max-width: 420px;
        margin: 0 auto;
        animation: fadeUp .8s ease-out;
        box-shadow:
            0 8px 32px rgba(0,0,0,.4),
            inset 0 1px 0 rgba(255,255,255,.15);
    }
    .login-logo {
        text-align: center;
        margin-bottom: 28px;
    }
    .login-logo .icon { font-size: 52px; animation: float 4s ease-in-out infinite; display:inline-block; }
    .login-logo h1 {
        font-size: 1.9rem;
        font-weight: 800;
        background: linear-gradient(90deg, #63b3ed, #90cdf4, #4299e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0 4px;
        letter-spacing: -0.5px;
    }
    .login-logo p { color: rgba(255,255,255,.5); font-size: .85rem; margin:0; }

    /* ══════════════════════════════════════════════════════════
       SIDEBAR
    ══════════════════════════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020c1b 0%, #0a1f3d 100%) !important;
        border-right: 1px solid rgba(99,179,237,.15) !important;
    }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,.07) !important;
        border: 1px solid rgba(99,179,237,.25) !important;
        border-radius: 10px !important;
    }

    /* ══════════════════════════════════════════════════════════
       MAIN CONTENT
    ══════════════════════════════════════════════════════════ */
    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px;
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(160deg, #020c1b 0%, #071429 60%, #030e1e 100%) !important;
    }

    /* ── Header ───────────────────────────────────────────── */
    .page-header {
        display: flex;
        align-items: center;
        gap: 14px;
        padding-bottom: 20px;
        border-bottom: 1px solid rgba(99,179,237,.15);
        margin-bottom: 28px;
        animation: fadeUp .5s ease-out;
    }
    .page-header .icon { font-size: 2.2rem; }
    .page-header h2 {
        margin: 0;
        font-size: 1.65rem;
        font-weight: 800;
        background: linear-gradient(90deg, #90cdf4, #63b3ed 60%, #4299e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .page-header span {
        font-size: .82rem;
        color: rgba(160,210,255,.55);
        font-weight: 400;
        margin-top: 2px;
        display: block;
    }

    /* ══════════════════════════════════════════════════════════
       KPI CARDS  (glassmorphism premium)
    ══════════════════════════════════════════════════════════ */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 20px;
        margin-bottom: 32px;
    }
    .kpi-card {
        position: relative;
        background: rgba(255,255,255,.05);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,.1);
        border-radius: 20px;
        padding: 28px 24px;
        overflow: hidden;
        animation: fadeUp .6s ease-out both;
        transition: transform .25s, box-shadow .25s;
        cursor: default;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 48px rgba(0,0,0,.45);
    }
    /* Barra colorida superior */
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 20px 20px 0 0;
    }
    .kpi-card.green::before  { background: linear-gradient(90deg,#48bb78,#68d391); }
    .kpi-card.blue::before   { background: linear-gradient(90deg,#4299e1,#63b3ed); }
    .kpi-card.orange::before { background: linear-gradient(90deg,#ed8936,#fbd38d); }

    /* Orb de fundo do card */
    .kpi-card::after {
        content: '';
        position: absolute;
        width: 140px; height: 140px;
        border-radius: 50%;
        right: -30px; bottom: -40px;
        opacity: .08;
    }
    .kpi-card.green::after  { background: #48bb78; }
    .kpi-card.blue::after   { background: #4299e1; }
    .kpi-card.orange::after { background: #ed8936; }

    .kpi-label {
        font-size: .75rem;
        font-weight: 600;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: rgba(160,210,255,.6);
        margin-bottom: 10px;
    }
    .kpi-value {
        font-size: 1.95rem;
        font-weight: 800;
        color: #e2e8f0;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    .kpi-value.green  { color: #68d391; }
    .kpi-value.blue   { color: #90cdf4; }
    .kpi-value.orange { color: #fbd38d; }
    .kpi-icon {
        font-size: 2rem;
        position: absolute;
        top: 24px; right: 24px;
        opacity: .35;
    }
    .kpi-sub {
        font-size: .78rem;
        color: rgba(160,210,255,.4);
        margin-top: 6px;
    }

    /* ── Atraso de entrada escalonado ─────────────────────── */
    .kpi-card:nth-child(1) { animation-delay: .05s; }
    .kpi-card:nth-child(2) { animation-delay: .15s; }
    .kpi-card:nth-child(3) { animation-delay: .25s; }

    /* ══════════════════════════════════════════════════════════
       SEÇÕES
    ══════════════════════════════════════════════════════════ */
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #90cdf4;
        letter-spacing: .3px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        animation: fadeUp .6s ease-out .3s both;
    }
    .section-title::after {
        content: '';
        flex: 1;
        height: 1px;
        background: rgba(99,179,237,.15);
        margin-left: 8px;
    }

    /* ── Tabela ───────────────────────────────────────────── */
    [data-testid="stDataFrame"] {
        background: rgba(255,255,255,.03) !important;
        border: 1px solid rgba(99,179,237,.12) !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        animation: fadeUp .6s ease-out .4s both;
    }
    [data-testid="stDataFrame"] th {
        background: rgba(66,153,225,.12) !important;
        color: #90cdf4 !important;
        font-weight: 600 !important;
        letter-spacing: .5px !important;
    }
    [data-testid="stDataFrame"] tr:hover td {
        background: rgba(66,153,225,.06) !important;
    }

    /* ── Gráfico ──────────────────────────────────────────── */
    [data-testid="stArrowVegaLiteChart"],
    [data-testid="stVegaLiteChart"] {
        background: transparent !important;
        border: 1px solid rgba(255,255,255,.18) !important;
        border-radius: 16px !important;
        padding: 12px !important;
        animation: fadeUp .6s ease-out .35s both;
    }
    /* Forçar canvas/svg do gráfico com fundo transparente */
    [data-testid="stArrowVegaLiteChart"] canvas,
    [data-testid="stVegaLiteChart"] canvas,
    [data-testid="stArrowVegaLiteChart"] svg,
    [data-testid="stVegaLiteChart"] svg {
        background: transparent !important;
    }

    /* ── Botões ───────────────────────────────────────────── */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        letter-spacing: .3px !important;
        transition: all .25s !important;
        border: 1px solid rgba(99,179,237,.3) !important;
        background: rgba(66,153,225,.15) !important;
        color: #90cdf4 !important;
    }
    .stButton > button:hover {
        background: rgba(66,153,225,.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(66,153,225,.25) !important;
        animation: pulse-border 1.5s ease-out;
    }

    /* ── Inputs de login ──────────────────────────────────── */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,.06) !important;
        border: 1px solid rgba(99,179,237,.25) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-size: .95rem !important;
        transition: border .25s, box-shadow .25s !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4299e1 !important;
        box-shadow: 0 0 0 3px rgba(66,153,225,.2) !important;
    }
    .stTextInput label { color: rgba(160,210,255,.7) !important; font-size:.85rem !important; font-weight:500 !important; }

    /* ── Submit button no form ────────────────────────────── */
    [data-testid="stForm"] .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg,#2b6cb0,#4299e1) !important;
        color: #fff !important;
        border: none !important;
        padding: 14px !important;
        font-size: 1rem !important;
        border-radius: 12px !important;
        margin-top: 8px !important;
        box-shadow: 0 4px 20px rgba(66,153,225,.4) !important;
    }
    [data-testid="stForm"] .stButton > button:hover {
        background: linear-gradient(135deg,#2c5282,#2b6cb0) !important;
        box-shadow: 0 8px 28px rgba(66,153,225,.55) !important;
        transform: translateY(-2px) !important;
    }

    /* ── Alertas ──────────────────────────────────────────── */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }

    /* ══════════════════════════════════════════════════════════
       RESPONSIVIDADE MOBILE
    ══════════════════════════════════════════════════════════ */
    @media (max-width: 768px) {
        .main .block-container { padding: 1rem .75rem !important; }
        .kpi-grid { grid-template-columns: 1fr 1fr !important; gap: 12px !important; }
        .kpi-value { font-size: 1.5rem !important; }
        .page-header h2 { font-size: 1.2rem !important; }
        .login-card { padding: 32px 20px !important; margin: 0 12px !important; }
    }
    @media (max-width: 480px) {
        .kpi-grid { grid-template-columns: 1fr !important; }
    }

    /* Esconde o menu hamburger padrão do Streamlit no mobile */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  CONEXÃO / DADOS
# ══════════════════════════════════════════════════════════════════
@st.cache_data(ttl=18000)
def get_data(empresa_selecionada):
    USER     = st.secrets["user"]
    PASSWORD = st.secrets["password"]
    HOST     = st.secrets["host"]
    PORT     = st.secrets["port"]
    DBNAME   = st.secrets["dbname"]

    db_url = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    engine = create_engine(db_url)

    nome_tabela = f'"tabela_{empresa_selecionada}"'
    query = f'SELECT * FROM {nome_tabela}'

    df = pd.read_sql(query, engine)
    df['Vencimento'] = pd.to_datetime(df['Vencimento'])
    df['Valor']      = df['Valor'].astype(float)
    return df


# ══════════════════════════════════════════════════════════════════
#  TELA DE LOGIN
# ══════════════════════════════════════════════════════════════════
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        inject_global_css()

        # Efeito de fundo (orbs + grade oceânica)
        st.markdown("""
        <div class="login-bg"></div>
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
        <div class="ship-deco">🚢</div>
        """, unsafe_allow_html=True)

        # Centralizar verticalmente no Streamlit
        _, center, _ = st.columns([1, 2.2, 1])
        with center:
            st.markdown("""
            <div class="login-card">
                <div class="login-logo">
                    <span class="icon">🌐</span>
                    <h1>Shoptan & Xangai</h1>
                    <p>Plataforma de Gestão de Importações</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.form("login_form"):
                usuario = st.text_input("👤  Usuário", placeholder="Digite seu usuário")
                senha   = st.text_input("🔒  Senha",   placeholder="Digite sua senha", type="password")
                submit  = st.form_submit_button("Entrar →")

                if submit:
                    if (usuario == st.secrets["LOGIN_USER"] and
                            senha == st.secrets["LOGIN_PASS"]):
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("❌  Usuário ou senha incorretos. Tente novamente.")

        # Rodapé discreto
        st.markdown("""
        <p style="text-align:center;color:rgba(255,255,255,.2);font-size:.75rem;margin-top:40px;">
            © 2025 Shoptan & Xangai · Gestão Financeira Corporativa
        </p>
        """, unsafe_allow_html=True)
        return False

    return True


# ══════════════════════════════════════════════════════════════════
#  CONTEÚDO PRINCIPAL
# ══════════════════════════════════════════════════════════════════
def render_kpi_cards(total_receber, qtd_aberto, qtd_vencidos):
    valor_fmt = f"R$ {total_receber:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    pct_venc  = round((qtd_vencidos / qtd_aberto * 100) if qtd_aberto else 0, 1)

    st.markdown(f"""
    <div class="kpi-grid">

      <div class="kpi-card green">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Valor a Receber</div>
        <div class="kpi-value green">{valor_fmt}</div>
        <div class="kpi-sub">Total em carteira</div>
      </div>

      <div class="kpi-card blue">
        <div class="kpi-icon">📄</div>
        <div class="kpi-label">Boletos em Aberto</div>
        <div class="kpi-value blue">{qtd_aberto}</div>
        <div class="kpi-sub">Documentos pendentes</div>
      </div>

      <div class="kpi-card orange">
        <div class="kpi-icon">⚠️</div>
        <div class="kpi-label">Boletos Vencidos</div>
        <div class="kpi-value orange">{qtd_vencidos}</div>
        <div class="kpi-sub">{pct_venc}% do total em aberto</div>
      </div>

    </div>
    """, unsafe_allow_html=True)


def main():
    inject_global_css()

    # ── SIDEBAR ──────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:20px 0 12px;">
            <span style="font-size:2.2rem;">🌐</span>
            <p style="font-size:1.15rem;font-weight:800;
               background:linear-gradient(90deg,#63b3ed,#90cdf4);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               margin:6px 0 2px;letter-spacing:-.5px;">Shoptan & Xangai</p>
            <p style="font-size:.72rem;color:rgba(160,210,255,.45);margin:0;">
               Gestão de Importações
            </p>
        </div>
        <hr style="border-color:rgba(99,179,237,.15);margin:0 0 20px;">
        """, unsafe_allow_html=True)

        empresa = st.selectbox("🏢  Empresa", ["Shoptan", "Xangai"])

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔄  Atualizar Dados"):
            st.cache_data.clear()
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪  Sair"):
            st.session_state.logged_in = False
            st.rerun()

        # ── FILTROS (serão populados após carregar os dados) ──
        st.markdown("""
        <hr style="border-color:rgba(99,179,237,.15);margin:16px 0;">
        <p style="font-size:.72rem;letter-spacing:1px;text-transform:uppercase;
                  color:rgba(160,210,255,.45);margin:0 0 10px;">🔎 Filtros</p>
        """, unsafe_allow_html=True)

        filtro_processo_placeholder = st.empty()
        filtro_tag_placeholder      = st.empty()

        st.markdown("""
        <p style="position:absolute;bottom:16px;left:0;right:0;
           text-align:center;font-size:.7rem;color:rgba(160,210,255,.2);">
           © 2025 Shoptan & Xangai
        </p>
        """, unsafe_allow_html=True)

    # ── HEADER ───────────────────────────────────────────────────
    st.markdown(f"""
    <div class="page-header">
        <span class="icon">📦</span>
        <div>
            <h2>Painel Financeiro — {empresa}</h2>
            <span>Contas a Receber · Atualização automática a cada 5 horas</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── DADOS ────────────────────────────────────────────────────
    try:
        with st.spinner("Carregando dados do banco..."):
            df = get_data(empresa)

        # ── FILTRO: PROCESSO (sidebar, populado com dados reais) ──
        processos_disponiveis = sorted(df['Processo'].dropna().unique().tolist())
        processos_selecionados = filtro_processo_placeholder.multiselect(
            "📦  Processo",
            options=processos_disponiveis,
            default=[],
            placeholder="Todos os processos"
        )

        # ── FILTRO: TAG (apenas Xangai) ───────────────────────────
        tags_selecionadas = []
        if empresa == "Xangai" and "tags" in df.columns:
            tags_disponiveis = sorted(
                set(t.strip() for tags in df['tags'].dropna() for t in str(tags).split(',') if t.strip())
            )
            if tags_disponiveis:
                tags_selecionadas = filtro_tag_placeholder.multiselect(
                    "🏷️  Tag",
                    options=tags_disponiveis,
                    default=[],
                    placeholder="Todas as tags"
                )

        # ── APLICA FILTROS ────────────────────────────────────────
        df_filtrado = df.copy()

        if processos_selecionados:
            df_filtrado = df_filtrado[df_filtrado['Processo'].isin(processos_selecionados)]

        if tags_selecionadas and "tags" in df_filtrado.columns:
            df_filtrado = df_filtrado[
                df_filtrado['tags'].apply(
                    lambda cell: any(
                        tag in str(cell).split(',') for tag in tags_selecionadas
                    ) if pd.notna(cell) else False
                )
            ]

        # ── KPIs (calculados sobre dados filtrados) ───────────────
        hoje          = pd.Timestamp.now().normalize()
        total_receber = df_filtrado['Valor'].sum()
        qtd_aberto    = len(df_filtrado)
        vencidos_df   = df_filtrado[df_filtrado['Vencimento'] < hoje]
        qtd_vencidos  = len(vencidos_df)

        render_kpi_cards(total_receber, qtd_aberto, qtd_vencidos)

        # ── GRÁFICO ──────────────────────────────────────────────
        st.markdown('<div class="section-title">💰 Valor por Processo</div>', unsafe_allow_html=True)
        chart_data = (
            df_filtrado.groupby("Processo")["Valor"]
              .sum()
              .sort_values(ascending=True)
              .reset_index()
        )
        if chart_data.empty:
            st.info("Nenhum dado encontrado para os filtros selecionados.")
        else:
            # Formata rótulos em R$
            chart_data['Valor_fmt'] = chart_data['Valor'].apply(
                lambda v: f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            )

            fig = go.Figure(go.Bar(
                x=chart_data['Valor'],
                y=chart_data['Processo'],
                orientation='h',
                text=chart_data['Valor_fmt'],
                textposition='outside',          # rótulo fora da barra
                textfont=dict(color='#90cdf4', size=12, family='Inter'),
                marker=dict(
                    color='#4299e1',
                    line=dict(color='rgba(99,179,237,.3)', width=1)
                ),
                hovertemplate='<b>%{y}</b><br>Valor: %{text}<extra></extra>',
            ))

            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',   # fundo externo transparente
                plot_bgcolor='rgba(0,0,0,0)',    # fundo do plot transparente
                margin=dict(l=10, r=120, t=10, b=10),  # espaço à direita para rótulo
                height=max(300, len(chart_data) * 48),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,.08)',
                    tickfont=dict(color='rgba(255,255,255,.5)', size=10),
                    tickformat=',.0f',
                    title='',
                    zeroline=False,
                ),
                yaxis=dict(
                    tickfont=dict(color='#e2e8f0', size=12),
                    title='',
                    automargin=True,
                ),
                showlegend=False,
            )

            st.plotly_chart(fig, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── TABELA ───────────────────────────────────────────────
        st.markdown('<div class="section-title">📋 Lista de Documentos</div>', unsafe_allow_html=True)

        colunas_display = ['Processo', 'numero_do_documento', 'Valor', 'Vencimento']
        if empresa == "Xangai" and "tags" in df_filtrado.columns:
            colunas_display.append('tags')

        df_display = df_filtrado[colunas_display].copy()
        df_display['Vencimento'] = df_display['Vencimento'].dt.strftime('%d/%m/%Y')
        df_display['Valor']      = df_display['Valor'].apply(
            lambda v: f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")
        )

        col_config = {
            "Processo":            st.column_config.TextColumn("Processo"),
            "numero_do_documento": st.column_config.TextColumn("Nº Documento"),
            "Valor":               st.column_config.TextColumn("Valor"),
            "Vencimento":          st.column_config.TextColumn("Vencimento"),
        }
        if empresa == "Xangai" and "tags" in df_display.columns:
            col_config["tags"] = st.column_config.TextColumn("Tags")

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config=col_config
        )

    except Exception as e:
        st.error(f"**Erro ao carregar dados:** {e}")
        st.info("Verifique se as tabelas existem no banco e se as credenciais estão configuradas corretamente.")


# ══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════
if login():
    main()
