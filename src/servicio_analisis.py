import os
import traceback
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

from analisis_datos import AnalisisDatos
from logger_sistema import LoggerSistema
from procesamiento_datos import ProcesamientoDatos


class ServicioAnalisis:

    ARCHIVOS_GRAFICAS = [
        "histograma_duracion.png",
        "builds_por_estado.png",
        "boxplot_outliers.png",
        "comparacion_normales_outliers.png",
        "outliers_por_estado.png",
        "tendencia_fallos.png",
        "proporcion_fallos_tiempo.png",
    ]

    def __init__(
        self,
        ruta_csv: str,
        carpeta_resultados: str,
        nombre_archivo_original: str | None = None,
    ) -> None:
        self.ruta_csv = Path(
            ruta_csv
        ).resolve()

        self.carpeta_resultados = Path(
            carpeta_resultados
        ).resolve()

        self.nombre_archivo_original = (
            nombre_archivo_original
            if nombre_archivo_original
            else self.ruta_csv.name
        )

        self.ruta_dataset_limpio = (
            self.carpeta_resultados
            / "dataset_limpio.csv"
        )

        self.ruta_outliers = (
            self.carpeta_resultados
            / "outliers_detectados.csv"
        )

        self.ruta_resumen = (
            self.carpeta_resultados
            / "resumen_resultados.txt"
        )

        self.ruta_log = (
            self.carpeta_resultados
            / "ejecucion_sistema.log"
        )

        self.ruta_graficas = (
            self.carpeta_resultados
            / "graficas"
        )

        self.ruta_zip = (
            self.carpeta_resultados
            / "resultados_analisis.zip"
        )

        self.logger: LoggerSistema | None = None

    def ejecutar(self) -> dict[str, Any]:
        fecha_inicio = datetime.now()

        try:
            self._validar_archivo_entrada()
            self._crear_carpetas()

            self.logger = LoggerSistema(
                str(self.ruta_log)
            )

            self.logger.registrar_evento(
                "Inicio del servicio de análisis."
            )

            self.logger.registrar_evento(
                "Archivo recibido: "
                f"{self.nombre_archivo_original}"
            )

            metricas_procesamiento = (
                self._ejecutar_procesamiento()
            )

            resultado_analisis = (
                self._ejecutar_analisis()
            )

            fecha_fin = datetime.now()

            duracion_segundos = round(
                (
                    fecha_fin - fecha_inicio
                ).total_seconds(),
                2,
            )

            resultados = {
                "archivo_original": (
                    self.nombre_archivo_original
                ),
                "registros_iniciales": (
                    metricas_procesamiento[
                        "registros_iniciales"
                    ]
                ),
                "columnas_iniciales": (
                    metricas_procesamiento[
                        "columnas_iniciales"
                    ]
                ),
                "registros_procesados": (
                    metricas_procesamiento[
                        "registros_procesados"
                    ]
                ),
                "registros_eliminados": (
                    metricas_procesamiento[
                        "registros_eliminados"
                    ]
                ),
                "columnas_finales": (
                    metricas_procesamiento[
                        "columnas_finales"
                    ]
                ),
                "estadisticas": (
                    resultado_analisis[
                        "estadisticas"
                    ]
                ),
                "q1": (
                    resultado_analisis["q1"]
                ),
                "q3": (
                    resultado_analisis["q3"]
                ),
                "iqr": (
                    resultado_analisis["iqr"]
                ),
                "limite_inferior": (
                    resultado_analisis[
                        "limite_inferior"
                    ]
                ),
                "limite_superior": (
                    resultado_analisis[
                        "limite_superior"
                    ]
                ),
                "total_outliers": (
                    resultado_analisis[
                        "total_outliers"
                    ]
                ),
                "total_normales": (
                    resultado_analisis[
                        "total_normales"
                    ]
                ),
                "porcentaje_outliers": (
                    resultado_analisis[
                        "porcentaje_outliers"
                    ]
                ),
                "outliers_inferiores": (
                    resultado_analisis[
                        "outliers_inferiores"
                    ]
                ),
                "outliers_superiores": (
                    resultado_analisis[
                        "outliers_superiores"
                    ]
                ),
                "outliers_por_estado": (
                    resultado_analisis[
                        "outliers_por_estado"
                    ]
                ),
                "validacion_correcta": (
                    resultado_analisis[
                        "validacion_correcta"
                    ]
                ),
                "graficas": (
                    resultado_analisis[
                        "graficas"
                    ]
                ),
                "fecha_inicio": (
                    fecha_inicio.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                ),
                "fecha_fin": (
                    fecha_fin.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                ),
                "duracion_segundos": (
                    duracion_segundos
                ),
                "ruta_dataset_limpio": str(
                    self.ruta_dataset_limpio
                ),
                "ruta_outliers": str(
                    self.ruta_outliers
                ),
                "ruta_resumen": str(
                    self.ruta_resumen
                ),
                "ruta_log": str(
                    self.ruta_log
                ),
                "ruta_graficas": str(
                    self.ruta_graficas
                ),
                "ruta_zip": str(
                    self.ruta_zip
                ),
                "ejecucion_correcta": True,
            }

            self._crear_resumen(
                resultados
            )

            self.logger.registrar_evento(
                "Resumen de resultados generado."
            )

            self.logger.registrar_evento(
                "Procesamiento y análisis "
                "finalizados correctamente."
            )

            self._crear_zip()

            print()
            print(
                "==================================="
            )
            print(
                "SERVICIO FINALIZADO CORRECTAMENTE"
            )
            print(
                "==================================="
            )
            print(
                "Carpeta de resultados:"
            )
            print(
                self.carpeta_resultados
            )
            print(
                "Archivo ZIP:"
            )
            print(
                self.ruta_zip
            )

            return resultados

        except Exception as error:
            detalle = traceback.format_exc()

            if self.logger is not None:
                self.logger.registrar_error(
                    str(error)
                )
                self.logger.registrar_error(
                    detalle
                )

            raise

    def _validar_archivo_entrada(
        self,
    ) -> None:
        if not self.ruta_csv.exists():
            raise FileNotFoundError(
                "No se encontró el archivo CSV: "
                f"{self.ruta_csv}"
            )

        if not self.ruta_csv.is_file():
            raise ValueError(
                "La ruta de entrada no corresponde "
                "a un archivo."
            )

        if (
            self.ruta_csv.suffix.lower()
            != ".csv"
        ):
            raise ValueError(
                "El archivo debe tener extensión .csv."
            )

    def _crear_carpetas(self) -> None:
        self.carpeta_resultados.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.ruta_graficas.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _ejecutar_procesamiento(
        self,
    ) -> dict[str, Any]:
        self.logger.registrar_evento(
            "Inicio del procesamiento "
            "del dataset."
        )

        procesamiento = ProcesamientoDatos(
            ruta_entrada=str(
                self.ruta_csv
            ),
            ruta_salida=str(
                self.ruta_dataset_limpio
            ),
        )

        if not procesamiento.cargar_dataset():
            raise RuntimeError(
                "No fue posible cargar "
                "el dataset."
            )

        if not procesamiento.limpiar_dataset():
            raise RuntimeError(
                "No fue posible limpiar "
                "el dataset."
            )

        if not procesamiento.validar_dataset():
            raise RuntimeError(
                "El dataset limpio no superó "
                "la validación."
            )

        if not procesamiento.guardar_dataset():
            raise RuntimeError(
                "No fue posible guardar "
                "el dataset limpio."
            )

        metricas = (
            procesamiento.obtener_metricas()
        )

        self.logger.registrar_evento(
            "Procesamiento completado. "
            f"Registros iniciales: "
            f"{metricas['registros_iniciales']}. "
            f"Registros procesados: "
            f"{metricas['registros_procesados']}."
        )

        return metricas

    def _ejecutar_analisis(
        self,
    ) -> dict[str, Any]:
        self.logger.registrar_evento(
            "Inicio del análisis estadístico."
        )

        analisis = AnalisisDatos(
            ruta_dataset=str(
                self.ruta_dataset_limpio
            ),
            ruta_graficas=str(
                self.ruta_graficas
            ),
            ruta_outliers=str(
                self.ruta_outliers
            ),
        )

        if not analisis.cargar_dataset():
            raise RuntimeError(
                "No fue posible cargar el "
                "dataset limpio para analizarlo."
            )

        estadisticas = (
            analisis.analizar_distribucion()
        )

        metricas_iqr = (
            analisis.calcular_iqr()
        )

        limite_inferior = (
            metricas_iqr[
                "limite_inferior"
            ]
        )

        limite_superior = (
            metricas_iqr[
                "limite_superior"
            ]
        )

        analisis.detectar_outliers(
            limite_inferior=limite_inferior,
            limite_superior=limite_superior,
        )

        validacion = (
            analisis.validar_calculo(
                limite_inferior=limite_inferior,
                limite_superior=limite_superior,
            )
        )

        graficas = (
            analisis.generar_todas_las_graficas()
        )

        metricas = (
            analisis.obtener_metricas()
        )

        metricas[
            "validacion_correcta"
        ] = validacion[
            "validacion_correcta"
        ]

        metricas[
            "estadisticas"
        ] = estadisticas

        metricas[
            "graficas"
        ] = graficas

        self.logger.registrar_evento(
            "Análisis completado. "
            f"Outliers detectados: "
            f"{metricas['total_outliers']}. "
            f"Porcentaje: "
            f"{metricas['porcentaje_outliers']}%."
        )

        return metricas

    def _crear_resumen(
        self,
        resultados: dict[str, Any],
    ) -> None:
        estadisticas = (
            resultados["estadisticas"]
        )

        estados = (
            resultados[
                "outliers_por_estado"
            ]
        )

        lineas_estados = []

        for estado, cantidad in estados.items():
            lineas_estados.append(
                f"- {estado}: {cantidad}"
            )

        if not lineas_estados:
            lineas_estados.append(
                "- No se detectaron outliers."
            )

        contenido = [
            (
                "SISTEMA DE DETECCIÓN DE "
                "ANOMALÍAS EN BUILDS"
            ),
            "=" * 50,
            "",
            "INFORMACIÓN GENERAL",
            (
                "Archivo analizado: "
                f"{resultados['archivo_original']}"
            ),
            (
                "Fecha de inicio: "
                f"{resultados['fecha_inicio']}"
            ),
            (
                "Fecha de finalización: "
                f"{resultados['fecha_fin']}"
            ),
            (
                "Duración de la ejecución: "
                f"{resultados['duracion_segundos']} "
                "segundos"
            ),
            "",
            "PROCESAMIENTO",
            (
                "Registros iniciales: "
                f"{resultados['registros_iniciales']}"
            ),
            (
                "Registros procesados: "
                f"{resultados['registros_procesados']}"
            ),
            (
                "Registros eliminados: "
                f"{resultados['registros_eliminados']}"
            ),
            (
                "Columnas iniciales: "
                f"{resultados['columnas_iniciales']}"
            ),
            (
                "Columnas finales: "
                f"{resultados['columnas_finales']}"
            ),
            "",
            "ESTADÍSTICAS DE TR_DURATION",
            (
                "Cantidad: "
                f"{estadisticas['cantidad']}"
            ),
            (
                "Media: "
                f"{estadisticas['media']:.6f}"
            ),
            (
                "Desviación estándar: "
                f"{estadisticas['desviacion_estandar']:.6f}"
            ),
            (
                "Mínimo: "
                f"{estadisticas['minimo']:.2f}"
            ),
            (
                "Mediana: "
                f"{estadisticas['mediana']:.2f}"
            ),
            (
                "Máximo: "
                f"{estadisticas['maximo']:.2f}"
            ),
            "",
            "RANGO INTERCUARTÍLICO",
            f"Q1: {resultados['q1']:.2f}",
            f"Q3: {resultados['q3']:.2f}",
            f"IQR: {resultados['iqr']:.2f}",
            (
                "Límite inferior: "
                f"{resultados['limite_inferior']:.2f}"
            ),
            (
                "Límite superior: "
                f"{resultados['limite_superior']:.2f}"
            ),
            "",
            "DETECCIÓN DE ANOMALÍAS",
            (
                "Outliers detectados: "
                f"{resultados['total_outliers']}"
            ),
            (
                "Porcentaje de outliers: "
                f"{resultados['porcentaje_outliers']:.2f}%"
            ),
            (
                "Outliers inferiores: "
                f"{resultados['outliers_inferiores']}"
            ),
            (
                "Outliers superiores: "
                f"{resultados['outliers_superiores']}"
            ),
            (
                "Validación correcta: "
                f"{resultados['validacion_correcta']}"
            ),
            "",
            "OUTLIERS POR ESTADO",
            *lineas_estados,
            "",
            "INTERPRETACIÓN",
            (
                "Los registros detectados como "
                "outliers presentan una duración "
                "fuera de los límites calculados "
                "mediante el rango intercuartílico."
            ),
        ]

        self.ruta_resumen.write_text(
            "\n".join(contenido),
            encoding="utf-8",
        )

    def _crear_zip(self) -> None:
        archivos_obligatorios = [
            self.ruta_dataset_limpio,
            self.ruta_outliers,
            self.ruta_resumen,
            self.ruta_log,
        ]

        for ruta_archivo in (
            archivos_obligatorios
        ):
            if not ruta_archivo.exists():
                raise FileNotFoundError(
                    "No se puede crear el ZIP. "
                    f"Falta: {ruta_archivo}"
                )

        for nombre_grafica in (
            self.ARCHIVOS_GRAFICAS
        ):
            ruta_grafica = (
                self.ruta_graficas
                / nombre_grafica
            )

            if not ruta_grafica.exists():
                raise FileNotFoundError(
                    "No se puede crear el ZIP. "
                    "Falta la gráfica: "
                    f"{nombre_grafica}"
                )

        if self.ruta_zip.exists():
            self.ruta_zip.unlink()

        with zipfile.ZipFile(
            self.ruta_zip,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
        ) as archivo_zip:
            archivo_zip.write(
                self.ruta_dataset_limpio,
                arcname="dataset_limpio.csv",
            )

            archivo_zip.write(
                self.ruta_outliers,
                arcname="outliers_detectados.csv",
            )

            archivo_zip.write(
                self.ruta_resumen,
                arcname="resumen_resultados.txt",
            )

            archivo_zip.write(
                self.ruta_log,
                arcname="ejecucion_sistema.log",
            )

            for nombre_grafica in (
                self.ARCHIVOS_GRAFICAS
            ):
                ruta_grafica = (
                    self.ruta_graficas
                    / nombre_grafica
                )

                archivo_zip.write(
                    ruta_grafica,
                    arcname=(
                        "graficas/"
                        f"{nombre_grafica}"
                    ),
                )

        print(
            "Archivo ZIP generado correctamente:"
        )
        print(self.ruta_zip)