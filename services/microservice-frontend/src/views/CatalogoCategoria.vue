<template>
  <div class="page font-sans min-h-screen">
    <Navbar />
    <section class="px-4 py-12 max-w-7xl mx-auto">
      <h2 class="text-3xl font-bold mb-8 strong-text">
        Categoría: {{ categoriaActual || '—' }}
      </h2>

      <div v-if="loading" class="text-center muted text-lg py-10">
        Cargando servicios...
      </div>

      <div v-else-if="error" class="text-center text-red-500 text-lg py-10">
        <p>Ocurrió un error al cargar los servicios.</p>
        <p class="mt-2 text-sm">{{ error }}</p>
      </div>

      <div v-else>
        <div v-if="totalCatServ > 0">
          <!-- grilla -->
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
            <ServiceCard
              v-for="serv in serviciosPaginadosDeCategoria"
              :key="serv.id"
              :servicio="serv"
            />
          </div>

          <!-- mini resumen -->
          <p class="text-sm muted mt-4">
            Mostrando {{ serviciosPaginadosDeCategoria.length }} de {{ totalCatServ }} resultados
          </p>

          <!-- Controles de paginación (mismo HTML que Servicios) -->
          <div class="flex items-center gap-3 justify-center mt-6 select-none">
            <button
              class="btn-plain px-3 py-2 rounded border"
              @click="catServPage = Math.max(1, catServPage - 1)"
              :disabled="catServPage === 1"
            >
              Anterior
            </button>

            <span class="muted">
              Página {{ catServPage }} de {{ totalCatServPages }}
            </span>

            <button
              class="btn-plain px-3 py-2 rounded border"
              @click="catServPage = Math.min(totalCatServPages, catServPage + 1)"
              :disabled="catServPage >= totalCatServPages"
            >
              Siguiente
            </button>
          </div>
        </div>

        <!-- estado vacío -->
        <div v-else class="text-center muted text-lg py-10">
          No hay servicios en esta categoría.
        </div>
      </div>
    </section>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import ServiceCard from '@/components/ServiceCard.vue';
import { useServices } from '@/composables/useServices.js';

const route = useRoute();
const categoriaActual = computed(() => route.params.nombre)

const { services, loadAll, loading, error } = useServices()
onMounted(loadAll)

const PAGE_SIZE = 4
const catServPage = ref(1)

const serviciosDeCategoria = computed(() => {
  const arr = services.value || []
  return arr.filter(s => s.categoria === categoriaActual.value)
})

const totalCatServ = computed(() => serviciosDeCategoria.value.length)
const totalCatServPages = computed(() =>
  Math.max(1, Math.ceil(totalCatServ.value / PAGE_SIZE))
)

const serviciosPaginadosDeCategoria = computed(() => {
  const start = (catServPage.value - 1) * PAGE_SIZE
  return serviciosDeCategoria.value.slice(start, start + PAGE_SIZE)
})

watch([categoriaActual, services], () => { catServPage.value = 1 })
</script>

<style scoped>
.page {
  background-color: var(--color-body-bg);
  color: var(--color-text);
  min-height: 100vh;
}
.strong-text {
  color: var(--color-text);
}
.muted {
  color: var(--color-text-light);
}
</style>