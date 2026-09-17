
import sqlite3
import pandas as pd
from datetime import datetime

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



def mostrar_categorias():
    consulta = """
    SELECT
        categoria,
        COUNT(*) AS numero_ventas,
        SUM(cantidad) AS unidades_vendidas,
        SUM(cantidad * precio) AS ingresos
    FROM ventas
    GROUP BY categoria
    ORDER BY ingresos DESC
    """

    resultado = pd.read_sql_query(consulta, conexion)

    print("========== ANÁLISIS POR CATEGORÍA ==========")
    print(resultado.to_string(index=False))
    print("=============================================")



def mostrar_producto_mayor_ingreso():
    consulta = """
    SELECT
        producto,
        SUM(cantidad * precio) AS ingresos
    FROM ventas
    GROUP BY producto
    ORDER BY ingresos DESC
    LIMIT 1
    """

    resultado = pd.read_sql_query(consulta, conexion)

    print("========== PRODUCTO CON MAYOR INGRESO ==========")
    print(f"Producto: {resultado.iloc[0]['producto']}")
    print(f"Ingresos: ${resultado.iloc[0]['ingresos']:.2f}")
    print("================================================")



def mostrar_cliente_mayor_ingreso():
    consulta = """
    SELECT
        cliente,
        SUM(cantidad * precio) AS ingresos
    FROM ventas
    GROUP BY cliente
    ORDER BY ingresos DESC
    LIMIT 1
    """

    resultado = pd.read_sql_query(consulta, conexion)

    print("========== CLIENTE CON MAYOR INGRESO ==========")
    print(f"Cliente: {resultado.iloc[0]['cliente']}")
    print(f"Ingresos: ${resultado.iloc[0]['ingresos']:.2f}")
    print("===============================================")



def mostrar_mayor_venta():
    consulta = """
    SELECT
        cliente,
        producto,
        cantidad,
        precio,
        cantidad * precio AS total_venta
    FROM ventas
    ORDER BY total_venta DESC
    LIMIT 1
    """

    resultado = pd.read_sql_query(consulta, conexion)

    print("========== MAYOR VENTA INDIVIDUAL ==========")
    print(f"Cliente: {resultado.iloc[0]['cliente']}")
    print(f"Producto: {resultado.iloc[0]['producto']}")
    print(f"Cantidad: {int(resultado.iloc[0]['cantidad'])}")
    print(f"Precio unitario: ${resultado.iloc[0]['precio']:.2f}")
    print(f"Total de la venta: ${resultado.iloc[0]['total_venta']:.2f}")
    print("============================================")



def registrar_venta():
    print()
    print("========== REGISTRAR NUEVA VENTA ==========")

    while True:
        fecha = input("Fecha (DD/MM/AAAA): ")
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            break
        except ValueError:
            print("Fecha no válida. Usa el formato DD/MM/AAAA.")
    cliente = input("Cliente: ")
    producto = input("Producto: ")
    categoria = input("Categoría: ")

    while True:
        try:
            cantidad = int(input("Cantidad: "))
            if cantidad > 0:
                break
            print("La cantidad debe ser mayor que 0.")
        except ValueError:
            print("Por favor, introduce un número entero.")

    while True:
        try:
            precio = float(input("Precio unitario: "))
            if precio > 0:
                break
            print("El precio debe ser mayor que 0.")
        except ValueError:
            print("Por favor, introduce un número válido.")

    consulta = """
    INSERT INTO ventas
    (fecha, cliente, producto, categoria, cantidad, precio)
    VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor = conexion.cursor()

    cursor.execute(
        consulta,
        (fecha, cliente, producto, categoria, cantidad, precio)
    )

    conexion.commit()

    total = cantidad * precio

    print()
    print("Venta registrada correctamente.")
    print(f"Total de la venta: ${total:.2f}")
    print("===========================================")



def menu():
    while True:
        print()
        print("========== SISTEMA DE VENTAS ==========")
        print("1. Ver resumen")
        print("2. Ver análisis por producto")
        print("3. Ver análisis por cliente")
        print("4. Ver análisis por categoría")
        print("5. Ver producto con mayor ingreso")
        print("6. Ver cliente con mayor ingreso")
        print("7. Ver mayor venta individual")
        print("8. Registrar nueva venta")
        print("9. Salir")
        print("=======================================")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            mostrar_resumen()

        elif opcion == "2":
            mostrar_productos()

        elif opcion == "3":
            mostrar_clientes()

        elif opcion == "4":
            mostrar_categorias()

        elif opcion == "5":
            mostrar_producto_mayor_ingreso()

        elif opcion == "6":
            mostrar_cliente_mayor_ingreso()

        elif opcion == "7":
            mostrar_mayor_venta()

        elif opcion == "8":
            registrar_venta()

        elif opcion == "9":
            print("Programa finalizado.")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
