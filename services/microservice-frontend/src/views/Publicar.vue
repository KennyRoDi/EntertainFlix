<template>
    <div class="page font-sans min-h-screen flex flex-col">
        <Navbar />

        <section class="px-4 py-12 max-w-4xl mx-auto">
            <h1 class="text-2xl font-bold mb-6 text-center text-primary-heading">Publicar Nuevo Servicio</h1>

            <form @submit.prevent="handleSubmit" class="form-card space-y-6">

                <div>
                    <label for="titulo" class="block text-sm font-medium text-form-label">Título del Servicio</label>
                    <input type="text" id="titulo" v-model="form.titulo" required
                        class="mt-1 block w-full rounded-md shadow-sm input-field">
                </div>

                <div>
                    <label for="eslogan" class="block text-sm font-medium text-form-label">Eslogan</label>
                    <input type="text" id="eslogan" v-model="form.eslogan"
                        class="mt-1 block w-full rounded-md shadow-sm input-field">
                </div>

                <div>
                    <label for="quien_soy" class="block text-sm font-medium text-form-label">¿Quién Soy?</label>
                    <textarea id="quien_soy" v-model="form.quien_soy" rows="4" required
                        class="mt-1 block w-full rounded-md shadow-sm input-field"></textarea>
                </div>

                <div>
                    <label for="que_hago" class="block text-sm font-medium text-form-label">¿Qué Hago?</label>
                    <textarea id="que_hago" v-model="form.que_hago" rows="4" required
                        class="mt-1 block w-full rounded-md shadow-sm input-field"></textarea>
                </div>

                <div>
                    <label class="block text-sm font-medium text-form-label">Imágenes del Servicio</label>
                    <input type="file" @change="handleFileChange($event, 'header')" required
                        class="mt-1 block w-full text-sm text-file-input-text file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100">
                </div>

                <div>
                    <h2 class="text-xl font-semibold mb-3 text-primary-heading">Paquetes</h2>
                    <div v-for="(paquete, index) in form.paquetes" :key="index"
                        class="package-card p-4 rounded-md mb-4 border">
                        <button type="button" @click="removePackage(index)"
                            class="text-red-500 hover:text-red-700 text-sm">Eliminar Paquete</button>
                    </div>
                    <button type="button" @click="addPackage"
                        class="mt-2 btn-secondary px-4 py-2 rounded text-sm hover:opacity-90">
                        + Añadir Paquete
                    </button>
                </div>

                <div class="flex justify-center">
                    <button type="submit" class="btn-submit px-8 py-3 rounded-full font-semibold hover:opacity-90">
                        Publicar Servicio
                    </button>
                </div>
            </form>
        </section>

        <Footer />
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'

// --- Estado principal del formulario ---
const form = reactive({
    titulo: '',           // Título del servicio
    eslogan: '',          // Eslogan promocional
    quien_soy: '',        // Descripción personal
    que_hago: '',         // Descripción de lo que se ofrece
    imagenes: {           // Imágenes asociadas
        header: null,
    },
    paquetes: [],         // Lista de paquetes agregados
})

// --- Manejo de imágenes ---
const handleFileChange = (event, imageType) => {
    form.imagenes[imageType] = event.target.files[0]
}

// --- Gestión de paquetes ---
const addPackage = () => {
    form.paquetes.push({
        nombre: '',           // Nombre del paquete
        descripcion: '',      // Detalle del paquete
        precio: '',           // Precio del paquete
        imagen: null,         // Imagen opcional
        video_youtube: '',    // Video asociado
        detalles: [],         // Lista de extras o detalles
    })
}

const removePackage = (index) => {
    form.paquetes.splice(index, 1)
}

// --- Envío del formulario ---
const handleSubmit = () => {
    console.log('Form data submitted:', form)
}
</script>


<style scoped>
.page {
    background-color: var(--color-body-bg);
    color: var(--color-text);
    min-height: 100vh;
    transition: background-color 180ms ease, color 180ms ease;
}

.form-card {
    background-color: var(--color-background-light);
    color: var(--color-text);
    padding: 1.5rem;
    border-radius: 0.5rem;
    transition: background-color 180ms ease, color 180ms ease;
}

.text-primary-heading {
    color: var(--color-text);
    transition: color 180ms ease;
}

.text-form-label {
    color: var(--color-text-light);
    transition: color 180ms ease;
}

.input-field {
    background-color: var(--color-body-bg);
    color: var(--color-text);
    border: 1px solid var(--color-text2);
    padding: 0.5rem 0.75rem;
    transition: background-color 180ms ease, color 180ms ease, border-color 180ms ease;
    outline: none;
}

.input-field:focus {
    border-color: var(--color-header-bg);
    box-shadow: 0 0 0 3px rgba(var(--color-header-bg), 0.2);
}

.package-card {
    background-color: var(--color-solicitud);
    color: var(--color-text);
    border-color: var(--color-text2);
    transition: all 180ms ease;
}

.btn-submit {
    background-color: #10B981;
    color: white;

    transition: filter 120ms ease;
}

.btn-secondary {
    background-color: var(--color-secondary-button-bg);
    color: var(--color-secondary-button-text);
    border: 1px solid var(--color-secondary-button-bg);
    transition: background-color 180ms ease, color 180ms ease, opacity 120ms ease;
}

.text-file-input-text {
    color: var(--color-text);
}
</style>