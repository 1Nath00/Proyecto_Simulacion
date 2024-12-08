import simpy
import random
import time


def humano_resuelve(n):
    """Simula la resolución del problema por el humano usando un enfoque determinista."""
    start = time.time()

    def es_seguro(tablero, fila, col):
        """Verifica si es seguro colocar una reina en la posición (fila, col)."""
        for i in range(fila):
            # Comprobar conflictos en columnas y diagonales
            if tablero[i] == col or \
               tablero[i] - i == col - fila or \
               tablero[i] + i == col + fila:
                return False
        return True

    def resolver(tablero, fila):
        """Coloca reinas recursivamente usando backtracking."""
        if fila == n:
            return True  # Solución encontrada
        for col in range(n):
            if es_seguro(tablero, fila, col):
                tablero[fila] = col  # Colocar reina
                if resolver(tablero, fila + 1):  # Intentar en la siguiente fila
                    return True
                tablero[fila] = -1  # Retroceso
        return False

    # Inicializar tablero
    tablero = [-1] * n
    resolver(tablero, 0)

    # Devolver el tiempo que tomó resolverlo
    return time.time() - start


def robot_resuelve(n, max_intentos=10000):
    """Simula la resolución del problema por el robot usando el enfoque Las Vegas."""
    start = time.time()

    for intento in range(max_intentos):
        tablero = [-1] * n  # Inicializar tablero con -1 (sin reinas colocadas)
        # Todas las columnas disponibles
        posiciones_disponibles = list(range(n))

        valido = True
        for fila in range(n):
            if not posiciones_disponibles:
                valido = False  # No hay columnas disponibles para esta fila
                break

            # Elegir una columna aleatoria disponible
            col = random.choice(posiciones_disponibles)
            posiciones_disponibles.remove(col)
            tablero[fila] = col

            # Verificar conflictos con filas anteriores
            for i in range(fila):
                if tablero[i] - i == col - fila or tablero[i] + i == col + fila:
                    valido = False  # Conflicto diagonal
                    break

            if not valido:
                break

        if valido:
            # Solución encontrada
            return time.time() - start

    # Si no se encuentra solución en los intentos permitidos
    return time.time() - start


def juego(env, ganancias):
    """Simula un juego entre el humano y el robot."""
    n = random.choice([4, 5, 6, 8, 10, 12, 15])  # Selección de tablero
    tiempo_humano = humano_resuelve(n)
    print(f"El humano: {n} reinas en {tiempo_humano:.10f} segundos")
    tiempo_robot = robot_resuelve(n)
    print(f"El robot: {n} reinas en {tiempo_robot:.10f} segundos")

    if tiempo_humano < tiempo_robot:
        ganancias[0] += 30  # Humano gana
        print("Humano Gana +30")
    else:
        ganancias[0] -= 10  # Robot gana
        print("Humano pierde -10")

    # Tiempo de llegada de un nuevo robot
    yield env.timeout(random.uniform(10, 30))


def simulacion():
    """Configura y ejecuta la simulación."""
    env = simpy.Environment()
    ganancias = [0]  # Ganancias acumuladas

    def generar_juegos(env, ganancias):
        """Genera nuevos juegos de manera continua mientras haya tiempo."""
        while True:
            env.process(juego(env, ganancias))
            # Tiempo entre el inicio de cada juego
            yield env.timeout(random.uniform(1, 5))

    # Iniciar el generador de juegos
    env.process(generar_juegos(env, ganancias))
    env.run(until=3600*8)  # Simular por 8 horas
    print(f"Ganancia total: {ganancias[0]}")


if __name__ == "__main__":
    simulacion()
