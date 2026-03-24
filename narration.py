# Geração de texto e narração em voz

def generate_narration_script(description):
    """
    Gera um texto descritivo para narração a partir da descrição do projeto.
    (Simulação: retorna um texto pronto)
    """
    return f"Bem-vindo ao tour virtual do projeto: {description}. Este vídeo apresenta todos os detalhes e diferenciais deste empreendimento."

import requests
import os
from config import NARRATION_API_KEY

def synthesize_voice(script, voice_id="EXAVITQu4vr4xnSDxMaL"):
    """
    Gera áudio de narração usando ElevenLabs (ou simula se não houver chave).
    Salva o arquivo MP3 localmente.
    """
    if not NARRATION_API_KEY:
        print("[Simulação] Chave ElevenLabs não configurada. Gerando áudio simulado.")
        audio_path = "narracao_simulada.mp3"
        # Aqui você pode gerar um arquivo vazio ou apenas simular
        with open(audio_path, "wb") as f:
            f.write(b"")
        return audio_path

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": NARRATION_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": script,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        audio_path = "narracao_gerada.mp3"
        with open(audio_path, "wb") as f:
            f.write(response.content)
        print(f"Áudio gerado com sucesso: {audio_path}")
        return audio_path
    else:
        print(f"Erro na API ElevenLabs: {response.status_code} - {response.text}")
        return None
