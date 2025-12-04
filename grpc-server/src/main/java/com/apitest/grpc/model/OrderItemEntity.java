package com.apitest.grpc.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderItemEntity {
    private Long id;
    private String productName;
    private Integer quantity;
    private BigDecimal unitPrice;
}
