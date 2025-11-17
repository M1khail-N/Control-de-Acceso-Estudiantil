import { RegistroBaseAPI } from "../api.js";

document.addEventListener("DOMContentLoaded", () => {

    const formSalida = document.getElementById("formSalida");

    formSalida.addEventListener("submit", async (e) => {
        e.preventDefault();

        const codigo = document.getElementById("codigoAlumnoSalida").value.trim();
        const mensaje = document.getElementById("mensajeSalida");

        try {
            await RegistroBaseAPI.marcarSalida({ codigo_alumno: codigo });
            mensaje.textContent = "Salida registrada correctamente.";
            mensaje.className = "success";
            formSalida.reset();
        } catch (err) {
            mensaje.textContent = err.message;
            mensaje.className = "error";
        }
    });

});