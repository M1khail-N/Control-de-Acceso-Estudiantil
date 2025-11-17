import { GestionAPI } from "../api.js";

document.addEventListener("DOMContentLoaded", () => {
    
    const tabla = document.getElementById("tabla-maquinas");
    const modal = document.getElementById("modalMaquina");
    const btnAgregar = document.getElementById("btnAgregar");
    const btnCerrarModal = document.getElementById("btnCerrarModal");
    const form = document.getElementById("formMaquina");
    let editId = null;

    function cargarMaquinas() {
        GestionAPI.getMaquinas().then(data => {
            tabla.innerHTML = "";
            data.forEach(m => {
                tabla.innerHTML += `
                    <tr>
                        <td>${m.nombre}</td>
                        <td class="text-center">
                            <button class="btn-edit" data-id="${m.id_maquina}">Editar</button>
                            <button class="btn-delete" data-id="${m.id_maquina}">Eliminar</button>
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

            GestionAPI.getMaquina(id).then(data => {
                document.getElementById("nombre").value = data.nombre;
                modal.classList.remove("hidden");
            });
        }

        if (e.target.classList.contains("btn-delete")) {
            const id = e.target.dataset.id;
            if (confirm("¿Eliminar máquina?")) {
                GestionAPI.deleteMaquina(id).then(() => cargarMaquinas());
            }
        }
    };

    form.onsubmit = (e) => {
        e.preventDefault();
        const payload = {
            nombre: document.getElementById("nombre").value
        };

        if (editId) {
            GestionAPI.updateMaquina(editId, payload).then(() => {
                modal.classList.add("hidden");
                cargarMaquinas();
            });
        } else {
            GestionAPI.createMaquina(payload).then(() => {
                modal.classList.add("hidden");
                cargarMaquinas();
            });
        }
    };

    cargarMaquinas();
});