<template>
  <div class="page font-sans min-h-screen flex flex-col">
    <Navbar />
    <main class="flex-grow flex items-center justify-center px-4 py-16">
      <form
        @submit.prevent="registrarUsuario"
        class="form-card shadow rounded p-6 space-y-4 w-full max-w-md"
      >
        <h2 class="text-2xl font-bold text-center mb-4">Crear una Cuenta</h2>
        <div>
          <label class="label block text-sm font-semibold mb-1">Nombre</label>
          <input
            v-model="nombre"
            type="text"
            placeholder="Tu nombre completo"
            class="input"
          />
        </div>

        <div>
          <label class="label block text-sm font-semibold mb-1"
            >Nombre de Usuario</label
          >
          <input
            v-model="usuario"
            type="text"
            placeholder="usuario123"
            class="input"
          />
        </div>
        <div>
          <label class="label block text-sm font-semibold mb-1"
            >Correo Electrónico</label
          >
          <input
            v-model="correo"
            type="email"
            placeholder="correo@ejemplo.com"
            class="input"
          />
        </div>
        <div>
          <label class="label block text-sm font-semibold mb-1"
            >Contraseña</label
          >
          <input
            v-model="contraseña"
            type="password"
            placeholder="********"
            class="input"
          />
        </div>
        <div>
          <label class="label block text-sm font-semibold mb-1"
            >Confirmar Contraseña</label
          >
          <input
            v-model="confirmar"
            type="password"
            placeholder="********"
            class="input"
          />
        </div>
        <div>
          <label class="label block text-sm font-semibold mb-1">Rol</label>
          <select v-model="rol" class="input">
            <option disabled value="">Selecciona un rol</option>
            <option value="contratista">Contratista</option>
            <option value="oferente">Oferente</option>
          </select>
        </div>
        <p v-if="error" class="error text-sm text-center">{{ error }}</p>
        <button
          type="submit"
          class="btn-primary w-full py-2 rounded"
          :disabled="loading"
        >
        {{ loading ? "Registrando..." : "Registrarse" }}
        </button>
        <div class="text-sm text-center muted mt-4">
          ¿Ya tienes cuenta?
          <router-link to="/inicio-sesion" class="link-cta"
            >Inicia sesión</router-link
          >
        </div>
      </form>
    </main>
    <Footer />
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";
import { useUsers } from "@/composables/useUser.js";

// --- Router para redirección tras registro ---
const router = useRouter();

// --- Composable de usuarios (maneja registro y estado) ---
const { registerUser, loading, error } = useUsers();

// --- Campos del formulario ---
const nombre = ref("");        // Nombre completo del usuario
const correo = ref("");        // Correo electrónico
const usuario = ref("");       // Nombre de usuario único
const contraseña = ref("");    // Contraseña
const confirmar = ref("");     // Confirmación de contraseña
const rol = ref("contratista") // Rol asignado por defecto

// --- Lógica de registro ---
async function registrarUsuario() {
  error.value = "";

  // Validación de campos obligatorios
  if (
    !nombre.value ||
    !correo.value ||
    !usuario.value ||
    !contraseña.value ||
    !confirmar.value ||
    !rol.value
  ) {
    error.value = "Todos los campos son obligatorios.";
    return;
  }

  // Validación de coincidencia de contraseñas
  if (contraseña.value !== confirmar.value) {
    error.value = "Las contraseñas no coinciden.";
    return;
  }

  // Creación del objeto de usuario nuevo
  const nuevoUsuario = {
    nombre: nombre.value,
    correo: correo.value,
    usuario: usuario.value,
    contraseña: contraseña.value,
    rol: rol.value,
  };

  // Registro en el sistema
  try {
    await registerUser(nuevoUsuario);
    alert("¡Registro completado con éxito!");
    router.push("/inicio-sesion"); // Redirige a login tras registro exitoso
  } catch (err) {
    console.error("Fallo en el registro desde el componente:", err);
  }
}
</script>

<style scoped>
.page {
  background-color: var(--color-body-bg);
  color: var(--color-text);
  min-height: 100vh;
  transition: background-color 180ms ease, color 180ms ease;
  display: block;
}

.form-card {
  background-color: var(--color-background-light);
  color: var(--color-text);
  transition: background-color 180ms ease, color 180ms ease,
    border-color 180ms ease;
}

.label {
  color: var(--color-text);
}

.input {
  background-color: var(--color-body-bg);
  color: var(--color-text);
  border-radius: 0.375rem;
  padding: 0.5rem 0.75rem;
  width: 100%;
  box-sizing: border-box;
  transition: background-color 180ms ease, color 180ms ease,
    border-color 180ms ease, box-shadow 150ms ease;
}

.input:focus {
  outline: none;
  border-color: var(--color-primary-button-bg);
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.06);
}

.btn-primary {
  background-color: var(--color-primary-button-bg);
  color: var(--color-primary-button-text);
  border: 1px solid transparent;
  transition: background-color 150ms ease, color 150ms ease, opacity 120ms ease;
  cursor: pointer;
  text-align: center;
}

.btn-primary:hover {
  opacity: 0.95;
}

.link-cta {
  color: var(--color-primary-button-bg);
  font-weight: 600;
  text-decoration: none;
  margin-left: 0.25rem;
}

.muted {
  color: var(--color-text-light);
}

.error {
  color: #ef4444;
}

h1,h2,h3,h4,label,
.font-semibold {
  color: var(--color-text);
}
</style>
