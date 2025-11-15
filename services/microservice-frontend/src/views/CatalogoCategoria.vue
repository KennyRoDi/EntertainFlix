<template>
  <div class="page font-sans min-h-screen">
    <Navbar />
    <section class="px-4 py-12 max-w-7xl mx-auto">
      <h2 class="text-3xl font-bold mb-8 strong-text text-center">
        Servicios en la categoría: {{ categoriaSeleccionada }}
      </h2>
      
      <div v-if="loading" class="text-center muted text-lg py-10">
        <p>Cargando servicios...</p>
      </div>

      <div v-else-if="error" class="text-center text-red-500 text-lg py-10">
        <p>Ocurrió un error al cargar los servicios:</p>
        <p class="mt-2 text-sm">{{ error }}</p>
      </div>

      <div v-else>
        <div v-if="serviciosFiltrados.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          <ServiceCard
            v-for="serv in serviciosFiltrados"
            :key="serv.id"
            :servicio="serv"
          />
        </div>
        <div v-else class="text-center muted text-lg py-10">
          <p>No se encontraron servicios en la categoría {{ categoriaSeleccionada }}.</p>
          <p class="mt-2">Intenta explorar otras categorías.</p>
        </div>
      </div>
    </section>
    <Footer />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import ServiceCard from '@/components/ServiceCard.vue';
import { useServices } from '@/composables/useServices.js';

// Llama al composable para obtener los datos y funciones
const { services, loading, error, loadAll } = useServices();

const route = useRoute();
const categoriaSeleccionada = route.params.nombre;

// El 'computed' ahora filtra sobre 'services.value' que viene de la API
const serviciosFiltrados = computed(() => {
  return services.value ? services.value.filter(s => s.categoria === categoriaSeleccionada) : [];
});

// Llama a loadAll() cuando el componente se monta para obtener los datos
onMounted(() => {
  loadAll();
});
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