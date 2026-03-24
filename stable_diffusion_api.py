import os
import requests
import time

# ---------------------------------------------------------------
# Integracao com Google Gemini Imagen 3 via API REST
# Configure sua chave em variavel de ambiente:
#   export GEMINI_API_KEY="sua_chave_aqui"
# Ou obtenha em: https://aistudio.google.com/app/apikey
# ---------------------------------------------------------------

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

IMAGEN_URL = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "imagen-3.0-generate-002:predict"
)


def gerar_imagem(prompt, output_path="imagem_gemini.png"):
        """
            Gera uma imagem usando o Gemini Imagen 3 e salva no output_path.
                Retorna o caminho do arquivo salvo, ou None em caso de erro.
                    """
        if not GEMINI_API_KEY:
                    print("[ERRO Gemini] GEMINI_API_KEY nao configurada.")
                    print("[ERRO Gemini] Configure: export GEMINI_API_KEY='sua_chave'")
                    return None

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY,
        }

    payload = {
                "instances": [
                                {"prompt": prompt}
                ],
                "parameters": {
                                "sampleCount": 1,
                                "aspectRatio": "16:9",
                                "safetyFilterLevel": "block_few",
                                "personGeneration": "dont_allow"
                }
    }

    try:
                print(f"[Gemini Imagen 3] Gerando imagem para prompt: {prompt[:60]}...")
                response = requests.post(IMAGEN_URL, json=payload, headers=headers, timeout=60)

        if response.status_code != 200:
                        print(f"[ERRO Gemini] Status: {response.status_code}")
                        print(f"[ERRO Gemini] Resposta: {response.text}")
                        return None

        data = response.json()
        predictions = data.get("predictions", [])

        if not predictions:
                        print("[ERRO Gemini] Nenhuma imagem retornada na resposta.")
                        return None

        # A imagem vem em base64
        import base64
        image_b64 = predictions[0].get("bytesBase64Encoded", "")
        if not image_b64:
                        print("[ERRO Gemini] Campo bytesBase64Encoded ausente.")
                        return None

        image_bytes = base64.b64decode(image_b64)
        with open(output_path, "wb") as f:
                        f.write(image_bytes)

        print(f"[Gemini Imagen 3] Imagem salva em: {output_path}")
        return output_path

except requests.exceptions.Timeout:
        print("[ERRO Gemini] Timeout na requisicao (60s).")
        return None
except Exception as e:
        print(f"[ERRO Gemini] Excecao inesperada: {e}")
        return None
