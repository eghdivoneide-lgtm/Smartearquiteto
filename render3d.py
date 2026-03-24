# Integração com APIs de renderização 3D

import os
import re
from stable_diffusion_api import gerar_imagem

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'web', 'static')
os.makedirs(STATIC_DIR, exist_ok=True)

def sanitize_filename(text):
        return re.sub(r'[^\w\-]', '_', text)[:40]

def extrair_comodos(description):
        """
            Detecta cômodos numerados na descrição.
                Exemplo: '1 Sala de estar 2 Cozinha 3 Quarto'
                    Retorna lista de strings com os nomes dos cômodos.
                        """
        padrao = r'\d+[\.\-\)]?\s+([A-Za-zÀ-ú\s]+?)(?=\d+[\.\-\)]?\s+[A-Za-zÀ-ú]|$)'
        comodos = re.findall(padrao, description.strip())
        comodos = [c.strip() for c in comodos if c.strip()]
        return comodos

def build_prompt(comodo, description):
        """
            Monta um prompt profissional para cada cômodo.
                """
        return (
            f"Interior de {comodo}, estilo arquitetônico moderno contemporâneo, "
            f"projeto residencial brasileiro, {description[:80]}, "
            f"iluminação natural, móveis modernos, ultra realista, "
            f"renderização 3D arquitetônica profissional, 8k, alta qualidade"
        )

def generate_3d_render(description, plan):
        """
            Detecta cômodos numerados na descrição e gera uma imagem para cada um.
                Retorna (caminho_principal, lista_de_resultados)
                    """
        safe_desc = sanitize_filename(description or "projeto")
        comodos = extrair_comodos(description)

    if not comodos:
                comodos = ["fachada externa moderna do projeto"]

    results = []

    for comodo in comodos:
                safe_label = sanitize_filename(comodo)
                output_path = os.path.join(STATIC_DIR, f"render_{safe_desc}_{safe_label}.png")
                prompt = build_prompt(comodo, description)

        try:
                        print(f"[StableDiffusion] Gerando imagem para comodo: {comodo}")
                        result = gerar_imagem(prompt, output_path)
                        if result:
                                            results.append({
                                                                    "label": comodo,
                                                                    "path": f"static/render_{safe_desc}_{safe_label}.png"
                                            })
        else:
                raise Exception("Falha na geracao")
        except Exception as e:
            print(f"[Simulacao] Erro em '{comodo}': {e}. Gerando simulado.")
            with open(output_path, "wb") as f:
                                f.write(b"")
                            results.append({
                                                "label": comodo,
                                                "path": f"static/render_{safe_desc}_{safe_label}.png"
                            })

    caminho_principal = results[0]["path"] if results else f"static/render3d_{safe_desc}.png"
    return caminho_principal, results
