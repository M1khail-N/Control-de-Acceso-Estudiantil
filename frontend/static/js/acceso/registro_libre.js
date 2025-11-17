import { RegistroLibreAPI, GestionAPI } from "../api.js";

document.addEventListener("DOMContentLoaded", () => {

    const formLibre = document.getElementById("formRegistroLibre");
    const selectMaquina = document.getElementById("maquina");

    // Cargar máquinas
    GestionAPI.getMaquinas().then(data => {
        selectMaquina.innerHTML = "<option value=''>Seleccione...</option>";
        data.forEach(m => {
            selectMaquina.innerHTML += `<option value="${m.id_maquina}">${m.nombre}</option>`;
        });
    });

    formLibre.addEventListener("submit", async (e) => {
        e.preventDefault();

        const payload = {
            codigo_alumno: document.getElementById("codigoAlumno").value,
            maquina_id: selectMaquina.value,
            motivo: document.getElementById("motivo").value.trim()
        };

        const mensaje = document.getElementById("mensajeLibre");

        try {
            await RegistroLibreAPI.marcarEntrada(payload);
            mensaje.textContent = "Entrada libre registrada correctamente.";
            mensaje.className = "success";
            formLibre.reset();
        } catch (err) {
            mensaje.textContent = err.message;
            mensaje.className = "error";
        }
    });

});