import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from flask import (
    Flask,
    abort,
    render_template,
    request,
    send_file,
    url_for,
)
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from servicio_analisis import ServicioAnalisis


CARPETA_SRC = Path(__file__).resolve().parent
CARPETA_PROYECTO = CARPETA_SRC.parent

CARPETA_UPLOADS = CARPETA_PROYECTO / "uploads"
CARPETA_RESULTADOS = CARPETA_PROYECTO / "resultados"
CARPETA_TEMPLATES = CARPETA_PROYECTO / "templates"
CARPETA_STATIC = CARPETA_PROYECTO / "static"

EXTENSIONES_PERMITIDAS = {"csv"}

CARPETA_UPLOADS.mkdir(
    parents=True,
    exist_ok=True,
)

CARPETA_RESULTADOS.mkdir(
    parents=True,
    exist_ok=True,
)

app = Flask(
    __name__,
    template_folder=str(CARPETA_TEMPLATES),
    static_folder=str(CARPETA_STATIC),
)

app.config["MAX_CONTENT_LENGTH"] = (
    4 * 1024 * 1024 * 1024
)

app.config["UPLOAD_FOLDER"] = str(
    CARPETA_UPLOADS
)

app.config["RESULTADOS_FOLDER"] = str(
    CARPETA_RESULTADOS
)


def extension_permitida(
    nombre_archivo: str,
) -> bool:
    """
    Verifica que el archivo tenga una extensión permitida.
    """

    return (
        "." in nombre_archivo
        and nombre_archivo.rsplit(
            ".",
            1,
        )[1].lower()
        in EXTENSIONES_PERMITIDAS
    )


def crear_identificador_analisis() -> str:
    """
    Crea un identificador único para cada ejecución.
    """

    fecha = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    identificador_corto = (
        uuid.uuid4().hex[:8]
    )

    return (
        f"analisis_{fecha}_"
        f"{identificador_corto}"
    )


def crear_interpretacion(
    resultados: dict[str, Any],
) -> str:
    """
    Genera una interpretación sencilla para mostrar en la web.
    """

    total_outliers = resultados[
        "total_outliers"
    ]

    porcentaje = resultados[
        "porcentaje_outliers"
    ]

    limite_inferior = resultados[
        "limite_inferior"
    ]

    limite_superior = resultados[
        "limite_superior"
    ]

    if total_outliers == 0:
        return (
            "No se detectaron valores atípicos en la "
            "duración de los builds mediante el método IQR."
        )

    if limite_inferior < 0:
        return (
            f"Se detectaron {total_outliers} builds "
            f"anómalos, equivalentes al {porcentaje:.2f}% "
            "de los registros procesados. Debido a que el "
            "límite inferior calculado fue negativo, las "
            "anomalías corresponden a builds cuya duración "
            f"supera los {limite_superior:.2f} segundos."
        )

    return (
        f"Se detectaron {total_outliers} builds "
        f"anómalos, equivalentes al {porcentaje:.2f}% "
        "de los registros procesados. Los valores "
        f"fuera del rango de {limite_inferior:.2f} a "
        f"{limite_superior:.2f} segundos fueron "
        "clasificados como outliers."
    )


def preparar_graficas(
    resultados: dict[str, Any],
    identificador: str,
) -> list[dict[str, str]]:
    """
    Convierte las rutas de las gráficas en datos utilizables
    desde la plantilla HTML.
    """

    titulos = {
        "histograma_duracion.png": (
            "Distribución de la duración"
        ),
        "builds_por_estado.png": (
            "Builds por estado"
        ),
        "boxplot_outliers.png": (
            "Boxplot de duración"
        ),
        "comparacion_normales_outliers.png": (
            "Normales frente a outliers"
        ),
        "outliers_por_estado.png": (
            "Outliers por estado"
        ),
        "tendencia_fallos.png": (
            "Tendencia de fallos"
        ),
        "proporcion_fallos_tiempo.png": (
            "Proporción de fallos en el tiempo"
        ),
    }

    graficas = []

    for ruta_grafica in resultados["graficas"]:
        nombre_archivo = Path(
            ruta_grafica
        ).name

        graficas.append(
            {
                "nombre": nombre_archivo,
                "titulo": titulos.get(
                    nombre_archivo,
                    nombre_archivo,
                ),
                "url": url_for(
                    "mostrar_grafica",
                    identificador=identificador,
                    nombre_archivo=nombre_archivo,
                ),
            }
        )

    return graficas


