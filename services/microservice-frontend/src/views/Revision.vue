<template>
  <div class="page font-sans min-h-screen flex flex-col">
    <Navbar />

    <div v-if="loading" class="flex-grow flex justify-center items-center">
      <p class="text-lg muted">Cargando servicios por revisar...</p>
    </div>
    <div v-else-if="error" class="flex-grow flex justify-center items-center text-red-500">
      <p>Error al cargar los datos: {{ error }}</p>
    </div>

    <section v-else class="px-4 py-12 max-w-7xl mx-auto">
      <h2 class="text-3xl font-bold mb-8">Revisión de Servicios Pendientes</h2>
      
      <div class="mb-6 text-right">
        <button @click="restaurarServiciosRevision" class="restore-btn flex items-center gap-2 ml-auto px-4 py-2 rounded transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 icon" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.121a3 3 0 010 5.758V16a1 1 0 11-2 0v-6.121a3 3 0 010-5.758V3a1 1 0 011-1zm3 4a1 1 0 011 1v.707a3 3 0 014.586 0V7a1 1 0 112 0v.707a5 5 0 00-7.071 0V7a1 1 0 011-1z" clip-rule="evenodd" />
            <path fill-rule="evenodd" d="M13 10a1 1 0 011-1h.707a3 3 0 014.586 0V10a1 1 0 112 0v.707a5 5 0 00-7.071 0V10a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          Restaurar Pendientes
        </button>
      </div>

      <div v-if="serviciosPendientes.length === 0" class="text-center muted">
        No hay servicios pendientes por aprobar.
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        <div v-for="serv in serviciosPendientes" :key="serv.id" class="card-pending p-4 text-center rounded shadow">
          <img :src="`/assets/images/${serv.imagenes[0]}`" class="w-full h-48 img-cover rounded mb-2" />
          <h3 class="text-xl font-semibold">{{ serv.titulo }}</h3>
          <p class="text-sm muted mb-2">{{ serv.eslogan }}</p>
          <p class="text-xs muted mb-4">Solicitado por: {{ serv.solicitadoPor || 'N/A' }} ({{ serv.correoContacto || 'N/A' }})</p>

          <div class="flex justify-center gap-2 mt-4">
            <RouterLink :to="`/detalle-prevista/${serv.id}`" class="link-cta">Ver más</RouterLink>
            <button @click="aceptarServicio(serv)" class="accept-btn font-medium">Aceptar</button>
            <button @click="rechazarServicio(serv)" class="reject-btn font-medium">Rechazar</button>
          </div>
        </div>
      </div>

      <hr class="my-12 divider">

      <h2 class="text-3xl font-bold mb-8">Servicios Aprobados (En Memoria)</h2>
      <div v-if="serviciosAprobados.length === 0" class="text-center muted">
        No hay servicios aprobados aún.
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        <div v-for="serv in serviciosAprobados" :key="serv.id" class="card-approved p-4 text-center rounded shadow">
          <img :src="`/assets/images/${serv.imagenes[0]}`" class="w-full h-48 img-cover rounded mb-2" />
          <h3 class="text-xl font-semibold">{{ serv.titulo }}</h3>
          <p class="text-sm muted mb-2">{{ serv.eslogan }}</p>
          <p class="text-xs muted mb-4">Aprobado por: {{ serv.solicitadoPor || 'N/A' }}</p>
          <span class="badge-approved">Aprobado</span>
        </div>
      </div>

    </section>
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { useServices } from '@/composables/useServices.js';

const { services, loadAll, loading, error } = useServices();

const serviciosPendientes = ref([]);
const serviciosAprobados = ref([]);

function guardarServiciosPendientes(servs) {
    localStorage.setItem('serviciosPendientesRevision', JSON.stringify(servs));
}

function guardarServiciosAprobados(servs) {
    localStorage.setItem('approvedServices', JSON.stringify(servs));
}

async function inicializarServicios() {
    const storedPendientes = localStorage.getItem('serviciosPendientesRevision');
    if (storedPendientes) {
        serviciosPendientes.value = JSON.parse(storedPendientes);
    } else {
        await loadAll();
        serviciosPendientes.value = services.value.filter(serv => serv.estado === 'pendiente-revision');
        guardarServiciosPendientes(serviciosPendientes.value);
    }

    const storedAprobados = localStorage.getItem('approvedServices');
    if (storedAprobados) {
        serviciosAprobados.value = JSON.parse(storedAprobados);
    } else {
        serviciosAprobados.value = [];
    }
}

