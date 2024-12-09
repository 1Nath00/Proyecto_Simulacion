import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
from PIL import Image, ImageTk  # Asegúrate de instalar Pillow


def ejecutar_simulacion(horas):
    try:
        # Pasar las horas como argumento al script de simulación
        subprocess.run(["python", "simulacion.py", str(horas)])
        messagebox.showinfo(
            "Éxito", "Simulación completada. Revisa la consola para los resultados.")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema: {e}")


def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Simulación - Maestro del Ajedrez")
    ventana.geometry("600x400")

    # Fondo del tablero de ajedrez
    # Asegúrate de tener una imagen llamada 'tablero.png'
    img_tablero = Image.open("tablero.png")
    img_tablero = img_tablero.resize((600, 400), Image.ANTIALIAS)
    fondo = ImageTk.PhotoImage(img_tablero)
    etiqueta_fondo = tk.Label(ventana, image=fondo)
    etiqueta_fondo.place(x=0, y=0, relwidth=1, relheight=1)

    # Etiqueta de título
    etiqueta = tk.Label(
        ventana, text="Simulación del juego de las n-reinas", font=("Arial", 16), bg="white")
    etiqueta.pack(pady=10)

    # Control para seleccionar horas
    frame_horas = tk.Frame(ventana, bg="white")
    frame_horas.pack(pady=20)
    tk.Label(frame_horas, text="Horas de simulación:", font=(
        "Arial", 12), bg="white").pack(side=tk.LEFT, padx=10)
    horas_var = tk.IntVar(value=8)  # Valor predeterminado de 8 horas
    spin_horas = tk.Spinbox(frame_horas, from_=1, to=24,
                            textvariable=horas_var, font=("Arial", 12), width=5)
    spin_horas.pack(side=tk.LEFT)

    # Botón para ejecutar simulación
    boton = tk.Button(
        ventana,
        text="Ejecutar Simulación",
        command=lambda: ejecutar_simulacion(horas_var.get()),
        bg="green",
        fg="white",
        font=("Arial", 14),
    )
    boton.pack(pady=20)

    ventana.mainloop()


if __name__ == "__main__":
    crear_interfaz()
