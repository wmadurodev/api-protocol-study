package com.apitest.grpc.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderEntity {
    private Long id;
    private Long userId;
    private Instant orderDate;
    private BigDecimal totalAmount;
    private OrderStatus status;

    @Builder.Default
    private List<OrderItemEntity> items = new ArrayList<>();

    public enum OrderStatus {
        PENDING, COMPLETED, CANCELLED
    }
}
