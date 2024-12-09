import simpy
import random
import time
import sys


def humano_resuelve(n):
    """Simula la resolución del problema por el humano usando un enfoque determinista."""
    start = time.time()

    def es_seguro(tablero, fila, col):
        """Verifica si es seguro colocar una reina en la posición (fila, col)."""
        for i in range(fila):
            if tablero[i] == col or \
               tablero[i] - i == col - fila or \
               tablero[i] + i == col + fila:
                return False
        return True

    def resolver(tablero, fila):
        """Coloca reinas recursivamente usando backtracking."""
        if fila == n:
            return True
        for col in range(n):
            if es_seguro(tablero, fila, col):
                tablero[fila] = col
                if resolver(tablero, fila + 1):
                    return True
                tablero[fila] = -1
        return False

    tablero = [-1] * n
    resolver(tablero, 0)
    return time.time() - start


def robot_resuelve(n, max_intentos=10000):
    """Simula la resolución del problema por el robot usando el enfoque Las Vegas."""
    start = time.time()

    for intento in range(max_intentos):
        tablero = [-1] * n
        posiciones_disponibles = list(range(n))

        valido = True
        for fila in range(n):
            if not posiciones_disponibles:
                valido = False
                break

            col = random.choice(posiciones_disponibles)
            posiciones_disponibles.remove(col)
            tablero[fila] = col

            for i in range(fila):
                if tablero[i] - i == col - fila or tablero[i] + i == col + fila:
                    valido = False
                    break

            if not valido:
                break

        if valido:
            return time.time() - start

    return time.time() - start


def juego(env, ganancias, tiempos_humanos, tiempos_robot):
    """Simula un juego entre el humano y el robot."""
    n = random.choice([4, 5, 6, 8, 10, 12, 15])
    tiempo_humano = humano_resuelve(n)
    print(f"El humano: {n} reinas en {tiempo_humano:.10f} segundos")
    tiempo_robot = robot_resuelve(n)
    print(f"El robot: {n} reinas en {tiempo_robot:.10f} segundos")

    tiempos_humanos.append(tiempo_humano)
    tiempos_robot.append(tiempo_robot)

    if tiempo_humano < tiempo_robot:
        ganancias[0] += 30
        print("Humano Gana +30")
    else:
        ganancias[0] -= 10
        print("Humano pierde -10")

    yield env.timeout(random.uniform(10, 30))


def simulacion(horas):
    """Configura y ejecuta la simulación."""
    env = simpy.Environment()
    ganancias = [0]
    tiempos_humanos = []
    tiempos_robot = []

    def generar_juegos(env, ganancias, tiempos_humanos, tiempos_robot):
        while True:
            env.process(juego(env, ganancias, tiempos_humanos, tiempos_robot))
            yield env.timeout(random.uniform(1, 5))

    env.process(generar_juegos(env, ganancias, tiempos_humanos, tiempos_robot))
    env.run(until=horas * 3600)

    # Calcular promedios
    if tiempos_humanos and tiempos_robot:
        promedio_humano = sum(tiempos_humanos) / len(tiempos_humanos)
        promedio_robot = sum(tiempos_robot) / len(tiempos_robot)
        print(f"Promedio Humano: {promedio_humano:.10f}")
        print(f"Promedio Robot: {promedio_robot:.10f}")
    else:
        print("No se pudo calcular los promedios.")

    print(f"Ganancia total: {ganancias[0]}")


if __name__ == "__main__":
    horas = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    simulacion(horas)
