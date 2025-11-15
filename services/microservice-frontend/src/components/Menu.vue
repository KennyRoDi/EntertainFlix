<template>
  <div class="menu-container" ref="menuContainerRef">
    <button @click="toggleMenu" class="menu-button">Menú</button>

    <div v-if="isMenuOpen" @click="closeMenu" class="menu-overlay"></div>

    <div class="dropdown-menu" :class="{ 'is-open': isMenuOpen }">
      <a class="logo-container">
        <img
          :src="isDark ? '/assets/images/logoEFD.png' : '/assets/images/logoEFL.png'"
          alt="Logo principal"
          class="header-logo"
        />
        <img
          :src="isDark ? '/assets/images/logoTextD.png' : '/assets/images/logoTextL.png'"
          alt="Texto del logo"
          class="header-logo-text"
        />
      </a>
      <hr class="dropdown-divider" />
      <RouterLink to="/" class="dropdown-link" @click="closeMenu">
        <HomeIcon class="dropdown-icon" />
        <span>Inicio</span>
      </RouterLink>
      <RouterLink to="/categorias" class="dropdown-link" @click="closeMenu">
        <Squares2X2Icon class="dropdown-icon" />
        <span>Categorías</span>
      </RouterLink>
      <RouterLink to="/servicios" class="dropdown-link" @click="closeMenu">
        <MusicalNoteIcon class="dropdown-icon" />
        <span>Servicios</span>
      </RouterLink>
      <RouterLink
        v-if="usuario && usuario.rol === 'oferente'"
        to="/publicar"
        class="dropdown-link"
        @click="closeMenu"
      >
        <ArrowUpTrayIcon class="dropdown-icon" />
        <span>Publicar</span>
      </RouterLink>
      <RouterLink
        v-if="usuario"
        :to="
          usuario.rol === 'oferente'
            ? `/perfil/${usuario.usuario}`
            : usuario.rol === 'administrador'
            ? '/revision'
            : '/cliente'
        "
        class="dropdown-link"
        @click="closeMenu"
      >
        <UserIcon class="dropdown-icon" />
        <span>Pefil</span>
      </RouterLink>

      <button @click="openConfigPanel" class="dropdown-link">
        <Cog6ToothIcon class="dropdown-icon" />
        <span>Configuración</span>
      </button>
      <Config :is-open="isConfigOpen" @close="closeConfigPanel" />

      <hr class="dropdown-divider" />
      <RouterLink
        v-if="!usuario"
        to="/inicio-sesion"
        class="dropdown-link"
        @click="closeMenu"
      >
        <ArrowRightEndOnRectangleIcon class="dropdown-icon" />
        <span>Iniciar Sesión</span>
      </RouterLink>
      <button v-else @click="onCerrarSesion" class="dropdown-logout-button">
        <ArrowLeftStartOnRectangleIcon class="dropdown-icon" />
        <span>Cerrar Sesión</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { RouterLink } from "vue-router";
import Config from './Config.vue';
import {
  HomeIcon,
  UserIcon,
  ArrowRightEndOnRectangleIcon,
  ArrowLeftStartOnRectangleIcon,
  Squares2X2Icon,
  MusicalNoteIcon,
  ArrowUpTrayIcon,
  Cog6ToothIcon,
} from "@heroicons/vue/24/solid";

// 1. Definir las props que el componente recibirá.
defineProps({
  usuario: {
    type: Object,
    default: null,
  },
});

// 2. Definir los eventos que el componente emitirá.
const emit = defineEmits(["cerrar-sesion"]);
const isMenuOpen = ref(false);
const menuContainerRef = ref(null);
const isConfigOpen = ref(false);

function openConfigPanel() {
  isConfigOpen.value = true;
}

function closeConfigPanel() {
  isConfigOpen.value = false;
}

function toggleMenu() {
  isMenuOpen.value = !isMenuOpen.value;
}

function closeMenu() {
  isMenuOpen.value = false;
}

// 3. Emitir el evento cuando se hace clic en el botón.
function onCerrarSesion() {
  emit("cerrar-sesion");
  closeMenu();
}

const handleClickOutside = (event) => {
  if (menuContainerRef.value && !menuContainerRef.value.contains(event.target)) {
    closeMenu();
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

const isDark = ref(false);
function actualizarTema() {
  // Detecta si el body tiene la clase dark-mode
  isDark.value = document.body.classList.contains("dark-mode");
}

onMounted(() => {
  actualizarTema();
  const observer = new MutationObserver(actualizarTema);
  observer.observe(document.body, { attributes: true, attributeFilter: ["class"] });
  onUnmounted(() => observer.disconnect());
});
</script>

<style scoped>
.logo-container {
  display: flex;
  align-items: center;
  text-decoration: none;
  margin-bottom: 10%;
}
.header-logo {
  height: 4rem;
  width: auto;
}
.header-logo-text {
  height: 3rem;
  width: auto;
  margin-top: 4.5%;
}

.menu-container {
  position: relative;
  display: inline-block;
}

.menu-button {
  background-color: var(--color-eslogan-primary);
  color: var(--color-text-button-slogan);
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.menu-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 15px var(--color-eslogan-hover);
}

/* --- ESTILOS MODIFICADOS Y AÑADIDOS --- */

/* Estilo para el fondo oscuro */
.menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Negro semi-transparente */
  z-index: 99; /* Justo debajo del menú */
}

/* Estilos base del menú lateral (cuando está CERRADO) */
.dropdown-menu {
  position: fixed;
  top: 0;
  right: 0;
  height: 100vh;
  width: 300px;
  max-width: 80vw;
  background-color: var(--color-menu-display);
  box-shadow: -4px 0 15px rgba(0, 0, 0, 0.2);
  padding: 2rem 1rem;
  display: flex;
  flex-direction: column;
  z-index: 100;
  transform: translateX(100%);
  transition: transform 0.3s ease-in-out;
}

/* Estilo que se aplica cuando el menú está ABIERTO */
.dropdown-menu.is-open {
  transform: translateX(0);
}

body.dark-mode .dropdown-menu {
  border-color: #4a5568;
}

.dropdown-link {
  text-decoration: none;
  color: var(--color-header-text);
  padding: 0.75rem 1.5rem;
  display: block;
  transition: background-color 0.2s ease;
  text-align: left;
  background: none;
  border: none;
  width: 100%;
  font-size: 1rem;
}

.dropdown-icon {
  height: 1.25rem;
  width: 1.25rem;
  color: var(--color-eslogan-primary);
}

.dropdown-link,
.dropdown-logout-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.dropdown-link:hover {
  background-color: rgba(66, 65, 65, 0.534);
}

body.dark-mode .dropdown-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.dropdown-divider {
  border: none;
  border-top: 1px solid var(--color-primary-button-text);
  margin: 0.5rem 0;
}

body.dark-mode .dropdown-divider {
  border-top-color: #4a5568;
}

.dropdown-logout-button {
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  transition: background-color 0.2s ease;
  text-align: left;
  background: none;
  border: none;
  width: 100%;
  cursor: pointer;
  font-size: 1rem;
  color: #ef4444;
}

.dropdown-logout-button:hover {
  background-color: rgba(239, 68, 68, 0.1);
}
@media (max-width: 768px) {
  .menu-button {
    padding: 0.4rem 0.6rem;
    font-size: 0.8rem;
  }
}
</style>
