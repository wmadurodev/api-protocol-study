package com.apitest.graphql.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserEntity {
    private Long id;
    private String username;
    private String email;
    private String firstName;
    private String lastName;
    private OffsetDateTime createdAt;
    private Boolean isActive;

    @Builder.Default
    private List<OrderEntity> orders = new ArrayList<>();
}
