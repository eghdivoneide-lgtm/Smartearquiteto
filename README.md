# EDS SmartArquiteto

Projeto para automação de geração de vídeos arquitetônicos/imobiliários com pipeline modular.

## Estrutura Inicial

| Módulo                | Função Principal                                  |
|-----------------------|---------------------------------------------------|
| input_handler.py      | Recebe e valida entrada do usuário                |
| render3d.py           | Integração com APIs de renderização 3D            |
| narration.py          | Geração de texto e narração em voz                |
| subtitles.py          | Sincronização e geração de legendas               |
| soundtrack.py         | Adição de trilha sonora                           |
| video_assembler.py    | Montagem e exportação do vídeo final              |
| config.py             | Configurações globais e chaves de API             |
| main.py               | Orquestra o pipeline completo                     |

## Como usar
1. Configure as APIs em `config.py`
2. Execute `main.py` para iniciar o fluxo

---

Este projeto está pronto para expansão e integração com novas funcionalidades.