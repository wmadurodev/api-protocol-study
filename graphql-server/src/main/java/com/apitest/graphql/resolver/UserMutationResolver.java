package com.apitest.graphql.resolver;

import com.apitest.graphql.model.UserEntity;
import com.apitest.graphql.service.DataService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.stereotype.Controller;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Slf4j
@Controller
@RequiredArgsConstructor
public class UserMutationResolver {

    private final DataService dataService;

    @MutationMapping
    public UserEntity createUser(@Argument Map<String, String> input) {
        long startTime = System.nanoTime();
        try {
            UserEntity user = dataService.createUser(
                    input.get("username"),
                    input.get("email"),
                    input.get("firstName"),
                    input.get("lastName")
            );
            long duration = System.nanoTime() - startTime;
            log.debug("createUser mutation completed in {} ms", duration / 1_000_000.0);
            return user;
        } catch (Exception e) {
            log.error("Error in createUser mutation", e);
            throw e;
        }
    }

    @MutationMapping
    public List<UserEntity> bulkCreateUsers(@Argument List<Map<String, String>> inputs) {
        long startTime = System.nanoTime();
        try {
            List<UserEntity> usersToCreate = inputs.stream()
                    .map(input -> UserEntity.builder()
                            .username(input.get("username"))
                            .email(input.get("email"))
                            .firstName(input.get("firstName"))
                            .lastName(input.get("lastName"))
                            .build())
                    .collect(Collectors.toList());

            List<UserEntity> createdUsers = dataService.bulkCreateUsers(usersToCreate);
            long duration = System.nanoTime() - startTime;
            log.debug("bulkCreateUsers mutation completed in {} ms", duration / 1_000_000.0);
            return createdUsers;
        } catch (Exception e) {
            log.error("Error in bulkCreateUsers mutation", e);
            throw e;
        }
    }
}
