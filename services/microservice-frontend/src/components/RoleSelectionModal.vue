<template>
    <Transition name="modal">
        <div v-if="isOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div class="bg-white dark:bg-slate-800 rounded-lg shadow-xl p-8 max-w-md w-full mx-4">
                <h2 class="text-2xl font-bold mb-2" :style="{ color: 'var(--color-text)' }">
                    Completa tu Perfil
                </h2>
                <p class="mb-6" :style="{ color: 'var(--color-text-light)' }">
                    ¿Qué tipo de cuenta deseas crear?
                </p>

                <div class="space-y-3">
                    <!-- Contratista Option -->
                    <button @click="selectRole('contratista')"
                        class="w-full p-4 rounded-lg border-2 transition-all text-left" :class="{
                            'border-green-500 bg-green-50': selectedRole === 'contratista',
                            'border-gray-300 hover:border-gray-400': selectedRole !== 'contratista'
                        }">
                        <h3 class="font-semibold text-lg">Contratista</h3>
                        <p class="text-sm text-gray-600">Busco servicios y entretenimiento para mis eventos</p>
                    </button>

                    <!-- Oferente Option -->
                    <button @click="selectRole('oferente')"
                        class="w-full p-4 rounded-lg border-2 transition-all text-left" :class="{
                            'border-blue-500 bg-blue-50': selectedRole === 'oferente',
                            'border-gray-300 hover:border-gray-400': selectedRole !== 'oferente'
                        }">
                        <h3 class="font-semibold text-lg">Oferente</h3>
                        <p class="text-sm text-gray-600">Ofrezco servicios de entretenimiento</p>
                    </button>
                </div>

                <!-- Oferente Fields -->
                <div v-if="selectedRole === 'oferente'" class="mt-6 space-y-4 p-4 bg-blue-50 rounded">
                    <h3 class="font-semibold text-blue-900">Información Adicional</h3>

                    <div>
                        <label class="block text-sm font-semibold mb-1">Categoría de Servicio</label>
                        <select v-model="oferenteData.categoria" class="input-field">
                            <option disabled value="">Selecciona una categoría</option>
                            <option value="Música">Música</option>
                            <option value="Interpretación">Interpretación</option>
                            <option value="Comedia">Comedia</option>
                            <option value="Magia">Magia</option>
                            <option value="Cultura">Cultura</option>
                            <option value="Otro">Otro</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-sm font-semibold mb-1">Descripción</label>
                        <textarea v-model="oferenteData.descripcion" placeholder="Describe tu servicio..."
                            class="input-field" rows="2"></textarea>
                    </div>

                    <div>
                        <label class="block text-sm font-semibold mb-1">Ubicación</label>
                        <select v-model="oferenteData.ubicacion" class="input-field">
                            <option disabled value="">Selecciona provincia</option>
                            <option value="San José">San José</option>
                            <option value="Alajuela">Alajuela</option>
                            <option value="Cartago">Cartago</option>
                            <option value="Heredia">Heredia</option>
                            <option value="Guanacaste">Guanacaste</option>
                            <option value="Puntarenas">Puntarenas</option>
                            <option value="Limón">Limón</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-sm font-semibold mb-1">Teléfono</label>
                        <input v-model="oferenteData.telefono" type="tel" placeholder="8888-1234" class="input-field" />
                    </div>
                </div>

                <!-- Buttons -->
                <div class="flex gap-3 mt-6 justify-end">
                    <button @click="cancel" class="px-4 py-2 rounded font-semibold" :style="{
                        backgroundColor: 'var(--color-background-light)',
                        color: 'var(--color-text)'
                    }">
                        Cancelar
                    </button>
                    <button @click="confirm" :disabled="!isValid"
                        class="px-6 py-2 rounded font-semibold text-white bg-green-500 hover:bg-green-600 disabled:opacity-50">
                        Continuar
                    </button>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import { ref, computed } from 'vue';

const isOpen = ref(false);
const selectedRole = ref('contratista');
const oferenteData = ref({
    categoria: '',
    descripcion: '',
    ubicacion: '',
    telefono: ''
});

let resolvePromise = null;

const isValid = computed(() => {
    if (selectedRole.value === 'contratista') return true;
    return (
        oferenteData.value.categoria &&
        oferenteData.value.descripcion &&
        oferenteData.value.ubicacion &&
        oferenteData.value.telefono
    );
});

const show = () => {
    return new Promise((resolve) => {
        resolvePromise = resolve;
        isOpen.value = true;
        selectedRole.value = 'contratista';
        oferenteData.value = {
            categoria: '',
            descripcion: '',
            ubicacion: '',
            telefono: ''
        };
    });
};

const selectRole = (role) => {
    selectedRole.value = role;
};

const confirm = () => {
    if (!isValid.value) return;

    isOpen.value = false;
    if (resolvePromise) {
        resolvePromise({
            rol: selectedRole.value,
            ...(selectedRole.value === 'oferente' && oferenteData.value)
        });
    }
};

const cancel = () => {
    isOpen.value = false;
    if (resolvePromise) resolvePromise(null);
};

defineExpose({
    show
});
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
    transition: opacity 300ms ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}

.modal-enter-active>div,
.modal-leave-active>div {
    transition: transform 300ms ease;
}

.modal-enter-from>div,
.modal-leave-to>div {
    transform: scale(0.95);
}

.input-field {
    width: 100%;
    background-color: var(--color-body-bg);
    color: var(--color-text);
    border: 1px solid var(--color-background-light);
    border-radius: 0.375rem;
    padding: 0.5rem 0.75rem;
    font-size: 1rem;
}

.input-field:focus {
    outline: none;
    border-color: var(--color-primary-button-bg);
    box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.06);
}
</style>