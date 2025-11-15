import { ref } from "vue";

// Manejo de categorías desde la API
export function useCategories() {
  const categories = ref([]); // Lista de categorías
  const loading = ref(false); // Estado de carga
  const error = ref(null); // Error al cargar

  const API_URL = "https://entertainflix.azure-api.net/categories";

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
      categories.value = Array.isArray(data) ? data : data.data || [];
      return categories.value;
    } catch (err) {
      console.error("Error cargando categorías:", err);
      error.value = err.message || String(err);
      categories.value = [];
      return [];
    } finally {
      loading.value = false;
    }
  }

  function getById(id) {
    return categories.value.find((c) => String(c.id) === String(id)) || null;
  }

  return { categories, loading, error, loadAll, getById };
}
