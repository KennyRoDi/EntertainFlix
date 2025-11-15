import { ref } from "vue";

// Manejo de usuarios desde la API
export function useUsers() {
  const users = ref([]); // Lista de usuarios
  const loading = ref(false); // Estado de carga
  const error = ref(null); // Mensaje de error

  const API_URL_GET = "https://entertainflix.azure-api.net/users";
  const API_URL_POST = "https://entertainflix.azure-api.net/puser";

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
      users.value = Array.isArray(data) ? data : data.data || [];
      return users.value;
    } catch (err) {
      console.error("Error cargando usuarios:", err);
      error.value = err.message || String(err);
      users.value = [];
      return [];
    } finally {
      loading.value = false;
    }
  }

  async function registerUser(newUserData) {
    loading.value = true;
    error.value = null;

    try {
      await loadAll();
      const userExists = users.value.find(
        (u) => u.correo.toLowerCase() === newUserData.correo.toLowerCase()
      );
      if (userExists)
        throw new Error("El correo electrónico ya está registrado.");

      const res = await fetch(API_URL_POST, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Ocp-Apim-Subscription-Key": import.meta.env.VITE_API_KEY,
        },
        body: JSON.stringify(newUserData),
      });

      if (res.status !== 201 && res.status !== 200) {
        const errorBody = await res.text();
        throw new Error(
          `Error al registrar usuario: ${res.statusText} - ${errorBody}`
        );
      }

      const createdUserApi = await res.json();
      const newUser = { ...newUserData, id: createdUserApi.id };

      users.value.push(newUser);
      return newUser;
    } catch (err) {
      console.error("Error al registrar usuario:", err);
      error.value = err.message || String(err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  function getById(id) {
    return users.value.find((u) => String(u.id) === String(id)) || null;
  }

  return { users, loading, error, loadAll, getById, registerUser };
}
