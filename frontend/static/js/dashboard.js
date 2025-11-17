import { apiRequest } from "./api.js";

document.addEventListener("DOMContentLoaded", async () => {
    try {
        const data = await apiRequest("/api/estadisticas/dashboard/resumen/");

        document.getElementById("sesiones_activas").textContent =
            data.sesiones_activas;

        document.getElementById("promedio_tiempo").textContent =
            data.promedio_tiempo_minutos.toFixed(2);

        document.getElementById("ciclo_top").textContent =
            data.ciclo_con_mas_uso ?? "-";

        document.getElementById("ciclo_total").textContent =
            data.total_sesiones_ciclo;
    } catch (error) {
        console.error("Error cargando dashboard:", error);
    }
});