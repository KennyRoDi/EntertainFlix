<template>
  <div
    :class="[
      'solicitud-card transition-shadow rounded-lg p-6',
      solicitud.estado === 'aceptada'
        ? 'solicitud-accepted'
        : solicitud.estado === 'rechazada'
        ? 'solicitud-rejected'
        : 'solicitud-pending',
    ]"
  >
    <div class="flex justify-between items-start mb-4">
      <div>
        <h3 class="font-bold text-xl strong-text mb-1">{{ solicitud.cliente }}</h3>
        <span :class="['badge inline-block text-sm px-3 py-1 rounded-full', badgeClass]">
          <span v-if="solicitud.estado === 'aceptada'">Aceptada - </span>
          <span v-else-if="solicitud.estado === 'rechazada'">Rechazada - </span>
          {{ solicitud.paquete }}
        </span>
      </div>
    </div>

    <div class="grid md:grid-cols-2 gap-4 mb-4">
      <div class="space-y-2">
        <div class="flex items-center gap-2">
          <span class="font-semibold strong-text">Email:</span>
          <a :href="`mailto:${solicitud.correo}`" class="link">{{ solicitud.correo }}</a>
        </div>
        <div class="flex items-center gap-2">
          <span class="font-semibold strong-text">Teléfono:</span>
          <span class="muted">{{ solicitud.telefono || "N/A" }}</span>
        </div>
      </div>
      <div class="space-y-2">
        <div class="flex items-center gap-2">
          <span class="font-semibold strong-text">Fecha:</span>
          <span class="muted">{{ formatearFecha(solicitud.fecha) }}</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="font-semibold strong-text">Ubicación:</span>
          <span class="muted">{{ solicitud.ubicacion }}</span>
        </div>
      </div>
    </div>

    <div class="mb-4">
      <p class="font-semibold strong-text mb-2">Mensaje:</p>
      <div class="textContainer ['p-3 rounded-lg', messageClass]">
        <p class="muted leading-relaxed mensaje">{{ solicitud.mensaje }}</p>
      </div>
    </div>

    <div
      v-if="solicitud.estado === 'pendiente' || !solicitud.estado"
      class="flex gap-3 pt-4"
    >
      <button @click="$emit('accept', solicitud.id)" class="btn-accept">Aceptar</button>
      <button @click="$emit('reject', solicitud.id)" class="btn-reject">Rechazar</button>
    </div>
    <div v-else class="flex gap-3 pt-4 border-t muted text-sm">
      Esta solicitud ha sido
      {{ solicitud.estado === "aceptada" ? "aceptada" : "rechazada" }}.
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  solicitud: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["accept", "reject"]);

const badgeClass = computed(() => {
  if (props.solicitud.estado === "aceptada") return "badge-accepted";
  if (props.solicitud.estado === "rechazada") return "badge-rejected";
  return "badge-pending";
});

const messageClass = computed(() => {
  if (props.solicitud.estado === "aceptada") return "msg-accepted";
  if (props.solicitud.estado === "rechazada") return "msg-rejected";
  return "msg-pending";
});

function formatearFecha(fecha) {
  const opciones = { year: "numeric", month: "long", day: "numeric" };
  return new Date(fecha).toLocaleDateString("es-CR", opciones);
}
</script>

<style scoped>
.textContainer {
  background-color: var(--color-solicitudmsg);
  padding: 2%;
  border-radius: 0.5rem;
}
.strong-text {
  color: var(--color-text);
}
.muted {
  color: var(--color-text-light);
}
.link {
  color: #00bfff;
  text-decoration: none;
}
.link:hover {
  text-decoration: underline;
}
.solicitud-card {
  border-radius: 0.75rem;
}
.solicitud-pending {
  background-color: var(--color-background-light);
}
.solicitud-accepted {
  background-color: var(--color-background-light);
  border-left: 4px solid #16a34a;
}
.solicitud-rejected {
  background-color: var(--color-background-light);
  border-left: 4px solid #dc2626;
}
.badge {
  font-weight: 600;
}
.badge-pending {
  background-color: var(--color-solicitud);
  color: var(--color-primary-button-bg);
}
.badge-accepted {
  background-color: #17c76c;
  color: #ffffff;
}
.badge-rejected {
  background-color: #e40202;
  color: #ffffff;
}
.msg-pending,
.msg-accepted,
.msg-rejected {
  background-color: #ffffff;
}
.mensaje {
  color: var(--color-text);
}
.btn-accept,
.btn-reject {
  display: flex;
  flex-direction: column;
  text-align: center;
  width: 13%;
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: transform 120ms ease, filter 120ms ease;
  color: #ffffff;
}
.btn-accept {
  background-color: #24ca61;
}
.btn-accept:hover {
  background-color: #15803d;
  transform: translateY(-1px);
}
.btn-reject {
  background-color: #dc2626;
}
.btn-reject:hover {
  background-color: #b91c1c;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .btn-accept,
  .btn-reject {
    width: 30%;
    padding: 0.5rem 0.75rem;
    border-radius: 0.375rem;
    font-weight: 600;
    cursor: pointer;
    border: none;
    transition: transform 120ms ease, filter 120ms ease;
    color: #ffffff;
  }
}
</style>
