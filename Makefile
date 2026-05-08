# Variáveis
PYTHON = python3
PIP = pip

install:
	$(PIP) install -r requirements.txt

monitor:
	streamlit run monitor.py

dashboard:
	streamlit run monitoramento.py

clean:
	rm -rf __pycache__
	rm -rf .streamlit