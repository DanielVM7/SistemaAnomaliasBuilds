import os
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


class AnalisisDatos:

    def __init__(
        self,
        ruta_dataset: str,
        ruta_graficas: str,
        ruta_outliers: str,
    ) -> None:
        self.ruta_dataset = ruta_dataset
        self.ruta_graficas = ruta_graficas
        self.ruta_outliers = ruta_outliers

        self.df: pd.DataFrame | None = None
        self.outliers: pd.DataFrame | None = None

        self.metricas: dict[str, Any] = {
            "q1": 0.0,
            "q3": 0.0,
            "iqr": 0.0,
            "limite_inferior": 0.0,
            "limite_superior": 0.0,
            "total_registros": 0,
            "total_outliers": 0,
            "total_normales": 0,
            "porcentaje_outliers": 0.0,
            "outliers_inferiores": 0,
            "outliers_superiores": 0,
            "outliers_por_estado": {},
            "validacion_correcta": False,
        }

        os.makedirs(
            self.ruta_graficas,
            exist_ok=True,
        )

    def cargar_dataset(self) -> bool:
        if not os.path.exists(self.ruta_dataset):
            print(
                "No se encontró el dataset limpio:"
            )
            print(self.ruta_dataset)
            return False

        try:
            self.df = pd.read_csv(
                self.ruta_dataset,
                low_memory=False,
            )
        except Exception as error:
            print(
                "Error al cargar el dataset limpio: "
                f"{error}"
            )
            return False

        columnas_requeridas = [
            "tr_duration",
            "gh_build_started_at",
            "tr_status",
        ]

        columnas_faltantes = [
            columna
            for columna in columnas_requeridas
            if columna not in self.df.columns
        ]

        if columnas_faltantes:
            print(
                "El dataset limpio no contiene las "
                "columnas necesarias: "
                + ", ".join(columnas_faltantes)
            )
            return False

        self.df["tr_duration"] = pd.to_numeric(
            self.df["tr_duration"],
            errors="coerce",
        )

        self.df["gh_build_started_at"] = (
            pd.to_datetime(
                self.df["gh_build_started_at"],
                errors="coerce",
            )
        )

        self.df["tr_status"] = (
            self.df["tr_status"]
            .astype("string")
            .str.strip()
            .str.lower()
        )

        self.df = self.df.dropna(
            subset=[
                "tr_duration",
                "gh_build_started_at",
            ]
        ).copy()

        self.metricas[
            "total_registros"
        ] = int(len(self.df))

        print(
            "Dataset limpio cargado correctamente."
        )
        print(
            "Registros disponibles para análisis: "
            f"{len(self.df)}"
        )
        print()

        return True

    def analizar_distribucion(self) -> dict[str, float]:
        self._validar_dataset_cargado()

        descripcion = (
            self.df["tr_duration"]
            .describe()
        )

        estadisticas = {
            "cantidad": int(
                descripcion["count"]
            ),
            "media": float(
                descripcion["mean"]
            ),
            "desviacion_estandar": float(
                descripcion["std"]
            ),
            "minimo": float(
                descripcion["min"]
            ),
            "q1": float(
                descripcion["25%"]
            ),
            "mediana": float(
                descripcion["50%"]
            ),
            "q3": float(
                descripcion["75%"]
            ),
            "maximo": float(
                descripcion["max"]
            ),
        }

        print("===================================")
        print("ANÁLISIS DE tr_duration")
        print("===================================")
        print(self.df["tr_duration"].describe())
        print()

        return estadisticas

    def calcular_iqr(self) -> dict[str, float]:
        self._validar_dataset_cargado()

        q1 = float(
            self.df[
                "tr_duration"
            ].quantile(0.25)
        )

        q3 = float(
            self.df[
                "tr_duration"
            ].quantile(0.75)
        )

        iqr = q3 - q1

        limite_inferior = (
            q1 - (1.5 * iqr)
        )

        limite_superior = (
            q3 + (1.5 * iqr)
        )

        resultado = {
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "limite_inferior": limite_inferior,
            "limite_superior": limite_superior,
        }

        self.metricas.update(resultado)

        print(
            "========== CÁLCULO Q1, Q3 E IQR =========="
        )
        print(f"Q1: {q1}")
        print(f"Q3: {q3}")
        print(f"IQR: {iqr}")
        print(
            f"Límite inferior: {limite_inferior}"
        )
        print(
            f"Límite superior: {limite_superior}"
        )
        print()

        return resultado

    def detectar_outliers(
        self,
        limite_inferior: float,
        limite_superior: float,
    ) -> dict[str, Any]:
        self._validar_dataset_cargado()

        mascara_outliers = (
            (
                self.df["tr_duration"]
                < limite_inferior
            )
            |
            (
                self.df["tr_duration"]
                > limite_superior
            )
        )

        self.outliers = self.df.loc[
            mascara_outliers
        ].copy()

        total_registros = int(
            len(self.df)
        )

        total_outliers = int(
            len(self.outliers)
        )

        total_normales = (
            total_registros - total_outliers
        )

        porcentaje_outliers = (
            (
                total_outliers
                / total_registros
            )
            * 100
            if total_registros > 0
            else 0.0
        )

        outliers_inferiores = int(
            (
                self.df["tr_duration"]
                < limite_inferior
            ).sum()
        )

        outliers_superiores = int(
            (
                self.df["tr_duration"]
                > limite_superior
            ).sum()
        )

        outliers_por_estado = (
            self.outliers["tr_status"]
            .fillna("sin estado")
            .astype(str)
            .value_counts()
            .astype(int)
            .to_dict()
        )

        self.metricas.update(
            {
                "total_registros": total_registros,
                "total_outliers": total_outliers,
                "total_normales": total_normales,
                "porcentaje_outliers": round(
                    porcentaje_outliers,
                    2,
                ),
                "outliers_inferiores": (
                    outliers_inferiores
                ),
                "outliers_superiores": (
                    outliers_superiores
                ),
                "outliers_por_estado": (
                    outliers_por_estado
                ),
            }
        )

        directorio_outliers = os.path.dirname(
            self.ruta_outliers
        )

        if directorio_outliers:
            os.makedirs(
                directorio_outliers,
                exist_ok=True,
            )

        self.outliers.to_csv(
            self.ruta_outliers,
            index=False,
            encoding="utf-8-sig",
        )

        print(
            "========== DETECCIÓN DE OUTLIERS =========="
        )
        print(
            "Total de registros analizados: "
            f"{total_registros}"
        )
        print(
            "Total de outliers detectados: "
            f"{total_outliers}"
        )
        print(
            "Porcentaje de outliers: "
            f"{porcentaje_outliers:.2f}%"
        )
        print(
            "Outliers inferiores: "
            f"{outliers_inferiores}"
        )
        print(
            "Outliers superiores: "
            f"{outliers_superiores}"
        )
        print()
        print(
            "Archivo de outliers guardado en:"
        )
        print(self.ruta_outliers)
        print()

        return self.metricas.copy()

    def validar_calculo(
        self,
        limite_inferior: float,
        limite_superior: float,
    ) -> dict[str, Any]:
        self._validar_dataset_cargado()

        total_menores = int(
            (
                self.df["tr_duration"]
                < limite_inferior
            ).sum()
        )

        total_mayores = int(
            (
                self.df["tr_duration"]
                > limite_superior
            ).sum()
        )

        total_validado = (
            total_menores + total_mayores
        )

        total_almacenado = (
            int(len(self.outliers))
            if self.outliers is not None
            else 0
        )

        validacion_correcta = (
            total_validado == total_almacenado
        )

        self.metricas[
            "validacion_correcta"
        ] = validacion_correcta

        print(
            "========== VALIDACIÓN DEL CÁLCULO =========="
        )
        print(
            "Registros menores al límite inferior: "
            f"{total_menores}"
        )
        print(
            "Registros mayores al límite superior: "
            f"{total_mayores}"
        )
        print(
            "Total validado como outliers: "
            f"{total_validado}"
        )
        print(
            "Total almacenado en self.outliers: "
            f"{total_almacenado}"
        )

        if validacion_correcta:
            print(
                "Validación correcta: el cálculo "
                "coincide con los outliers almacenados."
            )
        else:
            print(
                "Advertencia: el cálculo no coincide "
                "con los outliers almacenados."
            )

        print()

        return {
            "total_menores": total_menores,
            "total_mayores": total_mayores,
            "total_validado": total_validado,
            "total_almacenado": total_almacenado,
            "validacion_correcta": (
                validacion_correcta
            ),
        }

    def generar_histograma(self) -> str:
        self._validar_dataset_cargado()

        plt.figure(figsize=(10, 6))

        plt.hist(
            self.df["tr_duration"],
            bins=50,
        )

        plt.title(
            "Distribución de la duración de builds"
        )
        plt.xlabel("Duración (segundos)")
        plt.ylabel("Frecuencia")

        return self._guardar_figura(
            "histograma_duracion.png"
        )

    def generar_grafica_estados(self) -> str:
        self._validar_dataset_cargado()

        estados = (
            self.df["tr_status"]
            .fillna("sin estado")
            .value_counts()
        )

        plt.figure(figsize=(8, 6))
        estados.plot(kind="bar")

        plt.title(
            "Cantidad de builds por estado"
        )
        plt.xlabel("Estado")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=45)

        return self._guardar_figura(
            "builds_por_estado.png"
        )

    def generar_boxplot_outliers(self) -> str:
        self._validar_dataset_cargado()

        plt.figure(figsize=(10, 6))

        plt.boxplot(
            self.df["tr_duration"],
            vert=False,
        )

        plt.title(
            "Boxplot de duración de builds"
        )
        plt.xlabel("Duración (segundos)")

        return self._guardar_figura(
            "boxplot_outliers.png"
        )

    def generar_comparacion_normales_outliers(
        self,
    ) -> str:
        self._validar_outliers_generados()

        datos = {
            "Normales": (
                self.metricas["total_normales"]
            ),
            "Outliers": (
                self.metricas["total_outliers"]
            ),
        }

        plt.figure(figsize=(8, 6))

        plt.bar(
            datos.keys(),
            datos.values(),
        )

        plt.title(
            "Comparación entre builds normales y outliers"
        )
        plt.xlabel("Clasificación")
        plt.ylabel("Cantidad de builds")

        return self._guardar_figura(
            "comparacion_normales_outliers.png"
        )

    def generar_outliers_por_estado(
        self,
    ) -> str:
        self._validar_outliers_generados()

        estados = (
            self.outliers["tr_status"]
            .fillna("sin estado")
            .value_counts()
        )

        plt.figure(figsize=(8, 6))
        estados.plot(kind="bar")

        plt.title(
            "Outliers por estado del build"
        )
        plt.xlabel("Estado")
        plt.ylabel("Cantidad de outliers")
        plt.xticks(rotation=45)

        return self._guardar_figura(
            "outliers_por_estado.png"
        )

    def generar_tendencia_fallos(
        self,
    ) -> str:
        self._validar_dataset_cargado()

        datos = self.df.copy()

        datos["fecha"] = (
            datos["gh_build_started_at"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )

        fallos = datos[
            datos["tr_status"].isin(
                ["failed", "errored"]
            )
        ].copy()

        tendencia = (
            fallos.groupby("fecha")
            .size()
            .sort_index()
        )

        plt.figure(figsize=(11, 6))

        if tendencia.empty:
            plt.text(
                0.5,
                0.5,
                "No existen builds con estado "
                "failed o errored.",
                horizontalalignment="center",
                verticalalignment="center",
                transform=plt.gca().transAxes,
            )
        else:
            plt.plot(
                tendencia.index,
                tendencia.values,
                marker="o",
            )

        plt.title(
            "Tendencia de fallos en el tiempo"
        )
        plt.xlabel("Fecha")
        plt.ylabel(
            "Cantidad de builds con fallo"
        )
        plt.xticks(rotation=45)

        return self._guardar_figura(
            "tendencia_fallos.png"
        )

    def generar_proporcion_fallos_tiempo(
        self,
    ) -> str:
        self._validar_dataset_cargado()

        datos = self.df.copy()

        datos["fecha"] = (
            datos["gh_build_started_at"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )

        datos["es_fallo"] = (
            datos["tr_status"].isin(
                ["failed", "errored"]
            )
        )

        proporcion = (
            datos.groupby("fecha")["es_fallo"]
            .mean()
            .mul(100)
            .sort_index()
        )

        plt.figure(figsize=(11, 6))

        if proporcion.empty:
            plt.text(
                0.5,
                0.5,
                "No existen datos temporales "
                "disponibles.",
                horizontalalignment="center",
                verticalalignment="center",
                transform=plt.gca().transAxes,
            )
        else:
            plt.plot(
                proporcion.index,
                proporcion.values,
                marker="o",
            )

        plt.title(
            "Proporción de fallos en el tiempo"
        )
        plt.xlabel("Fecha")
        plt.ylabel(
            "Porcentaje de builds con fallo"
        )
        plt.xticks(rotation=45)

        return self._guardar_figura(
            "proporcion_fallos_tiempo.png"
        )

    def generar_todas_las_graficas(
        self,
    ) -> list[str]:
        rutas = [
            self.generar_histograma(),
            self.generar_grafica_estados(),
            self.generar_boxplot_outliers(),
            self.generar_comparacion_normales_outliers(),
            self.generar_outliers_por_estado(),
            self.generar_tendencia_fallos(),
            self.generar_proporcion_fallos_tiempo(),
        ]

        print(
            "Las siete gráficas fueron generadas "
            "correctamente."
        )
        print()

        return rutas

    def obtener_metricas(self) -> dict[str, Any]:
        return self.metricas.copy()

    def _guardar_figura(
        self,
        nombre_archivo: str,
    ) -> str:
        os.makedirs(
            self.ruta_graficas,
            exist_ok=True,
        )

        ruta = os.path.join(
            self.ruta_graficas,
            nombre_archivo,
        )

        plt.tight_layout()

        plt.savefig(
            ruta,
            dpi=150,
            bbox_inches="tight",
        )

        plt.close()

        print(
            f"Gráfica generada: {nombre_archivo}"
        )

        return ruta

    def _validar_dataset_cargado(
        self,
    ) -> None:
        if self.df is None:
            raise ValueError(
                "Debe cargarse el dataset antes "
                "de ejecutar el análisis."
            )

    def _validar_outliers_generados(
        self,
    ) -> None:
        if self.outliers is None:
            raise ValueError(
                "Primero debe ejecutarse la "
                "detección de outliers."
            )