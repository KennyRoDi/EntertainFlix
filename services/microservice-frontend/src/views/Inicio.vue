<template>
  <div class="page font-sans">
    <Banner />

    <section class="text-center px-4 py-12">
      <h2 class="text-3xl font-bold mb-4">Conecta con servicios de entretenimiento</h2>
      <p class="text-lg muted mb-6">
        Disfruta de la facilidad de comunicación con artistas y oferentes de entretenimiento como nunca antes se
        había visto
      </p>
      <RouterLink to="/categorias" class="btn-primary inline-block px-6 py-2 rounded mb-8">Ver Categorías</RouterLink>

      <div v-if="loadingCategories" class="text-center py-4">Cargando categorías...</div>
      <div v-else-if="errorCategories" class="text-center text-red-500 py-4">
        Error: {{ errorCategories }}
      </div>
      <div v-else-if="categories.length" class="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-5xl mx-auto">
        <CategoryCard
          v-for="cat in categories.slice(0, 3)"
          :key="cat.nombre"
          :categoria="cat"
        />
      </div>
      <div v-else class="text-center py-4">No se encontraron categorías.</div>
    </section>

    <section class="px-4 py-12">
      <div class="text-center mb-6">
        <RouterLink to="/servicios" class="btn-primary inline-block px-6 py-2 rounded mb-8">Ver Servicios</RouterLink>
      </div>
      <div v-if="loadingServices" class="text-center py-4">Cargando servicios...</div>
      <div v-else-if="errorServices" class="text-center text-red-500 py-4">
        Error: {{ errorServices }}
      </div>
      <div v-else-if="services.length" class="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-5xl mx-auto">
        <ServiceCard
          v-for="serv in services.slice(0, 3)"
          :key="serv.id"
          :servicio="serv"
        />
      </div>
       <div v-else class="text-center py-4">No se encontraron servicios.</div>
    </section>

    <section class="px-4 py-12">
      <div class="text-center mb-6">
        <RouterLink to="/servicios" class="btn-primary inline-block px-6 py-2 rounded mb-8">Destacados</RouterLink>
      </div>
       <div v-if="loadingServices" class="text-center py-4">Cargando destacados...</div>
      <div v-else-if="errorServices" class="text-center text-red-500 py-4">
        Error: {{ errorServices }}
      </div>
      <div v-else-if="destacados.length" class="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-5xl mx-auto">
        <ServiceCard
          v-for="dest in destacados"
          :key="dest.id"
          :servicio="dest"
        />
      </div>
      <div v-else class="text-center py-4">No se encontraron servicios destacados.</div>
    </section>

    <section class="px-4 py-12">
      <div class="text-center mb-6">
        <span class="btn-primary inline-block px-6 py-2 rounded mb-8">Comentarios</span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-5xl mx-auto">
        <div v-for="com in comentarios.slice(0, 3)" :key="com.usuario + com.servicio" class="p-4 card rounded">
          <p class="mb-2 font-medium">{{ com.titulo }}</p>
          <div class="flex items-center space-x-2">
            <img :src="`/assets/images/${com.pfp}`" class="w-8 h-8 rounded-full" />
            <div>
              <p class="text-sm font-semibold">{{ com.usuario }}</p>
              <p class="text-xs muted">{{ com.puntuacion }}/5</p>
            </div>
          </div>
          <p class="mt-2 text-sm muted">{{ com.comentario }}</p>
        </div>
      </div>
      <div class="flex justify-center gap-4 mt-6">
        <RouterLink to="/" class="btn-primary px-4 py-2 rounded">Inicio</RouterLink>
        <button class="btn-secondary px-4 py-2 rounded">Deja un comentario</button>
      </div>
    </section>

    <Footer />
  </div>
</template>

<script setup>
/* Importaciones */
import { ref, computed, onMounted } from 'vue' 
import { RouterLink } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import CategoryCard from '@/components/CategoryCard.vue'
import ServiceCard from '@/components/ServiceCard.vue'
import comentariosData from '@/assets/json/comentarios.json'
import { useCategories } from '@/composables/useCategories.js'
import { useServices } from '@/composables/useServices.js'
import Banner from '../components/Banner.vue'

/* Composables y estado */
const { categories, loading: loadingCategories, error: errorCategories, loadAll: loadAllCategories } = useCategories()
const { services, loading: loadingServices, error: errorServices, loadAll: loadAllServices } = useServices()

/* Computed: servicios destacados (los primeros 3) */
const destacados = computed(() => {
  return services.value.slice(0, 3)
})

/* Ciclo de vida: cargar categorías y servicios al montar */
onMounted(() => {
  loadAllCategories()
  loadAllServices()
})

/* Datos estáticos: comentarios cargados desde JSON */
const comentarios = ref(comentariosData)
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

.card {
  background-color: var(--color-background-light);
  color: var(--color-text);
  border: 1px solid var(--color-background-light);
  transition: background-color 180ms ease, color 180ms ease, border-color 180ms ease;
}

.btn-primary {
  background-color: var(--color-primary-button-bg);
  color: var(--color-primary-button-text);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: background-color 180ms ease, color 180ms ease;
}

.btn-secondary {
  background-color: var(--color-background-light);
  color: var(--color-text);
  transition: background-color 180ms ease, color 180ms ease;
}

img.rounded-md {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 0.375rem;
}

a.btn-primary, a.btn-secondary {
  text-decoration: none;
}
</style>