from typing import Dict
from app.domain.models import Notification, NotificationType
from app.domain.ports import NotificationRepository


def handle_request_created_event(
    payload: Dict,
    repo: NotificationRepository
) -> Notification:
    """
    Evento cuando un cliente envía una solicitud a un servicio/ofertante.

    Ejemplo de payload:
    {
      "cliente":"CamiFlow de jesus",
      "correo":"camiflow@music.com",
      "telefono":"88883456",
      "mensaje":"231",
      "fecha":"2025-11-10",
      "ubicacion":"Heredia",
      "paquete":"Boda estándar",
      "artista":"CamiFlow",
      "estado":"pendiente",
      "id":"69163a62a0ea65f966833f36"
    }
    """

    artista = payload.get("artista")
    cliente = payload.get("cliente")
    paquete = payload.get("paquete")
    fecha = payload.get("fecha")
    ubicacion = payload.get("ubicacion")
    solicitud_id = payload.get("id")

    # La notificación va para el servicio/ofertante
    user_id = artista

    title = "Nueva solicitud de agenda"
    message = (
        f"Nueva solicitud de {cliente} para el paquete '{paquete}' "
        f"el {fecha} en {ubicacion} (ID solicitud: {solicitud_id})."
    )

    notification = Notification.new(
        user_id=user_id,
        type=NotificationType.REQUEST_CREATED,
        title=title,
        message=message,
        metadata={
            "raw_payload": payload,
            "request_id": solicitud_id,
            "cliente": cliente,
            "artista": artista,
        },
    )

    return repo.save(notification)


def handle_request_status_changed_event(
    payload: Dict,
    repo: NotificationRepository
) -> Notification:
    """
    Evento cuando el ofertante acepta o rechaza la solicitud.

    Ejemplo de payload:
    {
      "requestId":"TEST-001",
      "ofertantId":"testofertant",
      "customerId":"Test Client",
      "newStatus":"ACCEPTED",
      "timestamp":"2025-11-11T22:34:34.98540852",
      "reason":"Testing"
    }
    """

    request_id = payload.get("requestId")
    ofertant_id = payload.get("ofertantId")
    customer_id = payload.get("customerId")
    new_status = payload.get("newStatus")
    reason = payload.get("reason")

    # La notificación ahora va al cliente
    user_id = customer_id

    if new_status == "ACCEPTED":
        n_type = NotificationType.REQUEST_ACCEPTED
        title = "Tu solicitud fue aceptada"
        message = (
            f"Tu solicitud {request_id} fue aceptada por {ofertant_id}."
        )
    elif new_status == "REJECTED":
        n_type = NotificationType.REQUEST_REJECTED
        title = "Tu solicitud fue rechazada"
        message = (
            f"Tu solicitud {request_id} fue rechazada por {ofertant_id}."
        )
        if reason:
            message += f" Motivo: {reason}"
    else:
        # Si llega otro estado, lo tratamos como texto genérico
        n_type = NotificationType.REQUEST_REJECTED
        title = f"Cambio de estado: {new_status}"
        message = (
            f"Tu solicitud {request_id} cambió de estado a {new_status} "
            f"por {ofertant_id}."
        )

    notification = Notification.new(
        user_id=user_id,
        type=n_type,
        title=title,
        message=message,
        metadata={
            "raw_payload": payload,
            "request_id": request_id,
            "ofertant_id": ofertant_id,
        },
    )

    return repo.save(notification)


def handle_raw_event(payload: Dict, repo: NotificationRepository) -> Notification:
    """
    Router simple que decide qué tipo de evento es basado en las claves del JSON.
    - Si tiene 'newStatus' -> evento de cambio de estado (aceptar/rechazar).
    - Si no -> asumimos que es creación de solicitud.
    """

    if "newStatus" in payload:
        return handle_request_status_changed_event(payload, repo)
    else:
        return handle_request_created_event(payload, repo)
