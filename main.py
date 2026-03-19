import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import VideoFileClip, AudioFileClip
import threading


def hhmmss_para_segundos(hhmmss):
    try:
        h, m, s = map(int, hhmmss.split(":"))
        return h * 3600 + m * 60 + s
    except:
        return 0

def segundos_para_hhmmss(seg):
    h = int(seg // 3600)
    m = int((seg % 3600) // 60)
    s = int(seg % 60)
    return f"{h:02}:{m:02}:{s:02}"

def escolher_arquivo():
    global duracao_video, clip, tipo_clip
    caminho = filedialog.askopenfilename(filetypes=[("Mídia", "*.mp4 *.avi *.mov *.mkv *.mp3 *.wav *.m4a")])
    if caminho:
        entrada_entry.delete(0, tk.END)
        entrada_entry.insert(0, caminho)
        try:
            if caminho.lower().endswith((".mp3", ".wav", ".m4a")):
                clip = AudioFileClip(caminho)
                tipo_clip = "audio"
            else:
                clip = VideoFileClip(caminho)
                tipo_clip = "video"

            duracao_video = clip.duration
            label_duracao.config(text=f"Duração total: {segundos_para_hhmmss(duracao_video)}")

            slider_inicio.config(to=duracao_video)
            slider_fim.config(to=duracao_video)

            slider_inicio.set(0)
            slider_fim.set(duracao_video)

            campo_inicio.delete(0, tk.END)
            campo_fim.delete(0, tk.END)
            campo_inicio.insert(0, "00:00:00")
            campo_fim.insert(0, segundos_para_hhmmss(duracao_video))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar mídia: {e}")

def atualizar_sliders_por_campos(*args):
    try:
        slider_inicio.set(hhmmss_para_segundos(campo_inicio.get()))
        slider_fim.set(hhmmss_para_segundos(campo_fim.get()))
    except:
        pass

def atualizar_campos_por_sliders(*args):
    campo_inicio.delete(0, tk.END)
    campo_fim.delete(0, tk.END)
    campo_inicio.insert(0, segundos_para_hhmmss(slider_inicio.get()))
    campo_fim.insert(0, segundos_para_hhmmss(slider_fim.get()))

def mostrar_preview():
    if not entrada_entry.get():
        messagebox.showwarning("Atenção", "Selecione um vídeo primeiro.")
        return
    if tipo_clip == "video":
        try:
            clip.preview()
        except Exception as e:
            messagebox.showerror("Erro no preview", str(e))
    else:
        messagebox.showinfo("Aviso", "Preview não disponível para áudio.")

def atualizar_progresso(valor):
    barra_progresso['value'] = valor
    janela.update_idletasks()

def processar_video():
    try:
        atualizar_progresso(10)
        t1 = hhmmss_para_segundos(campo_inicio.get())
        t2 = hhmmss_para_segundos(campo_fim.get())

        if t1 >= t2:
            raise ValueError("O tempo de início deve ser menor que o de fim.")

        novo_clip = clip.subclip(t1, t2)
        atualizar_progresso(50)

        extensao = ".mp3" if tipo_clip == "audio" else ".mp4"
        salvar_como = filedialog.asksaveasfilename(
            defaultextension=extensao,
            filetypes=[("Áudio" if tipo_clip == "audio" else "Vídeo", "*" + extensao)],
            title="Salvar como"
        )

        if salvar_como:
            atualizar_progresso(80)
            novo_clip.write_audiofile(salvar_como) if tipo_clip == "audio" else novo_clip.write_videofile(salvar_como)
            atualizar_progresso(100)
            messagebox.showinfo("Sucesso", "Arquivo recortado com sucesso!")

        novo_clip.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")
    finally:
        atualizar_progresso(0)

def iniciar_processamento():
    threading.Thread(target=processar_video).start()


# Interface
janela = tk.Tk()
janela.title("Cortador de Vídeo/Áudio com HH:MM:SS")
janela.geometry("520x530")
janela.configure(bg="#f0f0f0")

duracao_video = 0
clip = None
tipo_clip = "video"

tk.Label(janela, text="Selecione um arquivo:", bg="#f0f0f0").pack(pady=5)
entrada_entry = tk.Entry(janela, width=60)
entrada_entry.pack(pady=5)
tk.Button(janela, text="Escolher Arquivo", command=escolher_arquivo).pack(pady=5)

label_duracao = tk.Label(janela, text="Duração total: --:--:--", bg="#f0f0f0")
label_duracao.pack(pady=5)

# Sliders e campos HH:MM:SS
tk.Label(janela, text="Início:", bg="#f0f0f0").pack()
campo_inicio = tk.Entry(janela, width=10, justify='center')
campo_inicio.pack()
campo_inicio.bind("<KeyRelease>", atualizar_sliders_por_campos)

slider_inicio = tk.Scale(janela, from_=0, to=100, orient="horizontal", length=400, command=atualizar_campos_por_sliders)
slider_inicio.pack()

tk.Label(janela, text="Fim:", bg="#f0f0f0").pack()
campo_fim = tk.Entry(janela, width=10, justify='center')
campo_fim.pack()
campo_fim.bind("<KeyRelease>", atualizar_sliders_por_campos)

slider_fim = tk.Scale(janela, from_=0, to=100, orient="horizontal", length=400, command=atualizar_campos_por_sliders)
slider_fim.pack()

# Preview e progresso
tk.Button(janela, text="Mostrar Preview", bg="#2196F3", fg="white", command=mostrar_preview).pack(pady=10)
barra_progresso = ttk.Progressbar(janela, orient='horizontal', length=400, mode='determinate')
barra_progresso.pack(pady=10)

tk.Button(janela, text="Recortar e Salvar", bg="#4CAF50", fg="white", command=iniciar_processamento).pack(pady=10)

janela.mainloop()