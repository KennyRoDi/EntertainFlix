<template>
  <div class="page font-sans min-h-screen flex flex-col">
    <Navbar />
    <main class="flex-grow flex items-center justify-center px-4 py-16">
      <form
        @submit.prevent="registrarUsuario"
        class="form-card shadow rounded p-6 space-y-4 w-full max-w-md"
      >
        <h2 class="text-2xl font-bold text-center mb-4">Crear una Cuenta</h2>

        <!-- Role Selection -->
        <div>
          <label class="label block text-sm font-semibold mb-3">
            ¿Qué tipo de cuenta deseas crear?
          </label>
          <div class="space-y-2">
            <label class="flex items-center cursor-pointer">
              <input
                v-model="rol"
                type="radio"
                value="contratista"
                class="mr-3"
              />
              <span class="font-medium">Contratista</span>
              <span class="text-xs text-gray-500 ml-2">(Busco servicios)</span>
            </label>
            <label class="flex items-center cursor-pointer">
              <input
                v-model="rol"
                type="radio"
                value="oferente"
                class="mr-3"
              />
              <span class="font-medium">Oferente</span>
              <span class="text-xs text-gray-500 ml-2">(Ofrezco servicios)</span>
            </label>
          </div>
        </div>

        <hr class="my-4 border-gray-300" />

        <!-- Common Fields -->
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
          <label class="label block text-sm font-semibold mb-1">
            Nombre de Usuario
          </label>
          <input
            v-model="usuario"
            type="text"
            placeholder="usuario123"
            class="input"
          />
        </div>

        <div>
          <label class="label block text-sm font-semibold mb-1">
            Correo Electrónico
          </label>
          <input
            v-model="correo"
            type="email"
            placeholder="correo@ejemplo.com"
            class="input"
          />
        </div>

        <!-- Oferente-Specific Fields -->
        <div v-if="rol === 'oferente'" class="space-y-4 p-4 bg-blue-50 rounded">
          <h3 class="font-semibold text-blue-900">Información del Oferente</h3>

          <div>
            <label class="label block text-sm font-semibold mb-1">
              Categoría de Servicio
            </label>
            <select v-model="oferente.categoria" class="input">
              <option disabled value="">Selecciona una categoría</option>
              <option value="Música">Música</option>
              <option value="Interpretación">Interpretación</option>
              <option value="Comedia">Comedia</option>
              <option value="Magia">Magia</option>
              <option value="Cultura">Cultura</option>
              <option value="Otro">Otro</option>
            </select>
          </div>

          <div>
            <label class="label block text-sm font-semibold mb-1">
              Descripción de tu Servicio
            </label>
            <textarea
              v-model="oferente.descripcion"
              placeholder="Describe brevemente qué servicio ofreces..."
              class="input"
              rows="3"
            ></textarea>
          </div>

          <div>
            <label class="label block text-sm font-semibold mb-1">
              Lema/Eslogan
            </label>
            <input
              v-model="oferente.eslogan"
              type="text"
              placeholder="Ej: Música de calidad para tus eventos"
              class="input"
            />
          </div>

          <div>
            <label class="label block text-sm font-semibold mb-1">
              Ubicación
            </label>
            <select v-model="oferente.ubicacion" class="input">
              <option disabled value="">Selecciona una provincia</option>
              <option value="San José">San José</option>
              <option value="Alajuela">Alajuela</option>
              <option value="Cartago">Cartago</option>
              <option value="Heredia">Heredia</option>
              <option value="Guanacaste">Guanacaste</option>
              <option value="Puntarenas">Puntarenas</option>
              <option value="Limón">Limón</option>
            </select>
          </div>

          <div>
            <label class="label block text-sm font-semibold mb-1">
              Teléfono de Contacto
            </label>
            <input
              v-model="oferente.telefono"
              type="tel"
              placeholder="8888-1234"
              class="input"
            />
          </div>

          <div>
            <label class="label block text-sm font-semibold mb-1">
              Rango de Precios (Mínimo)
            </label>
            <input
              v-model.number="oferente.precioMinimo"
              type="number"
              placeholder="1000"
              class="input"
            />
          </div>
        </div>

        <!-- Password Fields -->
        <div>
          <label class="label block text-sm font-semibold mb-1">
            Contraseña
          </label>
          <input
            v-model="contraseña"
            type="password"
            placeholder="********"
            class="input"
          />
        </div>

        <div>
          <label class="label block text-sm font-semibold mb-1">
            Confirmar Contraseña
          </label>
          <input
            v-model="confirmar"
            type="password"
            placeholder="********"
            class="input"
          />
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
          <router-link to="/inicio-sesion" class="link-cta">
            Inicia sesión
          </router-link>
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

