import { apiRequest } from "../../js/api.js";

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("formSemana");
    const inputSemana = document.getElementById("inputSemana");
    const inputAnio = document.getElementById("inputAnio");
    const mensaje = document.getElementById("mensaje");
    const tablaCard = document.getElementById("tablaCard");
    const tbody = document.querySelector("#tablaResultados tbody");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const semana = inputSemana.value;
        const anio = inputAnio.value;

        if (!semana || !anio) {
            mensaje.textContent = "Debe ingresar semana y año.";
            mensaje.className = "error";
            return;
        }

        mensaje.textContent = "";
        mensaje.className = "";

        try {
            const url =
                `/api/estadisticas/laboratorio/uso-semana/?semana=${semana}&anio=${anio}`;

            const data = await apiRequest(url);

            if (!data || data.length === 0) {
                mensaje.textContent = "No hay registros para esta semana.";
                mensaje.className = "warning";
                tablaCard.style.display = "none";
                return;
            }

            tbody.innerHTML = "";

            data.forEach(item => {
                tbody.innerHTML += `
                    <tr>
                        <td>${item.codigo_alumno}</td>
                        <td>${item.nombre}</td>
                        <td>${item.apellido}</td>
                        <td>${item.edad}</td>
                        <td>${new Date(item.fecha_entrada).toLocaleString()}</td>
                        <td>${item.fecha_salida ? new Date(item.fecha_salida).toLocaleString() : "-"}</td>
                    </tr>
                `;
            });

            tablaCard.style.display = "block";

        } catch (error) {
            mensaje.textContent = "Error al consultar datos.";
            mensaje.className = "error";
            console.error("Error:", error);
        }
    });

});
