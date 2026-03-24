# Integracao com APIs de renderizacao 3D

import os
import re
from stable_diffusion_api import gerar_imagem

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'web', 'static')
os.makedirs(STATIC_DIR, exist_ok=True)


def sanitize_filename(text):
    return re.sub(r'[^\w\-]', '_', text)[:40]


def extrair_comodos(description):
    padrao = r'\d+[\.\-\)]?\s+([A-Za-z\u00C0-\u00FA\s]+?)(?=\d+[\.\-\)]?\s+[A-Za-z\u00C0-\u00FA]|$)'
    comodos = re.findall(padrao, description.strip())
    comodos = [c.strip() for c in comodos if c.strip()]
    return comodos


def build_prompt(comodo, description):
    return (
        "Interior de " + comodo + ", estilo arquitetonico moderno contemporaneo, "
        "projeto residencial brasileiro, " + description[:80] + ", "
        "iluminacao natural, moveis modernos, ultra realista, "
        "renderizacao 3D arquitetonica profissional, 8k, alta qualidade"
    )


def generate_3d_render(description, plan):
    safe_desc = sanitize_filename(description or "projeto")
    comodos = extrair_comodos(description)

    if not comodos:
        comodos = ["fachada externa moderna do projeto"]

    results = []

    for comodo in comodos:
        safe_label = sanitize_filename(comodo)
        output_path = os.path.join(STATIC_DIR, "render_" + safe_desc + "_" + safe_label + ".png")
        prompt = build_prompt(comodo, description)

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
