<template>
    <div class="calendar-container">
        <FullCalendar :options="calendarOptions" />
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import googleCalendarPlugin from '@fullcalendar/google-calendar';

const GOOGLE_CALENDAR_API_KEY = import.meta.env.VITE_GOOGLE_CALENDAR_API_KEY;
const GOOGLE_CALENDAR_ID = import.meta.env.VITE_GOOGLE_CALENDAR_ID;

const calendarOptions = ref({
    plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin, googleCalendarPlugin],
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    initialView: 'dayGridMonth',
    editable: true,
    selectable: true,
    selectConstraint: 'businessHours',
    eventClick: handleEventClick,
    select: handleDateSelect,
    googleCalendarApiKey: GOOGLE_CALENDAR_API_KEY,
    events: {
        googleCalendarId: GOOGLE_CALENDAR_ID
    },
    height: 'auto',
    contentHeight: 'auto'
});

function handleEventClick(info) {
    console.log('Event clicked:', info.event);
}

function handleDateSelect(info) {
    console.log('Date selected:', info.startStr, info.endStr);
}
</script>

<style scoped>
.calendar-container {
    background-color: var(--color-background-light);
    color: var(--color-text);
    padding: 2rem;
    border-radius: 0.5rem;
    margin-top: 2rem;
}

:deep(.fc) {
    font-family: inherit;
    --fc-text-muted: var(--color-text-light);
    --fc-bg-event: var(--color-primary-button-bg);
    --fc-event-text-color: white;
}

:deep(.fc-button-primary) {
    background-color: var(--color-primary-button-bg);
    border-color: var(--color-primary-button-bg);
}

:deep(.fc-button-primary:not(:disabled):hover) {
    background-color: var(--color-primary-button-bg);
    opacity: 0.9;
}

:deep(.fc-button-primary.fc-button-active) {
    background-color: var(--color-primary-button-bg);
}

:deep(.fc-daygrid-day) {
    background-color: var(--color-body-bg);
}

:deep(.fc-col-header-cell) {
    background-color: var(--color-background-light);
    color: var(--color-text);
}

:deep(.fc-daygrid-day-number) {
    color: var(--color-text);
}

:deep(.fc-daygrid-day-frame) {
    background-color: var(--color-body-bg);
}

:deep(.fc-event) {
    border-color: var(--color-primary-button-bg);
}
</style>