@app.route(
    "/",
    methods=["GET", "POST"],
)
def index():
    """
    Muestra el formulario y procesa el dataset enviado.
    """

    mensaje_error = None
    resultados = None
    interpretacion = None
    graficas = []
    identificador = None

    if request.method == "POST":
        if "archivo_csv" not in request.files:
            mensaje_error = (
                "No se recibió ningún archivo."
            )

            return render_template(
                "index.html",
                mensaje_error=mensaje_error,
                resultados=resultados,
                interpretacion=interpretacion,
                graficas=graficas,
                identificador=identificador,
            )

        archivo = request.files[
            "archivo_csv"
        ]

        if archivo.filename is None:
            mensaje_error = (
                "El archivo seleccionado no tiene "
                "un nombre válido."
            )

            return render_template(
                "index.html",
                mensaje_error=mensaje_error,
                resultados=resultados,
                interpretacion=interpretacion,
                graficas=graficas,
                identificador=identificador,
            )

        if archivo.filename.strip() == "":
            mensaje_error = (
                "Debes seleccionar un archivo CSV."
            )

            return render_template(
                "index.html",
                mensaje_error=mensaje_error,
                resultados=resultados,
                interpretacion=interpretacion,
                graficas=graficas,
                identificador=identificador,
            )

        if not extension_permitida(
            archivo.filename
        ):
            mensaje_error = (
                "El archivo debe tener extensión .csv."
            )

            return render_template(
                "index.html",
                mensaje_error=mensaje_error,
                resultados=resultados,
                interpretacion=interpretacion,
                graficas=graficas,
                identificador=identificador,
            )

        nombre_seguro = secure_filename(
            archivo.filename
        )

        if not nombre_seguro:
            mensaje_error = (
                "No fue posible obtener un nombre "
                "seguro para el archivo."
            )

            return render_template(
                "index.html",
                mensaje_error=mensaje_error,
                resultados=resultados,
                interpretacion=interpretacion,
                graficas=graficas,
                identificador=identificador,
            )

        identificador = (
            crear_identificador_analisis()
        )

        carpeta_upload = (
            CARPETA_UPLOADS
            / identificador
        )

        carpeta_resultado = (
            CARPETA_RESULTADOS
            / identificador
        )

        carpeta_upload.mkdir(
            parents=True,
            exist_ok=True,
        )

        ruta_archivo = (
            carpeta_upload
            / nombre_seguro
        )

        archivo.save(
            ruta_archivo
        )

        try:
            servicio = ServicioAnalisis(
                ruta_csv=str(ruta_archivo),
                carpeta_resultados=str(
                    carpeta_resultado
                ),
                nombre_archivo_original=(
                    archivo.filename
                ),
            )

            resultados = servicio.ejecutar()

            interpretacion = (
                crear_interpretacion(
                    resultados
                )
            )

            graficas = preparar_graficas(
                resultados=resultados,
                identificador=identificador,
            )

        except (
            FileNotFoundError,
            ValueError,
            RuntimeError,
        ) as error:
            mensaje_error = str(error)

        except Exception as error:
            mensaje_error = (
                "Ocurrió un error inesperado durante "
                f"el análisis: {error}"
            )

    return render_template(
        "index.html",
        mensaje_error=mensaje_error,
        resultados=resultados,
        interpretacion=interpretacion,
        graficas=graficas,
        identificador=identificador,
    )


@app.route(
    "/graficas/<identificador>/<nombre_archivo>"
)
def mostrar_grafica(
    identificador: str,
    nombre_archivo: str,
):
    """
    Muestra una gráfica generada por el análisis.
    """

    nombre_seguro = secure_filename(
        nombre_archivo
    )

    ruta_grafica = (
        CARPETA_RESULTADOS
        / identificador
        / "graficas"
        / nombre_seguro
    )

    if not ruta_grafica.exists():
        abort(404)

    return send_file(
        ruta_grafica,
        mimetype="image/png",
    )


@app.route(
    "/descargar/<identificador>"
)
def descargar_resultados(
    identificador: str,
):
    """
    Descarga el único archivo ZIP de una ejecución.
    """

    ruta_zip = (
        CARPETA_RESULTADOS
        / identificador
        / "resultados_analisis.zip"
    )

    if not ruta_zip.exists():
        abort(404)

    return send_file(
        ruta_zip,
        as_attachment=True,
        download_name=(
            f"{identificador}_resultados.zip"
        ),
        mimetype="application/zip",
    )


@app.errorhandler(
    RequestEntityTooLarge
)
def archivo_demasiado_grande(
    error: RequestEntityTooLarge,
):
    """
    Maneja archivos que superen el límite configurado.
    """

    return render_template(
        "index.html",
        mensaje_error=(
            "El archivo supera el tamaño máximo "
            "permitido de 4 GB."
        ),
        resultados=None,
        interpretacion=None,
        graficas=[],
        identificador=None,
    ), 413


@app.errorhandler(404)
def recurso_no_encontrado(
    error,
):
    """
    Muestra un mensaje cuando no existe un resultado.
    """

    return render_template(
        "index.html",
        mensaje_error=(
            "El recurso solicitado no existe "
            "o ya no está disponible."
        ),
        resultados=None,
        interpretacion=None,
        graficas=[],
        identificador=None,
    ), 404


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )