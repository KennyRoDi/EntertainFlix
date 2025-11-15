<template>
  <section v-if="servicio && reseñas.length > 0" class="w-full">
    <h2 class="text-2xl font-bold strong-text mb-6">
      Reseñas de {{ servicio.titulo }}
    </h2>
    <div class="resenaContainer grid md:grid-cols-2 gap-6">
      <div
        v-for="(resena, index) in reseñas"
        :key="index"
        class="card p-4 rounded shadow"
      >
        <div class="flex items-center gap-3 mb-2">
          <img
            :src="`/assets/images/${resena.pfp}`"
            class="w-10 h-10 rounded-full object-cover"
          />
          <div>
            <p class="font-semibold strong-text">{{ resena.titulo }}</p>
            <p class="text-sm muted">{{ resena.usuario }}</p>
          </div>
        </div>
        <p class="text-sm muted">{{ resena.comentario }}</p>
      </div>
    </div>
  </section>
  <div v-else class="empty-card p-8 rounded-lg muted text-center">
    <p class="text-lg">Este servicio aún no tiene reseñas.</p>
  </div>
</template>

<script setup>
defineProps({
  servicio: {
    type: Object,
    required: true
  },
  reseñas: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
.resenaContainer {
  width: 90%;
  border-radius: 0.5rem;
  background-color: var(--color-background-light);
}
</style>