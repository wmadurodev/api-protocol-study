package com.apitest.grpc.service;

import com.apitest.grpc.model.OrderEntity;
import com.apitest.grpc.model.OrderItemEntity;
import com.apitest.grpc.model.UserEntity;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import jakarta.annotation.PostConstruct;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import java.util.stream.Collectors;

@Slf4j
@Service
public class DataService {

    private static final int TOTAL_USERS = 10000;
    private static final int TOTAL_ORDERS = 50000;
    private static final long SEED = 12345L;
    private static final String[] FIRST_NAMES = {"John", "Jane", "Michael", "Sarah", "David", "Emily", "Robert", "Lisa", "William", "Jennifer"};
    private static final String[] LAST_NAMES = {"Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"};
    private static final String[] PRODUCTS = {"Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam", "Microphone", "Desk", "Chair", "Tablet"};

    private final Map<Long, UserEntity> users = new ConcurrentHashMap<>();
    private final Map<Long, List<OrderEntity>> userOrders = new ConcurrentHashMap<>();
    private final AtomicLong userIdCounter = new AtomicLong(1);
    private final AtomicLong orderIdCounter = new AtomicLong(1);
    private final AtomicLong orderItemIdCounter = new AtomicLong(1);

    @PostConstruct
    public void initialize() {
        log.info("Starting data generation with seed: {}", SEED);
        long startTime = System.currentTimeMillis();

        generateUsers();
        generateOrders();

        long endTime = System.currentTimeMillis();
        log.info("Data generation completed in {} ms. Users: {}, Orders: {}",
                endTime - startTime, users.size(), userOrders.values().stream().mapToLong(List::size).sum());
    }

    private void generateUsers() {
        Random random = new Random(SEED);

        for (int i = 0; i < TOTAL_USERS; i++) {
            Long userId = userIdCounter.getAndIncrement();
            String firstName = FIRST_NAMES[random.nextInt(FIRST_NAMES.length)];
            String lastName = LAST_NAMES[random.nextInt(LAST_NAMES.length)];
            String username = (firstName + lastName + i).toLowerCase();

            UserEntity user = UserEntity.builder()
                    .id(userId)
                    .username(username)
                    .email(username + "@example.com")
                    .firstName(firstName)
                    .lastName(lastName)
                    .createdAt(Instant.now().minusSeconds(random.nextInt(31536000))) // Random time within last year
                    .isActive(random.nextBoolean())
                    .build();

            users.put(userId, user);
            userOrders.put(userId, new ArrayList<>());
        }
    }

    private void generateOrders() {
        Random random = new Random(SEED + 1);
        List<Long> userIds = new ArrayList<>(users.keySet());

        for (int i = 0; i < TOTAL_ORDERS; i++) {
            Long userId = userIds.get(random.nextInt(userIds.size()));
            Long orderId = orderIdCounter.getAndIncrement();

            int itemCount = random.nextInt(5) + 1;
            List<OrderItemEntity> items = new ArrayList<>();
            BigDecimal total = BigDecimal.ZERO;

            for (int j = 0; j < itemCount; j++) {
                String product = PRODUCTS[random.nextInt(PRODUCTS.length)];
                int quantity = random.nextInt(5) + 1;
                BigDecimal price = BigDecimal.valueOf(random.nextDouble() * 1000).setScale(2, RoundingMode.HALF_UP);

                OrderItemEntity item = OrderItemEntity.builder()
                        .id(orderItemIdCounter.getAndIncrement())
                        .productName(product)
                        .quantity(quantity)
                        .unitPrice(price)
                        .build();

                items.add(item);
                total = total.add(price.multiply(BigDecimal.valueOf(quantity)));
            }

            OrderEntity.OrderStatus[] statuses = OrderEntity.OrderStatus.values();
            OrderEntity order = OrderEntity.builder()
                    .id(orderId)
                    .userId(userId)
                    .orderDate(Instant.now().minusSeconds(random.nextInt(31536000)))
                    .totalAmount(total.setScale(2, RoundingMode.HALF_UP))
                    .status(statuses[random.nextInt(statuses.length)])
                    .items(items)
                    .build();

            userOrders.get(userId).add(order);
        }
    }

    public UserEntity getUserById(Long id) {
        return users.get(id);
    }

    public List<UserEntity> listUsers(int page, int size) {
        return users.values().stream()
                .sorted(Comparator.comparing(UserEntity::getId))
                .skip((long) page * size)
                .limit(size)
                .collect(Collectors.toList());
    }

    public long getTotalUsers() {
        return users.size();
    }

    public UserEntity createUser(String username, String email, String firstName, String lastName) {
        Long userId = userIdCounter.getAndIncrement();
        UserEntity user = UserEntity.builder()
                .id(userId)
                .username(username)
                .email(email)
                .firstName(firstName)
                .lastName(lastName)
                .createdAt(Instant.now())
                .isActive(true)
                .build();

        users.put(userId, user);
        userOrders.put(userId, new ArrayList<>());
        return user;
    }

    public List<OrderEntity> getUserOrders(Long userId) {
        return userOrders.getOrDefault(userId, Collections.emptyList());
    }

    public List<UserEntity> searchUsers(String query, int limit) {
        String lowerQuery = query.toLowerCase();
        return users.values().stream()
                .filter(user ->
                        user.getUsername().toLowerCase().contains(lowerQuery) ||
                        user.getEmail().toLowerCase().contains(lowerQuery) ||
                        user.getFirstName().toLowerCase().contains(lowerQuery) ||
                        user.getLastName().toLowerCase().contains(lowerQuery)
                )
                .limit(limit)
                .collect(Collectors.toList());
    }

    public List<UserEntity> bulkCreateUsers(List<UserEntity> usersToCreate) {
        List<UserEntity> createdUsers = new ArrayList<>();
        for (UserEntity user : usersToCreate) {
            UserEntity created = createUser(
                    user.getUsername(),
                    user.getEmail(),
                    user.getFirstName(),
                    user.getLastName()
            );
            createdUsers.add(created);
        }
        return createdUsers;
    }
}
