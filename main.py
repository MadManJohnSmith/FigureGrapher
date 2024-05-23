import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from screeninfo import get_monitors

# Historial de figuras
historial = []

# Color y coordenadas seleccionados
color_seleccionado = 'red'  # Rojo por defecto
coordenada_seleccionada = (0, 0)  # Centro por defecto


def circulo(ax, radio, color, coord=(0, 0)):
    circle = plt.Circle(coord, radio, color=color)
    ax.add_patch(circle)
    historial.append(circle)


def triangulo(ax, base, altura, color, coord=(0, 0)):
    x, y = coord
    triangle = plt.Polygon([[x, y], [x + base, y], [x + base / 2, y + altura]], color=color)
    ax.add_patch(triangle)
    historial.append(triangle)


def rectangulo(ax, width, altura, color, coord=(0, 0)):
    x, y = coord
    rectangle = plt.Rectangle((x, y), width, altura, color=color)
    ax.add_patch(rectangle)
    historial.append(rectangle)


def seleccionar_color(new_color):
    global color_seleccionado
    color_seleccionado = new_color


def seleccionar_coordenada(new_coord):
    global coordenada_seleccionada
    coordenada_seleccionada = new_coord


def actualizarPlot(plot_function, *args):
    try:
        args = [float(arg.get()) for arg in args]
    except ValueError:
        messagebox.showerror("Error", "Todos los valores deben ser números.")
        return

    plot_function(ax, *args, color=color_seleccionado, coord=coordenada_seleccionada)
    ax.relim()
    ax.autoscale_view()
    canvas.draw()


def validarCirculo():
    if not radius_entry.get():
        messagebox.showerror("Error", "Por favor ingrese el valor del radio.")
    else:
        actualizarPlot(circulo, radius_entry)


def validarTriangulo():
    if not base_entry.get() or not altura_entry.get():
        messagebox.showerror("Error", "Por favor ingrese los valores de base y altura.")
    else:
        actualizarPlot(triangulo, base_entry, altura_entry)


def validarRectangulo():
    if not width_entry.get() or not altura2_entry.get():
        messagebox.showerror("Error", "Por favor ingrese los valores de ancho y alto.")
    else:
        actualizarPlot(rectangulo, width_entry, altura2_entry)


def deshacer():
    if historial:
        last_patch = historial.pop()
        last_patch.remove()
        ax.relim()
        ax.autoscale_view()
        canvas.draw()
    else:
        messagebox.showinfo("Info", "No hay figuras para deshacer.")


def parse_command(command):
    tokens = command.split()
    if not tokens:
        return

    action = tokens[0].lower()

    try:
        if action == "crear":
            shape_type = tokens[1].lower()
            if shape_type == "circulo":
                x, y, r = map(float, tokens[2:5])
                circulo(ax, r, color=color_seleccionado, coord=(x, y))
            elif shape_type == "rectangulo":
                x, y, width, height = map(float, tokens[2:6])
                rectangulo(ax, width, height, color=color_seleccionado, coord=(x, y))
            elif shape_type == "cuadrado":
                x, y, side = map(float, tokens[2:5])
                rectangulo(ax, side, side, color=color_seleccionado, coord=(x, y))
            elif shape_type == "triangulo":
                x, y, base, height = map(float, tokens[2:6])
                triangulo(ax, base, height, color=color_seleccionado, coord=(x, y))
            ax.relim()
            ax.autoscale_view()
            canvas.draw()
        elif action == "deshacer":
            deshacer()
    except (IndexError, ValueError):
        print("Error en el comando o parámetros incorrectos")


def execute_command(event):
    command = command_entry.get()
    command_entry.delete(0, tk.END)
    parse_command(command)


# Tamaño de pantalla
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

# Ventana con Tkinter
root = tk.Tk()
root.geometry(f'{screen_width // 2 - 300}x{screen_height - 90}+0+0')  # Ventana más ancha
root.title('Graficador de Figuras Geométricas')

