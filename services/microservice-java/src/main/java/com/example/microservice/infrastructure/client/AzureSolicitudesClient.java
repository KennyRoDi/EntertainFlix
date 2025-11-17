package com.example.microservice.infrastructure.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Component
public class AzureSolicitudesClient {

    private final WebClient webClient;
    private final String apiKey;

    public AzureSolicitudesClient(
            @Value("${azure.api.subscription-key:}") String apiKey) {
        this.apiKey = apiKey;
        // Use APIM URL
        this.webClient = WebClient.builder()
                .baseUrl("https://entertainflix.azure-api.net/agendarsolicitudes")
                .build();
    }

    public Mono<String> updateSolicitudEstado(String solicitudId, String decision) {
        String estado = decision.equals("ACCEPTED") ? "aceptado" : "denegado";
        
        return webClient.patch()
                .uri("/solicitudes/{id}", solicitudId)
                .header("Ocp-Apim-Subscription-Key", apiKey)
                .header("Content-Type", "application/json")
                .bodyValue("{\"estado\":\"" + estado + "\"}")
                .retrieve()
                .bodyToMono(String.class)
                .doOnError(e -> System.err.println("Error updating Azure API: " + e.getMessage()));
    }
}