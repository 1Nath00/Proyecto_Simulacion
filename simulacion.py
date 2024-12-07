import simpy
import random
import time

def humano_resuelve(n):
    """Simula la resolución del problema por el humano usando un enfoque determinista."""
    start = time.time()
    # Implementar algoritmo determinista (ejemplo: backtracking)
    solucionado = False
    while not solucionado:
        # Ejemplo básico de simulación de tiempo
        time.sleep(0.01 * n)
        solucionado = True
    return time.time() - start

def robot_resuelve(n):
    """Simula la resolución del problema por el robot usando un enfoque Las Vegas."""
    start = time.time()
    solucionado = False
    while not solucionado:
        # Ejemplo básico de solución aleatoria con retroceso
        if random.random() > 0.7:  # Probabilidad de éxito
            solucionado = True
        time.sleep(0.005 * n)
    return time.time() - start

def juego(env, ganancias):
    """Simula un juego entre el humano y el robot."""
    n = random.choice([4, 5, 6, 8, 10, 12, 15])  # Selección de tablero
    tiempo_humano = humano_resuelve(n)
    tiempo_robot = robot_resuelve(n)

    if tiempo_humano < tiempo_robot:
        ganancias[0] += 30  # Humano gana
    else:
        ganancias[0] -= 10  # Robot gana

    yield env.timeout(random.uniform(10, 30))  # Tiempo de llegada de un nuevo robot

def simulacion():
    """Configura y ejecuta la simulación."""
    env = simpy.Environment()
    ganancias = [0]  # Ganancias acumuladas
    for _ in range(100):  # Número de juegos en 8 horas
        env.process(juego(env, ganancias))
    env.run(until=8 * 3600)  # 8 horas
    print(f"Ganancia total: {ganancias[0]}")

if __name__ == "__main__":
    simulacion()
