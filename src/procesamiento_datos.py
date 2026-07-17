import os
from typing import Any

import pandas as pd


class ProcesamientoDatos:

    COLUMNAS_ESTANDAR = [
        "tr_duration",
        "gh_build_started_at",
        "tr_status",
        "gh_project_name",
        "tr_log_num_tests_run",
        "tr_log_num_tests_failed",
        "tr_log_frameworks",
    ]

    COLUMNAS_ESQUEMA_NUEVO = [
        "tr_duration",
        "gh_build_started_at",
        "tr_status",
        "gh_project_name",
        "tr_log_num_tests_run",
        "tr_log_num_tests_failed",
        "tr_log_frameworks",
    ]

    COLUMNAS_ESQUEMA_ANTIGUO = [
        "tr_duration",
        "tr_started_at",
        "tr_status",
        "gh_project_name",
        "tr_tests_run",
        "tr_tests_fail",
        "tr_frameworks",
    ]

    EQUIVALENCIAS_ESQUEMA_ANTIGUO = {
        "tr_started_at": "gh_build_started_at",
        "tr_tests_run": "tr_log_num_tests_run",
        "tr_tests_fail": "tr_log_num_tests_failed",
        "tr_frameworks": "tr_log_frameworks",
    }

    COLUMNAS_NUMERICAS = [
        "tr_duration",
        "tr_log_num_tests_run",
        "tr_log_num_tests_failed",
    ]

    def __init__(
        self,
        ruta_entrada: str,
        ruta_salida: str,
    ) -> None:
        self.ruta_entrada = ruta_entrada
        self.ruta_salida = ruta_salida

        self.df: pd.DataFrame | None = None
        self.df_limpio: pd.DataFrame | None = None

        self.esquema_detectado: str | None = None
        self.columnas_origen: list[str] = []

        self.metricas: dict[str, Any] = {
            "registros_iniciales": 0,
            "columnas_iniciales": 0,
            "registros_procesados": 0,
            "registros_eliminados": 0,
            "columnas_finales": 0,
            "esquema_detectado": "",
            "columnas_requeridas": (
                self.COLUMNAS_ESTANDAR.copy()
            ),
            "columnas_faltantes": [],
            "validacion_correcta": False,
        }

    def cargar_dataset(self) -> bool:
        """
        Detecta el esquema del CSV y carga solamente las siete
        columnas necesarias para el análisis.

        El archivo original no se modifica.
        """

        if not os.path.exists(self.ruta_entrada):
            print(
                "Error: no se encontró el archivo del dataset:"
            )
            print(self.ruta_entrada)
            return False

        if not os.path.isfile(self.ruta_entrada):
            print(
                "Error: la ruta proporcionada no corresponde "
                "a un archivo."
            )
            return False

        if not self.ruta_entrada.lower().endswith(".csv"):
            print(
                "Error: el archivo de entrada debe tener "
                "extensión .csv."
            )
            return False

        try:
            encabezado = pd.read_csv(
                self.ruta_entrada,
                nrows=0,
            )
        except Exception as error:
            print(
                "Error al leer el encabezado del dataset: "
                f"{error}"
            )
            return False

        columnas_disponibles = (
            encabezado.columns.tolist()
        )

        self.metricas["columnas_iniciales"] = int(
            len(columnas_disponibles)
        )

        if self._contiene_columnas(
            columnas_disponibles,
            self.COLUMNAS_ESQUEMA_NUEVO,
        ):
            self.esquema_detectado = "nuevo"
            self.columnas_origen = (
                self.COLUMNAS_ESQUEMA_NUEVO.copy()
            )

        elif self._contiene_columnas(
            columnas_disponibles,
            self.COLUMNAS_ESQUEMA_ANTIGUO,
        ):
            self.esquema_detectado = "antiguo"
            self.columnas_origen = (
                self.COLUMNAS_ESQUEMA_ANTIGUO.copy()
            )

        else:
            faltantes_nuevo = [
                columna
                for columna in self.COLUMNAS_ESQUEMA_NUEVO
                if columna not in columnas_disponibles
            ]

            faltantes_antiguo = [
                columna
                for columna in self.COLUMNAS_ESQUEMA_ANTIGUO
                if columna not in columnas_disponibles
            ]

            self.metricas[
                "columnas_faltantes"
            ] = faltantes_nuevo

            print(
                "El dataset no coincide con ninguno de "
                "los esquemas compatibles."
            )

            print(
                "Columnas faltantes para el esquema nuevo:"
            )

            print(
                ", ".join(faltantes_nuevo)
                if faltantes_nuevo
                else "Ninguna"
            )

            print(
                "Columnas faltantes para el esquema antiguo:"
            )

            print(
                ", ".join(faltantes_antiguo)
                if faltantes_antiguo
                else "Ninguna"
            )

            return False

        try:
            self.df = pd.read_csv(
                self.ruta_entrada,
                usecols=self.columnas_origen,
                low_memory=False,
            )
        except Exception as error:
            print(
                "Error al cargar las columnas requeridas: "
                f"{error}"
            )
            return False

        if self.esquema_detectado == "antiguo":
            self.df.rename(
                columns=(
                    self.EQUIVALENCIAS_ESQUEMA_ANTIGUO
                ),
                inplace=True,
            )

        self.metricas["registros_iniciales"] = int(
            self.df.shape[0]
        )

        self.metricas[
            "esquema_detectado"
        ] = self.esquema_detectado

        print("Dataset cargado correctamente.")

        print(
            "Esquema detectado: "
            f"{self.esquema_detectado}"
        )

        print(
            "Registros iniciales: "
            f"{self.metricas['registros_iniciales']}"
        )

        print(
            "Columnas originales del archivo: "
            f"{self.metricas['columnas_iniciales']}"
        )

        print(
            "Columnas cargadas para el análisis: "
            f"{self.df.shape[1]}"
        )

        print()

        return True

    def validar_columnas(self) -> bool:
        if self.df is None:
            raise ValueError(
                "Debe cargarse el dataset antes de validar "
                "las columnas."
            )

        columnas_faltantes = [
            columna
            for columna in self.COLUMNAS_ESTANDAR
            if columna not in self.df.columns
        ]

        self.metricas[
            "columnas_faltantes"
        ] = columnas_faltantes

        if columnas_faltantes:
            print(
                "El dataset no contiene todas las columnas "
                "estandarizadas requeridas."
            )

            print(
                "Columnas faltantes: "
                + ", ".join(columnas_faltantes)
            )

            return False

        print(
            "Validación de columnas completada "
            "correctamente."
        )

        return True

    def limpiar_dataset(self) -> bool:
        if self.df is None:
            raise ValueError(
                "Debe cargarse el dataset antes de realizar "
                "la limpieza."
            )

        if not self.validar_columnas():
            return False

        datos = self.df[
            self.COLUMNAS_ESTANDAR
        ].copy()

        for columna in self.COLUMNAS_NUMERICAS:
            datos[columna] = pd.to_numeric(
                datos[columna],
                errors="coerce",
            )

        datos["gh_build_started_at"] = pd.to_datetime(
            datos["gh_build_started_at"],
            errors="coerce",
        )

        datos["tr_status"] = (
            datos["tr_status"]
            .astype("string")
            .str.strip()
            .str.lower()
        )

        datos["gh_project_name"] = (
            datos["gh_project_name"]
            .astype("string")
            .str.strip()
        )

        datos["tr_log_frameworks"] = (
            datos["tr_log_frameworks"]
            .astype("string")
            .str.strip()
        )

        datos = datos.dropna(
            subset=[
                "tr_duration",
                "gh_build_started_at",
            ]
        )

        datos = datos[
            datos["tr_duration"] > 0
        ].copy()

        datos["anio"] = (
            datos["gh_build_started_at"].dt.year
        )

        datos["mes"] = (
            datos["gh_build_started_at"].dt.month
        )

        datos["dia"] = (
            datos["gh_build_started_at"].dt.day
        )

        datos["hora"] = (
            datos["gh_build_started_at"].dt.hour
        )

        datos.reset_index(
            drop=True,
            inplace=True,
        )

        self.df_limpio = datos

        registros_procesados = int(
            self.df_limpio.shape[0]
        )

        registros_eliminados = (
            self.metricas["registros_iniciales"]
            - registros_procesados
        )

        self.metricas.update(
            {
                "registros_procesados": (
                    registros_procesados
                ),
                "registros_eliminados": (
                    registros_eliminados
                ),
                "columnas_finales": int(
                    self.df_limpio.shape[1]
                ),
            }
        )

        print()
        print("Limpieza del dataset completada.")

        print(
            "Registros procesados: "
            f"{registros_procesados}"
        )

        print(
            "Registros eliminados: "
            f"{registros_eliminados}"
        )

        print(
            "Columnas finales: "
            f"{self.metricas['columnas_finales']}"
        )

        return True

    def validar_dataset(self) -> bool:
        if self.df_limpio is None:
            raise ValueError(
                "Primero debe ejecutarse la limpieza "
                "del dataset."
            )

        columnas_finales = (
            self.COLUMNAS_ESTANDAR
            + ["anio", "mes", "dia", "hora"]
        )

        columnas_faltantes = [
            columna
            for columna in columnas_finales
            if columna not in self.df_limpio.columns
        ]

        if columnas_faltantes:
            print(
                "Error de validación. Faltan columnas: "
                + ", ".join(columnas_faltantes)
            )

            self.metricas[
                "validacion_correcta"
            ] = False

            return False

        if self.df_limpio.empty:
            print(
                "Error de validación: el dataset limpio "
                "está vacío."
            )

            self.metricas[
                "validacion_correcta"
            ] = False

            return False

        if self.df_limpio[
            "tr_duration"
        ].isna().any():
            print(
                "Error de validación: existen valores "
                "nulos en tr_duration."
            )

            self.metricas[
                "validacion_correcta"
            ] = False

            return False

        if (
            self.df_limpio["tr_duration"] <= 0
        ).any():
            print(
                "Error de validación: existen duraciones "
                "menores o iguales a cero."
            )

            self.metricas[
                "validacion_correcta"
            ] = False

            return False

        if self.df_limpio[
            "gh_build_started_at"
        ].isna().any():
            print(
                "Error de validación: existen fechas "
                "inválidas."
            )

            self.metricas[
                "validacion_correcta"
            ] = False

            return False

        self.metricas[
            "validacion_correcta"
        ] = True

        print()
        print(
            "Validación del dataset limpio completada "
            "correctamente."
        )

        return True

    def guardar_dataset(self) -> bool:
        if self.df_limpio is None:
            raise ValueError(
                "No existe un dataset limpio para guardar."
            )

        directorio_salida = os.path.dirname(
            self.ruta_salida
        )

        if directorio_salida:
            os.makedirs(
                directorio_salida,
                exist_ok=True,
            )

        try:
            self.df_limpio.to_csv(
                self.ruta_salida,
                index=False,
                encoding="utf-8-sig",
            )
        except Exception as error:
            print(
                "Error al guardar el dataset limpio: "
                f"{error}"
            )

            return False

        print(
            "Dataset limpio guardado correctamente en:"
        )

        print(self.ruta_salida)
        print()

        return True

    def obtener_metricas(self) -> dict[str, Any]:
        return self.metricas.copy()

    @staticmethod
    def _contiene_columnas(
        columnas_disponibles: list[str],
        columnas_requeridas: list[str],
    ) -> bool:
        """
        Comprueba si todas las columnas requeridas se encuentran
        en el encabezado del archivo.
        """

        return all(
            columna in columnas_disponibles
            for columna in columnas_requeridas
        )