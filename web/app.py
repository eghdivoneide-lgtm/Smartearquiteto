
import os
from flask import Flask, render_template, request, redirect, url_for

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from render3d import generate_3d_render
from narration import generate_narration_script, synthesize_voice
from subtitles import generate_subtitles
from soundtrack import add_soundtrack
from video_assembler import assemble_video

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        descricao = request.form['descricao']
        planta = request.files.get('planta')
        planta_path = None
        if planta and planta.filename:
            planta_path = os.path.join(UPLOAD_FOLDER, planta.filename)
            planta.save(planta_path)

        # Executa pipeline real
        render_3d = generate_3d_render(descricao, planta_path)
        script = generate_narration_script(descricao)
        audio = synthesize_voice(script)
        legendas = generate_subtitles(script, audio)
        trilha = "violao_beethoven.mp3"  # Simulado
        video_com_trilha = add_soundtrack(render_3d, trilha)
        video_final = assemble_video(video_com_trilha, audio, legendas, trilha)

        # Passa caminhos dos arquivos para a página de sucesso
        return render_template('sucesso.html', descricao=descricao, planta=planta.filename if planta else '',
                      render_3d=render_3d, audio=audio, legendas=legendas,
                      trilha=trilha, video_final=video_final,
                      render_3d_img=render_3d if render_3d.endswith('.png') else None)
    return render_template('index.html')

@app.route('/sucesso')
def sucesso():
    # Rota não usada diretamente, apenas via POST
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
