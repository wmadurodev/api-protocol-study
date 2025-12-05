package com.apitest.graphql.resolver;

import com.apitest.graphql.model.OrderEntity;
import com.apitest.graphql.model.UserEntity;
import com.apitest.graphql.service.DataService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@Controller
@RequiredArgsConstructor
public class UserQueryResolver {

    private final DataService dataService;

    @QueryMapping
    public UserEntity user(@Argument Long id) {
        long startTime = System.nanoTime();
        try {
            UserEntity user = dataService.getUserById(id);
            long duration = System.nanoTime() - startTime;
            log.debug("user query completed in {} ms", duration / 1_000_000.0);
            return user;
        } catch (Exception e) {
            log.error("Error in user query", e);
            throw e;
        }
    }

    @QueryMapping
    public Map<String, Object> listUsers(@Argument Integer page,
                                         @Argument Integer size) {
        long startTime = System.nanoTime();
        try {
            int actualPage = page != null ? page : 0;
            int actualSize = size != null ? size : 20;
            List<UserEntity> users = dataService.listUsers(actualPage, actualSize);
            long totalElements = dataService.getTotalUsers();
            int totalPages = (int) Math.ceil((double) totalElements / actualSize);

            Map<String, Object> result = new HashMap<>();
            result.put("users", users);
            result.put("totalElements", totalElements);
            result.put("totalPages", totalPages);
            result.put("currentPage", actualPage);

            long duration = System.nanoTime() - startTime;
            log.debug("listUsers query completed in {} ms", duration / 1_000_000.0);

            return result;
        } catch (Exception e) {
            log.error("Error in listUsers query", e);
            throw e;
        }
    }

    @QueryMapping
    public List<OrderEntity> userOrders(@Argument Long userId) {
        long startTime = System.nanoTime();
        try {
            List<OrderEntity> orders = dataService.getUserOrders(userId);
            long duration = System.nanoTime() - startTime;
            log.debug("userOrders query completed in {} ms", duration / 1_000_000.0);
            return orders;
        } catch (Exception e) {
            log.error("Error in userOrders query", e);
            throw e;
        }
    }

    @QueryMapping
    public List<UserEntity> searchUsers(@Argument String query,
                                        @Argument Integer limit) {
        long startTime = System.nanoTime();
        try {
            int actualLimit = limit != null ? limit : 10;
            List<UserEntity> users = dataService.searchUsers(query, actualLimit);
            long duration = System.nanoTime() - startTime;
            log.debug("searchUsers query completed in {} ms", duration / 1_000_000.0);
            return users;
        } catch (Exception e) {
            log.error("Error in searchUsers query", e);
            throw e;
        }
    }
}
