document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById(
        "formulario-carga"
    );

    const archivoInput = document.getElementById(
        "archivo_csv"
    );

    const botonProcesar = document.getElementById(
        "boton-procesar"
    );

    const pantallaCarga = document.getElementById(
        "pantalla-carga"
    );

    const tituloProgreso = document.getElementById(
        "titulo-progreso"
    );

    const mensajeProgreso = document.getElementById(
        "mensaje-progreso"
    );

    const porcentajeProgreso = document.getElementById(
        "porcentaje-progreso"
    );

    const barraProgreso = document.getElementById(
        "barra-progreso"
    );

    const tiempoTranscurrido = document.getElementById(
        "tiempo-transcurrido"
    );

    if (
        !formulario
        || !archivoInput
        || !botonProcesar
        || !pantallaCarga
        || !tituloProgreso
        || !mensajeProgreso
        || !porcentajeProgreso
        || !barraProgreso
        || !tiempoTranscurrido
    ) {
        return;
    }

    let intervaloTiempo = null;
    let segundosTranscurridos = 0;

    function formatearTiempo(segundos) {
        const horas = Math.floor(
            segundos / 3600
        );

        const minutos = Math.floor(
            (segundos % 3600) / 60
        );

        const segundosRestantes = (
            segundos % 60
        );

        if (horas > 0) {
            return (
                String(horas).padStart(2, "0")
                + ":"
                + String(minutos).padStart(2, "0")
                + ":"
                + String(segundosRestantes).padStart(2, "0")
            );
        }

        return (
            String(minutos).padStart(2, "0")
            + ":"
            + String(segundosRestantes).padStart(2, "0")
        );
    }

    function iniciarContador() {
        segundosTranscurridos = 0;

        tiempoTranscurrido.textContent = (
            "Tiempo transcurrido: 00:00"
        );

        intervaloTiempo = window.setInterval(
            () => {
                segundosTranscurridos += 1;

                tiempoTranscurrido.textContent = (
                    "Tiempo transcurrido: "
                    + formatearTiempo(
                        segundosTranscurridos
                    )
                );
            },
            1000
        );
    }

    function detenerContador() {
        if (intervaloTiempo !== null) {
            window.clearInterval(
                intervaloTiempo
            );

            intervaloTiempo = null;
        }
    }

    function mostrarPantallaCarga() {
        pantallaCarga.classList.add(
            "visible"
        );

        pantallaCarga.setAttribute(
            "aria-hidden",
            "false"
        );

        document.body.classList.add(
            "procesando"
        );
    }

    function ocultarPantallaCarga() {
        pantallaCarga.classList.remove(
            "visible"
        );

        pantallaCarga.setAttribute(
            "aria-hidden",
            "true"
        );

        document.body.classList.remove(
            "procesando"
        );
    }

    function establecerFaseSubida(
        nombreArchivo
    ) {
        tituloProgreso.textContent = (
            "Cargando archivo"
        );

        mensajeProgreso.textContent = (
            "Subiendo "
            + nombreArchivo
            + " al servidor."
        );

        porcentajeProgreso.textContent = (
            "0 %"
        );

        barraProgreso.classList.remove(
            "indeterminada"
        );

        barraProgreso.style.width = "0%";
    }

    function establecerFaseProcesamiento() {
        tituloProgreso.textContent = (
            "Procesando dataset"
        );

        mensajeProgreso.textContent = (
            "El sistema está limpiando los datos, "
            + "calculando el IQR, detectando anomalías, "
            + "generando las gráficas y creando el ZIP."
        );

        porcentajeProgreso.textContent = (
            "Procesando..."
        );

        barraProgreso.style.width = "35%";

        barraProgreso.classList.add(
            "indeterminada"
        );
    }

    function restablecerFormulario() {
        botonProcesar.disabled = false;

        botonProcesar.textContent = (
            "Procesar dataset"
        );

        detenerContador();
        ocultarPantallaCarga();

        barraProgreso.classList.remove(
            "indeterminada"
        );

        barraProgreso.style.width = "0%";
    }

    formulario.addEventListener(
        "submit",
        (evento) => {
            evento.preventDefault();

            if (
                archivoInput.files.length === 0
            ) {
                window.alert(
                    "Debes seleccionar un archivo CSV."
                );

                return;
            }

            const archivo = (
                archivoInput.files[0]
            );

            if (
                !archivo.name
                    .toLowerCase()
                    .endsWith(".csv")
            ) {
                window.alert(
                    "El archivo seleccionado debe "
                    + "tener extensión .csv."
                );

                return;
            }

            botonProcesar.disabled = true;

            botonProcesar.textContent = (
                "Procesando..."
            );

            establecerFaseSubida(
                archivo.name
            );

            mostrarPantallaCarga();
            iniciarContador();

            const datosFormulario = (
                new FormData(formulario)
            );

            const solicitud = (
                new XMLHttpRequest()
            );

            solicitud.open(
                "POST",
                formulario.action
                    || window.location.href,
                true
            );

            solicitud.upload.addEventListener(
                "progress",
                (eventoProgreso) => {
                    if (
                        !eventoProgreso.lengthComputable
                    ) {
                        return;
                    }

                    const porcentaje = Math.round(
                        (
                            eventoProgreso.loaded
                            / eventoProgreso.total
                        )
                        * 100
                    );

                    barraProgreso.style.width = (
                        porcentaje + "%"
                    );

                    porcentajeProgreso.textContent = (
                        porcentaje + " %"
                    );

                    mensajeProgreso.textContent = (
                        "Subiendo "
                        + archivo.name
                        + " al servidor."
                    );
                }
            );

            solicitud.upload.addEventListener(
                "load",
                () => {
                    establecerFaseProcesamiento();
                }
            );

            solicitud.addEventListener(
                "load",
                () => {
                    detenerContador();

                    if (
                        solicitud.status >= 200
                        && solicitud.status < 400
                    ) {
                        document.open();

                        document.write(
                            solicitud.responseText
                        );

                        document.close();

                        return;
                    }

                    restablecerFormulario();

                    window.alert(
                        "El servidor no pudo completar "
                        + "el procesamiento. Código: "
                        + solicitud.status
                    );
                }
            );

            solicitud.addEventListener(
                "error",
                () => {
                    restablecerFormulario();

                    window.alert(
                        "Ocurrió un error de conexión "
                        + "durante la carga del archivo."
                    );
                }
            );

            solicitud.addEventListener(
                "abort",
                () => {
                    restablecerFormulario();

                    window.alert(
                        "La carga del archivo fue cancelada."
                    );
                }
            );

            solicitud.addEventListener(
                "timeout",
                () => {
                    restablecerFormulario();

                    window.alert(
                        "La solicitud tardó demasiado "
                        + "y fue interrumpida."
                    );
                }
            );

            solicitud.timeout = 0;

            solicitud.send(
                datosFormulario
            );
        }
    );
});