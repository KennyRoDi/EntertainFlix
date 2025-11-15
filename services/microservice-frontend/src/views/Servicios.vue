<template>
  <div class="page font-sans min-h-screen">
    <Navbar />
    <section class="px-4 py-12 max-w-7xl mx-auto">
      <h2 class="text-3xl font-bold mb-8 strong-text">Catálogo</h2>

      <div v-if="isLoading" class="text-center muted text-lg py-10">
        <p>Cargando catálogo...</p>
      </div>
      <div v-else-if="error" class="text-center text-red-500 text-lg py-10">
        <p>Ocurrió un error al cargar los datos: {{ error }}</p>
      </div>

      <div v-else>
        <div class="flex flex-col md:flex-row items-center gap-4 mb-8">
          <button @click="toggleSearch" class="btn-plain p-2 rounded">
            <span>Buscar</span>
          </button>
          <button @click="toggleFilters" class="btn-plain p-2 rounded">
            <span>Filtros</span>
          </button>
          <div v-if="showSearch" class="w-full md:w-1/3">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar por título..."
              class="w-full input-field px-4 py-2 mt-2 md:mt-0 rounded"
            />
          </div>
        </div>

        <div v-if="showFilters" class="mb-8 space-y-4 p-4 panel rounded-lg">
          <div>
            <h3 class="font-semibold mb-2 text-lg strong-text">Filtrar por Categoría</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="cat in categories"
                :key="cat.nombre"
                @click="filtroCategoria = filtroCategoria === cat.nombre ? '' : cat.nombre"
                class="chip px-4 py-2 rounded-full text-sm cursor-pointer transition"
                :class="{ 'chip-active': filtroCategoria === cat.nombre }"
              >
                {{ cat.nombre }}
              </span>
            </div>
          </div>
          <div>
            <h3 class="font-semibold mb-2 text-lg strong-text">Precio Máximo</h3>
            <input
              v-model="precioMax"
              type="range"
              min="0"
              max="10000"
              step="100"
              class="w-full range-input"
            />
            <p class="text-sm muted">Hasta <span class="font-bold strong-text">${{ precioMax }}</span></p>
          </div>
          <div>
            <h3 class="font-semibold mb-2 text-lg strong-text">Filtrar por Ubicación</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="ubi in ubicacionesDisponibles"
                :key="ubi"
                @click="filtroUbicacion = filtroUbicacion === ubi ? '' : ubi"
                class="chip px-4 py-2 rounded-full text-sm cursor-pointer transition"
                :class="{'chip-active': filtroUbicacion === ubi }"
              >
                {{ ubi }}
              </span>
            </div>
          </div>
        </div>

        <div v-if="serviciosFiltrados.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          <ServiceCard
            v-for="serv in serviciosFiltrados"
            :key="serv.id"
            :servicio="serv"
          />
        </div>
        <div v-else class="text-center muted text-lg py-10">
          <p>No se encontraron servicios que coincidan con los criterios de búsqueda y filtros.</p>
          <p class="mt-2">Intenta ajustar tus selecciones.</p>
        </div>
      </div>
    </section>
    <Footer />
  </div>
</template>

<script setup>
// Importamos funciones y componentes necesarios de Vue y del proyecto
import { ref, computed, onMounted } from 'vue';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import ServiceCard from '@/components/ServiceCard.vue';
import { useServices } from '@/composables/useServices.js';
import { useCategories } from '@/composables/useCategories.js';

// Obtenemos servicios y categorías desde los composables
const { services, loadAll: loadAllServices, loading: loadingServices, error: errorServices } = useServices();
const { categories, loadAll: loadAllCategories, loading: loadingCategories, error: errorCategories } = useCategories();

// Estados locales para mostrar/ocultar filtros y búsqueda
const showFilters = ref(false);
const showSearch = ref(false);

// Variables reactivas para filtros y búsqueda
const searchQuery = ref('');
const filtroCategoria = ref('');
const filtroUbicacion = ref('');
const precioMax = ref(10000); // Límite máximo de precio por defecto

// Estado global de carga y error combinando servicios y categorías
const isLoading = computed(() => loadingServices.value || loadingCategories.value);
const error = computed(() => errorServices.value || errorCategories.value);

// Computed para obtener todas las ubicaciones disponibles desde los servicios
const ubicacionesDisponibles = computed(() => {
  if (!services.value) return [];
  const locations = new Set(services.value.map(s => s.ubicacion));
  return Array.from(locations).sort();
});

// Computed que devuelve la lista de servicios filtrados según los criterios
const serviciosFiltrados = computed(() => {
  if (!services.value) return [];
  return services.value.filter(s => {
    // Normalizamos strings para búsqueda
    const tituloLower = s.titulo ? s.titulo.toLowerCase() : '';
    const ubicacionLower = s.ubicacion ? s.ubicacion.toLowerCase() : '';

    // Condiciones de filtrado
    const coincideBusqueda = tituloLower.includes(searchQuery.value.toLowerCase());
    const coincideCategoria = filtroCategoria.value ? s.categoria === filtroCategoria.value : true;
    const coincideUbicacion = filtroUbicacion.value ? ubicacionLower === filtroUbicacion.value.toLowerCase() : true;
    const coincidePrecio = s.paquetes && Array.isArray(s.paquetes) 
      ? s.paquetes.some(p => p.precio <= precioMax.value) 
      : true;

    // Retorna solo los servicios que cumplen con todos los filtros
    return coincideBusqueda && coincideCategoria && coincideUbicacion && coincidePrecio;
  });
});

// Funciones para alternar visibilidad de filtros y búsqueda
function toggleFilters() {
  showFilters.value = !showFilters.value;
}

function toggleSearch() {
  showSearch.value = !showSearch.value;
}

// Al montar el componente cargamos servicios y categorías
onMounted(() => {
  loadAllServices();
  loadAllCategories();
});
</script>


<style scoped>
.page {
  background-color: var(--color-body-bg);
  color: var(--color-text);
  min-height: 100vh;
  transition: background-color 180ms ease, color 180ms ease;
}

.strong-text {
  color: var(--color-text);
}

.muted {
  color: var(--color-text-light);
  transition: color 180ms ease;
}

.panel {
  background-color: var(--color-background-light);
  border: 1px solid transparent;
  color: var(--color-text);
  transition: background-color 180ms ease, color 180ms ease;
}

.btn-plain {
  background-color: var(--color-background-light);
  color: var(--color-text);
  border: 1px solid rgba(0,0,0,0.06);
  transition: filter 120ms ease, transform 120ms ease;
}

.btn-plain:hover {
  filter: brightness(0.98);
  transform: translateY(-1px);
}

.chip {
  background-color: var(--color-background-light);
  color: var(--color-text);
}

.chip-active {
  background-color: var(--color-primary-button-bg);
  color: var(--color-primary-button-text);
}

.range-input {
  accent-color: var(--color-primary-button-bg);
}

.input-field {
  background-color: var(--color-body-bg);
  color: var(--color-text);
  border: 1px solid var(--color-background-light);
  outline: none;
}

.input-field:focus {
  box-shadow: 0 0 0 3px var(--color-primary-button-bg);
}
</style>