<template>
    <div class="bg-white text-gray-900 font-sans min-h-screen flex flex-col">
        <Navbar />

        <main class="flex-grow px-4 py-8 mx-auto w-full max-w-5xl">
            <div class="text-center mb-8 w-3/4 mx-auto">
                <h2 class="text-3xl font-bold">IA Assistant</h2>
            </div>

            <div class="bg-gray-100 p-4 rounded shadow mb-6 w-3/4 mx-auto">
                <p class="text-sm text-gray-700">Hola, ¿en qué puedo ayudar?</p>
            </div>

            <div class="w-3/4 mx-auto">
                <textarea class="w-full h-40 border rounded p-4 resize-none text-sm text-gray-700 shadow mb-6"
                    placeholder="Escribe aquí tu mensaje..." disabled></textarea>

                <div class="flex items-center gap-4">
                    <input type="text" placeholder="Enter para enviar..."
                        class="flex-grow bg-gray-200 text-gray-600 rounded-full py-3 px-6 shadow" disabled />
                    <button class="bg-black text-white px-4 py-3 rounded-full">
                        ➤ <!-- flecha -->
                    </button>
                    <button class="bg-gray-300 px-4 py-3 rounded-full">
                        + <!-- clip de archivo -->
                    </button>
                </div>
            </div>
        </main>

        <Footer />
    </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
</script>

<style scoped></style>