import { ref, onMounted, onUnmounted } from 'vue';

// Exportamos la función para poder usarla en otros componentes
export function useTheme() {
    // Estado reactivo para saber si el modo oscuro está activo
    const isDark = ref(false);

    // Función que revisa la clase del body y actualiza el estado
    function actualizarTema() {
        isDark.value = document.body.classList.contains('dark-mode');
    }

    // Cuando el componente que usa este composable se monta...
    onMounted(() => {
        // 1. Revisa el tema actual al inicio
        actualizarTema();

        // 2. Observa si la clase del body cambia en el futuro
        const observer = new MutationObserver(actualizarTema);
        observer.observe(document.body, {
            attributes: true,
            attributeFilter: ['class']
        });

        // 3. Limpia el observador cuando el componente se destruye
        onUnmounted(() => observer.disconnect());
    });

    // Devuelve el estado reactivo para que el componente pueda usarlo
    return {
        isDark
    };
}