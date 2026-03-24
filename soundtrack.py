# Adição de trilha sonora

import os
import re

def sanitize_filename(text):
    return re.sub(r'[^\w\-]', '_', text)[:40]

def add_soundtrack(video, soundtrack="violao_beethoven.mp3"):
    """
    Simula a adição de trilha sonora ao vídeo.
    (No futuro: integrar com FFmpeg ou Creatomate)
    """
    print(f"[Simulação] Adicionando trilha sonora '{soundtrack}' ao vídeo '{video}'")
    base = os.path.splitext(video)[0]
    base = sanitize_filename(base)
    output_video = f"{base}_com_trilha.mp4"
    with open(output_video, "wb") as f:
        f.write(b"")
    return output_video
