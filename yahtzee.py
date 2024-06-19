import random


# Función para lanzar dados
def lanzar_dados(n=5):
    return [random.randint(1, 6) for _ in range(n)]


# Función de frecuencia de dados
def contar_frecuencia(dados):
    frecuencia = {x: dados.count(x) for x in set(dados)}
    return frecuencia


# Full house
def full_house(dados):
    frecuencia = contar_frecuencia(dados)
    if sorted(frecuencia.values()) == [2, 3]:
        return 25, "Full House"
    return 0, None


# Póker o Four of a kind
def poker(dados):
    frecuencia = contar_frecuencia(dados)
    if 4 in frecuencia.values():
        return sum(dados), "Póker"
    return 0, None


# Escalera grande
def escalera_grande(dados):
    if sorted(dados) == list(range(min(dados), min(dados) + 5)):
        return 40, "Escalera Grande"
    return 0, None


# Escalera pequeña
def escalera_pequena(dados):
    posibles_escaleras = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
    if any(escalera.issubset(dados) for escalera in posibles_escaleras):
        return 30, "Escalera Pequeña"
    return 0, None


# Yahtzee!
def yahtzee(dados):
    if len(set(dados)) == 1:
        return 50, "Yahtzee"
    return 0, None


# Chance (Suma de todos los dados)
def chance(dados):
    return sum(dados), "Chance"


# Upper section
def upper_section(dados):
    puntuacion_upper = 0
    for numero in range(1, 7):
        puntuacion_upper += dados.count(numero) * numero
    return puntuacion_upper


# Cálculo de puntuación
def puntuacion(dados):
    puntos, combinaciones = 0, []
    for func in [full_house, poker, escalera_grande, escalera_pequena, yahtzee]:
        punto, combinacion = func(dados)
        if punto:
            puntos += punto
            if combinacion:
                combinaciones.append(combinacion)
    return puntos, combinaciones


def simulacion_montecarlo(n_simulaciones):
    resultados = {
        "Full House": 0,
        "Póker": 0,
        "Escalera Grande": 0,
        "Escalera Pequeña": 0,
        "Yahtzee": 0,
        "Upper Section": [],
        "Full House Scores": [],
        "Póker Scores": [],
        "Escalera Grande Scores": [],
        "Escalera Pequeña Scores": [],
        "Yahtzee Scores": [],
    }

    for _ in range(n_simulaciones):
        dados = lanzar_dados()
        puntos, combinaciones = puntuacion(dados)
        puntuacion_upper = upper_section(dados)

        resultados["Upper Section"].append(puntuacion_upper)
        for combinacion in combinaciones:
            resultados[combinacion] += 1
            resultados[f"{combinacion} Scores"].append(puntos)

    total_simulaciones = n_simulaciones
    print("Resultados de la simulación de Montecarlo:")
    print(f"Total de simulaciones: {total_simulaciones}")
    for combinacion, count in resultados.items():
        if combinacion == "Upper Section":
            promedio_upper = sum(resultados["Upper Section"]) / len(
                resultados["Upper Section"]
            )
            print(f"Puntuación promedio en la Upper Section: {promedio_upper:.2f}")
        elif "Scores" in combinacion:
            promedio_combinacion = (
                sum(resultados[combinacion]) / len(resultados[combinacion])
                if resultados[combinacion]
                else 0
            )
            combinacion_name = combinacion.replace(" Scores", "")
            print(
                f"Puntuación promedio para {combinacion_name}: {promedio_combinacion:.2f}"
            )
        else:
            probabilidad = (count / total_simulaciones) * 100
            print(f"Probabilidad de obtener {combinacion}: {probabilidad:.4f}%")


# Turnos
def turno_jugadores(
    puntuacion_yahtzees,
    lanzamientos_jugador,
    puntajes_jugador,
    combinaciones_jugador,
    bonos_jugador,
):
    input("Presiona Enter para lanzar los dados...")
    dados = lanzar_dados()
    print("El lanzamiento fue de: ", dados)
    lanzamientos_jugador.append(dados)

    puntuacion_especial, combinaciones = puntuacion(dados)
    puntuacion_upper = upper_section(dados)
    puntuacion_final = puntuacion_especial + puntuacion_upper

    # Bono de Yahtzee adicional
    yahtzee_puntos, yahtzee_combinacion = yahtzee(dados)
    if yahtzee_combinacion:
        puntuacion_yahtzees.append(1)
        if len(puntuacion_yahtzees) > 1:
            puntuacion_final += 100
            bonos_jugador.append(100)
            print("¡Bono de Yahtzee adicional!")
        else:
            bonos_jugador.append(0)
    else:
        bonos_jugador.append(0)

    print(f"Puntuación de combinaciones especiales: {puntuacion_especial}")
    print(f"Combinaciones: {combinaciones}")
    print(f"Puntuación de la upper section: {puntuacion_upper}")
    print(f"Puntuación total del turno: {puntuacion_final}")

    puntajes_jugador.append(puntuacion_final)
    combinaciones_jugador.append(combinaciones)
    return puntuacion_final, puntuacion_yahtzees


