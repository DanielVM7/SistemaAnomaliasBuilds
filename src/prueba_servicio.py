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

    fecha = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    carpeta_resultados = os.path.join(
        carpeta_proyecto,
        "resultados",
        f"analisis_{fecha}",
    )

    servicio = ServicioAnalisis(
        ruta_csv=ruta_csv,
        carpeta_resultados=carpeta_resultados,
        nombre_archivo_original="muestra.csv",
    )

    resultados = servicio.ejecutar()

    print()
    print(
        "==================================="
    )
    print(
        "RESUMEN DE RESULTADOS"
    )
    print(
        "==================================="
    )

    print(
        "Archivo: "
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
        f"Q1: {resultados['q1']}"
    )

    print(
        f"Q3: {resultados['q3']}"
    )

    print(
        f"IQR: {resultados['iqr']}"
    )

    print(
        "Límite inferior: "
        f"{resultados['limite_inferior']}"
    )

    print(
        "Límite superior: "
        f"{resultados['limite_superior']}"
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
        "Archivo ZIP: "
        f"{resultados['ruta_zip']}"
    )


if __name__ == "__main__":
    main()