const router = useRouter();
const { registerUser, loading, error } = useUsers();

// Common fields
const nombre = ref("");
const correo = ref("");
const usuario = ref("");
const contraseña = ref("");
const confirmar = ref("");
const rol = ref("contratista");

// Oferente-specific fields
const oferente = ref({
  categoria: "",
  descripcion: "",
  eslogan: "",
  ubicacion: "",
  telefono: "",
  precioMinimo: null
});

async function registrarUsuario() {
  error.value = "";

  // Validate common fields
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

  // Validate oferente fields if applicable
  if (rol.value === "oferente") {
    if (
      !oferente.value.categoria ||
      !oferente.value.descripcion ||
      !oferente.value.eslogan ||
      !oferente.value.ubicacion ||
      !oferente.value.telefono ||
      !oferente.value.precioMinimo
    ) {
      error.value = "Completa todos los campos del oferente.";
      return;
    }
  }

  if (contraseña.value !== confirmar.value) {
    error.value = "Las contraseñas no coinciden.";
    return;
  }

  const nuevoUsuario = {
    nombre: nombre.value,
    correo: correo.value,
    usuario: usuario.value,
    contraseña: contraseña.value,
    rol: rol.value,
    ...(rol.value === "oferente" && {
      categoria: oferente.value.categoria,
      descripcion: oferente.value.descripcion,
      eslogan: oferente.value.eslogan,
      ubicacion: oferente.value.ubicacion,
      telefono: oferente.value.telefono,
      precioMinimo: oferente.value.precioMinimo,
      imagen: "default.jpg", // Default, user can update later
      paquetes: [] // Empty initially, user adds later
    })
  };

  try {
    await registerUser(nuevoUsuario);
    alert("¡Registro completado con éxito!");
    router.push("/inicio-sesion");
  } catch (err) {
    console.error("Fallo en el registro:", err);
  }
}
</script>

<style scoped>
.page {
  background-color: var(--color-body-bg);
  color: var(--color-text);
  min-height: 100vh;
  transition: background-color 180ms ease, color 180ms ease;
}

.form-card {
  background-color: var(--color-background-light);
  color: var(--color-text);
  transition: background-color 180ms ease, color 180ms ease;
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
  border: 1px solid var(--color-background-light);
  transition: background-color 180ms ease, color 180ms ease,
    border-color 180ms ease, box-shadow 150ms ease;
}

.input:focus {
  outline: none;
  border-color: var(--color-primary-button-bg);
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.06);
}

textarea.input {
  resize: vertical;
}

.btn-primary {
  background-color: var(--color-primary-button-bg);
  color: var(--color-primary-button-text);
  border: 1px solid transparent;
  transition: background-color 150ms ease, opacity 120ms ease;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.link-cta {
  color: var(--color-primary-button-bg);
  font-weight: 600;
  text-decoration: none;
  margin-left: 0.25rem;
}

.link-cta:hover {
  text-decoration: underline;
}

.muted {
  color: var(--color-text-light);
}

.error {
  color: #ef4444;
}

h1,
h2,
h3,
h4,
label,
.font-semibold {
  color: var(--color-text);
}
</style>