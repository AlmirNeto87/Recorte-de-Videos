Aplicativo desktop em Python para recortar segmentos de vídeos e áudios usando tempo de início e fim em formato `HH:MM:SS`, com interface gráfica (Tkinter) e processamento via MoviePy.

## Funcionalidades

- Suporte a arquivos de vídeo: MP4, AVI, MOV, MKV
- Suporte a arquivos de áudio: MP3, WAV, M4A
- Exibição de duração total da mídia
- Seleção de intervalo via campos de texto `HH:MM:SS` e sliders
- Preview (somente para vídeo)
- Barra de progresso durante exportação
- Exporta corte para arquivo de vídeo (`.mp4`) ou áudio (`.mp3`)

## Requisitos

- Python 3.8+
- Bibliotecas:
  - `moviepy`

## Instalação

1. Crie/ative um ambiente virtual (opcional, recomendado):

```bash
python -m venv venv
venv\\Scripts\\activate
```

2. Instale dependências:

```bash
pip install moviepy
```

## Uso

1. Execute o programa:

```bash
python main.py
```

2. Na janela, clique em `Escolher Arquivo` e selecione o arquivo de vídeo/áudio.
3. Ajuste o início e o fim manualmente (`HH:MM:SS`) ou via slider.
4. (Vídeo) clique em `Mostrar Preview` para checar o trecho.
5. Clique em `Recortar e Salvar`, escolha um caminho e aguarde o fim do processo.

## Observações

- O tempo de início deve ser menor que o tempo de fim.
- Em caso de erro na leitura ou na gravação, será mostrado um alerta.

## Estrutura do código

- `main.py`: interface e lógica principal
- Funções utilitárias:
  - `hhmmss_para_segundos`
  - `segundos_para_hhmmss`
  - `escolher_arquivo`
  - `atualizar_sliders_por_campos`
  - `atualizar_campos_por_sliders`
  - `mostrar_preview`
  - `processar_video`
  - `iniciar_processamento`

## Melhoria futura

- Suporte a mais formatos e codecs de vídeo
- Exportar para `.wav` usando `write_audiofile` para áudio
- Melhor tratamento de exceções e validação de entrada
- Tradução/internacionalização da interface
'''; open('README.md','w',encoding='utf-8').write(text); print('README gerado com sucesso.')"