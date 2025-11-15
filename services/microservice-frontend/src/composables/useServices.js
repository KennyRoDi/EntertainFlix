import { ref } from "vue";

// Manejo de servicios desde la API
export function useServices() {
  const services = ref([]); // Lista de servicios
  const loading = ref(false); // Estado de carga
  const error = ref(null); // Mensaje de error

  const API_URL_GET = "https://entertainflix.azure-api.net/services";
  const API_URL_POST = "https://entertainflix.azure-api.net/pservice";
  const API_URL_DELETE = "https://entertainflix.azure-api.net";

  async function loadAll() {
    loading.value = true;
    error.value = null;
    try {
      const headers = { "Content-Type": "application/json" };
      const apiKey = import.meta.env.VITE_API_KEY;
      if (apiKey) headers["Ocp-Apim-Subscription-Key"] = apiKey;

      const res = await fetch(API_URL_GET, { headers });
      if (!res.ok) throw new Error(`HTTP ${res.status} - ${res.statusText}`);

      const data = await res.json();
      services.value = Array.isArray(data) ? data : data.data || [];
      return services.value;
    } catch (err) {
      console.error("Error cargando servicios:", err);
      error.value = err.message || String(err);
      services.value = [];
      return [];
    } finally {
      loading.value = false;
    }
  }

  async function addPackage(serviceId, newPackageData) {
    loading.value = true;
    error.value = null;
    try {
      const res = await fetch(API_URL_POST, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newPackageData),
      });
      if (res.status !== 201)
        throw new Error(`Error al crear el paquete: ${res.statusText}`);

      const serviceIndex = services.value.findIndex((s) => s.id === serviceId);
      if (serviceIndex === -1)
        throw new Error("Servicio no encontrado para añadir el paquete.");

      if (!services.value[serviceIndex].paquetes) {
        services.value[serviceIndex].paquetes = [];
      }
      services.value[serviceIndex].paquetes.push(newPackageData);

      return true;
    } catch (err) {
      console.error("Error al añadir paquete:", err);
      error.value = err.message || String(err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function deletePackage(serviceId, packageIndex) {
    loading.value = true;
    error.value = null;
    try {
      const res = await fetch(`${API_URL_DELETE}/${serviceId}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
      });
      if (res.status !== 204)
        throw new Error(`Error al eliminar paquete: ${res.statusText}`);

      const serviceIndex = services.value.findIndex((s) => s.id === serviceId);
      if (serviceIndex === -1)
        throw new Error("Servicio no encontrado para eliminar el paquete.");

      services.value[serviceIndex].paquetes.splice(packageIndex, 1);
      return true;
    } catch (err) {
      console.error("Error al eliminar paquete:", err);
      error.value = err.message || String(err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  function getById(id) {
    return services.value.find((s) => String(s.id) === String(id)) || null;
  }

  return {
    services,
    loading,
    error,
    loadAll,
    getById,
    addPackage,
    deletePackage,
  };
}
