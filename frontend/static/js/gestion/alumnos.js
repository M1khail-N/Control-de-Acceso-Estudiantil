import { GestionAPI } from "../api.js";

document.addEventListener("DOMContentLoaded", () => {
    const tabla = document.getElementById("tabla-alumnos");
    const modal = document.getElementById("modalAlumno");
    const btnAgregar = document.getElementById("btnAgregar");
    const btnCerrarModal = document.getElementById("btnCerrarModal");
    const form = document.getElementById("formAlumno");
    let editId = null;

    function cargarAlumnos() {
        GestionAPI.getAlumnos().then(data => {
            tabla.innerHTML = "";
            data.forEach(alumno => {
                tabla.innerHTML += `
                    <tr>
                        <td>${alumno.codigo_alumno}</td>
                        <td>${alumno.nombre}</td>
                        <td>${alumno.apellido}</td>
                        <td>${alumno.carrera}</td>
                        <td>${alumno.ciclo}</td>
                        <td>${alumno.fecha_nacimiento}</td>
                        <td class="text-center">
                            <button class="btn-edit" data-id="${alumno.id_alumno}">Editar</button>
                            <button class="btn-delete" data-id="${alumno.id_alumno}">Eliminar</button>
                        </td>
                    </tr>`;
            });
        });
    }

    // Abrir modal (crear)
    btnAgregar.onclick = () => {
        editId = null;
        form.reset();
        modal.classList.remove("hidden");
    };

    // Cerrar modal
    btnCerrarModal.onclick = () => modal.classList.add("hidden");

    // Clicks en la tabla (editar/eliminar)
    tabla.onclick = (e) => {
        if (e.target.classList.contains("btn-edit")) {
            const id = e.target.dataset.id;
            editId = id;
            GestionAPI.getAlumno(id).then(data => {
                document.getElementById("codigo_alumno").value = data.codigo_alumno;
                document.getElementById("nombre").value = data.nombre;
                document.getElementById("apellido").value = data.apellido;
                document.getElementById("carrera").value = data.carrera;
                document.getElementById("ciclo").value = data.ciclo;
                document.getElementById("fecha_nacimiento").value = data.fecha_nacimiento;
                modal.classList.remove("hidden");
            });
        }

        if (e.target.classList.contains("btn-delete")) {
            const id = e.target.dataset.id;
            if (confirm("¿Eliminar alumno?")) {
                GestionAPI.deleteAlumno(id).then(() => cargarAlumnos());
            }
        }
    };

    form.onsubmit = (e) => {
        e.preventDefault();
        const payload = {
            codigo_alumno: document.getElementById("codigo_alumno").value,
            nombre: document.getElementById("nombre").value,
            apellido: document.getElementById("apellido").value,
            carrera: document.getElementById("carrera").value,
            ciclo: document.getElementById("ciclo").value,
            fecha_nacimiento: document.getElementById("fecha_nacimiento").value
        };

        if (editId) {
            GestionAPI.updateAlumno(editId, payload).then(() => {
                modal.classList.add("hidden");
                cargarAlumnos();
            });
        } else {
            GestionAPI.createAlumno(payload).then(() => {
                modal.classList.add("hidden");
                cargarAlumnos();
            });
        }
    };

    cargarAlumnos();
});