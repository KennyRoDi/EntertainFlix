<template>
  <div>
    <div v-if="isOpen" @click="closePanel" class="config-overlay"></div>

    <div class="config-panel" :class="{ 'is-open': isOpen }" ref="panelRef" @click.stop>
      <div class="config-header">
        <h2>Configuración</h2>
        <button @click="closePanel" class="close-button">
          <XMarkIcon class="close-icon" />
        </button>
      </div>
      <hr class="dropdown-divider" />

      <div class="config-section">
        <a class="change_theme">
          <h3 class="section-title">Cambiar tema</h3>
          <div class="theme-switcher-wrapper">
            <button
              @click="toggleTheme"
              class="theme-toggle-button"
              title="Alternar tema"
            >
              <component :is="themeIcon" class="toggle-icon" />
            </button>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import { SunIcon, MoonIcon, XMarkIcon } from "@heroicons/vue/24/solid";

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
});

// 2. Definir los eventos que el componente emitirá.
const emit = defineEmits(["close"]);
const panelRef = ref(null);
const currentTheme = ref("light");

// 4. Lógica para cerrar el panel al hacer clic fuera.
const handleClickOutside = (event) => {
  if (props.isOpen && panelRef.value && !panelRef.value.contains(event.target)) {
    closePanel();
  }
};

// 5. Funciones principales.
function setTheme(theme) {
  currentTheme.value = theme;
  localStorage.setItem("theme", theme);
  if (theme === "dark") {
    document.body.classList.add("dark-mode");
  } else {
    document.body.classList.remove("dark-mode");
  }
}

function closePanel() {
  emit("close");
}

function toggleTheme() {
  const newTheme = currentTheme.value === "light" ? "dark" : "light";
  setTheme(newTheme);
}

// 6. Propiedad computada para el ícono dinámico.
const themeIcon = computed(() => {
  return currentTheme.value === "light" ? MoonIcon : SunIcon;
});

// 7. Ciclos de vida del componente.
onMounted(() => {
  // Añadir listener para clics fuera del panel
  document.addEventListener("mousedown", handleClickOutside);

  // Cargar el tema guardado al iniciar
  const savedTheme = localStorage.getItem("theme");
  const prefersDark =
    window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  if (savedTheme) {
    setTheme(savedTheme);
  } else if (prefersDark) {
    setTheme("dark");
  } else {
    setTheme("light");
  }
});

onUnmounted(() => {
  // Limpiar el listener al destruir el componente para evitar fugas de memoria
  document.removeEventListener("mousedown", handleClickOutside);
});
</script>

<style scoped>
/* Estilos generales del panel y overlay */
.config-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 199;
}
.change_theme {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  text-decoration: none;
}

.config-panel {
  position: fixed;
  top: 0;
  right: 0;
  height: 100vh;
  width: 320px;
  max-width: 85vw;
  background-color: var(--color-menu-display);
  box-shadow: -4px 0 15px rgba(0, 0, 0, 0.2);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  z-index: 200;
  transform: translateX(100%);
  transition: transform 0.3s ease-in-out;
}

.config-panel.is-open {
  transform: translateX(0);
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.config-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-header-text);
}

.close-button {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.close-button:hover {
  background-color: rgba(128, 128, 128, 0.2);
}

.close-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: var(--color-header-text);
}

.dropdown-divider {
  border: none;
  border-top: 1px solid var(--color-primary-button-text);
  margin: 0.5rem 0;
}

.config-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.section-title {
  margin-top: 6%;
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--color-header-text);
}

/* Estilos para el botón único de tema */
.theme-switcher-wrapper {
  margin-top: 0.5rem;
}

.theme-toggle-button {
  
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-background-soft);
  border: 1px solid;
  border-radius: 0.5rem; /* Esquinas redondeadas */
  border-color: var(--color-eslogan-primary);
  cursor: pointer;
  transition: all 0.2s ease;

  /* El ícono hereda este color primario */
  color: var(--color-eslogan-primary);
}

.theme-toggle-button:hover {
  border-color: var(--color-eslogan-primary);
  box-shadow: 0 0 0 3px var(--color-eslogan-hover);
}

.toggle-icon {
  width: 1.5rem; /* 24px */
  height: 1.5rem;
}
</style>
