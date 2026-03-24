# Sincronização e geração de legendas

import os

def generate_subtitles(script, audio):
    """
    Simula a geração de um arquivo de legendas (SRT) a partir do script de narração.
    (No futuro: sincronizar com áudio real)
    """
    srt_path = "legendas_automaticas.srt"
    print(f"[Simulação] Gerando legendas automáticas: {srt_path}")
    # Simula um arquivo SRT simples
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("1\n00:00:00,000 --> 00:00:05,000\n" + script + "\n")
    return srt_path
