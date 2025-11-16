<template>
  <div class="page font-sans min-h-screen flex flex-col">
    <Navbar />
    <div v-if="isLoading" class="flex-grow flex justify-center items-center">
      <p class="text-lg muted">Cargando perfil...</p>
    </div>
    <div v-else-if="error" class="flex-grow flex justify-center items-center text-red-500">
      <p>Error al cargar los datos: {{ error }}</p>
    </div>
    <main v-else class="flex-grow">
      <div v-if="perfil">
        <div class="profile-header-container">
          <div class="banner h-56 w-full">
            <img :src="isDark
              ? '/assets/images/bannerPerfilD.png'
              : '/assets/images/bannerPerfilL.png'
              " alt="Banner de perfil" class="w-full h-full object-cover" />
          </div>
          <div class="profile-details max-w-4xl mx-auto px-4 relative -mt-24">
            <img :src="`/assets/images/${perfil.imagen}`" alt="Foto de perfil"
              class="w-48 h-48 object-coverimg rounded-full border-4 mx-auto profile-photo"
              style="border-color: var(--color-body-bg)" />
            <div class="profile-card p-6 rounded shadow text-center -mt-18">
              <h3 class="text-2xl font-bold strong-text">
                {{ perfil.usuario }}
              </h3>
              <hr class="dropdown-divider" />
              <p class="muted mt-2">{{ perfil.descripcion }}</p>
              <p class="meta-text text-sm mt-2">
                {{ perfil.categoria }} - {{ perfil.ubicacion }}
              </p>
            </div>
          </div>
        </div>

        <div class="max-w-6xl mx-auto mt-12 px-4">
          <nav class="menuPerfil flex space-x-8">
            <router-link :to="{ name: 'paquetesPerfil' }" class="py-4 px-1 text-lg">Paquetes</router-link>
            <router-link :to="{ name: 'resenasPerfil' }" class="py-4 px-1 text-lg">Reseñas</router-link>
            <router-link :to="{ name: 'solicitudesPerfil' }" class="py-4 px-1 text-lg">Solicitudes</router-link>
          </nav>
        </div>

        <div class="max-w-6xl mx-auto px-4 py-12">
          <router-view :servicio="servicioAsociadoAlPerfil" :reseñas="reseñasDelServicio"
            :solicitudes="solicitudesGestionadas" @crear="abrirModalParaCrear" @editar="abrirModalParaEditar"
            @eliminar="eliminarPaquete" @restaurar="restaurarDatos" @accept="aceptarSolicitud"
            @reject="rechazarSolicitud" />
        </div>
      </div>
      <div v-else class="text-center muted mt-10">
        No se encontró ningún perfil con ese nombre.
      </div>
      <!-- Add after </router-view> and before </main> -->
      <Transition name="notification">
        <div v-if="showNotification" :class="[
          'fixed bottom-4 right-4 px-6 py-4 rounded-lg text-white font-semibold shadow-lg',
          notificationType === 'success'
            ? 'bg-green-500'
            : 'bg-red-500'
        ]">
          {{ notificationMessage }}
        </div>
      </Transition>
    </main>

    <Footer />

    <PackageModal v-if="mostrarModal" :paquete="paqueteEditable" :is-editing="editandoIndex !== null"
      @close="cerrarModal" @save="guardarPaquete" />

    <!-- Add this after PackageModal -->
    <ConfirmDialog ref="confirmDialog" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";
import PackageModal from "@/components/PackageModal.vue";
import ConfirmDialog from "@/components/ConfirmDialog.vue";
import { useProfiles } from "@/composables/useArtist.js";
import { useServices } from "@/composables/useServices.js";
import comentariosData from "@/assets/json/comentarios.json";
import solicitudesData from "@/assets/json/solicitudes.json";
import { useTheme } from "@/composables/useTheme.js";

const API_BASE_URL = "http://localhost:8080";
const { isDark } = useTheme();
const route = useRoute();

const {
  profiles,
  loadAll: loadAllProfiles,
  loading: loadingProfiles,
  error: errorProfiles,
} = useProfiles();

const {
  services,
  loadAll: loadAllServices,
  loading: loadingServices,
  error: errorServices,
  addPackage,
  deletePackage,
} = useServices();

