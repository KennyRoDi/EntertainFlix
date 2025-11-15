<template>
  <div class="mi-contenedor-principal">
    <div class="fondo-borroso"></div>

    <header class="hero-header">
      <a href="/" class="logo-container">
        <img
          :src="isDark ? '/assets/images/logoEFD.png' : '/assets/images/logoEFL.png'"
          alt="Logo principal"
          class="header-logo-img"
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
    <div class="contenido-nitido">
      <div class="pill-tag">Más Eventos, Menos Complicaciones</div>
      <h1 class="slogan-text">
        Encuentra tu próxima <span class="highlight-word">experiencia</span> inolvidable
      </h1>
      <p class="sub-headline">
        Busca, descubre y disfruta tus eventos favoritos en un solo lugar.
      </p>

      <div class="cta-buttons">
        <router-link to="/categorias" class="cta-primary"
          >Explorar Categorías</router-link
        >
        <router-link to="/servicios" class="cta-secondary">Ver Catálogo</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { useAuth } from "@/composables/useAuth.js";
import MenuDesplegable from "./Menu.vue";

const router = useRouter();
const { usuario, logout } = useAuth();

const isDark = ref(false);
function actualizarTema() {
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
.highlight-word {
  font-weight: 700;
  font-family: monospace;
  color: var(--color-eslogan-primary);
}

.mi-contenedor-principal {
  position: relative;
  width: 100%;
  height: 800px;
  overflow: hidden;
}

.fondo-borroso {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("/assets/images/banner.png");
  background-size: cover;
  background-position: center;
  filter: blur(3px) brightness(0.7);
  z-index: 1;
}

.contenido-nitido {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  text-align: center;
  gap: 1.5rem;
}
.hero-header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  z-index: 3;
  background: transparent;
}

.logo-container {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.header-logo-img {
  height: 4.2rem;
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
.pill-tag {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.slogan-text {
  font-family: "Montserrat", sans-serif;
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  font-weight: 700;
  color: #ffffff;
  line-height: 1.1;
  max-width: 800px;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
}

.sub-headline {
  font-size: clamp(1rem, 2vw, 1.25rem);
  color: rgba(255, 255, 255, 0.85);
  font-weight: 400;
  max-width: 650px;
  line-height: 1.6;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.cta-primary,
.cta-secondary {
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cta-primary {
  background-color: var(--color-eslogan-primary);
  color: var(--color-text-button-slogan);
}
.cta-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 15px var(--color-eslogan-hover);
}

.cta-secondary {
  background-color: transparent;
  color: white;
  border: 2px solid white;
}
.cta-secondary:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
}
@media (max-width: 768px) {
  .header-logo-text {
    display: none;
  }
}
</style>
