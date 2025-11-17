package com.example.microservice.infrastructure.api.controller;

import com.example.microservice.application.dto.RequestDecisionRequestDTO;
import com.example.microservice.application.dto.RequestDecisionResponseDTO;
import com.example.microservice.application.service.RequestDecisionService;
import com.example.microservice.infrastructure.client.AzureSolicitudesClient;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/requests")
public class RequestDecisionController {
        private final RequestDecisionService requestDecisionService;
        private final AzureSolicitudesClient azureClient;

        @Autowired
        public RequestDecisionController(
                        RequestDecisionService requestDecisionService,
                        AzureSolicitudesClient azureClient) {
                this.requestDecisionService = requestDecisionService;
                this.azureClient = azureClient;
        }

        @PostMapping("/{id}/decision")
        public Mono<ResponseEntity<RequestDecisionResponseDTO>> makeDecisionPost(
                        @PathVariable("id") String requestId,
                        @Valid @RequestBody RequestDecisionRequestDTO request,
                        Authentication authentication) {

                String userId = authentication != null
                                ? authentication.getName()
                                : "SYSTEM";

                RequestDecisionResponseDTO response = requestDecisionService.makeDecision(request, userId);

                // Update Azure API
                return azureClient.updateSolicitudEstado(requestId, request.getDecision())
                                .map(ignored -> new ResponseEntity<>(response, HttpStatus.CREATED))
                                .onErrorReturn(new ResponseEntity<>(response, HttpStatus.CREATED)); // Still return
                                                                                                    // success locally
        }

        @PatchMapping("/{id}/decision")
        public Mono<ResponseEntity<RequestDecisionResponseDTO>> makeDecisionPatch(
                        @PathVariable("id") String requestId,
                        @Valid @RequestBody RequestDecisionRequestDTO request,
                        Authentication authentication) {

                String userId = authentication != null
                                ? authentication.getName()
                                : "SYSTEM";

                RequestDecisionResponseDTO response = requestDecisionService.makeDecision(request, userId);

                // Update Azure API
                return azureClient.updateSolicitudEstado(requestId, request.getDecision())
                                .map(ignored -> new ResponseEntity<>(response, HttpStatus.OK))
                                .onErrorReturn(new ResponseEntity<>(response, HttpStatus.OK)); // Still return success
                                                                                               // locally
        }

        @GetMapping("/{id}/status")
        public ResponseEntity<String> getRequestStatus(@PathVariable("id") String requestId) {
                return ResponseEntity.ok(
                                String.format("{\"message\":\"Request %s status check not yet implemented\"}",
                                                requestId));
        }
}