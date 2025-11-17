<template>
  <div class="notifications-wrapper" ref="root">
    <button class="bell-button" @click.stop="toggleOpen">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 28 28"
      fill="none"
      class="w-7 h-7"
    >
      <g transform="translate(0, 2)">
        <path
          d="M20 10a6 6 0 00-12 0c0 4-1 5-2 6h16c-1-1-2-2-2-6z"
          stroke="#00C4CC"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />

        <path
          d="M15 21a2 2 0 01-4 0"
          stroke="#00C4CC"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </g>
    </svg>

        <span
        v-if="unreadCount > 0"
        class="absolute -top-1 right-0 w-3 h-3 rounded-full bg-red-500"
      ></span>
    </button>

    <div v-if="isOpen" class="dropdown">
      <div class="dropdown-header">
        <span>Notificaciones</span>
        <button class="refresh-btn" @click.stop="loadNotifications(false)">
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="#00C4CC"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="w-5 h-5"
        >
          <path d="M21 12a9 9 0 11-3.23-6.87" />
          <path d="M21 3v7h-7" />
        </svg>

        </button>
      </div>

      <div v-if="isLoading" class="dropdown-body">
        <p>Cargando notificaciones...</p>
      </div>

      <div v-else-if="error" class="dropdown-body error">
        <p>Error: {{ error }}</p>
      </div>

      <div v-else class="dropdown-body">
        <p v-if="notifications.length === 0">No tienes notificaciones.</p>

        <ul v-else class="notifications-list">
          <li
            v-for="n in notifications"
            :key="n.id"
            :class="['notification-item', { unread: !n.is_read }]"
            @click.stop="handleClickNotification(n)"
          >
            <div class="notification-title">
              {{ n.title }}
            </div>
            <div class="notification-message">
              {{ n.message }}
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import {
  fetchNotifications,
  markNotificationAsRead,
} from "@/services/notificationsApi";

const props = defineProps({
  userId: {
    type: String,
    required: true,
  },
});

const root = ref(null);
const notifications = ref([]);
const isOpen = ref(false);
const isLoading = ref(false);
const error = ref("");

const knownIds = ref(new Set());
const pollingIntervalId = ref(null);

const unreadCount = computed(() =>
  notifications.value.filter((n) => !n.is_read).length
);

async function loadNotifications(showNewPopup = true) {
  if (!props.userId) {
    console.warn("NotificationsBell: userId vacío", props.userId);
    return;
  }

  isLoading.value = true;
  error.value = "";

  try {
    console.log("Pidiendo notificaciones para:", props.userId);
    const data = await fetchNotifications(props.userId);
    console.log("Respuesta notificaciones:", data);

    if (showNewPopup) {
      const newOnes = data.filter((n) => !knownIds.value.has(n.id));
      if (newOnes.length > 0) {
        newOnes.forEach((n) => {
          console.log("Nueva notificación:", n.title, "-", n.message);
        });
      }
    }

    notifications.value = data;
    knownIds.value = new Set(data.map((n) => n.id));
  } catch (err) {
    console.error(err);
    error.value = err.message || "Error desconocido";
  } finally {
    isLoading.value = false;
  }
}

function toggleOpen() {
  isOpen.value = !isOpen.value;
  if (isOpen.value && notifications.value.length === 0) {
    // AQUÍ estaba el bug: antes llamabas a "cargarNotificaciones()"
    loadNotifications(false);
  }
}

async function handleClickNotification(notification) {
  try {
    const updated = await markNotificationAsRead(notification.id);
    notifications.value = notifications.value.map((n) =>
      n.id === updated.id ? updated : n
    );
  } catch (err) {
    console.error(err);
    alert("No se pudo marcar la notificación como leída");
  }
}

function handleClickOutside(event) {
  if (isOpen.value && root.value && !root.value.contains(event.target)) {
    isOpen.value = false;
  }
}

onMounted(() => {
  console.log("NotificationsBell montado con userId:", props.userId);

  if (props.userId) {
    loadNotifications(false);
    pollingIntervalId.value = setInterval(() => {
      loadNotifications(true);
    }, 10000); // 10s
  }

  window.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  if (pollingIntervalId.value) clearInterval(pollingIntervalId.value);
  window.removeEventListener("click", handleClickOutside);
});

watch(
  () => props.userId,
  (nuevo, viejo) => {
    console.log("Cambio de userId:", viejo, "→", nuevo);
    knownIds.value = new Set();
    notifications.value = [];

    if (pollingIntervalId.value) clearInterval(pollingIntervalId.value);

    if (nuevo) {
      loadNotifications(false);
      pollingIntervalId.value = setInterval(() => {
        loadNotifications(true);
      }, 10000);
    }
  }
);
</script>

<style scoped>
.notifications-wrapper {
  position: relative;
  display: inline-block;
}

.bell-button {
  position: relative;
  border: none;
  background: transparent;
  font-size: 1.4rem;
  cursor: pointer;
}

.badge {
  position: absolute;
  top: -4px;
  right: -8px;
  background: #ef4444;
  color: white;
  border-radius: 999px;
  padding: 0 6px;
  font-size: 0.7rem;
  font-weight: bold;
}

.dropdown {
  position: absolute;
  right: 0;
  margin-top: 8px;
  width: 260px;
  background: var(--color-menu-display);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 999;
  overflow: hidden;
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 10px;
  border-bottom: 1px solid #eee;
  font-weight: bold;
  font-size: 0.9rem;
}

.refresh-btn {
  border: none;
  background: transparent;
  cursor: pointer;
}

.dropdown-body {
  max-height: 260px;
  overflow-y: auto;
  padding: 8px 10px;
  font-size: 0.85rem;
}

.dropdown-body.error {
  color: #ef4444;
}

.notifications-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.notification-item {
  padding: 6px 4px;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 4px;
}

.notification-item.unread {
  background-color: var(--color-background-light);
  font-weight: 600;
}

.notification-item:hover {
  background-color: var(--color-solicitud);
}

.notification-title {
  font-size: 0.85rem;
}

.notification-message {
  font-size: 0.8rem;
  color: var(--color-secondary-button-text);
}
</style>