# Juego principal
def jugar_yahtzee():
    puntuacion_jugador1 = 0
    puntuacion_jugador2 = 0
    puntuacion_yahtzees_jugador1 = []
    puntuacion_yahtzees_jugador2 = []
    lanzamientos_jugador1 = []
    lanzamientos_jugador2 = []
    puntajes_jugador1 = []
    puntajes_jugador2 = []
    combinaciones_jugador1 = []
    combinaciones_jugador2 = []
    bonos_jugador1 = []
    bonos_jugador2 = []

    for _ in range(3):
        print("¡Turno del jugador 1!")
        puntuacion_turno, puntuacion_yahtzees_jugador1 = turno_jugadores(
            puntuacion_yahtzees_jugador1,
            lanzamientos_jugador1,
            puntajes_jugador1,
            combinaciones_jugador1,
            bonos_jugador1,
        )
        puntuacion_jugador1 += puntuacion_turno

        print("¡Turno del jugador 2!")
        puntuacion_turno, puntuacion_yahtzees_jugador2 = turno_jugadores(
            puntuacion_yahtzees_jugador2,
            lanzamientos_jugador2,
            puntajes_jugador2,
            combinaciones_jugador2,
            bonos_jugador2,
        )
        puntuacion_jugador2 += puntuacion_turno

    # Calcular bono de la upper section
    bono_upper_jugador1 = (
        35
        if sum([upper_section(lanzamiento) for lanzamiento in lanzamientos_jugador1])
        >= 63
        else 0
    )
    bono_upper_jugador2 = (
        35
        if sum([upper_section(lanzamiento) for lanzamiento in lanzamientos_jugador2])
        >= 63
        else 0
    )
    puntuacion_jugador1 += bono_upper_jugador1
    puntuacion_jugador2 += bono_upper_jugador2

    if bono_upper_jugador1 > 0:
        print("¡Jugador 1 recibe un bono de 35 puntos en la upper section!")
        bonos_jugador1.append(35)
    else:
        bonos_jugador1.append(0)

    if bono_upper_jugador2 > 0:
        print("¡Jugador 2 recibe un bono de 35 puntos en la upper section!")
        bonos_jugador2.append(35)
    else:
        bonos_jugador2.append(0)

    # Puntuaciones de jugadores
    print(f"Puntuación final jugador 1: {puntuacion_jugador1}")
    print(f"Puntuación final jugador 2: {puntuacion_jugador2}")

    # Ganadores
    if puntuacion_jugador1 > puntuacion_jugador2:
        print("¡Jugador 1 gana!")
    elif puntuacion_jugador1 < puntuacion_jugador2:
        print("¡Jugador 2 gana!")
    else:
        print("¡Es un empate!")

    print("\nResumen de lanzamientos, puntajes, combinaciones y bonos:")
    print("Jugador 1:")
    for i in range(len(lanzamientos_jugador1)):
        print(
            f"Turno {i + 1}: Lanzamientos = {lanzamientos_jugador1[i]}, Puntaje = {puntajes_jugador1[i]}, Combinaciones = {combinaciones_jugador1[i]}, Bonos = {bonos_jugador1[i]}"
        )
    print("Jugador 2:")
    for i in range(len(lanzamientos_jugador2)):
        print(
            f"Turno {i + 1}: Lanzamientos = {lanzamientos_jugador2[i]}, Puntaje = {puntajes_jugador2[i]}, Combinaciones = {combinaciones_jugador2[i]}, Bonos = {bonos_jugador2[i]}"
        )


# Mostrar reglas
def mostrar_reglas():
    print("Reglas de Yahtzee:")
    print("1. En cada turno, el jugador lanza cinco dados.")
    print("2. El jugador puede relanzar algunos o todos los dados hasta dos veces más.")
    print(
        "3. Después de los lanzamientos, el jugador debe elegir una categoría para puntuar."
    )
    print(
        "4. Las categorías incluyen combinaciones como Full House, Póker, Escalera Grande, Escalera Pequeña, Yahtzee y Chance."
    )
    print("5. El juego continúa hasta que todas las categorías hayan sido puntuadas.")
    print("6. Gana el jugador con la puntuación más alta.")


def menu():
    print("Bienvenido a Yahtzee")
    print("A: Empezar el juego")
    print("B: Ver cómo se juega")
    print("C: Simulación Montecarlo")
    opcion = input("Selecciona una opción: ").strip().upper()

    if opcion == "A":
        jugar_yahtzee()
    elif opcion == "B":
        mostrar_reglas()
        menu()
    elif opcion == "C":
        try:
            n_simulaciones = int(input("Ingresa el número de simulaciones: "))
            simulacion_montecarlo(n_simulaciones)
        except ValueError:
            print("Por favor, ingresa un número válido.")
        menu()
    else:
        print("Opción no válida. Inténtalo de nuevo.")
        menu()


menu()
