import requests
import time

# Substitua pela sua chave válida do Replicate
REPLICATE_API_TOKEN = "r8_PtZglm16uOf0iZE301BKQDe5HBs7YU32TqNcTpodee"

# Versão correta do modelo Stable Diffusion XL (SDXL) no Replicate
MODEL_VERSION = "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc"

def gerar_imagem(prompt, output_path="imagem_sd.png"):
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "version": MODEL_VERSION,
        "input": {"prompt": prompt}
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 201:
        print("[ERRO Replicate] Status:", response.status_code)
        print("[ERRO Replicate] Resposta completa:", response.text)
        try:
            print("[ERRO Replicate] JSON:", response.json())
        except Exception as e:
            print("[ERRO Replicate] Não foi possível decodificar JSON:", e)
        return None

    prediction = response.json()
    prediction_id = prediction["id"]

    # Polling para aguardar a geração da imagem
    for _ in range(30):
        time.sleep(3)
        poll = requests.get(f"https://api.replicate.com/v1/predictions/{prediction_id}", headers=headers)
        result = poll.json()
        if result["status"] == "succeeded":
            image_url = result["output"][0]
            img_data = requests.get(image_url).content
            with open(output_path, "wb") as f:
                f.write(img_data)
            print(f"Imagem salva em {output_path}")
            return output_path
        elif result["status"] == "failed":
            print("Geração falhou:", result)
            return None

    print("Tempo limite atingido para geração da imagem.")
    return None
