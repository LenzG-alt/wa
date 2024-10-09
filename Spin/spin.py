import random
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# Archivo donde se guardarán los datos
filename = 'equipos.txt'

# Función para cargar los equipos desde el archivo
def cargar_equipos():
    equipos = {}
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            current_team = None
            for line in f:
                line = line.strip()
                if line.startswith("Equipo:"):
                    current_team = line.split(": ")[1]
                    equipos[current_team] = []
                elif current_team:
                    equipos[current_team].append(line)
    return equipos

# Función para guardar los equipos en el archivo
def guardar_equipos(equipos):
    with open(filename, 'w') as f:
        for equipo, integrantes in equipos.items():
            f.write(f"Equipo: {equipo}\n")
            for integrante in integrantes:
                f.write(f"{integrante}\n")

# Función para agregar un equipo y sus integrantes
def agregar_equipo():
    equipo = simpledialog.askstring("Agregar equipo", "Ingrese el nombre del equipo:")
    if equipo:
        integrantes = []
        while True:
            integrante = simpledialog.askstring("Agregar integrante", "Ingrese el nombre del integrante (o presione Cancelar para finalizar):")
            if not integrante:
                break
            integrantes.append(integrante)
        equipos[equipo] = integrantes
        guardar_equipos(equipos)
        messagebox.showinfo("Equipo agregado", f"Equipo '{equipo}' agregado exitosamente.")

# Función para modificar un equipo existente
def modificar_equipo():
    equipo = simpledialog.askstring("Modificar equipo", "Ingrese el nombre del equipo a modificar:")
    if equipo in equipos:
        nuevo_nombre = simpledialog.askstring("Modificar equipo", f"Ingrese el nuevo nombre del equipo (o deje en blanco para mantener '{equipo}'):")
        if nuevo_nombre:
            equipos[nuevo_nombre] = equipos.pop(equipo)
            equipo = nuevo_nombre
        
        integrantes = []
        while True:
            integrante = simpledialog.askstring("Modificar integrante", "Ingrese el nombre del integrante (o presione Cancelar para finalizar):")
            if not integrante:
                break
            integrantes.append(integrante)
        equipos[equipo] = integrantes
        guardar_equipos(equipos)
        messagebox.showinfo("Equipo modificado", f"Equipo '{equipo}' modificado exitosamente.")
    else:
        messagebox.showerror("Error", "El equipo no existe.")

# Función para realizar un sorteo de equipos (sin repetir)
def sorteo_equipos():
    cantidad = simpledialog.askinteger("Sorteo de equipos", "Ingrese la cantidad de equipos a sortear:")
    if cantidad and cantidad <= len(equipos):
        equipos_sorteados = random.sample(list(equipos.keys()), cantidad)
        resultado = "\n".join(equipos_sorteados)
        messagebox.showinfo("Equipos sorteados", resultado)
        
        with open('sorteo_resultados.txt', 'a') as f:
            f.write(f"Equipos sorteados: {', '.join(equipos_sorteados)}\n")
    else:
        messagebox.showerror("Error", "Cantidad inválida o mayor que el número de equipos disponibles.")

# Función para realizar un sorteo de integrantes de los equipos seleccionados
def sorteo_integrantes():
    equipos_a_sortear = simpledialog.askstring("Sorteo de integrantes", "Ingrese los equipos separados por coma (deje en blanco para sortear de todos los equipos):").split(",")
    equipos_a_sortear = [equipo.strip() for equipo in equipos_a_sortear if equipo.strip()]
    
    if not equipos_a_sortear:
        equipos_a_sortear = list(equipos.keys())
    
    sorteados = []
    for equipo in equipos_a_sortear:
        if equipo in equipos and equipos[equipo]:
            integrante_sorteado = random.choice(equipos[equipo])
            sorteados.append(f"{integrante_sorteado} del equipo {equipo}")
    
    resultado = "\n".join(sorteados)
    messagebox.showinfo("Integrantes sorteados", resultado)
    
    with open('sorteo_resultados.txt', 'a') as f:
        for s in sorteados:
            f.write(f"{s}\n")

# Interfaz gráfica con tkinter
def iniciar_interfaz():
    global equipos
    equipos = cargar_equipos()

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Sorteo de Equipos e Integrantes")

    # Estilos personalizados
    bg_color = "#f5f5f5"  # Fondo claro
    header_color = "#8bc34a"  # Verde suave
    button_color = "#4caf50"  # Verde más oscuro
    button_hover = "#81c784"  # Verde más claro al pasar el cursor
    text_color = "#ffffff"  # Color de texto blanco

    root.config(bg=bg_color)
    
    # Barra superior decorativa
    header = tk.Frame(root, bg=header_color, height=60)
    header.pack(fill="x")
    
    tk.Label(header, text="Sorteo de Equipos e Integrantes", font=("Helvetica", 18), bg=header_color, fg=text_color).pack(pady=10)
    
    # Configuración del menú principal
    menu_frame = tk.Frame(root, bg=bg_color, padx=20, pady=20)
    menu_frame.pack()

    def on_enter(e, button):
        button['bg'] = button_hover

    def on_leave(e, button):
        button['bg'] = button_color

    def create_button(text, command):
        button = tk.Button(menu_frame, text=text, width=25, height=2, bg=button_color, fg=text_color, font=("Helvetica", 12), command=command, relief="flat", bd=0)
        button.pack(pady=10)

        button.bind("<Enter>", lambda e: on_enter(e, button))
        button.bind("<Leave>", lambda e: on_leave(e, button))

    create_button("Agregar equipo", agregar_equipo)
    create_button("Modificar equipo", modificar_equipo)
    create_button("Sorteo de equipos", sorteo_equipos)
    create_button("Sorteo de integrantes", sorteo_integrantes)
    create_button("Salir", root.quit)

    root.mainloop()

# Iniciar la interfaz gráfica
if __name__ == "__main__":
    iniciar_interfaz()
