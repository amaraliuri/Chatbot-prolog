import subprocess
import unicodedata
import tkinter as tk
from tkinter import scrolledtext

CAMINHO_SWIPL = "swipl"


def limpar_texto(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    for char in "?!.,;:'\"":
        texto = texto.replace(char, "")
    return texto


def consultar_prolog(pergunta):
    pergunta_limpa = limpar_texto(pergunta)
    if not pergunta_limpa:
        return ""

    comando_prolog = (
        f"set_prolog_flag(encoding, utf8), "
        f"responder_pergunta(['{pergunta_limpa}'], Resposta), "
        f"write(Resposta)"
    )

    try:
        resultado = subprocess.run(
            [CAMINHO_SWIPL, "-q", "-s", "chatbot.pl", "-g", comando_prolog, "-t", "halt"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        resposta = resultado.stdout.strip()
        return resposta if resposta else "Desculpe, não entendi sua pergunta."
    except FileNotFoundError:
        return "Erro: SWI-Prolog (swipl) não encontrado. Verifique a variável CAMINHO_SWIPL."


def enviar_pergunta(event=None):
    pergunta = campo_entrada.get().strip()
    if not pergunta:
        return

    if pergunta.lower() == "sair":
        janela.destroy()
        return

    exibir_mensagem("Você", pergunta, "usuario")
    campo_entrada.delete(0, tk.END)

    resposta = consultar_prolog(pergunta)
    exibir_mensagem("Bot", resposta, "bot")


def exibir_mensagem(remetente, texto, tag):
    area_chat.config(state=tk.NORMAL)
    area_chat.insert(tk.END, f"{remetente}: ", tag)
    area_chat.insert(tk.END, f"{texto}\n\n")
    area_chat.config(state=tk.DISABLED)
    area_chat.see(tk.END)


janela = tk.Tk()
janela.title("Chatbot Foz do Iguaçu - Prolog + Python")
janela.geometry("540x450")
janela.configure(bg="#f0f2f5")

area_chat = scrolledtext.ScrolledText(
    janela, wrap=tk.WORD, state=tk.DISABLED, font=("Segoe UI", 10), bg="white", padx=10, pady=10
)
area_chat.pack(padx=12, pady=(12, 6), fill=tk.BOTH, expand=True)

area_chat.tag_config("usuario", foreground="#0b57d0", font=("Segoe UI", 10, "bold"))
area_chat.tag_config("bot", foreground="#146c2e", font=("Segoe UI", 10, "bold"))

frame_inferior = tk.Frame(janela, bg="#f0f2f5")
frame_inferior.pack(padx=12, pady=(0, 12), fill=tk.X)

campo_entrada = tk.Entry(frame_inferior, font=("Segoe UI", 11))
campo_entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
campo_entrada.bind("<Return>", enviar_pergunta)
campo_entrada.focus()

botao_enviar = tk.Button(
    frame_inferior,
    text="Enviar",
    command=enviar_pergunta,
    font=("Segoe UI", 10, "bold"),
    bg="#0b57d0",
    fg="white",
    padx=15,
    cursor="hand2"
)
botao_enviar.pack(side=tk.RIGHT, padx=(8, 0), ipady=3)

exibir_mensagem("Bot", "Olá! Pergunte algo sobre Foz do Iguaçu (ou digite 'sair' para fechar).", "bot")

janela.mainloop()