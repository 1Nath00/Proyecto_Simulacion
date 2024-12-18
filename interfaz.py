import tkinter as tk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk, ImageEnhance
import matplotlib.pyplot as plt


def ejecutar_simulacion(horas):
    try:
        # Ejecutar el script de simulación y capturar la salida
        messagebox.showinfo(
            "Advertencia", "simulación en proceso, esto tardara la cantidad de horas que usted escogio en minutos"
        )
        resultado = subprocess.run(
            ["python", "simulacion.py", str(horas)],
            capture_output=True,
            text=True,
        )

        # Parsear los tiempos promedio desde la salida
        output = resultado.stdout
        print(output)  # Para depuración
        tiempos = parsear_tiempos(output)

        if tiempos:
            promedio_humano, promedio_robot = tiempos
            mostrar_grafica(promedio_humano, promedio_robot)
            messagebox.showinfo(
                "Éxito", "Simulación completada. Revisa la consola para los resultados."
            )
        else:
            messagebox.showwarning(
                "Advertencia", "No se pudieron calcular los promedios de los tiempos."
            )

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema: {e}")


def parsear_tiempos(output):
    """
    Extrae los promedios de los tiempos del humano y el robot de la salida del script.
    Se espera un formato específico en la salida.
    """
    try:
        # Buscar líneas específicas en la salida
        for line in output.split("\n"):
            if "Promedio Humano" in line:
                promedio_humano = float(line.split(":")[1].strip())
            if "Promedio Robot" in line:
                promedio_robot = float(line.split(":")[1].strip())
        return promedio_humano, promedio_robot
    except Exception as e:
        print(f"Error al parsear los tiempos: {e}")
        return None


def mostrar_grafica(promedio_humano, promedio_robot):
    """
    Muestra una gráfica de barras con los tiempos promedio del humano y el robot.
    """
    # Datos para la gráfica
    categorias = ["Humano", "Robot"]
    valores = [promedio_humano, promedio_robot]

    # Crear la gráfica
    plt.figure(figsize=(8, 5))
    plt.bar(categorias, valores, color=["blue", "orange"], alpha=0.7)
    plt.title("Tiempos Promedio de Resolución", fontsize=16)
    plt.ylabel("Tiempo (segundos)", fontsize=14)
    plt.xlabel("Participantes", fontsize=14)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    # Mostrar la gráfica
    plt.show()


def crear_interfaz():
    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("Simulación - Maestro del Ajedrez")
    ventana.geometry("600x400")
    ventana.resizable(False, False)

    # Fondo del tablero de ajedrez (oscurecido)
    img_tablero = Image.open("tablero.png").convert("RGB")  # Convertir a RGB
    img_tablero = img_tablero.resize((600, 400), Image.LANCZOS)
    enhancer = ImageEnhance.Brightness(img_tablero)
    img_tablero_oscura = enhancer.enhance(0.4)  # Reducir brillo al 40%
    fondo = ImageTk.PhotoImage(img_tablero_oscura)
    etiqueta_fondo = tk.Label(ventana, image=fondo)
    etiqueta_fondo.place(x=0, y=0, relwidth=1, relheight=1)

    # Frame principal para centrar todo
    frame_central = tk.Frame(ventana, bg="white")
    frame_central.place(relx=0.5, rely=0.5, anchor="center")

    # Etiqueta de título
    etiqueta = tk.Label(
        frame_central,
        text="Simulación del juego de las n-reinas",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="black"
    )
    etiqueta.pack(pady=10)

    # Frame para el selector de horas
    frame_horas = tk.Frame(frame_central, bg="white")
    frame_horas.pack(pady=10)
    tk.Label(
        frame_horas,
        text="Horas de simulación:",
        font=("Arial", 12),
        bg="white"
    ).pack(side=tk.LEFT, padx=5)

    horas_var = tk.IntVar(value=8)  # Valor predeterminado: 8 horas
    spin_horas = tk.Spinbox(
        frame_horas,
        from_=1,
        to=24,
        textvariable=horas_var,
        font=("Arial", 12),
        width=5,
    )
    spin_horas.pack(side=tk.LEFT, padx=5)

    # Botón para ejecutar simulación
    boton = tk.Button(
        frame_central,
        text="Ejecutar Simulación",
        command=lambda: ejecutar_simulacion(horas_var.get()),
        bg="green",
        fg="white",
        font=("Arial", 14),
        cursor="hand2"  # Cursor tipo pointer
    )
    boton.pack(pady=20)

    # Iniciar loop de la ventana
    ventana.mainloop()


if __name__ == "__main__":
    crear_interfaz()
