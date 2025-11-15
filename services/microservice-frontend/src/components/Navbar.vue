<template>
  <header class="header">
    <a href="/" class="logo-container">
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
    <nav class="header-nav">
      <MenuDesplegable :usuario="usuario" @cerrar-sesion="cerrarSesion" />
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "@/composables/useAuth.js";
import MenuDesplegable from "./Menu.vue";

const router = useRouter();
const { usuario, logout } = useAuth();

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

function cerrarSesion() {
  logout();
  router.push("/");
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  height: 68px;
  background-color: var(--color-header-bg);
  color: var(--color-header-text);
}

.logo-container {
  display: flex;
  align-items: center;
  text-decoration: none;
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

.header-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.menu-container {
  position: relative;
  display: inline-block;
}

.menu-button {
  background-color: var(--color-primary-button-bg);
  color: var(--color-primary-button-text);
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s, color 0.3s;
}

.menu-button:hover {
  background-color: var(--color-primary-button-text);
  color: var(--color-primary-button-bg);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 5px);
  left: 0;
  background-color: var(--color-header-bg);
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  border-radius: 0.375rem;
  padding: 0.5rem 0;
  z-index: 50;
  min-width: 180px;
  display: flex;
  flex-direction: column;
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
.dropdown-menu {
  right: 0;
  left: auto;
}

.dropdown-link:hover {
  background-color: rgba(66, 65, 65, 0.534);
}

body.dark-mode .dropdown-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.dropdown-divider {
  border: none;
  border-top: 1px solid #e2e8f0;
  margin: 0.5rem 0;
}

body.dark-mode .dropdown-divider {
  border-top-color: #4a5568;
}

.dropdown-logout-button {
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  display: block;
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
  .header-logo-text {
    display: none;
  }
}
</style>
