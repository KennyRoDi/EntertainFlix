const API_BASE = "http://127.0.0.1:8000"; //cambiar cuando monte con azure

export async function fetchNotifications(userId) {
  const url = `${API_BASE}/notifications?user_id=${encodeURIComponent(userId)}`;
  const res = await fetch(url);

  if (!res.ok) {
    throw new Error(`Error al obtener notificaciones: ${res.status}`);
  }

  return await res.json(); 
}

export async function markNotificationAsRead(notificationId) {
  const url = `${API_BASE}/notifications/${encodeURIComponent(
    notificationId
  )}/read`;

  const res = await fetch(url, {
    method: "PATCH",
  });

  if (!res.ok) {
    throw new Error(`Error al marcar como leída: ${res.status}`);
  }

  return await res.json();
}
