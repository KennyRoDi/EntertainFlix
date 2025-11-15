<template>
  <section v-if="solicitudes.length > 0 || servicio" class="w-full">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold strong-text">
        Todas las Solicitudes ({{ solicitudes.length }})
      </h2>
      <button
        @click="$emit('restaurar')"
        class="btn-plain flex items-center gap-2"
        aria-label="Restaurar solicitudes"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M4 2a1 1 0 011 1v2.121a3 3 0 010 5.758V16a1 1 0 11-2 0v-6.121a3 3 0 010-5.758V3a1 1 0 011-1zm3 4a1 1 0 011 1v.707a3 3 0 014.586 0V7a1 1 0 112 0v.707a5 5 0 00-7.071 0V7a1 1 0 011-1z"
            clip-rule="evenodd"
          />
          <path
            fill-rule="evenodd"
            d="M13 10a1 1 0 011-1h.707a3 3 0 014.586 0V10a1 1 0 112 0v.707a5 5 0 00-7.071 0V10a1 1 0 011-1z"
            clip-rule="evenodd"
          />
        </svg>
        Restaurar Solicitudes
      </button>
    </div>
    <div v-if="solicitudes.length > 0" class="grid gap-6">
      <SolicitudCard
        v-for="solicitud in solicitudes"
        :key="solicitud.id"
        :solicitud="solicitud"
        @accept="$emit('accept', solicitud.id)"
        @reject="$emit('reject', solicitud.id)"
      />
    </div>
    <div v-else class="empty-card p-8 rounded-lg muted text-center">
      <p class="text-lg">No se han recibido solicitudes aún.</p>
      <p class="text-sm mt-2">
        Las nuevas solicitudes aparecerán aquí automáticamente.
      </p>
    </div>
  </section>
</template>

<script setup>
import SolicitudCard from "@/components/SolicitudCard.vue";

defineProps({
  solicitudes: {
    type: Array,
    required: true,
  },
  servicio: { // Lo pasamos para el v-if inicial, aunque no se use directamente en el template
    type: Object,
    required: false // Puede ser null si el perfil no tiene servicio
  }
});

defineEmits(['accept', 'reject', 'restaurar']);
</script>

<style scoped>
</style>