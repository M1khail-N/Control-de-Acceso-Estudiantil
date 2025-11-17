import { RegistroClaseAPI, GestionAPI } from "../api.js";

document.addEventListener("DOMContentLoaded", () => {

    const formClase = document.getElementById("formRegistroClase");
    const selectMaquina = document.getElementById("maquinaClase");
    const selectAsignatura = document.getElementById("asignaturaClase");
    const selectProfesor = document.getElementById("profesorClase");

    let asignaturasRaw = [];

    // =============================
    // Cargar máquinas
    // =============================
    GestionAPI.getMaquinas().then(data => {
        selectMaquina.innerHTML = "<option value=''>Seleccione...</option>";
        data.forEach(m => {
            selectMaquina.innerHTML += `<option value="${m.id_maquina}">${m.nombre}</option>`;
        });
    });

    // =============================
    // Cargar asignaturas
    // =============================
    GestionAPI.getAsignaturas().then(data => {

        asignaturasRaw = data;

        selectAsignatura.innerHTML = "<option value=''>Seleccione...</option>";

        // Extraer nombres únicos
        const nombresUnicos = [...new Set(data.map(a => a.nombre))];

        nombresUnicos.forEach(nombre => {
            selectAsignatura.innerHTML += `
                <option value="${nombre}">${nombre}</option>
            `;
        });
    });

    // =============================
    // Al elegir asignatura → cargar profesores
    // =============================
    selectAsignatura.addEventListener("change", () => {
        const nombreSeleccionado = selectAsignatura.value;
        if (!nombreSeleccionado) return;

        const grupo = asignaturasRaw.filter(a => a.nombre === nombreSeleccionado);

        selectProfesor.innerHTML = "<option value=''>Seleccione...</option>";

        grupo.forEach(a => {
            selectProfesor.innerHTML += `
                <option value="${a.profesor}" data-asignatura="${a.id_asignatura}">
                    ${a.nombre_profesor} ${a.apellido_profesor}
                </option>
            `;
        });
    });

    // =============================
    // Enviar formulario
    // =============================
    formClase.addEventListener("submit", async (e) => {
        e.preventDefault();

        const profesorOption = selectProfesor.selectedOptions[0];
        const asignaturaId = profesorOption.getAttribute("data-asignatura");

        const payload = {
            codigo_alumno: document.getElementById("codigoAlumnoClase").value,
            maquina_id: selectMaquina.value,
            asignatura_id: Number(asignaturaId),
            profesor_id: Number(selectProfesor.value)
        };

        const mensaje = document.getElementById("mensajeClase");

        try {
            await RegistroClaseAPI.marcarEntrada(payload);
            mensaje.textContent = "Entrada registrada correctamente.";
            mensaje.className = "success";
            formClase.reset();
        } catch (err) {
            mensaje.textContent = err.message;
            mensaje.className = "error";
        }
    });

});