// State
const perfil = ref(null);
const comentarios = ref(comentariosData);
const todasLasSolicitudes = ref([]);
const showNotification = ref(false);
const notificationType = ref("success");
const notificationMessage = ref("");
const mostrarModal = ref(false);
const paqueteEditable = ref({ nombre: "", descripcion: "", precio: null });
const editandoIndex = ref(null);
const confirmDialog = ref(null);

// Computed
const isLoading = computed(
  () => loadingProfiles.value || loadingServices.value
);

const error = computed(() => errorProfiles.value || errorServices.value);

const servicioAsociadoAlPerfil = computed(() => {
  if (!perfil.value || !services.value || !perfil.value.usuario) return null;
  const perfilUsuarioLower = perfil.value.usuario.toLowerCase();
  return (
    services.value.find((s) => {
      const serviceTitle = (s?.titulo || "").toLowerCase();
      return serviceTitle === perfilUsuarioLower;
    }) || null
  );
});

const reseñasDelServicio = computed(() => {
  if (!servicioAsociadoAlPerfil.value) return [];
  const servicioTituloLower = (
    servicioAsociadoAlPerfil.value?.titulo || ""
  ).toLowerCase();
  return comentarios.value.filter(
    (c) => (c?.servicio || "").toLowerCase() === servicioTituloLower
  );
});

const solicitudesGestionadas = computed(() => {
  if (!servicioAsociadoAlPerfil.value) return [];
  const servicioTituloLower = (
    servicioAsociadoAlPerfil.value?.titulo || ""
  ).toLowerCase();
  return todasLasSolicitudes.value
    .filter(
      (sol) => (sol?.servicio || "").toLowerCase() === servicioTituloLower
    )
    .sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
});

// Methods
function displayNotification(message, type = "success", duration = 3000) {
  notificationMessage.value = message;
  notificationType.value = type;
  showNotification.value = true;
  setTimeout(() => {
    showNotification.value = false;
  }, duration);
}

function actualizarEstadoSolicitud(solicitudId, nuevoEstado) {
  const solicitudIndex = todasLasSolicitudes.value.findIndex(
    (s) => s.id === solicitudId
  );
  if (solicitudIndex !== -1) {
    todasLasSolicitudes.value[solicitudIndex].estado = nuevoEstado;
  }
}

