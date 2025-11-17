import { apiRequest } from "../../js/api.js";

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("formMotivoMes");
    const selectMes = document.getElementById("selectMes");
    const tablaCard = document.getElementById("tablaCard");
    const tbody = document.querySelector("#tablaResultados tbody");
    const mensaje = document.getElementById("mensajeMotivoMes");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const mes = selectMes.value;
        if (!mes) {
            mensaje.textContent = "Debe seleccionar un mes.";
            mensaje.className = "error";
            return;
        }

        mensaje.textContent = "";
        mensaje.className = "";

        try {
            const data = await apiRequest(`/api/estadisticas/motivo/promedio/?mes=${mes}`);

            if (!data || data.length === 0) {
                mensaje.textContent = "No hay resultados para este mes.";
                mensaje.className = "warning";
                tablaCard.style.display = "none";
                return;
            }

            // Poblar tabla
            tbody.innerHTML = "";
            data.forEach(item => {
                tbody.innerHTML += `
                    <tr>
                        <td>${item.motivo}</td>
                        <td>${item.promedio_minutos.toFixed(2)}</td>
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