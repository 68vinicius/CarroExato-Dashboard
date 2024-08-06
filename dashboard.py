import streamlit as st
import pandas as pd

df = pd.read_csv('Data/dataset_reparos_2024.csv')

st.set_page_config(page_title='Dashboard Carro Exato')
st.markdown('<h1 style=\'text-align: center;\'>Diagnósticos e Manutenções</h1>', unsafe_allow_html=True)
st.image('https://github.com/68vinicius/Carro-Exato-Dashboard/raw/main/Imagens/CarroExatoBanner.jpg', caption='www.carroexato.com.br')
st.subheader('Explore os Detalhes das Manutenções')
st.markdown('Apresentamos uma variedade de manutenções recentes feitas pela Carro Exato, desde problemas comuns como falhas no motor até questões específicas como vazamentos de óleo. Convidamos você a explorar nossos dados e visualizar detalhes das manutenções realizadas.')

meses = df['data'].str.slice(3, 10).unique()
mes_selecionado = st.selectbox('Selecione o Mês:', meses)

class GerenciadorKPI:
    def __init__(self, dataframe):
        self.df = dataframe
        self.df_mes = None

    def filtrar_por_mes(self, mes):
        self.df_mes = self.df[self.df['data'].str.contains(mes)]

    def calcular_kpis(self):
        if self.df_mes is None:
            raise ValueError('DataFrame não filtrado. Chame o método filtrar_por_mes primeiro.')
        
        total_diagnosticos = self.df_mes.shape[0]
        custo_total_pecas = self.df_mes['valor_peca'].sum()
        custo_total_maodeobra = self.df_mes['valor_maodeobra'].sum()
        return total_diagnosticos, custo_total_pecas, custo_total_maodeobra

    def display_kpis(self):
        total_diagnosticos, custo_total_pecas, custo_total_maodeobra = self.calcular_kpis()

        col1, col2, col3 = st.columns(3)
        col1.metric('Total de Serviços', total_diagnosticos)
        col2.metric('Custo Total de Peças', f'R$ {custo_total_pecas}')
        col3.metric('Custo Total de Mão de Obra', f'R$ {custo_total_maodeobra}')

    def diagnostico_analise(self):
        if self.df_mes is None:
            raise ValueError('DataFrame não filtrado. Chame o método filtrar_por_mes primeiro.')
        
        diagnostico_contagem = self.df_mes['diagnostico'].value_counts()
        diagnostico_mais_frequente = diagnostico_contagem.idxmax()
        quantidade_diagnosticos = diagnostico_contagem.max()
        return diagnostico_contagem, diagnostico_mais_frequente, quantidade_diagnosticos

    def display_diagnostico_analise(self):
        diagnostico_contagem, diagnostico_mais_frequente, quantidade_diagnosticos = self.diagnostico_analise()

        st.subheader('Análise de Diagnósticos:')
        st.write(f'O diagnóstico mais frequente foi {diagnostico_mais_frequente} com {quantidade_diagnosticos} ocorrências.')
        st.bar_chart(diagnostico_contagem)

kpi_manager = GerenciadorKPI(df)
kpi_manager.filtrar_por_mes(mes_selecionado)
kpi_manager.display_kpis()
kpi_manager.display_diagnostico_analise()

# Seletores
opcao = st.selectbox('Selecione um Diagnóstico:', kpi_manager.df_mes['diagnostico'].unique())
st.write(kpi_manager.df_mes[kpi_manager.df_mes['diagnostico'] == opcao])

# Tabela
st.subheader('Registro de Manutenções Realizadas')
st.write(kpi_manager.df_mes)

# Widgets Adicionais 
st.sidebar.title('Informações Adicionais')
st.sidebar.subheader('Opções Adicionais')

opcao_sidebar = st.sidebar.selectbox('Selecione uma Opção:', ['Informações Gerais', 'Contato', 'FAQ'])
if opcao_sidebar == 'Informações Gerais':
    st.sidebar.markdown("### Informações Gerais")
    st.sidebar.markdown("""
    Esse Projeto tem como objetivo Analisar Dados de Manutenção de Veículos da Carro Exato visa explorar e visualizar dados de manutenções realizadas:
    
    Principais Funcionalidades:
    - **Dashboard Interativo**
    - **Visualizações Detalhadas**
    - **Facilidade de Uso**
                        
    Utilizando técnicas de análise e visualização de dados, ele oferece insights sobre diagnósticos frequentes, troca de componentes, entre outros.
    """)

elif opcao_sidebar == 'Contato':
    st.sidebar.markdown("""
    Para mais informações ou dúvidas, entre em contato:
    
    - **Telefone:** (11) 4055-3475
    - **LinkedIn:** [@CarroExato](https://www.linkedin.com/company/carroexato/)
    - **Instagram:** [@CarroExato](https://www.instagram.com/carroexato)
    - **E-mail:** contato@carroexato.com
    """)

elif opcao_sidebar == 'FAQ':
    st.sidebar.markdown("### FAQ")
    st.sidebar.markdown("""
    Esse Projeto tem como objetivo Analisar Dados de Manutenção de Veículos da Carro Exato visa explorar e visualizar dados de manutenções realizadas:
    
    Principais Funcionalidades:
    - **1. Qual é o objetivo deste projeto?** Analisar e visualizar dados de manutenção de veículos.
    - **2. Quais ferramentas foram utilizadas?** Python, Pandas, Matplotlib e Streamlit.
    - **3. Como posso executar o projeto?** Execute *streamlit run dashboard.py* para o dashboard.
    - **4. Onde estão os dados?** No arquivo *Data/trabalhos.csv.*
    - **5. Posso contribuir com o projeto?.** Sim, contribuições são bem-vindas!
                    
    """)

st.info(f'Estes dados foram coletados em {mes_selecionado}.')