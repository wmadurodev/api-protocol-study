package com.apitest.grpc.service;

import com.apitest.grpc.*;
import com.apitest.grpc.model.OrderEntity;
import com.apitest.grpc.model.OrderItemEntity;
import com.apitest.grpc.model.UserEntity;
import com.google.protobuf.Timestamp;
import io.grpc.stub.StreamObserver;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import net.devh.boot.grpc.server.service.GrpcService;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@GrpcService
@RequiredArgsConstructor
public class UserGrpcService extends UserServiceGrpc.UserServiceImplBase {

    private final DataService dataService;

    @Override
    public void getUser(GetUserRequest request, StreamObserver<GetUserResponse> responseObserver) {
        long startTime = System.nanoTime();
        try {
            UserEntity userEntity = dataService.getUserById(request.getUserId());
            if (userEntity == null) {
                responseObserver.onError(new RuntimeException("User not found: " + request.getUserId()));
                return;
            }

            User user = convertToProtoUser(userEntity);
            GetUserResponse response = GetUserResponse.newBuilder()
                    .setUser(user)
                    .build();

            responseObserver.onNext(response);
            responseObserver.onCompleted();

            long duration = System.nanoTime() - startTime;
            log.debug("getUser completed in {} ms", duration / 1_000_000.0);
        } catch (Exception e) {
            log.error("Error in getUser", e);
            responseObserver.onError(e);
        }
    }

    @Override
    public void listUsers(ListUsersRequest request, StreamObserver<ListUsersResponse> responseObserver) {
        long startTime = System.nanoTime();
        try {
            int page = request.getPage();
            int size = request.getSize() > 0 ? request.getSize() : 20;

            List<UserEntity> userEntities = dataService.listUsers(page, size);
            long totalElements = dataService.getTotalUsers();
            int totalPages = (int) Math.ceil((double) totalElements / size);

            List<User> users = userEntities.stream()
                    .map(this::convertToProtoUser)
                    .collect(Collectors.toList());

            ListUsersResponse response = ListUsersResponse.newBuilder()
                    .addAllUsers(users)
                    .setTotalElements(totalElements)
                    .setTotalPages(totalPages)
                    .setCurrentPage(page)
                    .build();

            responseObserver.onNext(response);
            responseObserver.onCompleted();

            long duration = System.nanoTime() - startTime;
            log.debug("listUsers completed in {} ms", duration / 1_000_000.0);
        } catch (Exception e) {
            log.error("Error in listUsers", e);
            responseObserver.onError(e);
        }
    }

    @Override
    public void createUser(CreateUserRequest request, StreamObserver<CreateUserResponse> responseObserver) {
        long startTime = System.nanoTime();
        try {
            UserEntity userEntity = dataService.createUser(
                    request.getUsername(),
                    request.getEmail(),
                    request.getFirstName(),
                    request.getLastName()
            );

            User user = convertToProtoUser(userEntity);
            CreateUserResponse response = CreateUserResponse.newBuilder()
                    .setUser(user)
                    .build();

            responseObserver.onNext(response);
            responseObserver.onCompleted();

            long duration = System.nanoTime() - startTime;
            log.debug("createUser completed in {} ms", duration / 1_000_000.0);
        } catch (Exception e) {
            log.error("Error in createUser", e);
            responseObserver.onError(e);
        }
    }

    @Override
    public void getUserOrders(GetUserOrdersRequest request, StreamObserver<GetUserOrdersResponse> responseObserver) {
        long startTime = System.nanoTime();
        try {
            List<OrderEntity> orderEntities = dataService.getUserOrders(request.getUserId());

            List<Order> orders = orderEntities.stream()
                    .map(this::convertToProtoOrder)
                    .collect(Collectors.toList());

            GetUserOrdersResponse response = GetUserOrdersResponse.newBuilder()
                    .addAllOrders(orders)
                    .build();

            responseObserver.onNext(response);
            responseObserver.onCompleted();

            long duration = System.nanoTime() - startTime;
            log.debug("getUserOrders completed in {} ms", duration / 1_000_000.0);
        } catch (Exception e) {
            log.error("Error in getUserOrders", e);
            responseObserver.onError(e);
        }
    }

