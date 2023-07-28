import socket
import threading
import tkinter
from tkinter import *
from tkinter import simpledialog


class Chat:
    def __init__(self):
        HOST = 'localhost'
        PORT = 55556
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        login = Tk()
        login.withdraw()

        self.janela_carregada = False
        self.ativo = True

        self.nome = simpledialog.askstring('Nome', 'Digite seu nome!', parent=login)
        self.sala = simpledialog.askstring('Sala', 'Digite a sala que deseja entrar!', parent=login)

        thread = threading.Thread(target=self.conecta)
        thread.start()
        self.janela()


    def janela(self):
        self.root = Tk()
        self.root.geometry('800x800')
        self.root.title('Chat')

        self.caixa_texto = Text(self.root)
        self.caixa_texto.place(relx=0.05, rely=0.01, width=700, height=600)

        self.input = Entry(self.root)
        self.input.place(relx=0.05, rely=0.8, width=500, height=30)

        self.btn_enviar = Button(self.root, text='Enviar', command=self.enviar_mensagem)
        self.btn_enviar.place(relx=0.7, rely=0.8, width=100, height=30)

        self.root.protocol('WM_DELETE_WINDOW', self.fechar)

        self.root.mainloop()


    def fechar(self):
        self.root.destroy()
        self.client.close()


    def enviar_mensagem(self):
        mensagem = self.input.get()
        self.client.send(mensagem.encode())


    def conecta(self):
        while True:
            recebido = self.client.recv(1024)
            if recebido == b'SALA':
                self.client.send(self.sala.encode())
                self.client.send(self.nome.encode())
            else:
                try:
                    self.caixa_texto.insert('end', recebido.decode())
                except Exception as e:
                    print(f'Erro: {e}')


chat = Chat()