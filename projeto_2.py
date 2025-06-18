import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt 
import seaborn as sns
import statistics as sts

#streamlit run c:/Users/gustavo/Desktop/STREAMLIT/projeto2.0/projeto_2.py
#cd C:\Users\gustavo\Desktop\STREAMLIT\projeto2.0
#pip install -r requirements.txt

st.title("Análise Exploratória com Dados CSV (USANDO STREAMLIT)")

# CAMINHO E SEPARADOR
caminho_csv = "Churn.csv"
sep_csv = ";"

# CARREGAR OS DADOS
@st.cache_data
def carregar_dados():
    try:
        base = pd.read_csv(caminho_csv, sep=sep_csv)
        return base
    except FileExistsError:
        st.error(f"ARQUIVOS NAO ENCONTRADOS: {caminho_csv}")
        return None
    
base = carregar_dados()

if base is not None:
    base.columns = ["ID", "SCORE", "ESTADOS", "GENERO", "IDADE", "PATRIMONIO",
                    "SALDO", "PRODUTOS", "CARTAODECREDITO", "ATIVO", "SALARIO", "SAIU"]

    variaveis_categoricas = ['GENERO', 'ESTADOS']
    variaveis_numericas = ['ID', 'SCORE', 'IDADE', 'PATRIMONIO', 'SALDO', 
                           'PRODUTOS', 'CARTAODECREDITO', 'ATIVO', 'SALARIO', 'SAIU']
   
    # TABS DE NAVEGAÇAO
    aba1, aba2, aba3, aba4 = st.tabs([" Análise Exploratória", " Tratamento de Dados", "Machine learning", " Exportação"])

    # ABA 1 - Análise Exploratória
    with aba1:
        st.subheader("VIZUALIZAÇAO GERAL DOS DADOS")
        st.dataframe(base)

        st.subheader("VALORES NULOS")
        st.write(base.isnull().sum())

        st.markdown("### VARIAVEIS CATEGORICAS")
        for coluna in variaveis_categoricas:
            fig, ax = plt.subplots(figsize=(10,6))
            base[coluna].value_counts().plot(kind="bar", ax=ax)
            ax.set_title(f"INFORMAÇOES GERAIS DE: {coluna}")
            st.pyplot(fig)
            st.write(base[coluna].describe())
           
        st.markdown("VARIAVEIS NUMERICAS")
        colu1, colu2 = st.columns(2)
        for i, coluna in enumerate(variaveis_numericas):
            if coluna in base.columns:
                if i % 2 == 0:
                    with colu1:
                        st.write(f"BOXPLOT DE {coluna}")
                        fig, ax = plt.subplots(figsize=(10,6))
                        sns.boxplot(data=base, x=coluna, ax=ax)
                        st.pyplot(fig)
                        st.write(base[coluna].describe())
                else:
                    with colu2:
                        st.write(f"BOXPLOT DE {coluna}")
                        fig, ax = plt.subplots(figsize=(10,6))
                        sns.boxplot(data=base, x=coluna, ax=ax)
                        st.pyplot(fig)
                        st.write(base[coluna].describe())

    # ABA 2 - Tratamento de Dados
    with aba2:
        st.sidebar.markdown("OPÇOES DE TRATAMENTOS")

        if st.sidebar.checkbox("RETIRAR VALORES DUPLICADOS IDS"):
            quatidade_antes = base.shape[0]
            base.drop_duplicates(subset="ID", keep="first", inplace=True)
            quantidade_depois = base.shape[0]
            st.success(f"{quatidade_antes - quantidade_depois} REGISTRO ALTERADO COM SUCESSO")

        if st.sidebar.checkbox("PREENCHER SALARIOS NULOS PELA MEDIANA"):
            mediana_salario = sts.median(base["SALARIO"].dropna())
            base["SALARIO"] = base["SALARIO"].fillna(mediana_salario)
            st.success(f"SALARIOS NULOS PREENCHIDOS COM A MEDIANA {mediana_salario}")

        if st.sidebar.checkbox("TRATAR VALOR NULOS EM GENEROS"):
            base["GENERO"] = base["GENERO"].fillna("Masculino")
            st.success("GENEROS NULOS PREENCHIDOS COM MASCULINO")
            st.write(base.isnull().sum())
        
        if st.sidebar.checkbox("CORRIGIR IDADES INVALIDAS "):
            medina_idade = sts.median(base["IDADE"])
            base.loc[(base["IDADE"] < 0 ) | (base["IDADE"]> 110), "IDADE"] = medina_idade
            st.success(f"IDADES CORRIGIDAS PELA MEDIANA: {medina_idade}")
            fig, ax = plt.subplots()
            sns.boxplot(x= base["IDADE"], ax=ax)
            ax.set_title("DISTRIBUIÇAO DE IDADES CORRIGIDAS")
            st.pyplot(fig)
            
        if st.sidebar.checkbox("CORRIGIR NOMES DOS ESTADOS (RP, SP, TD → RS)"):
            base.loc[base["ESTADOS"].isin(["RP", "SP", "TD"]),"ESTADOS"] = "RS"
            st.success("ESTADOS PADRONIZADOS COM SUCESSO")
            fig,ax = plt.subplots()
            base["ESTADOS"].value_counts().plot(kind="bar", ax=ax)
            ax.set_title("DISTRIBUIÇAO DE ESTADOS CORRIGIDOS")
            st.pyplot(fig)
            
        if st.sidebar.checkbox("PADRONIZANDO VALORES DE GENERO "):
            base.loc[base['GENERO'] == 'F', 'GENERO'] = 'Feminino'
            base.loc[base['GENERO'] == 'Fem', 'GENERO'] = 'Feminino'
            base.loc[base['GENERO'] == 'M', 'GENERO'] = 'Masculino'
            st.success("VALORES PADRONIZADOS COM SUCESSO")
            fig,ax = plt.subplots()
            base["GENERO"].value_counts().plot(kind="bar",ax=ax)
            ax.set_title("DISTRIBUIÇAO DE GENEROS")
            st.pyplot(fig)
            
        if st.sidebar.checkbox("CORRIGIR OUTLIERS DE SALARIO"):
            desvio = sts.stdev(base['SALARIO'])
            mediana_salario = sts.median(base["SALARIO"])
            base.loc[base["SALARIO"] >= 2 * desvio, "SALARIO"] = mediana_salario
            st.success(f"OUTLIERS DE SALARIO ALTERADOS PELA MEDIANA: {mediana_salario}")
            fig, ax = plt.subplots()
            sns.boxplot(x=base['SALARIO'], ax=ax)
            ax.set_title("SALARIOS APOS O TRATAMENTO DOS OUTLIERS")
            st.pyplot(fig)
    
    with aba3:
        st.title("ESTA SENDO FEITO")
        
        
    with aba4:
        st.markdown("### Download dos Dados Tratados")
        st.download_button(
            label="Baixar CSV Tratado",
            data=base.to_csv(index=False).encode('utf-8'),
            file_name='dados_tratados.csv',
            mime='text/csv'
        )
            
            
        
            
            
         