async function callMicroservice(solicitud, decision) {
  try {
    const payload = {
      requestId: solicitud.id.toString(),
      cliente: solicitud.cliente,
      correo: solicitud.correo,
      telefono: solicitud.telefono,
      mensaje: solicitud.mensaje,
      ubicacion: solicitud.ubicacion,
      servicio: solicitud.servicio,
      paquete: solicitud.paquete,
      ofertante: perfil.value?.usuario || "unknown",
      decision: decision,
      razon:
        decision === "ACCEPTED"
          ? "Solicitud aprobada"
          : "Solicitud rechazada"
    };

    const response = await fetch(
      `${API_BASE_URL}/requests/${solicitud.id}/decision`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error calling microservice:", error);
    throw error;
  }
}

async function aceptarSolicitud(solicitudId) {
  const solicitud = todasLasSolicitudes.value.find((s) => s.id === solicitudId);
  if (!solicitud) return;

  const confirmed = await confirmDialog.value.show({
    title: "Aceptar solicitud",
    message: `¿Deseas aceptar la solicitud de ${solicitud.cliente}?`,
    confirmText: "Aceptar",
    type: "success"
  });

  if (!confirmed) return;

  try {
    await callMicroservice(solicitud, "ACCEPTED");
    actualizarEstadoSolicitud(solicitudId, "aceptada");

    displayNotification(
      `La solicitud de ${solicitud.cliente} ha sido aceptada`,
      "success",
      3000
    );

    setTimeout(() => {
      const asunto = `¡Su solicitud ha sido aceptada! - ${solicitud.paquete}`;
      const cuerpo = `Hola ${solicitud.cliente},\n\n¡Nos complace informarle que su solicitud para el paquete "${solicitud.paquete}" ha sido ACEPTADA!...\n\nSaludos cordiales,\n${
        perfil.value?.usuario || "El equipo"
      }`;
      const mailtoLink = `mailto:${solicitud.correo}?subject=${encodeURIComponent(
        asunto
      )}&body=${encodeURIComponent(cuerpo)}`;
      window.location.href = mailtoLink;
    }, 3000);
  } catch (error) {
    displayNotification(`Error: ${error.message}`, "error", 3000);
  }
}

async function rechazarSolicitud(solicitudId) {
  const solicitud = todasLasSolicitudes.value.find((s) => s.id === solicitudId);
  if (!solicitud) return;

  const confirmed = await confirmDialog.value.show({
    title: "Rechazar solicitud",
    message: `¿Deseas rechazar la solicitud de ${solicitud.cliente}?`,
    confirmText: "Rechazar",
    type: "danger"
  });

  if (!confirmed) return;

  try {
    await callMicroservice(solicitud, "REJECTED");
    actualizarEstadoSolicitud(solicitudId, "rechazada");

    displayNotification(
      `La solicitud de ${solicitud.cliente} ha sido cancelada`,
      "error",
      3000
    );

    setTimeout(() => {
      const asunto = `Información sobre su solicitud - ${solicitud.paquete}`;
      const cuerpo = `Hola ${solicitud.cliente},\n\nLamentamos informarle que no podremos aceptar su solicitud...\n\nSaludos cordiales,\n${
        perfil.value?.usuario || "El equipo"
      }`;
      const mailtoLink = `mailto:${solicitud.correo}?subject=${encodeURIComponent(
        asunto
      )}&body=${encodeURIComponent(cuerpo)}`;
      window.location.href = mailtoLink;
    }, 3000);
  } catch (error) {
    displayNotification(`Error: ${error.message}`, "error", 3000);
  }
}

function restaurarDatos() {
  if (
    confirm(
      "¿Estás seguro de que quieres restaurar todas las solicitudes a su estado inicial?"
    )
  ) {
    const initialSolicitudes = solicitudesData.map((sol) => ({
      ...sol,
      estado: "pendiente",
      id: sol.id || Date.now() + Math.random().toString(36).substr(2, 9)
    }));
    todasLasSolicitudes.value = initialSolicitudes;
    alert("Las solicitudes han sido restauradas exitosamente.");
  }
}

function abrirModalParaCrear() {
  editandoIndex.value = null;
  paqueteEditable.value = {
    nombre: "",
    descripcion: "",
    precio: 0,
    video_youtube: ""
  };
  mostrarModal.value = true;
}

function abrirModalParaEditar(index) {
  editandoIndex.value = index;
  paqueteEditable.value = {
    ...servicioAsociadoAlPerfil.value.paquetes[index]
  };
  mostrarModal.value = true;
}

function cerrarModal() {
  mostrarModal.value = false;
}

async function guardarPaquete(paqueteActualizado) {
  if (editandoIndex.value === null) {
    if (!servicioAsociadoAlPerfil.value) {
      alert("Error: No se puede añadir un paquete sin un servicio asociado.");
      return;
    }
    const serviceId = servicioAsociadoAlPerfil.value.id;
    try {
      await addPackage(serviceId, paqueteActualizado);
      cerrarModal();
    } catch (err) {
      alert(`Error al guardar el paquete: ${err.message}`);
    }
  } else {
    const indiceServicioActual = services.value.findIndex(
      (s) => s.id === servicioAsociadoAlPerfil.value.id
    );
    if (indiceServicioActual !== -1) {
      services.value[indiceServicioActual].paquetes[editandoIndex.value] =
        paqueteActualizado;
      cerrarModal();
    }
  }
}

async function eliminarPaquete(index) {
  if (confirm("¿Estás seguro de que quieres eliminar este paquete?")) {
    if (!servicioAsociadoAlPerfil.value) {
      alert("Error: No se ha encontrado el servicio asociado.");
      return;
    }
    const serviceId = servicioAsociadoAlPerfil.value.id;
    try {
      await deletePackage(serviceId, index);
      alert("Paquete eliminado exitosamente.");
    } catch (err) {
      alert(`Error al eliminar el paquete: ${err.message}`);
    }
  }
}

watch(
  () => route.params.usuario,
  async (newUsuario) => {
    if (newUsuario) {
      await Promise.all([loadAllProfiles(), loadAllServices()]);
      const nombre = newUsuario.trim().toLowerCase();
      perfil.value =
        profiles.value.find((p) => p.usuario.toLowerCase() === nombre) || null;
    }
  },
  { immediate: true }
);

onMounted(() => {
  todasLasSolicitudes.value = solicitudesData.map((sol) => ({
    ...sol,
    estado: "pendiente",
    id: sol.id || Date.now() + Math.random().toString(36).substr(2, 9)
  }));
});
</script>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: all 300ms ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.router-link-exact-active {
  border-bottom: 3px solid var(--color-primary-button-bg);
  color: var(--color-text);
  font-weight: 600;
}

nav a {
  color: var(--color-text-light);
  border-bottom: 3px solid transparent;
  transition: all 150ms ease-in-out;
}

.page {
  background-color: var(--color-body-bg);
  color: var(--color-text);
  min-height: 100vh;
  transition: background-color 180ms ease, color 180ms ease;
}

.menuPerfil {
  justify-content: center;
  align-items: center;
  gap: 12%;
}

.profile-details {
  position: relative;
  flex-direction: column;
  display: flex;
  align-items: center;
}

.dropdown-divider {
  border: none;
  border-top: 1px solid var(--color-primary-button-bg);
  margin: 0.5rem 0;
}

/* Perfil header card */
.profile-card {
  padding-top: 11%;
  position: inherit;
  z-index: 0;
  width: 90%;
  background-color: var(--color-background-light);
  color: var(--color-text);
  border-radius: 0.5rem;
  transition: background-color 180ms ease, color 180ms ease;
  box-shadow: 0 3px 20px var(--color-eslogan-hover);
}

.card {
  background-color: var(--color-background-light);
  color: var(--color-text);
  border: 1px solid transparent;
  transition: background-color 180ms ease, color 180ms ease,
    transform 180ms ease;
}

.strong-text {
  color: var(--color-text);
}

.muted {
  color: var(--color-text-light);
}

.meta-text {
  color: var(--color-text-light);
}

.link {
  color: var(--color-primary-button-bg);
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.btn-accept,
.btn-reject,
.btn-plain {
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: transform 120ms ease, filter 120ms ease;
}

.btn-accept {
  background-color: #16a34a;
  color: #ffffff;
}

.btn-accept:hover {
  background-color: #15803d;
  transform: translateY(-1px);
}

.btn-reject {
  background-color: #dc2626;
  color: #ffffff;
}

.btn-reject:hover {
  background-color: #b91c1c;
  transform: translateY(-1px);
}

.btn-plain {
  background-color: var(--color-background-light);
  color: var(--color-text);
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.btn-plain:hover {
  filter: brightness(0.98);
}

.empty-card {
  background-color: var(--color-background-light);
  color: var(--color-text-light);
}

/* Ajustes de imagen y objeto-cover */
img.object-coverimg {
  position: relative;
  z-index: 2;
  height: 240px;
  width: 240px;
}

img.object-cover {
  object-fit: cover;
  height: 150%;
}

.transition-shadow {
  transition: box-shadow 160ms ease, transform 160ms ease;
}

.btn-edit {
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  font-weight: 600;
  cursor: pointer;
  background-color: var(--color-primary-button-bg);
  color: var(--color-primary-button-text);
  transition: all 120ms ease;
}

.btn-edit:hover {
  background-color: var(--color-primary-button-text);
  color: var(--color-primary-button-bg);
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .menuPerfil {
    justify-content: center;
    align-items: center;
    gap: 5%;
  }

  img.object-coverimg {
    position: relative;
    z-index: 2;
    height: 200px;
    width: 200px;
  }

  .profile-card {
    padding-top: 21%;
    position: inherit;
    z-index: 0;
    width: 90%;
    background-color: var(--color-background-light);
    color: var(--color-text);
    border-radius: 0.5rem;
    transition: background-color 180ms ease, color 180ms ease;
    box-shadow: 0 3px 20px var(--color-eslogan-hover);
  }
}
</style>
