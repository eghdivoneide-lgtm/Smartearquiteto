# Integracao com APIs de renderizacao 3D

import os
import re
import time
from stable_diffusion_api import gerar_imagem

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'web', 'static')
os.makedirs(STATIC_DIR, exist_ok=True)


def sanitize_filename(text):
    return re.sub(r'[^\w\-]', '_', text)[:40]


def extrair_comodos(comodos_texto):
    # Detecta linhas ou itens numerados: 1 Sala, 1. Sala, 1- Sala, 1) Sala
    padrao = r'\d+[.\-)]?\s+([^\d\n]+?)(?=\d+[.\-)]?\s+|$)'
    comodos = re.findall(padrao, comodos_texto.strip())
    comodos = [c.strip().rstrip(',;') for c in comodos if c.strip()]
    return comodos


def build_prompt(comodo, descricao_projeto):
    return (
        "Interior de " + comodo + ", estilo arquitetonico moderno contemporaneo, "
        "projeto residencial brasileiro, " + descricao_projeto[:80] + ", "
        "iluminacao natural, moveis modernos, ultra realista, "
        "renderizacao 3D arquitetonica profissional, 8k, alta qualidade"
    )


def generate_3d_render(descricao_projeto, comodos_texto):
    safe_desc = sanitize_filename(descricao_projeto or "projeto")

    # Extrai comodos do campo especifico
    comodos = extrair_comodos(comodos_texto or "")

    # Se nao tiver comodos, gera so a fachada
    if not comodos:
        comodos = ["fachada externa moderna do projeto"]

    results = []

    for i, comodo in enumerate(comodos):
        safe_label = sanitize_filename(comodo)
        output_path = os.path.join(STATIC_DIR, "render_" + safe_desc + "_" + safe_label + ".png")
        prompt = build_prompt(comodo, descricao_projeto)

        # Aguarda entre requisicoes para evitar rate limit
        if i > 0:
            print("[Rate Limit] Aguardando 12 segundos antes da proxima imagem...")
            time.sleep(12)

        try:
            print("[StableDiffusion] Gerando imagem para comodo: " + comodo)
            result = gerar_imagem(prompt, output_path)
            if result:
                results.append({
                    "label": comodo,
                    "path": "static/render_" + safe_desc + "_" + safe_label + ".png"
                })
            else:
                raise Exception("Falha na geracao")
        except Exception as e:
            print("[Simulacao] Erro em " + comodo + ": " + str(e))
            with open(output_path, "wb") as f:
                f.write(b"")
            results.append({
                "label": comodo,
                "path": "static/render_" + safe_desc + "_" + safe_label + ".png"
            })

    caminho_principal = results[0]["path"] if results else "static/render3d_" + safe_desc + ".png"
    return caminho_principal, results
