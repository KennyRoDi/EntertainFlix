<template>
  <div class="relative pt-6">
    <button @click="emit('close')" class="modal-close-btn">×</button>

    <section
      class="px-4 py-12 max-w-6xl mx-auto grid md:grid-cols-2 gap-8 items-start pt-0"
    >
      <div>
        <h2 class="text-3xl font-bold mb-4">Requisitos</h2>
        <p class="muted mb-4">
          Se debe cumplir con la mayoría de estos para poder dar el servicio,
          caso de no cumplir con alguno, indicarlo en la sección de comentarios.
        </p>
        <ul class="list-disc list-inside">
          <li v-for="(req, i) in props.servicio.requisitos" :key="i">
            {{ req }}
          </li>
        </ul>
      </div>
      <img
        :src="`/assets/images/${props.servicio.imagenes[1]}`"
        alt="Imagen presentación"
        class="rounded-md"
      />
    </section>

    <section class="px-4 py-12 max-w-4xl mx-auto">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">Envía tu solicitud</h2>
      </div>

      <form @submit.prevent="enviarSolicitud" class="space-y-6">
        <div>
          <input
            v-model="nombre"
            type="text"
            placeholder="Nombre completo"
            class="input"
          />
        </div>

        <input
          v-model="correo"
          type="email"
          placeholder="Correo electrónico"
          class="input"
        />

        <input
          v-model="telefono"
          type="tel"
          placeholder="Número telefónico"
          class="input"
          pattern="[0-9]{8}"
          title="Por favor, ingresa un número de teléfono válido de 8 dígitos."
        />

        <input
          v-model="fechaEvento"
          type="date"
          placeholder="Fecha"
          class="input"
        />

        <select v-model="ubicacionSeleccionada" class="input">
          <option value="" disabled>Selecciona una provincia</option>
          <option
            v-for="provincia in provinciasCR"
            :key="provincia"
            :value="provincia"
          >
            {{ provincia }}
          </option>
        </select>

        <div class="flex flex-wrap gap-2">
          <span
            v-for="(paq, i) in props.servicio.paquetes"
            :key="i"
            @click="paqueteSeleccionado = paq.nombre"
            class="paquete cursor-pointer"
            :class="{ 'paquete-activo': paqueteSeleccionado === paq.nombre }"
          >
            {{ paq.nombre }}
          </span>
        </div>

        <textarea
          v-model="comentarios"
          rows="4"
          class="input"
          placeholder="Comentarios"
        ></textarea>

        <Transition name="fade-error">
          <div v-if="errorMessage" class="error-message-box">
            {{ errorMessage }}
          </div>
        </Transition>
        <button type="submit" class="btn-primary px-6 py-2 rounded">
          Enviar
        </button>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref, watchEffect } from "vue";
import { useAuth } from "@/composables/useAuth.js";
import { useUsers } from "@/composables/useUser.js";

const props = defineProps({
  servicio: {
    type: Object,
    required: true,
  },
});
const emit = defineEmits(["close", "submitted"]);
const { usuario } = useAuth();
const { users, loadAll: loadAllUsers } = useUsers();

const nombre = ref("");
const correo = ref("");
const telefono = ref("");
const ubicacionSeleccionada = ref("");
const paqueteSeleccionado = ref("");
const comentarios = ref("");
const fechaEvento = ref("");

const errorMessage = ref(null);

/* (watchEffect de auto-rellenado no cambia) */
watchEffect(async () => {
  if (users.value.length === 0) {
    await loadAllUsers();
  }
  if (usuario.value) {
    const fullUserDetails = users.value.find((u) => u.id === usuario.value.id);
    if (fullUserDetails) {
      nombre.value = fullUserDetails.nombre;
      correo.value = fullUserDetails.correo;
      telefono.value = fullUserDetails.contacto
        ? fullUserDetails.contacto.toString()
        : "";
    } else {
      nombre.value = usuario.value.nombre;
      correo.value = usuario.value.correo;
    }
  }
});

