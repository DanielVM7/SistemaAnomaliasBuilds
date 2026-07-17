import os
from datetime import datetime

from servicio_analisis import ServicioAnalisis


def main() -> None:
    carpeta_src = os.path.dirname(
        os.path.abspath(__file__)
    )

    carpeta_proyecto = os.path.dirname(
        carpeta_src
    )

    ruta_csv = os.path.join(
        carpeta_proyecto,
        "data",
        "muestra.csv",
    )

    fecha_ejecucion = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    carpeta_resultados = os.path.join(
        carpeta_proyecto,
        "resultados",
        f"analisis_{fecha_ejecucion}",
    )

    servicio = ServicioAnalisis(
        ruta_csv=ruta_csv,
        carpeta_resultados=carpeta_resultados,
        nombre_archivo_original="muestra.csv",
    )

    try:
        resultados = servicio.ejecutar()

        print()
        print(
            "==================================="
        )
        print(
            "RESUMEN FINAL DE LA EJECUCIÓN"
        )
        print(
            "==================================="
        )

        print(
            "Archivo analizado: "
            f"{resultados['archivo_original']}"
        )

        print(
            "Registros iniciales: "
            f"{resultados['registros_iniciales']}"
        )

        print(
            "Registros procesados: "
            f"{resultados['registros_procesados']}"
        )

        print(
            "Registros eliminados: "
            f"{resultados['registros_eliminados']}"
        )

        print(
            "Outliers detectados: "
            f"{resultados['total_outliers']}"
        )

        print(
            "Porcentaje de outliers: "
            f"{resultados['porcentaje_outliers']}%"
        )

        print(
            "Validación correcta: "
            f"{resultados['validacion_correcta']}"
        )

        print(
            "Gráficas generadas: "
            f"{len(resultados['graficas'])}"
        )

        print(
            "Carpeta de resultados:"
        )
        print(
            resultados["ruta_graficas"]
        )

        print(
            "Archivo ZIP:"
        )
        print(
            resultados["ruta_zip"]
        )

    except FileNotFoundError as error:
        print()
        print(
            "ERROR: no se encontró el archivo "
            "de entrada."
        )
        print(error)

    except ValueError as error:
        print()
        print(
            "ERROR: el archivo no contiene "
            "datos válidos."
        )
        print(error)

    except RuntimeError as error:
        print()
        print(
            "ERROR: no fue posible completar "
            "el análisis."
        )
        print(error)

    except Exception as error:
        print()
        print(
            "ERROR INESPERADO DURANTE LA EJECUCIÓN"
        )
        print(error)


if __name__ == "__main__":
    main()