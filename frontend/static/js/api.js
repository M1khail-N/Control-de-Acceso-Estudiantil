const API_BASE = "/api";

// Helper general para peticiones
async function apiRequest(url, method = "GET", data = null) {
    const options = {
        method: method,
        headers: { "Content-Type": "application/json" }
    };

    if (data) options.body = JSON.stringify(data);

    const response = await fetch(url, options);

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({
            detail: "Error desconocido"
        }));
        throw new Error(errorData.detail || "Error en la petición");
    }

    return response.json();
}

// GESTIÓN: API para CRUD de alumnos, máquinas, profesores, asignaturas
export const GestionAPI = {

    // Alumnos
    getAlumnos() {
        return apiRequest(`${API_BASE}/gestion/alumnos/`);
    },
    getAlumno(id) {
        return apiRequest(`${API_BASE}/gestion/alumnos/${id}/`);
    },
    createAlumno(data) {
        return apiRequest(`${API_BASE}/gestion/alumnos/`, "POST", data);
    },
    updateAlumno(id, data) {
        return apiRequest(`${API_BASE}/gestion/alumnos/${id}/`, "PUT", data);
    },
    deleteAlumno(id) {
        return apiRequest(`${API_BASE}/gestion/alumnos/${id}/`, "DELETE");
    },

    // Máquinas
    getMaquinas() {
        return apiRequest(`${API_BASE}/gestion/maquinas/`);
    },
    getMaquina(id) {
        return apiRequest(`${API_BASE}/gestion/maquinas/${id}/`);
    },
    createMaquina(data) {
        return apiRequest(`${API_BASE}/gestion/maquinas/`, "POST", data);
    },
    updateMaquina(id, data) {
        return apiRequest(`${API_BASE}/gestion/maquinas/${id}/`, "PUT", data);
    },
    deleteMaquina(id) {
        return apiRequest(`${API_BASE}/gestion/maquinas/${id}/`, "DELETE");
    },

    // Profesores
    getProfesores() {
        return apiRequest(`${API_BASE}/gestion/profesores/`);
    },
    getProfesor(id) {
        return apiRequest(`${API_BASE}/gestion/profesores/${id}/`);
    },
    createProfesor(data) {
        return apiRequest(`${API_BASE}/gestion/profesores/`, "POST", data);
    },
    updateProfesor(id, data) {
        return apiRequest(`${API_BASE}/gestion/profesores/${id}/`, "PUT", data);
    },
    deleteProfesor(id) {
        return apiRequest(`${API_BASE}/gestion/profesores/${id}/`, "DELETE");
    },

    // Asignaturas
    getAsignaturas() {
        return apiRequest(`${API_BASE}/gestion/asignaturas/`);
    },
    getAsignatura(id) {
        return apiRequest(`${API_BASE}/gestion/asignaturas/${id}/`);
    },
    createAsignatura(data) {
        return apiRequest(`${API_BASE}/gestion/asignaturas/`, "POST", data);
    },
    updateAsignatura(id, data) {
        return apiRequest(`${API_BASE}/gestion/asignaturas/${id}/`, "PUT", data);
    },
    deleteAsignatura(id) {
        return apiRequest(`${API_BASE}/gestion/asignaturas/${id}/`, "DELETE");
    },

    // Profesor asignado a una asignatura
    getProfesorDeAsignatura(id_asignatura) {
        return apiRequest(`${API_BASE}/gestion/asignaturas/${id_asignatura}/profesor/`);
    }
};

// REGISTRO BASE: Entradas y salidas
export const RegistroBaseAPI = {

    // Registrar entrada general (requiere: codigo_alumno + maquina)
    marcarEntrada(data) {
        return apiRequest(`${API_BASE}/acceso/registro-base/entrada/`, "POST", data);
    },

    // Registrar salida (solo requiere: codigo_alumno)
    marcarSalida(data) {
        return apiRequest(`${API_BASE}/acceso/registro-base/salida/`, "POST", data);
    },

    // Listar registros (por si acaso)
    getRegistros(params = "") {
        return apiRequest(`${API_BASE}/acceso/registro-base/${params}`);
    }
};

// REGISTRO LIBRE: Entrada
export const RegistroLibreAPI = {

    // Entrada libre (requiere: codigo_alumno, maquina, motivo)
    marcarEntrada(data) {
        return apiRequest(`${API_BASE}/acceso/registro-libre/entrada/`, "POST", data);
    }
};

// REGISTRO CLASE: Entrada
export const RegistroClaseAPI = {

    // Entrada clase (requiere: codigo_alumno, maquina, asignatura, profesor)
    marcarEntrada(data) {
        return apiRequest(`${API_BASE}/acceso/registro-clase/entrada/`, "POST", data);
    }
};

export { apiRequest };
