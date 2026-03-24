# Montagem e exportação do vídeo final

import os
import re

def sanitize_filename(text):
    return re.sub(r'[^\w\-]', '_', text)[:40]

def assemble_video(rendered_video, narration_audio, subtitles, soundtrack):
    """
    Simula a montagem final do vídeo, unindo todas as camadas.
    (No futuro: usar FFmpeg para merge real)
    """
    base = os.path.splitext(rendered_video)[0]
    base = sanitize_filename(base)
    output_final = f"{base}_final.mp4"
    print(f"[Simulação] Montando vídeo final: {output_final}")
    # Simula a criação do arquivo final
    with open(output_final, "wb") as f:
        f.write(b"")
    return output_final