function aceptarServicio(servicio) {
    const servicioAceptado = { ...servicio, estado: 'aprobado' };
    serviciosAprobados.value.push(servicioAceptado);
    guardarServiciosAprobados(serviciosAprobados.value);
    serviciosPendientes.value = serviciosPendientes.value.filter(s => s.id !== servicio.id);
    guardarServiciosPendientes(serviciosPendientes.value);

    const asunto = `¡Su servicio "${servicio.titulo}" ha sido APROBADO!`;
    const cuerpo = `Hola ${servicio.solicitadoPor || 'estimado proveedor'},\n\n¡Nos complace informarle que su servicio "${servicio.titulo}" ha sido revisado y APROBADO por nuestro equipo!...\n\nSaludos cordiales,\nEl equipo de EntertainFlix`;
    const mailtoLink = `mailto:${servicio.correoContacto || ''}?subject=${encodeURIComponent(asunto)}&body=${encodeURIComponent(cuerpo)}`;
    window.location.href = mailtoLink;
    alert(`Servicio "${servicio.titulo}" aceptado y movido a servicios aprobados.`);
}

function rechazarServicio(servicio) {
    serviciosPendientes.value = serviciosPendientes.value.filter(s => s.id !== servicio.id);
    guardarServiciosPendientes(serviciosPendientes.value);

    const asunto = `Información sobre su servicio "${servicio.titulo}"`;
    const cuerpo = `Hola ${servicio.solicitadoPor || 'estimado proveedor'},\n\nLamentamos informarle que su servicio "${servicio.titulo}" no ha sido aprobado en esta ocasión...\n\nAgradecemos su interés y esperamos poder colaborar en el futuro.\n\nSaludos cordiales,\nEl equipo de EntertainFlix`;
    const mailtoLink = `mailto:${servicio.correoContacto || ''}?subject=${encodeURIComponent(asunto)}&body=${encodeURIComponent(cuerpo)}`;
    window.location.href = mailtoLink;
    alert(`Servicio "${servicio.titulo}" rechazado.`);
}

async function restaurarServiciosRevision() {
    if (confirm('¿Estás seguro de que quieres restaurar la lista de servicios pendientes?')) {
        localStorage.removeItem('serviciosPendientesRevision');
        localStorage.removeItem('approvedServices');
        await inicializarServicios();
        alert('Los servicios pendientes han sido restaurados desde la fuente original (API).');
    }
}

onMounted(async () => {
    await inicializarServicios();
});
</script>

<style scoped>
.page {
  background-color: var(--color-body-bg);
  color: var(--color-text);
  min-height: 100vh;
  transition: background-color 180ms ease, color 180ms ease;
}

.muted {
  color: var(--color-text-light);
  transition: color 180ms ease;
}

.restore-btn {
  background-color: var(--color-background-light);
  color: var(--color-text);
  border: 1px solid var(--color-footer-text);
}
.restore-btn:hover {
  opacity: 0.95;
}

.restore-btn .icon {
  color: currentColor;
}

.card-pending {
  background-color: var(--color-background-light);
  color: var(--color-text);
  border: 1px solid var(--color-footer-text);
  transition: background-color 180ms ease, color 180ms ease, border-color 180ms ease;
}

.card-approved {
  background-color: var(--color-body-bg);
  color: var(--color-text);
  border: 1px solid var(--color-footer-text);
  transition: background-color 180ms ease, color 180ms ease, border-color 180ms ease;
}

.img-cover {
  object-fit: cover;
}

.link-cta {
  color: var(--color-primary-button-bg);
  text-decoration: none;
  font-weight: 600;
}
.link-cta:hover {
  text-decoration: underline;
}

.accept-btn {
  color: #16a34a;
  background: transparent;
  border: none;
  cursor: pointer;
}
.reject-btn {
  color: #dc2626;
  background: transparent;
  border: none;
  cursor: pointer;
}

.badge-approved {
  display: inline-block;
  background-color: rgba(57, 194, 15, 0.849); 
  color: #ffffff;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
}

.divider {
  border: none;
  height: 1px;
  background-color: var(--color-footer-text);
  opacity: 0.12;
  margin: 3rem 0;
}

h2, h3 {
  color: var(--color-text);
}

button:focus, a:focus {
  outline: 3px solid rgba(0,0,0,0.06);
  outline-offset: 2px;
}
</style>
