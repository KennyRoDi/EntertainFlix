<template>
    <Transition name="modal">
        <div v-if="isOpen" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div class="bg-white dark:bg-slate-800 rounded-lg shadow-xl p-6 max-w-sm w-full mx-4">
                <h2 class="text-xl font-bold mb-2" :style="{ color: 'var(--color-text)' }">
                    {{ title }}
                </h2>
                <p class="mb-6" :style="{ color: 'var(--color-text-light)' }">
                    {{ message }}
                </p>
                <div class="flex gap-3 justify-end">
                    <button 
                        @click="cancel" 
                        class="px-4 py-2 rounded font-semibold transition-all" 
                        :style="{
                            backgroundColor: 'var(--color-background-light)',
                            color: 'var(--color-text)',
                            border: '1px solid var(--color-text-light)'
                        }" 
                        @mouseenter="$event.target.style.filter = 'brightness(0.95)'"
                        @mouseleave="$event.target.style.filter = 'brightness(1)'">
                        Cancelar
                    </button>
                    <button 
                        @click="confirm" 
                        :class="[
                            'px-4 py-2 rounded font-semibold text-white transition-all',
                            type === 'danger' ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'
                        ]">
                        {{ confirmText }}
                    </button>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import { ref } from 'vue';

const isOpen = ref(false);
const title = ref('');
const message = ref('');
const confirmText = ref('Confirmar');
const type = ref('default'); // 'default', 'danger', 'success'
let resolvePromise = null;

const show = (options = {}) => {
    return new Promise((resolve) => {
        title.value = options.title || '¿Confirmar?';
        message.value = options.message || '';
        confirmText.value = options.confirmText || 'Confirmar';
        type.value = options.type || 'default';
        resolvePromise = resolve;
        isOpen.value = true;
    });
};

const confirm = () => {
    isOpen.value = false;
    if (resolvePromise) resolvePromise(true);
};

const cancel = () => {
    isOpen.value = false;
    if (resolvePromise) resolvePromise(false);
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

.modal-enter-active > div,
.modal-leave-active > div {
    transition: transform 300ms ease;
}

.modal-enter-from > div,
.modal-leave-to > div {
    transform: scale(0.95);
}
</style>