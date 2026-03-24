# Geracao de imagens arquitetonicas via Google Gemini Imagen 3

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
        """
            Monta um prompt detalhado e otimizado para o Gemini Imagen 3,
                focado em renderizacao arquitetonica de alta qualidade.
                    """
        estilo = descricao_projeto[:100] if descricao_projeto else ""
        return (
            f"Architectural interior render of '{comodo}', "
            "Brazilian modern residential project, "
            f"project description: {estilo}, "
            "natural lighting through large windows, "
            "contemporary furniture, clean lines, warm tones, "
            "professional architectural 3D rendering, "
            "photorealistic, ultra high quality, 8K resolution, "
            "wide angle view, no people"
        )


def build_prompt_fachada(descricao_projeto):
        """
            Prompt especial para fachada externa.
                """
        estilo = descricao_projeto[:120] if descricao_projeto else ""
        return (
            "Architectural exterior render of a modern Brazilian residential house, "
            f"project: {estilo}, "
            "contemporary facade, landscaping, natural daylight, "
            "professional architectural visualization, "
            "photorealistic, ultra high quality, 8K, wide angle, no people"
        )


def generate_3d_render(descricao_projeto, comodos_texto):
        safe_desc = sanitize_filename(descricao_projeto or "projeto")

    # Extrai comodos do campo especifico
        comodos = extrair_comodos(comodos_texto or "")

    # Se nao tiver comodos, gera so a fachada
        if not comodos:
                    comodos = ["fachada_externa"]

        results = []
        for i, comodo in enumerate(comodos):
                    safe_label = sanitize_filename(comodo)
                    output_path = os.path.join(
                        STATIC_DIR, f"render_{safe_desc}_{safe_label}.png"
                    )

            # Prompt otimizado: fachada tem prompt proprio
                    if "fachada" in comodo.lower():
                                    prompt = build_prompt_fachada(descricao_projeto)
else:
            prompt = build_prompt(comodo, descricao_projeto)

        # Aguarda entre requisicoes para respeitar rate limit da API
            if i > 0:
                            print(f"[Rate Limit] Aguardando 5 segundos antes da proxima imagem...")
                            time.sleep(5)

            try:
                            print(f"[Gemini Imagen 3] Gerando imagem para: {comodo}")
                            result = gerar_imagem(prompt, output_path)
                            if result:
                                                results.append({
                                                                        "label": comodo,
                                                                        "path": f"static/render_{safe_desc}_{safe_label}.png"
                                                })
            else:
                                raise Exception("Imagem nao gerada pela API")
except Exception as e:
                print(f"[Fallback] Erro em '{comodo}': {e}")
                # Cria arquivo vazio como placeholder
                with open(output_path, "wb") as f:
                                    f.write(b"")
                                results.append({
                                                    "label": comodo,
                                                    "path": f"static/render_{safe_desc}_{safe_label}.png"
                                })

    caminho_principal = results[0]["path"] if results else f"static/render_{safe_desc}.png"
    return caminho_principal, results
