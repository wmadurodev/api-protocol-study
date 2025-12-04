## 🚀 Project Specification: API Performance Comparison

### 🎯 Objective

The primary goal of this project is to rigorously test and compare the **performance metrics** of **gRPC**, **REST**, and **GraphQL** when serving the same dataset under similar conditions. The comparison will focus on **latency**, **network resource usage**, and **server resource consumption**.

---

### 💻 Technology Stack

| Component | Technology | Version/Framework | Role |
| :--- | :--- | :--- | :--- |
| **Client** | JavaScript/React | React 18+ (Vite/Next.js) | UI and simultaneous API calling |
| **Server Base** | Java | Spring Boot 3+ | Backend API implementation base |
| **gRPC Server** | Java | Spring Boot Starter for gRPC | Implements the gRPC API |
| **REST Server** | Java | Spring Web | Implements the RESTful API |
| **GraphQL Server**| Java | Spring for GraphQL (or DGS) | Implements the GraphQL API |

---

### 🏛️ Project Structure

The project will consist of four distinct, interconnected applications for clear **independent resource monitoring**:

1.  **`performance-client`** (React)
2.  **`grpc-server`** (Spring Boot)
3.  **`rest-server`** (Spring Boot)
4.  **`graphql-server`** (Spring Boot)

---

### ⚙️ Implementation Details

#### 1. Data Model (Product/Catalog Item)

All services must expose an endpoint that returns a list of **mock product/catalog items**.

* **Data Structure (`Product`):**
    * `id` (String/Integer)
    * `name` (String)
    * `description` (String - A longer text, e.g., 256 characters)
    * `price` (Double)
    * `stockQuantity` (Integer)
    * `category` (String)
    * `createdAt` (Long/Date String)
* **Dataset Size:** A fixed, large dataset (e.g., **5,000 to 10,000 items**) should be loaded into memory or a lightweight, fast local database (H2/in-memory) for quick, consistent retrieval across all services.

#### 2. Service Endpoints (Same Data, Different Protocols)

| Service Project | Protocol/Method | Endpoint/RPC | Data Contract | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **`grpc-server`** | Unary RPC | `ProductService.getProducts` | **Protobuf** definition of the `Product` message and a list response. | Efficient, binary serialization over HTTP/2. |
| **`rest-server`** | GET | `/api/v1/products` | **JSON** serialization of the Product List. | Standard REST endpoint over HTTP/1.1 or HTTP/2. |
| **`graphql-server`** | POST | `/graphql` | **GraphQL Query** to fetch all defined product fields (`id`, `name`, etc.). | Allows the client to request all required fields (mimicking the others). |

#### 3. Client Implementation (`performance-client`)

The React client acts as the testing harness.

* **Interface:** A simple UI with a **"Run Test"** button, input for the number of iterations/concurrency level, and clear display areas for results.
* **Execution Rule:** Upon clicking "Run Test," the client must execute **one call to *each* of the three server endpoints** in a parallel/simultaneous manner (e.g., using `Promise.all` in JavaScript).
* **Testing Requirement:** Include a loop to run the test **100 times** to gather statistically significant average metrics.

---

### 📏 Performance Metrics & Measurement

The following metrics will be tracked and compared. Server-side metrics require using tools like Spring Boot Actuator, JMX, or external system monitoring (e.g., Prometheus/JVisualVM).

| Metric | Measurement Tool/Location | Calculation/Focus |
| :--- | :--- | :--- |
| **End-to-End Latency** | **Client-side** (Browser `Performance API`) | Time from request initiation to the completion of the `onload` event (full response received). |
| **Payload Size** | **Client-side** (Browser DevTools/