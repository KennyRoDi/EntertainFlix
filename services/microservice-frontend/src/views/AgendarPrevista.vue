<template>
    <div v-if="servicio && servicio.titulo" class="bg-white text-gray-900 font-sans">
        <Navbar />

        <!-- Presentación -->
        <section class="relative h-[60vh] bg-cover bg-center"
            :style="`background-image: url('/assets/images/${servicio.imagenes[1]}')`">
            <div class="absolute inset-0 bg-black bg-opacity-50 flex flex-col justify-center items-center text-white">
                <h1 class="text-4xl font-bold mb-2">{{ servicio.titulo }}</h1>
                <p class="text-lg mb-4">{{ servicio.eslogan }}</p>
            </div>
        </section>

        <!-- Datos de Agendamiento -->
        <section class="px-4 py-12 max-w-3xl mx-auto">
            <h2 class="text-2xl font-bold mb-6">Solicitud de Agendamiento</h2>
            <form class="space-y-6 bg-gray-50 p-6 rounded shadow">
                <div>
                    <label class="block text-sm font-semibold mb-1">Nombre completo</label>
                    <input type="text" class="w-full border rounded px-4 py-2" placeholder="Tu nombre" />
                </div>

                <div>
                    <label class="block text-sm font-semibold mb-1">Correo electrónico</label>
                    <input type="email" class="w-full border rounded px-4 py-2" placeholder="correo@ejemplo.com" />
                </div>

                <div>
                    <label class="block text-sm font-semibold mb-1">Fecha del evento</label>
                    <input type="date" class="w-full border rounded px-4 py-2" />
                </div>

                <div>
                    <label class="block text-sm font-semibold mb-1">Ubicación</label>
                    <input type="text" class="w-full border rounded px-4 py-2" placeholder="San José, Costa Rica" />
                </div>

                <div>
                    <label class="block text-sm font-semibold mb-1">Mensaje adicional</label>
                    <textarea class="w-full border rounded px-4 py-2"
                        placeholder="Describe tu evento y cualquier requerimiento especial"></textarea>
                </div>

                <button type="submit" class="bg-black text-white px-6 py-2 rounded font-semibold hover:bg-gray-800">
                    Enviar Solicitud
                </button>
            </form>
        </section>

        <Footer />
    </div>
    <div v-else class="text-center py-20 text-gray-500">Cargando servicio...</div>
</template>

<script setup>
import { ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import previstaData from '@/assets/json/prevista.json'

const route = useRoute()
const servicio = ref(null)

watchEffect(() => {
    const id = parseInt(route.params.id)
    const encontrado = previstaData.find(s => s.id === id)
    servicio.value = encontrado || null
})
</script>

<style scoped></style>