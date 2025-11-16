import asyncio
from typing import List, Dict, Optional
from app.domain.ports import EventConsumer, NotificationRepository
from app.application.use_cases import handle_raw_event


class StubEventConsumer(EventConsumer):
    """
    Consumer de prueba que lee de una lista de eventos en memoria.
    Podés ignorarlo si querés trabajar solo con el endpoint /events/test.
    """

    def __init__(
        self,
        repo: NotificationRepository,
        events: Optional[List[Dict]] = None,
        interval_seconds: float = 5.0,
    ) -> None:
        self.repo = repo
        self.events = events or []
        self.interval_seconds = interval_seconds
        self._running = False

    async def start(self) -> None:
        self._running = True
        while self._running:
            for event in self.events:
                handle_raw_event(event, self.repo)
            await asyncio.sleep(self.interval_seconds)

    def stop(self) -> None:
        self._running = False
