package com.apitest.rest.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PagedUsersResponse {
    private List<UserResponse> users;
    private Long totalElements;
    private Integer totalPages;
    private Integer currentPage;
}
