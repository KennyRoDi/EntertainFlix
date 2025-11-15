<template>
  <section v-if="servicio" class="w-full">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold strong-text">
        Paquetes de {{ servicio.titulo }}
      </h2>
      <button @click="$emit('crear')" class="btn-accept">
        + Añadir Paquete
      </button>
    </div>
    <div
      v-if="servicio.paquetes && servicio.paquetes.length > 0"
      class="grid md:grid-cols-3 gap-6"
    >
      <div
        v-for="(paq, index) in servicio.paquetes"
        :key="index"
        class="containerCard card p-4 rounded shadow flex flex-col"
      >
        <img
          :src="`/assets/images/${servicio.imagenes[index % servicio.imagenes.length]}`"
          class="rounded mb-2 w-full h-40 object-cover"
          alt="Imagen del paquete"
        />
        <div class="dropdown-divider"></div>
        <div class="flex-1">
          <h3 class="font-semibold strong-text text-left">{{ paq.nombre }}</h3>
          <p class="text-sm muted mt-1">{{ paq.descripcion }}</p>
          <p class="font-bold mt-1 strong-text">$ {{ paq.precio }}</p>
        </div>
        <div class="flex gap-2 mt-4 pt-3 ">
          <button @click="$emit('editar', index)" class="btn-edit flex-1">
            Editar
          </button>
          <button @click="$emit('eliminar', index)" class="btn-reject flex-1">
            Eliminar
          </button>
        </div>
      </div>
    </div>
    <div v-else class="empty-card p-8 rounded-lg muted text-center">
      <p class="text-lg">No hay paquetes para mostrar.</p>
      <p class="text-sm mt-2">¡Añade tu primer paquete para empezar!</p>
    </div>
  </section>
</template>

<script setup>
defineProps({
  servicio: {
    type: Object,
    required: true
  }
});

defineEmits(['crear', 'editar', 'eliminar']);
</script>

<style scoped>
.containerCard {
  background-color: var(--color-background-light);
  border-radius: 0.5rem;
  width: auto;
  height: 110%;
  gap: 3%;
}

.dropdown-divider {
  border: none;
  border-top: 2px solid var(--color-primary-button-bg);
  margin: 0.5rem 0;
  align-self: stretch;
}
.btn-edit {
  font-weight: 600;
  border-radius: 0.5rem;
  border: 1px solid var(--color-footer-text);
  height: 120%;
}
.btn-edit:hover {
  background-color: var(--color-footer-text);
  color: var(--color-background-light);
  transform: translateY(-1px);
  cursor: pointer;
}
.btn-reject {
  font-weight: 600;
  border-radius: 0.5rem;
  background-color: red;
  height: 120%;
}
.btn-reject:hover {
  background-color: #b91c1c;
  transform: translateY(-1px);
  cursor: pointer;
}
</style>