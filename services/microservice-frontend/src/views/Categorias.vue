<template>
  <div class="page font-sans min-h-screen">
    <Navbar />

    <section class="px-4 py-12 max-w-7xl mx-auto">
      <h2 class="text-3xl font-bold mb-8 strong-text">Categorías</h2>

      <div v-if="loading" class="text-center muted text-lg py-10">
        Cargando categorías...
      </div>
      <div v-else-if="error" class="text-center text-red-500 text-lg py-10">
        <p>Ocurrió un error al cargar las categorías:</p>
        <p class="mt-2 text-sm">{{ error }}</p>
      </div>

      <div v-else>
        <div v-if="totalCat > 0">
          <!-- grilla -->
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
            <CategoryCard
              v-for="cat in categoriesPaged"
              :key="cat.id ?? cat.nombre"
              :categoria="cat"
            />
          </div>

          <!-- mini resumen -->
          <p class="text-sm muted mt-4">
            Mostrando {{ categoriesPaged.length }} de {{ totalCat }} resultados
          </p>

          <!-- Controles de paginación (mismo HTML que Servicios) -->
          <div class="flex items-center gap-3 justify-center mt-6 select-none">
            <button
              class="btn-plain px-3 py-2 rounded border"
              @click="catPage = Math.max(1, catPage - 1)"
              :disabled="catPage === 1"
            >
              Anterior
            </button>

            <span class="muted">
              Página {{ catPage }} de {{ totalCatPages }}
            </span>

            <button
              class="btn-plain px-3 py-2 rounded border"
              @click="catPage = Math.min(totalCatPages, catPage + 1)"
              :disabled="catPage >= totalCatPages"
            >
              Siguiente
            </button>
          </div>
        </div>

        <!-- estado vacío (pegado al v-if de arriba) -->
        <div v-else class="text-center muted text-lg py-10">
          No se encontraron categorías.
        </div>
      </div>
    </section>

    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";
import CategoryCard from "@/components/CategoryCard.vue";
import { useCategories } from "@/composables/useCategories.js";

const { categories, loading, error, loadAll } = useCategories();

onMounted(() => {
  loadAll();
});

const CAT_PAGE_SIZE = 4
const catPage = ref(1)

const totalCat = computed(() => (categories.value?.length ?? 0))
const totalCatPages = computed(() => 
Math.max(1, Math.ceil(totalCat.value / CAT_PAGE_SIZE)))

const categoriesPaged = computed(() =>{
  const arr = categories.value || []
  const start = (catPage.value - 1) * CAT_PAGE_SIZE
  return arr.slice(start, start + CAT_PAGE_SIZE)
})

watch([categories], () => { catPage.value = 1 })
</script>

<style scoped>
.page {
  background-color: var(--color-body-bg);
  color: var(--color-text);
  min-height: 100vh;
  transition: background-color 180ms ease, color 180ms ease;
}
</style>
