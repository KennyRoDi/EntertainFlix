import json
import logging
import os
import threading
import time
import base64  # 👈 NUEVO

from azure.storage.queue import QueueClient

from app.application.use_cases import handle_raw_event
from app.domain.ports import NotificationRepository

logger = logging.getLogger(__name__)


def _consume_queue(connection_string: str, queue_name: str, repo: NotificationRepository):
    """
    Hilo que escucha una cola de Azure Storage Queue y manda cada mensaje
    a handle_raw_event(payload, repo).
    """
    print(f"👂 Escuchando cola: {queue_name}")
    logger.info(f"Starting consumer for queue: {queue_name}")

    queue_client = QueueClient.from_connection_string(
        conn_str=connection_string,
        queue_name=queue_name,
    )

    while True:
        try:
            messages = queue_client.receive_messages(
                messages_per_page=16,
                visibility_timeout=30,
            )

            processed_any = False

            for msg in messages:
                processed_any = True
                try:
                    body = msg.content  # normalmente string
                    logger.info(f"[{queue_name}] Raw message body: {repr(body)}")

                    # Asegurarnos de tener un str
                    if isinstance(body, bytes):
                        body = body.decode("utf-8", errors="replace")

                    # 1) Vacío -> lo borramos
                    if not body or not str(body).strip():
                        logger.warning(f"[{queue_name}] Mensaje vacío, se elimina")
                        queue_client.delete_message(msg)
                        continue

                    # 2) Intentar parsear JSON directo
                    payload = None
                    try:
                        payload = json.loads(body)
                        logger.info(f"[{queue_name}] Parsed payload (JSON directo): {payload}")
                    except json.JSONDecodeError:
                        # 3) Si falla, asumir que viene en Base64
                        try:
                            decoded_bytes = base64.b64decode(body)
                            decoded_str = decoded_bytes.decode("utf-8")
                            logger.info(f"[{queue_name}] Decoded Base64 -> {decoded_str!r}")
                            payload = json.loads(decoded_str)
                            logger.info(f"[{queue_name}] Parsed payload (desde Base64): {payload}")
                        except Exception as e:
                            logger.error(
                                f"[{queue_name}] Mensaje no es JSON válido ni Base64 de JSON, se elimina. "
                                f"body={repr(body)} error={e}"
                            )
                            queue_client.delete_message(msg)
                            continue

                    # 4) Ya tenemos un dict JSON -> usamos tu lógica de dominio
                    try:
                        handle_raw_event(payload, repo)
                    except Exception:
                        logger.exception(
                            f"[{queue_name}] Error procesando mensaje en handle_raw_event, "
                            f"quedará visible de nuevo"
                        )
                        # NO lo borramos, para que pueda re-intentarse o quedar como poison
                        continue

                    # 5) Borramos el mensaje porque se procesó bien
                    queue_client.delete_message(msg)

                except Exception:
                    logger.exception(
                        f"[{queue_name}] Error procesando mensaje, quedará visible de nuevo"
                    )

            if not processed_any:
                time.sleep(1)

        except Exception:
            logger.exception(f"Unexpected error in consumer for {queue_name}")
            time.sleep(5)


def start_queue_consumers(repo: NotificationRepository):
    """
    Arranca dos hilos:
    - Cola de decisiones (ACCEPTED / REJECTED): decision-events
    - Cola de solicitudes nuevas: solicitudes
    """

    print("👉 start_queue_consumers llamado")

    # 1) Leer variables de entorno
    conn_decisions = os.getenv("AZURE_STORAGE_QUEUE_CONNECTION_STRING")
    queue_decisions = os.getenv("AZURE_STORAGE_QUEUE_NAME")

    conn_requests = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    queue_requests = os.getenv("QUEUE_NAME")

    # 2) Debug: ver exactamente qué está leyendo
    print("conn_decisions repr:", repr(conn_decisions))
    print("queue_decisions repr:", repr(queue_decisions))
    print("conn_requests repr:", repr(conn_requests))
    print("queue_requests repr:", repr(queue_requests))

    if not all([conn_decisions, queue_decisions, conn_requests, queue_requests]):
        print("❌ Faltan variables de entorno para las colas de Azure Storage")
        logger.error("Faltan vars de entorno para las colas de Azure Storage")
        return

    threads = []

    configs = [
        (conn_decisions, queue_decisions),  # decision-events
        (conn_requests, queue_requests),    # solicitudes
    ]

    for conn_str, q_name in configs:
        print(f"🚀 Creando hilo para cola: {q_name}")
        t = threading.Thread(
            target=_consume_queue,
            args=(conn_str, q_name, repo),
            daemon=True,
        )
        t.start()
        threads.append(t)
        logger.info(f"Consumer thread started for queue: {q_name}")

    print("✅ Hilos de colas inicializados")
    return threads
