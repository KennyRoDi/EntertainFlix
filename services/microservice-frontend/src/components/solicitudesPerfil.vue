<template>
  <section v-if="solicitudes.length > 0 || servicio" class="w-full">
    <div class="flex justify-center items-center mb-6">
    </div>
    <div v-if="solicitudes.length > 0" class="grid gap-6">
      <SolicitudCard v-for="solicitud in solicitudes" :key="solicitud.id" :solicitud="solicitud"
        @accept="$emit('accept', solicitud.id)" @reject="$emit('reject', solicitud.id)" />
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

<style scoped></style>