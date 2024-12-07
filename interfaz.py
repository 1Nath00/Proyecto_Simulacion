import tkinter as tk
from tkinter import messagebox
import subprocess

def ejecutar_simulacion():
    try:
        subprocess.run(["python", "simulacion.py"])
        messagebox.showinfo("Éxito", "Simulación completada. Revisa la consola para los resultados.")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema: {e}")

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Simulación - Maestro del Ajedrez")

    etiqueta = tk.Label(ventana, text="Simulación del juego de las n-reinas", font=("Arial", 14))
    etiqueta.pack(pady=10)

    boton = tk.Button(ventana, text="Ejecutar Simulación", command=ejecutar_simulacion, bg="green", fg="white", font=("Arial", 12))
    boton.pack(pady=20)

    ventana.mainloop()

if __name__ == "__main__":
    crear_interfaz()
