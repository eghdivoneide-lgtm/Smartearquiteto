# Orquestra o pipeline completo

def main():

    from render3d import generate_3d_render
    from narration import generate_narration_script, synthesize_voice
    from subtitles import generate_subtitles
    from soundtrack import add_soundtrack
    from video_assembler import assemble_video

    print("=== EDSSmarteArquiteto ===")
    print("Simulação de pipeline CLI\n")

    # 1. Receber entrada do usuário
    descricao = input("Descreva o projeto (ex: kitnet, casa, prédio): ")
    planta = input("Caminho do arquivo da planta (simulado): ")
    print(f"\nRecebido: {descricao}, planta: {planta}")

    # 2. Gerar render 3D (simulado ou real)
    render_3d = generate_3d_render(descricao, planta)
    print(f"Arquivo gerado: {render_3d}")

    # 3. Gerar narração (real)
    print("Gerando narração automática...")
    script = generate_narration_script(descricao)
    print(f"Script gerado:\n{script}")
    audio = synthesize_voice(script)
    print(f"Arquivo de áudio: {audio}")

    # 4. Gerar legendas automáticas (simulado ou real)
    legendas = generate_subtitles(script, audio)
    print(f"Arquivo de legendas: {legendas}")

    # 5. Adicionar trilha sonora (simulado ou real)
    trilha = "violao_beethoven.mp3"
    video_com_trilha = add_soundtrack(render_3d, trilha)
    print(f"Trilha: {trilha}\nVídeo com trilha: {video_com_trilha}")

    # 6. Montar vídeo final (simulado ou real)
    video_final = assemble_video(
        video_com_trilha,
        audio,
        legendas,
        trilha
    )
    print(f"Vídeo final gerado: {video_final}")

    print("\nPipeline concluído com sucesso!")

if __name__ == "__main__":
    main()
