package com.apitest.rest.controller;

import com.apitest.rest.dto.*;
import com.apitest.rest.model.OrderEntity;
import com.apitest.rest.model.OrderItemEntity;
import com.apitest.rest.model.UserEntity;
import com.apitest.rest.service.DataService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@RestController
@RequestMapping("/api/users")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class UserController {

    private final DataService dataService;

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        long startTime = System.nanoTime();
        try {
            UserEntity user = dataService.getUserById(id);
            if (user == null) {
                return ResponseEntity.notFound().build();
            }

            UserResponse response = convertToUserResponse(user);
            long duration = System.nanoTime() - startTime;
            log.debug("getUser completed in {} ms", duration / 1_000_000.0);

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("Error in getUser", e);
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping
    public ResponseEntity<PagedUsersResponse> listUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        long startTime = System.nanoTime();
        try {
            List<UserEntity> users = dataService.listUsers(page, size);
            long totalElements = dataService.getTotalUsers();
            int totalPages = (int) Math.ceil((double) totalElements / size);

            List<UserResponse> userResponses = users.stream()
                    .map(this::convertToUserResponse)
                    .collect(Collectors.toList());

            PagedUsersResponse response = PagedUsersResponse.builder()
                    .users(userResponses)
                    .totalElements(totalElements)
                    .totalPages(totalPages)
                    .currentPage(page)
                    .build();

            long duration = System.nanoTime() - startTime;
            log.debug("listUsers completed in {} ms", duration / 1_000_000.0);

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("Error in listUsers", e);
            return ResponseEntity.internalServerError().build();
        }
    }

    @PostMapping
    public ResponseEntity<UserResponse> createUser(@RequestBody CreateUserRequest request) {
        long startTime = System.nanoTime();
        try {
            UserEntity user = dataService.createUser(
                    request.getUsername(),
                    request.getEmail(),
                    request.getFirstName(),
                    request.getLastName()
            );

            UserResponse response = convertToUserResponse(user);
            long duration = System.nanoTime() - startTime;
            log.debug("createUser completed in {} ms", duration / 1_000_000.0);

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("Error in createUser", e);
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping("/{id}/orders")
    public ResponseEntity<List<OrderResponse>> getUserOrders(@PathVariable Long id) {
        long startTime = System.nanoTime();
        try {
            List<OrderEntity> orders = dataService.getUserOrders(id);

            List<OrderResponse> response = orders.stream()
                    .map(this::convertToOrderResponse)
                    .collect(Collectors.toList());

            long duration = System.nanoTime() - startTime;
            log.debug("getUserOrders completed in {} ms", duration / 1_000_000.0);

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("Error in getUserOrders", e);
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping("/search")
    public ResponseEntity<List<UserResponse>> searchUsers(
            @RequestParam String query,
            @RequestParam(defaultValue = "10") int limit) {
        long startTime = System.nanoTime();
        try {
            List<UserEntity> users = dataService.searchUsers(query, limit);

            List<UserResponse> response = users.stream()
                    .map(this::convertToUserResponse)
                    .collect(Collectors.toList());

            long duration = System.nanoTime() - startTime;
            log.debug("searchUsers completed in {} ms", duration / 1_000_000.0);

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("Error in searchUsers", e);
            return ResponseEntity.internalServerError().build();
        }
    }

    @PostMapping("/bulk")
    public ResponseEntity<List<UserResponse>> bulkCreateUsers(@RequestBody List<CreateUserRequest> requests) {
        long startTime = System.nanoTime();
        try {
            List<UserEntity> usersToCreate = requests.stream()
                    .map(req -> UserEntity.builder()
                            .username(req.getUsername())
                            .email(req.getEmail())
                            .firstName(req.getFirstName())
                            .lastName(req.getLastName())
                            .build())
                    .collect(Collectors.toList());

            List<UserEntity> createdUsers = dataService.bulkCreateUsers(usersToCreate);

            List<UserResponse> response = createdUsers.stream()
                    .map(this::convertToUserResponse)
                    .collect(Collectors.toList());

            long duration = System.nanoTime() - startTime;
            log.debug("bulkCreateUsers completed in {} ms", duration / 1_000_000.0);

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("Error in bulkCreateUsers", e);
            return ResponseEntity.internalServerError().build();
        }
    }

    private UserResponse convertToUserResponse(UserEntity entity) {
        return UserResponse.builder()
                .id(entity.getId())
                .username(entity.getUsername())
                .email(entity.getEmail())
                .firstName(entity.getFirstName())
                .lastName(entity.getLastName())
                .createdAt(entity.getCreatedAt())
                .isActive(entity.getIsActive())
                .build();
    }

    private OrderResponse convertToOrderResponse(OrderEntity entity) {
        List<OrderItemResponse> items = entity.getItems().stream()
                .map(this::convertToOrderItemResponse)
                .collect(Collectors.toList());

        return OrderResponse.builder()
                .id(entity.getId())
                .userId(entity.getUserId())
                .orderDate(entity.getOrderDate())
                .totalAmount(entity.getTotalAmount())
                .status(entity.getStatus().name())
                .items(items)
                .build();
    }

    private OrderItemResponse convertToOrderItemResponse(OrderItemEntity entity) {
        return OrderItemResponse.builder()
                .id(entity.getId())
                .productName(entity.getProductName())
                .quantity(entity.getQuantity())
                .unitPrice(entity.getUnitPrice())
                .build();
    }
}
