import streamlit as st
import sqlite3
import pandas as pd

# Banco de dados
def create_connection(db_file):
    return sqlite3.connect(db_file)

def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            skill_group TEXT NOT NULL,
            skill_name TEXT NOT NULL,
            relevance TEXT NOT NULL
        );
    """)

conn = create_connection("avaliacoes.db")
create_table(conn)

# Interface
st.title('Verdi Skill Relevance')
# st.subheader('Este é um subheader')

st.text('ES: Estamos desarrollando un proyecto para analizar la relevancia de las skills y su contribución es esencial. Hemos creado este formulario para que puedas compartir tu visión, clasificando las skills como Low, Medium, High o Very High. Todas las respuestas son válidas; no hay respuestas correctas o incorrectas. Queremos captar diferentes percepciones sobre la relevancia de las skills, y cada punto de vista es valioso para nuestro análisis.')

st.text('PT: Estamos desenvolvendo um projeto para analisar a relevância das skills e sua contribuição é essencial. Criamos este formulário para você compartilhar sua visão, classificando as skills como Low, Medium, High ou Very High. Todas as respostas são válidas; não há respostas certas ou erradas. Queremos captar diferentes percepções sobre a relevância das skills, e cada ponto de vista é valioso para nossa análise.')


times = ["mpcx", "pdd", "alf", "search tagger", "most used", "random"]
time_selecionado = st.selectbox("Choose the skill group you can best evaluate:", times)
username = st.text_input("Write your username:")

mapa_provas = {
    "mpcx": ['mpcx_lib', 'mpcx_process_identifier', 'mpcx_agents',
             'mpcx_lib_tester', 'mpcx_error_ux', 'mpcx_transaction_detail',
             'mpcx_faqs', 'mpcx_transaction_identifier', 'mpcx_standalone_faqs',
             'mpcx_cards_chargebacks', 'mpcx_rtr', 'mpcx_router_tester',
             'mpcx_phishing_handler'],
    "pdd": ['pdd_buyer', 'pdd_buyer_homolog', 'pdd_seller_proposal',
            'pdd_solution_unit_test', 'pdd_buyer_confirmation',
            'pdd_buyer_homolog_returns', 'pdd_buyer_free_return', 'pdd_dt',
            'pdd_buyer_diagnostic', 'pdd_seller_proposal_replace',
            'pdd_hydrate_solution', 'pdd_solution', 'pdd_culpability',
            'pdd_solutions', 'pdd_diagnostic_stress_test',
            'pdd_solution_replace', 'pdd_timeout', 'pdd_hydrate_purchase',
            'pdd_diagnostic', 'pdd_buyer_diagnostic_devolver_gratis',
            'pdd_try_catch_error'],
    "alf": ['a', 'b', 'c'],
    "search tagger": ['d', 'e', 'f'],
    "most used": ['mpcx', 'pdd_buyer', 'mlcx', 
                'chatbot-credits-debt-info', 'supply_seller_assistant', 
                'cards_chargebacks', 'mp_payservices', 'mpcx_lib', 
                'pdd_buyer_homolog', 'meli_mate'],
    "random": ['legal_assistant_bpp', 'agente_pagos_ml', 
                'ua_kyc_diagnostic_entity_registration_pj', 
                'cards_chargebacks_multi_trx', 'verdi_seed', 
                'sacura_ruteo_main', 'supply_autoevaluete_assistant', 
                'avengers_router', 'pdd_buyer_free_return', 
                'mlcxproactive']
}

# Agora com a nova opção
opcoes_avaliacao = ["Low", "Medium", "High", "Very High", "I can't evaluate"]

if username:
    st.subheader(f"Evaluate the skills of {time_selecionado}, {username}:")

    provas = mapa_provas[time_selecionado]
    avaliacoes = {}

    # Cabeçalho
    # Cabeçalho
    col1, col2 = st.columns([3, 7])
    with col1:
        st.markdown("**Skill**")
    with col2:
        st.markdown("**Relevance**")

    for prova in provas:
        col1, col2 = st.columns([3, 7])
        with col1:
            st.markdown(
                f"<p style='padding-top: 0.6rem; font-weight: bold'>{prova}</p>",
                unsafe_allow_html=True
            )
        with col2:
            aval = st.radio(
                label=" ",
                options=opcoes_avaliacao,
                key=f"radio_{prova}",
                horizontal=True,
                index=4
            )
            avaliacoes[prova] = aval

    if st.button("Done. Submit my evaluation"):
        for prova, avaliacao in avaliacoes.items():
            if avaliacao:
                conn.execute("INSERT INTO avaliacoes (username, skill_group ,skill_name, relevance) VALUES (?, ?, ?, ?)",
                             (username, time_selecionado, prova, avaliacao))
        conn.commit()
        st.success("Evaluations submitted successfully. Thank you!")

    # Botão para visualizar respostas
    if st.button("See evaluations"):
        # Consultar avaliações
        df = pd.read_sql_query("SELECT * FROM avaliacoes", conn)
        st.write("All of evaluations:")
        st.dataframe(df)  # Exibe como dataframe

else:
    st.warning("Please, write your username to continuous")
