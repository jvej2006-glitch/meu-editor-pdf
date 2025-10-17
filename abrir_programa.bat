@echo off
echo =======================================================
echo    Abrindo o seu Editor de Extracao de PDF...
echo    Aguarde um instante, seu navegador abrira em breve.
echo =======================================================

REM Ativa o ambiente virtual e, se der certo, executa o Streamlit
call .\venv\Scripts\activate && streamlit run editor_pdf.py

echo.
echo Para desligar o aplicativo, basta fechar esta janela preta.