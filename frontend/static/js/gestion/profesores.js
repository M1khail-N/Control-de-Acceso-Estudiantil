import { GestionAPI } from "../api.js";

document.addEventListener("DOMContentLoaded", () => {

    const tabla = document.getElementById("tabla-profesores");
    const modal = document.getElementById("modalProfesor");
    const btnAgregar = document.getElementById("btnAgregar");
    const btnCerrarModal = document.getElementById("btnCerrarModal");
    const form = document.getElementById("formProfesor");
    let editId = null;

    function cargarProfesores() {
        GestionAPI.getProfesores().then(data => {
            tabla.innerHTML = "";
            data.forEach(p => {
                tabla.innerHTML += `
                    <tr>
                        <td>${p.nombre}</td>
                        <td>${p.apellido}</td>
                        <td class="text-center">
                            <button class="btn-edit" data-id="${p.id_profesor}">Editar</button>
                            <button class="btn-delete" data-id="${p.id_profesor}">Eliminar</button>
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

            GestionAPI.getProfesor(id).then(data => {
                document.getElementById("nombre").value = data.nombre;
                document.getElementById("apellido").value = data.apellido;
                modal.classList.remove("hidden");
            });
        }

        if (e.target.classList.contains("btn-delete")) {
            const id = e.target.dataset.id;
            if (confirm("¿Eliminar profesor?")) {
                GestionAPI.deleteProfesor(id).then(() => cargarProfesores());
            }
        }
    };

    // Submit formulario
    form.onsubmit = (e) => {
        e.preventDefault();

        const payload = {
            nombre: document.getElementById("nombre").value,
            apellido: document.getElementById("apellido").value
        };

        if (editId) {
            GestionAPI.updateProfesor(editId, payload).then(() => {
                modal.classList.add("hidden");
                cargarProfesores();
            });
        } else {
            GestionAPI.createProfesor(payload).then(() => {
                modal.classList.add("hidden");
                cargarProfesores();
            });
        }
    };

    // Inicial
    cargarProfesores();
});