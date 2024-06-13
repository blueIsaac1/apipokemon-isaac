import tkinter as tk
from tkinter import messagebox
import requests
import json
from PIL import Image, ImageTk  # Importando classes necessárias do módulo PIL
from io import BytesIO  # Importando BytesIO para lidar com a imagem de forma eficiente

def requisicao(pokemon):
    try:
        req = requests.get('https://pokeapi.co/api/v2/pokemon/' + pokemon)
        if req.status_code == 404:
            messagebox.showerror('Erro', 'Pokemon não encontrado')
            return None
        else:
            return json.loads(req.text)
    except Exception as e:
        messagebox.showerror('Erro', f'Erro na conexão: {e}')
        return None

def mostrar_pokemon():
    pokemon = entry_pokemon.get()
    dados = requisicao(pokemon.lower())  # Convertendo para minúsculas para corresponder ao formato esperado pela API
    if dados:
        tipos = ', '.join([tipo['type']['name'] for tipo in dados['types']])
        altura = dados['height'] / 10  # Convertendo de decímetros para metros
        peso = dados['weight']
        messagebox.showinfo('Informações do Pokemon', f"Nome: {dados['name']}\nTipos: {tipos}\nAltura: {altura} m\nPeso: {peso} g")

        # Carregar e exibir a imagem do Pokemon
        imagem_url = dados['sprites']['front_default']
        imagem_bytes = requests.get(imagem_url).content
        imagem = Image.open(BytesIO(imagem_bytes))
        imagem = imagem.resize((150, 150))  # Redimensionar a imagem para 100x100 pixels
        imagem = ImageTk.PhotoImage(imagem)

        label_imagem.configure(image=imagem)
        label_imagem.image = imagem  # Mantém uma referência à imagem para evitar que seja coletada pelo garbage collector
    else:
        messagebox.showerror('Erro', 'Pokemon não encontrado')


root = tk.Tk()
root.title('Pokedex')
root.geometry('400x250')
root.configure(bg='#303030')

label_instrucao = tk.Label(root, text='Digite o nome de um Pokemon:', bg='#303030', fg='white', font=('Arial', 12))
label_instrucao.pack()

entry_pokemon = tk.Entry(root, bg='#505050', fg='white', font=('Arial', 12))
entry_pokemon.pack(pady=10)

button_pesquisar = tk.Button(root, text='Pesquisar', command=mostrar_pokemon, bg='#FF2400', fg='white', font=('Arial', 12))
button_pesquisar.pack(pady=10)

label_imagem = tk.Label(root, bg='#303030')
label_imagem.pack()

root.mainloop()
