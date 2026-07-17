import os
from datetime import datetime


class LoggerSistema:

    def __init__(
        self,
        ruta_archivo_log: str,
    ) -> None:
        self.ruta_archivo_log = (
            ruta_archivo_log
        )

        directorio = os.path.dirname(
            self.ruta_archivo_log
        )

        if directorio:
            os.makedirs(
                directorio,
                exist_ok=True,
            )

    def registrar(
        self,
        mensaje: str,
        nivel: str = "INFO",
    ) -> None:
        fecha_hora = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        linea = (
            f"[{fecha_hora}] "
            f"[{nivel.upper()}] "
            f"{mensaje}\n"
        )

        with open(
            self.ruta_archivo_log,
            mode="a",
            encoding="utf-8",
        ) as archivo:
            archivo.write(linea)

        print(
            f"LOG [{nivel.upper()}]: "
            f"{mensaje}"
        )

    def registrar_evento(
        self,
        mensaje: str,
    ) -> None:
        self.registrar(
            mensaje=mensaje,
            nivel="INFO",
        )

    def registrar_error(
        self,
        mensaje: str,
    ) -> None:
        self.registrar(
            mensaje=mensaje,
            nivel="ERROR",
        )

    def registrar_advertencia(
        self,
        mensaje: str,
    ) -> None:
        self.registrar(
            mensaje=mensaje,
            nivel="WARNING",
        )

    def obtener_ruta(self) -> str:
        return self.ruta_archivo_log