<template>
    <div v-if="servicio" class="bg-white text-gray-900 font-sans">
        <Navbar />

        <!-- Encabezado -->
        <section class="relative h-[60vh] bg-cover bg-center"
            :style="`background-image: url('/assets/images/${servicio.imagenes[1]}')`">
            <div class="absolute inset-0 bg-black bg-opacity-50 flex flex-col justify-center items-center text-white">
                <h1 class="text-4xl font-bold mb-2">{{ servicio.titulo }}</h1>
                <p class="text-lg mb-4">{{ servicio.eslogan }}</p>
                <RouterLink :to="`/agendarprevista/${servicio.id}`"
                    class="bg-white text-black px-6 py-2 rounded font-semibold hover:bg-gray-200">
                    Agendar
                </RouterLink>
            </div>
        </section>

        <!-- ¿Quién Soy? -->
        <section class="px-4 py-12 max-w-6xl mx-auto grid md:grid-cols-2 gap-8 items-center">
            <div>
                <h2 class="text-2xl font-bold mb-2">¿Quién Soy?</h2>
                <p class="text-gray-600">{{ servicio.quien_soy }}</p>
            </div>
            <img :src="`/assets/images/${servicio.imagenes[2]}`" class="rounded-md" />
        </section>

        <!-- ¿Qué Hago? -->
        <section class="px-4 py-12 max-w-6xl mx-auto grid md:grid-cols-2 gap-8 items-center">
            <img :src="`/assets/images/${servicio.imagenes[3]}`" class="rounded-md" />
            <div>
                <h2 class="text-2xl font-bold mb-2">¿Qué Hago?</h2>
                <p class="text-gray-600">{{ servicio.que_hago }}</p>
            </div>
        </section>

        <!-- Paquetes -->
        <section class="px-4 py-12 max-w-6xl mx-auto">
            <h2 class="text-2xl font-bold mb-6">Paquetes</h2>
            <div class="grid md:grid-cols-3 gap-6">
                <div v-for="(paq, index) in servicio.paquetes" :key="index" class="bg-white border rounded shadow p-4">
                    <img :src="`/assets/images/${servicio.imagenes[index + 4]}`" class="rounded mb-2" />
                    <h3 class="font-semibold">{{ paq.nombre }}</h3>
                    <p class="text-sm text-gray-600">{{ paq.descripcion }}</p>
                    <p class="font-bold mt-1">$ {{ paq.precio }}</p>
                </div>
            </div>
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
    servicio.value = previstaData.find(s => s.id === id) || null
})
</script>

<style scoped></style>
