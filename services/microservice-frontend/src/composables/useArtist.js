import { ref } from "vue";

// Manejo de perfiles de artistas desde la API
export function useProfiles() {
  const profiles = ref([]); // Lista de perfiles
  const loading = ref(false); // Estado de carga
  const error = ref(null); // Mensaje de error

  const API_URL = "https://entertainflix.azure-api.net/artist";

  async function loadAll() {
    loading.value = true;
    error.value = null;

    try {
      const headers = { "Content-Type": "application/json" };
      const apiKey = import.meta.env.VITE_API_KEY;
      if (apiKey) headers["Ocp-Apim-Subscription-Key"] = apiKey;

      const res = await fetch(API_URL, { headers });
      if (!res.ok) {
        const text = await res.text().catch(() => "");
        throw new Error(`HTTP ${res.status} - ${text || res.statusText}`);
      }

      const data = await res.json();
      profiles.value = Array.isArray(data) ? data : data.data || [];
      return profiles.value;
    } catch (err) {
      console.error("Error cargando perfiles:", err);
      error.value = err.message || String(err);
      profiles.value = [];
      return [];
    } finally {
      loading.value = false;
    }
  }

  function getById(id) {
    return profiles.value.find((p) => String(p.id) === String(id)) || null;
  }

  return { profiles, loading, error, loadAll, getById };
}
