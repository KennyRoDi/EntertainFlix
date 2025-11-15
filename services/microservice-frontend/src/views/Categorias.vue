<template>
  <div class="page font-sans">
    <Navbar />

    <section class="px-4 py-12">
      <div v-if="loading" class="text-center muted text-lg py-10">
        Cargando categorías...
      </div>
      <div v-else-if="error" class="text-center text-red-500 text-lg py-10">
        <p>Ocurrió un error al cargar las categorías:</p>
        <p class="mt-2 text-sm">{{ error }}</p>
      </div>

      <div
        v-else-if="categories.length > 0"
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 max-w-6xl mx-auto"
      >
        <CategoryCard
          v-for="cat in categories"
          :key="cat.nombre"
          :categoria="cat"
        />
      </div>
       <div v-else class="text-center muted text-lg py-10">
        No se encontraron categorías.
      </div>
    </section>

    <Footer />
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";
import CategoryCard from "@/components/CategoryCard.vue";
import { useCategories } from "@/composables/useCategories.js";

const { categories, loading, error, loadAll } = useCategories();

onMounted(() => {
  loadAll();
});
</script>

<style scoped>
.page {
  background-color: var(--color-body-bg);
  color: var(--color-text);
  min-height: 100vh;
  transition: background-color 180ms ease, color 180ms ease;
}
</style>
