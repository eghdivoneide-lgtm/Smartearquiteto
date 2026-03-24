import os

# =============================================================
# SmartArquiteto - Configuracoes globais
# =============================================================
# As chaves de API sao lidas de variaveis de ambiente.
# Veja o arquivo .env.example para instrucoes de configuracao.
# =============================================================

# Google Gemini Imagen 3 - Geracao de imagens arquitetonicas
# Configure: export GEMINI_API_KEY="sua_chave"
# Obtenha em: https://aistudio.google.com/app/apikey
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# APIs de narracao e trilha (para expansao futura)
NARRATION_API_KEY = os.environ.get("NARRATION_API_KEY", "")
SOUNDTRACK_API_KEY = os.environ.get("SOUNDTRACK_API_KEY", "")

# Configuracoes gerais do pipeline
RATE_LIMIT_SEGUNDOS = 5      # Espera entre requisicoes de imagem
IMAGEM_ASPECT_RATIO = "16:9" # Proporcao das imagens geradas
MAX_COMODOS = 10             # Limite de comodos por projeto
