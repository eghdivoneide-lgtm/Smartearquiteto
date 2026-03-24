# Integração com APIs de renderização 3D

import os
import re
from stable_diffusion_api import gerar_imagem

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'web', 'static')
os.makedirs(STATIC_DIR, exist_ok=True)

def sanitize_filename(text):
    # Remove caracteres inválidos para nomes de arquivos
    return re.sub(r'[^\w\-]', '_', text)[:40]  # Limita tamanho

def generate_3d_render(description, plan):
    """
    Gera uma imagem realista do projeto usando Stable Diffusion via Replicate.
    Se falhar, volta para simulação.
    """
    safe_desc = sanitize_filename(description or "projeto")
    output_path = os.path.join(STATIC_DIR, f"render3d_{safe_desc}.png")
    try:
        print(f"[StableDiffusion] Gerando imagem para: {description}")
        result = gerar_imagem(description, output_path)  # ← nome correto agora
        if result:
            return f"static/render3d_{safe_desc}.png"
        else:
            raise Exception("Falha na geração de imagem")
    except Exception as e:
        print(f"[Simulação] Erro ou indisponível: {e}. Gerando arquivo simulado.")
        with open(output_path, "wb") as f:
            f.write(b"")
        return f"static/render3d_{safe_desc}.png"
