<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    
    <div class="modal-content card">
      <h3 class="text-xl font-bold strong-text mb-4">
        {{ isEditing ? 'Editar Paquete' : 'Añadir Nuevo Paquete' }}
      </h3>
      
      <form @submit.prevent="handleSubmit">
        <div class="mb-4">
          <label class="block font-semibold strong-text mb-1" for="nombre">Nombre del Paquete</label>
          <input v-model="editablePackage.nombre" id="nombre" type="text" required class="modal-input" />
        </div>
        
        <div class="mb-4">
          <label class="block font-semibold strong-text mb-1" for="descripcion">Descripción</label>
          <textarea v-model="editablePackage.descripcion" id="descripcion" rows="3" required class="modal-input"></textarea>
        </div>
        
        <div class="mb-4">
          <label class="block font-semibold strong-text mb-1" for="precio">Precio ($)</label>
          <input v-model.number="editablePackage.precio" id="precio" type="number" required min="0" class="modal-input" />
        </div>

        <!-- =========== NUEVO CAMPO PARA EL ENLACE DE YOUTUBE =========== -->
        <div class="mb-4">
          <label class="block font-semibold strong-text mb-1" for="video_youtube">Enlace de YouTube (opcional)</label>
          <input v-model="editablePackage.video_youtube" id="video_youtube" type="url" class="modal-input" placeholder="https://www.youtube.com/watch?v=..." />
        </div>
        <!-- ============================================================= -->
        
        <div class="flex justify-end gap-3 mt-6">
          <button type="button" @click="$emit('close')" class="btn-plain">Cancelar</button>
          <button type="submit" class="btn-accept">Guardar Cambios</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  paquete: {
    type: Object,
    required: true,
  },
  isEditing: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['close', 'save']);

// No es necesario cambiar la lógica aquí. La copia con '...'
// incluirá automáticamente el campo 'video_youtube' si existe en la prop.
const editablePackage = ref({ ...props.paquete });

watch(() => props.paquete, (newVal) => {
  editablePackage.value = { ...newVal };
}, { deep: true });

const handleSubmit = () => {
  // Al guardar, 'editablePackage.value' ya contiene el nuevo campo 'video_youtube',
  // por lo que se enviará correctamente al componente padre (perfil.vue).
  emit('save', editablePackage.value);
};
</script>

<style scoped>
/* Todos los estilos necesarios para el modal están encapsulados aquí. */
/* No afectarán a otros componentes fuera de este archivo. */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}
.modal-content {
  width: 90%;
  max-width: 500px;
  padding: 1.5rem;
  border-radius: 0.75rem;
  background-color: var(--color-body-bg); /* Usa variables de CSS para el tema */
  color: var(--color-text);
  border: 1px solid transparent;
}
.modal-input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  border: 1px solid var(--color-text-light);
  background-color: var(--color-background-light);
  color: var(--color-text);
  transition: border-color 150ms ease, box-shadow 150ms ease;
}
.modal-input:focus {
  outline: none;
  border-color: var(--color-primary-button-bg);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.4);
}
.strong-text {
  color: var(--color-text);
}

/* Botones genéricos (pueden venir de un archivo global, pero se incluyen aquí para que sea autocontenido) */
.btn-accept,
.btn-plain {
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: transform 120ms ease, background-color 120ms ease;
}
.btn-accept {
  background-color: #16a34a; /* green-600 */
  color: #ffffff;
}
.btn-accept:hover {
  background-color: #15803d; /* green-700 */
  transform: translateY(-1px);
}
.btn-plain {
  background-color: var(--color-background-light);
  color: var(--color-text);
  border: 1px solid rgba(0,0,0,0.06);
}
.btn-plain:hover {
  filter: brightness(0.98);
}
</style>