# Título
label = tk.Label(root, text='Graficador de Figuras Geometricas', font=('Arial', 14))
label.pack(padx=5, pady=5)

# Plot con Matplotlib
fig, ax = plt.subplots(figsize=(14, 3), dpi=100)
ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)
ax.set_aspect('equal')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(padx=5)

# Frame principal
buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)

# Grid de colores y coordenadas en la misma fila
grids_frame = tk.Frame(root)
grids_frame.pack(pady=5)

# Grid de colores
color_frame = tk.Frame(grids_frame)
color_frame.grid(row=0, column=0, padx=10)
selected_color_button = None
colores = ['indianred', 'aquamarine', 'silver', 'skyblue', 'plum', 'lightyellow', 'navajowhite', 'blueviolet']
for i, color in enumerate(colores):
    btn = tk.Button(color_frame, bg=color, width=2, height=1, command=lambda c=color: seleccionar_color(c))
    btn.grid(row=i // 3, column=i % 3, padx=1, pady=1)
undo_button = tk.Button(color_frame, text='Des', font=('Arial', 7), command=deshacer)
undo_button.grid(row=2, column=2, padx=1, pady=1)

# Grid de coordenadas
coord_frame = tk.Frame(grids_frame)
coord_frame.grid(row=0, column=1, padx=10)
coordenadas = [(-8, 8), (0, 8), (8, 8), (-8, 0), (0, 0), (8, 0), (-8, -8), (0, -8), (8, -8)]
for i, coord in enumerate(coordenadas):
    btn = tk.Button(coord_frame, text=str(coord), width=5, command=lambda c=coord: seleccionar_coordenada(c))
    btn.grid(row=i // 3, column=i % 3)

# Campos círculo
btn1 = tk.Button(buttonframe, text='Crear Circulo', font=('Arial', 12, 'bold'), command=validarCirculo)
btn1.grid(row=0, column=0, columnspan=2, sticky=tk.W + tk.E)
radius_label = tk.Label(buttonframe, text="Radio:")
radius_label.grid(row=1, column=0, sticky=tk.W)
radius_entry = tk.Entry(buttonframe)
radius_entry.grid(row=1, column=1, sticky=tk.W + tk.E)

# Campos triángulo
btn2 = tk.Button(buttonframe, text='Crear Triángulo', font=('Arial', 12, 'bold'), command=validarTriangulo)
btn2.grid(row=2, column=0, columnspan=2, sticky=tk.W + tk.E)
base_label = tk.Label(buttonframe, text="Base:")
base_label.grid(row=3, column=0, sticky=tk.W)
base_entry = tk.Entry(buttonframe)
base_entry.grid(row=3, column=1, sticky=tk.W + tk.E)
altura_label = tk.Label(buttonframe, text="Altura:")
altura_label.grid(row=4, column=0, sticky=tk.W)
altura_entry = tk.Entry(buttonframe)
altura_entry.grid(row=4, column=1, sticky=tk.W + tk.E)

# Campos rectángulo
btn3 = tk.Button(buttonframe, text='Crear Rectangulo', font=('Arial', 12, 'bold'), command=validarRectangulo)
btn3.grid(row=5, column=0, columnspan=2, sticky=tk.W + tk.E)
width_label = tk.Label(buttonframe, text="Ancho:")
width_label.grid(row=6, column=0, sticky=tk.W)
width_entry = tk.Entry(buttonframe)
width_entry.grid(row=6, column=1, sticky=tk.W + tk.E)
altura2_label = tk.Label(buttonframe, text="Altura:")
altura2_label.grid(row=7, column=0, sticky=tk.W)
altura2_entry = tk.Entry(buttonframe)
altura2_entry.grid(row=7, column=1, sticky=tk.W + tk.E)

buttonframe.pack(fill='x', pady=5)

# Entrada de comandos
command_entry = tk.Entry(root)
command_entry.pack()
command_entry.bind("<Return>", execute_command)

root.mainloop()
