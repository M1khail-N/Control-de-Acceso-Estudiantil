import { apiRequest } from "../../js/api.js";

document.addEventListener("DOMContentLoaded", async () => {

    const form = document.getElementById("formFiltros");
    const selectMaquina = document.getElementById("selectMaquina");
    const selectAsignatura = document.getElementById("selectAsignatura");
    const inputFecha = document.getElementById("inputFecha");
    const mensaje = document.getElementById("mensaje");
    const tablaCard = document.getElementById("tablaCard");
    const tbody = document.querySelector("#tablaResultados tbody");

    // Cargar listas desde API
    await cargarSelect(selectMaquina, "/api/gestion/maquinas/");
    await cargarSelect(selectAsignatura, "/api/gestion/asignaturas/");

    async function cargarSelect(select, url) {
        const data = await apiRequest(url);

        select.innerHTML = `<option value="">Seleccione...</option>`;

        data.forEach(item => {

            let id, label;

            // Detectar si es máquina
            if (item.id_maquina) {
                id = item.id_maquina;
                label = item.nombre;
            }
            // Detectar si es asignatura (tiene profesor)
            else if (item.id_asignatura) {
                id = item.id_asignatura;

                const nombreAsig = item.nombre;
                const profNom = item.nombre_profesor || "";
                const profApe = item.apellido_profesor || "";

                // Formato solicitado:
                label = `${nombreAsig} - ${profNom} ${profApe}`.trim();
            }
            // Fallback genérico
            else {
                id = item.id;
                label = item.nombre || "Sin nombre";
            }

            select.innerHTML += `<option value="${id}">${label}</option>`;
        });
    }

    // Convertir fecha YYYY-MM-DD → DD/MM/YYYY
    function convertirFecha(fechaISO) {
        const [y, m, d] = fechaISO.split("-");
        return `${d}/${m}/${y}`;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const maquina = selectMaquina.value;
        const asignatura = selectAsignatura.value;
        const fechaISO = inputFecha.value;

        if (!maquina || !asignatura || !fechaISO) {
            mensaje.textContent = "Debe completar todos los filtros.";
            mensaje.className = "error";
            return;
        }

        const fecha = convertirFecha(fechaISO);

        mensaje.textContent = "";
        mensaje.className = "";

        try {
            const url =
                `/api/estadisticas/maquina/consulta/?maquina_id=${maquina}&asignatura_id=${asignatura}&fecha=${fecha}`;

            const data = await apiRequest(url);

            if (!data || data.length === 0) {
                mensaje.textContent = "No hay resultados para estos filtros.";
                mensaje.className = "warning";
                tablaCard.style.display = "none";
                return;
            }

            tbody.innerHTML = "";

            data.forEach(item => {
                tbody.innerHTML += `
                    <tr>
                        <td>${item.nombre} ${item.apellido}</td>
                        <td>${item.codigo_alumno}</td>
                        <td>${item.carrera}</td>
                        <td>${item.ciclo}</td>
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