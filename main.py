from parser import parsear
from validator import validar
from export import exportar_todo


def main():

    try:
        print("Leyendo plan...")

        materias = parsear("plan.txt")

        print(f"Materias encontradas: {len(materias)}")

        errores = validar(materias)

        if errores:

            print("\nSe encontraron errores:\n")

            for error in errores:
                print(" •", error)

            print("\nProceso cancelado.")

            return

        exportar_todo(materias)

        print("\nExportación finalizada correctamente.")

        print("\nArchivos generados:")

        print("   salida/materias.json")

        print("   salida/correlativas.json")

        print("   salida/desbloqueos.json")
    
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'plan.txt'.")
        return
    except Exception as e:
        print(f"Error inesperado: {e}")
        return


if __name__ == "__main__":
    main()