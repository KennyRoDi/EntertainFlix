const API_BASE_URL = "https://entertainflix.azure-api.net/agendarsolicitudes/api";

export async function fetchSolicitudes() {
    try {
        const response = await fetch(`${API_BASE_URL}/solicitudes`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("Fetched solicitudes:", data); // Debug
        return data;
    } catch (error) {
        console.error("Error fetching solicitudes:", error);
        throw error;
    }
}

export async function fetchSolicitudesByServicio(servicio) {
    try {
        const allSolicitudes = await fetchSolicitudes();
        return allSolicitudes.filter(
            (sol) => (sol.artista || sol.servicio || "").toLowerCase() === servicio.toLowerCase()
        );
    } catch (error) {
        console.error("Error fetching solicitudes by servicio:", error);
        throw error;
    }
}