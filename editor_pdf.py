import streamlit as st
import pdfplumber
import re

# --- Função para processar o PDF ---
# É uma boa prática organizar a lógica principal em uma função.
def extrair_texto_do_pdf(arquivo_pdf_carregado):
    """
    Abre um arquivo PDF carregado pelo Streamlit, extrai todo o texto
    e formata os decimais com vírgula para facilitar a leitura no Brasil.
    """
    texto_completo = ""
    try:
        # Usa o pdfplumber para abrir o arquivo que está em memória (não precisa salvar no disco)
        with pdfplumber.open(arquivo_pdf_carregado) as pdf:
            # Passa por cada página do PDF
            for pagina in pdf.pages:
                texto_da_pagina = pagina.extract_text()
                if texto_da_pagina:
                    texto_completo += texto_da_pagina + "\n\n" # Adiciona um espaço entre as páginas
        
        # Substitui ponto decimal por vírgula de forma segura (procura: dígito.dígito)
        texto_formatado = re.sub(r'(\d)\.(\d)', r'\1,\2', texto_completo)
        return texto_formatado
    except Exception as e:
        return f"Ocorreu um erro ao tentar ler o arquivo PDF: {e}"


# --- Interface Gráfica do Aplicativo com Streamlit ---

# st.set_page_config define o título que aparece na aba do navegador e usa a tela inteira.
st.set_page_config(page_title="Editor de Extração de PDF", layout="wide")

# st.title() -> Cria o título principal da página.
st.title("📄 Editor de Extração de PDF")

# st.markdown() -> Permite escrever textos com formatação.
st.markdown("""
Esta ferramenta extrai todo o texto de um arquivo PDF e o exibe em uma caixa editável.
**Como usar:**
1.  Faça o upload de um arquivo PDF.
2.  Clique no botão 'Processar PDF'.
3.  Edite o texto extraído diretamente na caixa de texto abaixo.
4.  Quando estiver pronto, selecione e copie o texto para onde precisar.
""")

# st.session_state é a "memória" do aplicativo. Usamos para guardar o texto extraído.
if 'texto_extraido' not in st.session_state:
    st.session_state.texto_extraido = ""

# st.file_uploader() -> Cria o componente de upload de arquivo.
uploaded_file = st.file_uploader(
    "Faça o upload de um arquivo PDF aqui",
    type="pdf",
    accept_multiple_files=False # Configurado para aceitar apenas um arquivo por vez.
)

# O código abaixo só executa se um arquivo tiver sido carregado.
if uploaded_file is not None:
    
    # st.button() -> Cria um botão. O código dentro do 'if' só roda quando o botão é clicado.
    if st.button("Processar PDF"):
        # st.spinner() -> Mostra uma mensagem de "carregando" enquanto a extração acontece.
        with st.spinner("Extraindo texto, por favor aguarde..."):
            texto = extrair_texto_do_pdf(uploaded_file)
            # Guarda o resultado na "memória" do aplicativo para não se perder.
            st.session_state.texto_extraido = texto
            st.success("Extração concluída!")

# Esta parte verifica se já existe algum texto na "memória" para ser exibido.
if st.session_state.texto_extraido:
    st.markdown("---") # Cria uma linha divisória.
    st.subheader("Texto Extraído (editável)")
    
    # st.text_area() -> Este é o componente principal: uma caixa de texto grande e editável.
    texto_editado = st.text_area(
        label="Corrija o texto abaixo e depois copie (Ctrl+A para selecionar tudo, Ctrl+C para copiar):",
        value=st.session_state.texto_extraido, # O valor inicial da caixa é o nosso texto extraído.
        height=600 # Altura da caixa em pixels, para dar bastante espaço.
    )