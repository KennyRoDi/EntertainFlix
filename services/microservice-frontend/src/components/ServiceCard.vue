<template>
  <div class="card rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300">
    <router-link :to="`/detalle/${servicio.id}`">
      <img 
        :src="`/assets/images/${servicio.imagenes[0]}`" 
        :alt="servicio.titulo" 
        class="w-full h-48 object-cover object-center" 
      />
    </router-link>
    <div class="p-4">
      <h3 class="font-bold text-lg mb-1 strong-text">{{ servicio.titulo }}</h3>
      <p class="text-sm muted mb-2">{{ servicio.categoria }}</p>
      <p class="text-sm muted mb-2">Ubicación: {{ servicio.ubicacion }}</p>
      
      <router-link 
        :to="`/detalle/${servicio.id}`" 
        class="btn-primary inline-block text-sm px-4 py-2 rounded mt-2"
      >
        Ver más
      </router-link>
    </div>
  </div>
</template>

<script setup>
defineProps({
  servicio: {
    type: Object,
    required: true
  }
});
</script>

<style scoped>
.card {
  background-color: var(--color-background-light);
  color: var(--color-text);
  border: 1px solid transparent;
  box-shadow: var(--container-shadow);
  transition: background-color 180ms ease, color 180ms ease, transform 180ms ease;
}

.strong-text {
  color: var(--color-text);
}

.muted {
  color: var(--color-text-light);
}

.btn-primary {
  background-color: var(--color-primary-button-bg);
  color: var(--color-primary-button-text);
  text-decoration: none;
  transition: filter 120ms ease;
}

.btn-primary:hover {
  filter: brightness(0.92);
}
</style>