    @Override
    public void searchUsers(SearchUsersRequest request, StreamObserver<SearchUsersResponse> responseObserver) {
        long startTime = System.nanoTime();
        try {
            int limit = request.getLimit() > 0 ? request.getLimit() : 10;
            List<UserEntity> userEntities = dataService.searchUsers(request.getQuery(), limit);

            List<User> users = userEntities.stream()
                    .map(this::convertToProtoUser)
                    .collect(Collectors.toList());

            SearchUsersResponse response = SearchUsersResponse.newBuilder()
                    .addAllUsers(users)
                    .build();

            responseObserver.onNext(response);
            responseObserver.onCompleted();

            long duration = System.nanoTime() - startTime;
            log.debug("searchUsers completed in {} ms", duration / 1_000_000.0);
        } catch (Exception e) {
            log.error("Error in searchUsers", e);
            responseObserver.onError(e);
        }
    }

    @Override
    public void bulkCreateUsers(BulkCreateUsersRequest request, StreamObserver<BulkCreateUsersResponse> responseObserver) {
        long startTime = System.nanoTime();
        try {
            List<UserEntity> usersToCreate = request.getUsersList().stream()
                    .map(createRequest -> UserEntity.builder()
                            .username(createRequest.getUsername())
                            .email(createRequest.getEmail())
                            .firstName(createRequest.getFirstName())
                            .lastName(createRequest.getLastName())
                            .build())
                    .collect(Collectors.toList());

            List<UserEntity> createdUsers = dataService.bulkCreateUsers(usersToCreate);

            List<User> users = createdUsers.stream()
                    .map(this::convertToProtoUser)
                    .collect(Collectors.toList());

            BulkCreateUsersResponse response = BulkCreateUsersResponse.newBuilder()
                    .addAllUsers(users)
                    .build();

            responseObserver.onNext(response);
            responseObserver.onCompleted();

            long duration = System.nanoTime() - startTime;
            log.debug("bulkCreateUsers completed in {} ms", duration / 1_000_000.0);
        } catch (Exception e) {
            log.error("Error in bulkCreateUsers", e);
            responseObserver.onError(e);
        }
    }

    private User convertToProtoUser(UserEntity entity) {
        Timestamp createdAt = Timestamp.newBuilder()
                .setSeconds(entity.getCreatedAt().getEpochSecond())
                .setNanos(entity.getCreatedAt().getNano())
                .build();

        return User.newBuilder()
                .setId(entity.getId())
                .setUsername(entity.getUsername())
                .setEmail(entity.getEmail())
                .setFirstName(entity.getFirstName())
                .setLastName(entity.getLastName())
                .setCreatedAt(createdAt)
                .setIsActive(entity.getIsActive())
                .build();
    }

    private Order convertToProtoOrder(OrderEntity entity) {
        Timestamp orderDate = Timestamp.newBuilder()
                .setSeconds(entity.getOrderDate().getEpochSecond())
                .setNanos(entity.getOrderDate().getNano())
                .build();

        List<OrderItem> items = entity.getItems().stream()
                .map(this::convertToProtoOrderItem)
                .collect(Collectors.toList());

        return Order.newBuilder()
                .setId(entity.getId())
                .setUserId(entity.getUserId())
                .setOrderDate(orderDate)
                .setTotalAmount(entity.getTotalAmount().toString())
                .setStatus(entity.getStatus().name())
                .addAllItems(items)
                .build();
    }

    private OrderItem convertToProtoOrderItem(OrderItemEntity entity) {
        return OrderItem.newBuilder()
                .setId(entity.getId())
                .setProductName(entity.getProductName())
                .setQuantity(entity.getQuantity())
                .setUnitPrice(entity.getUnitPrice().toString())
                .build();
    }
}
