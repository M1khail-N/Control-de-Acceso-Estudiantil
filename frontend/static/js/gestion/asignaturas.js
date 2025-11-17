import { GestionAPI } from "../api.js";

document.addEventListener("DOMContentLoaded", () => {
    const tabla = document.getElementById("tabla-asignaturas");
    const modal = document.getElementById("modalAsignatura");
    const btnAgregar = document.getElementById("btnAgregar");
    const btnCerrarModal = document.getElementById("btnCerrarModal");
    const form = document.getElementById("formAsignatura");
    const selectProfesor = document.getElementById("profesor");
    let editId = null;

    function cargarProfesores() {
        GestionAPI.getProfesores().then(data => {
            selectProfesor.innerHTML = "";
            data.forEach(p => {
                selectProfesor.innerHTML += `<option value="${p.id_profesor}">${p.nombre} ${p.apellido}</option>`;
            });
        });
    }

    function cargarAsignaturas() {
        GestionAPI.getAsignaturas().then(data => {
            tabla.innerHTML = "";
            data.forEach(a => {
                tabla.innerHTML += `
                    <tr>
                        <td>${a.nombre}</td>
                        <td>${a.nombre_profesor} ${a.apellido_profesor}</td>
                        <td class="text-center">
                            <button class="btn-edit" data-id="${a.id_asignatura}">Editar</button>
                            <button class="btn-delete" data-id="${a.id_asignatura}">Eliminar</button>
                        </td>
                    </tr>`;
            });
        });
    }

    btnAgregar.onclick = () => {
        editId = null;
        form.reset();
        cargarProfesores();
        modal.classList.remove("hidden");
    };

    btnCerrarModal.onclick = () => modal.classList.add("hidden");

    tabla.onclick = (e) => {
        if (e.target.classList.contains("btn-edit")) {
            const id = e.target.dataset.id;
            editId = id;
            cargarProfesores();

            GestionAPI.getAsignatura(id).then(data => {
                document.getElementById("nombre").value = data.nombre;
                selectProfesor.value = data.profesor;
                modal.classList.remove("hidden");
            });
        }

        if (e.target.classList.contains("btn-delete")) {
            const id = e.target.dataset.id;
            if (confirm("¿Eliminar asignatura?")) {
                GestionAPI.deleteAsignatura(id)
                    .then(() => cargarAsignaturas());
            }
        }
    };

    form.onsubmit = (e) => {
        e.preventDefault();
        const payload = {
            nombre: document.getElementById("nombre").value,
            profesor: selectProfesor.value
        };

        if (editId) {
            GestionAPI.updateAsignatura(editId, payload)
                .then(() => {
                    modal.classList.add("hidden");
                    cargarAsignaturas();
                });
        } else {
            GestionAPI.createAsignatura(payload)
                .then(() => {
                    modal.classList.add("hidden");
                    cargarAsignaturas();
                });
        }
    };

    cargarAsignaturas();
});