/* (ProvinciasCR no cambia) */
const provinciasCR = [
  "Alajuela",
  "Cartago",
  "Guanacaste",
  "Heredia",
  "Limón",
  "Puntarenas",
  "San José",
];

async function enviarSolicitud() {
  errorMessage.value = null;
  if (
    !nombre.value ||
    !correo.value ||
    !fechaEvento.value ||
    !ubicacionSeleccionada.value ||
    !paqueteSeleccionado.value
  ) {
    errorMessage.value = "Por favor, completa todos los campos obligatorios.";
    return;
  }

  if (telefono.value && !/^\d{8}$/.test(telefono.value)) {
    errorMessage.value = "Por favor, ingresa un número de teléfono válido de 8 dígitos.";
    return;
  }

  const nuevaSolicitud = {
    cliente: nombre.value,
    correo: correo.value,
    telefono: telefono.value,
    mensaje: comentarios.value,
    fecha: fechaEvento.value,
    ubicacion: ubicacionSeleccionada.value,
    paquete: paqueteSeleccionado.value,
    artista: props.servicio.titulo,
  };

  try {
    const response = await fetch("https://entertainflix.azure-api.net/agendarsolicitudes/api/solicitudes", {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
        },
        body: JSON.stringify(nuevaSolicitud),
    });

    if (!response.ok) {
      throw new Error(`Error del servidor: ${response.statusText}`);
    }
    
    emit("submitted");

  } catch (error) {
    console.error("Error al enviar la solicitud:", error);
    errorMessage.value = "Hubo un error al enviar la solicitud. Intenta de nuevo más tarde.";
  }
}
</script>

<style scoped>
.muted {
  color: var(--color-text-light);
  transition: color 180ms ease;
}

.input {
  background-color: var(--color-background-light);
  color: var(--color-text);
  border: 1px solid var(--color-footer-text);
  border-radius: 0.375rem;
  padding: 0.5rem 1rem;
  width: 100%;
  transition: background-color 180ms ease, color 180ms ease,
    border-color 180ms ease;
}

.paquete {
  background-color: var(--color-background-light);
  color: var(--color-text);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 180ms ease, color 180ms ease;
}

.paquete-activo {
  background-color: var(--color-primary-button-bg);
  color: var(--color-primary-button-text);
}

.btn-primary {
  background-color: var(--color-primary-button-bg);
  color: var(--color-primary-button-text);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: background-color 180ms ease, color 180ms ease;
  text-decoration: none;
  cursor: pointer;
}
.btn-primary:hover {
  opacity: 0.9;
}

.btn-alt {
  background-color: var(--color-background-light);
  color: var(--color-text);
  border: 1px solid var(--color-footer-text);
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  transition: background-color 180ms ease, color 180ms ease;
  cursor: pointer;
}
.btn-alt:hover {
  opacity: 0.9;
}

h2 {
  color: var(--color-text);
}

.modal-close-btn {
  position: absolute;
  top: 1rem;
  right: 1.5rem;
  background: transparent;
  border: none;
  font-size: 2.25rem;
  color: var(--color-text-light);
  cursor: pointer;
  line-height: 1;
  padding: 0;
  z-index: 10;
  transition: color 150ms ease;
}
.modal-close-btn:hover {
  color: var(--color-text);
}

section:first-of-type {
  padding-top: 3rem;
}


.error-message-box {
  background-color: #4c1d1d; /* Fondo rojo oscuro */
  color: #fecaca; /* Texto rojo claro */
  border: 1px solid #7f1d1d; /* Borde rojo más oscuro */
  border-radius: 0.375rem; /* 6px */
  padding: 0.75rem 1rem; /* 12px 16px */
  font-size: 0.875rem; /* 14px */
  font-weight: 500;
  text-align: center;
}

/* Animación de Fade */
.fade-error-enter-active,
.fade-error-leave-active {
  transition: opacity 0.3s ease;
}

.fade-error-enter-from,
.fade-error-leave-to {
  opacity: 0;
}
</style>