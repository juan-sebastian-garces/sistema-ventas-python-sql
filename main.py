
import sqlite3
import pandas as pd

conexion = sqlite3.connect("ventas.db")


def mostrar_resumen():
    consulta = """
    SELECT
        COUNT(*) AS total_ventas,
        SUM(cantidad) AS unidades_vendidas,
        SUM(cantidad * precio) AS ingresos_totales,
        AVG(cantidad * precio) AS promedio_por_venta
    FROM ventas
    """

    resultado = pd.read_sql_query(consulta, conexion)

    print("========== RESUMEN DE VENTAS ==========")
    print(f"Total de ventas: {int(resultado.iloc[0]["total_ventas"])}")
    print(f"Unidades vendidas: {int(resultado.iloc[0]["unidades_vendidas"])}")
    print(f"Ingresos totales: ${resultado.iloc[0]["ingresos_totales"]:.2f}")
    print(f"Promedio por venta: ${resultado.iloc[0]["promedio_por_venta"]:.2f}")
    print("========================================")


def mostrar_productos():
    consulta = """
    SELECT
        producto,
        SUM(cantidad) AS unidades_vendidas,
        SUM(cantidad * precio) AS ingresos
    FROM ventas
    GROUP BY producto
    ORDER BY ingresos DESC
    """

    resultado = pd.read_sql_query(consulta, conexion)

    print("========== ANÁLISIS POR PRODUCTO ==========")
    print(resultado.to_string(index=False))
    print("===========================================")



def mostrar_clientes():
    consulta = """
    SELECT
        cliente,
        COUNT(*) AS numero_ventas,
        SUM(cantidad) AS unidades_vendidas,
        SUM(cantidad * precio) AS ingresos
    FROM ventas
    GROUP BY cliente
    ORDER BY ingresos DESC
    """

    resultado = pd.read_sql_query(consulta, conexion)

    print("========== ANÁLISIS POR CLIENTE ==========")
    print(resultado.to_string(index=False))
    print("===========================================")


def menu():
    while True:
        print()
        print("========== SISTEMA DE VENTAS ==========")
        print("1. Ver resumen")
        print("2. Ver análisis por producto")
        print("3. Ver análisis por cliente")
        print("4. Salir")
        print("=======================================")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            mostrar_resumen()

        elif opcion == "2":
            mostrar_productos()

        elif opcion == "3":
            mostrar_clientes()

        elif opcion == "4":
            print("Programa finalizado.")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
