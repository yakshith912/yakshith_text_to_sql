# 3.7 Database Tables

The AaiTech Industries database is composed of five core tables designed to track customers, products, suppliers, and order transactions. Below is the detailed structural schema for each table.

### 1. `customers` Table
This table stores the information of businesses or individuals who place orders.

| Field Name | Data Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `customer_id` | VARCHAR(10) | **Primary Key** | Unique identifier for the customer. |
| `company_name` | VARCHAR(100) | None | The name of the customer's organization. |
| `contact_name` | VARCHAR(100) | None | Primary contact person for the customer. |
| `city` | VARCHAR(50) | None | City where the customer is located. |
| `country` | VARCHAR(50) | None | Country where the customer is located. |

### 2. `orders` Table
This table records the overarching details of a purchase transaction.

| Field Name | Data Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | INT | **Primary Key** | Unique identifier for the order. |
| `customer_id` | VARCHAR(10) | **Foreign Key** | References `customer_id` in `customers`. |
| `order_date` | DATE | None | The date the order was placed. |
| `ship_city` | VARCHAR(50) | None | Destination city for the delivery. |
| `freight` | FLOAT | None | The calculated cost of shipping/freight. |

### 3. `order_details` Table
A junction table that records the specific products and quantities associated with an order.

| Field Name | Data Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | INT | **Primary Key, Foreign Key** | References `order_id` in `orders`. |
| `product_id` | INT | **Primary Key, Foreign Key** | References `product_id` in `products`. |
| `quantity` | INT | None | The number of units ordered. |
| `unit_price` | FLOAT | None | The price per unit at the time of the order. |

### 4. `products` Table
This table contains the catalog of items available for sale.

| Field Name | Data Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `product_id` | INT | **Primary Key** | Unique identifier for the product. |
| `product_name` | VARCHAR(100) | None | The name of the product. |
| `supplier_id` | INT | **Foreign Key** | References `supplier_id` in `suppliers`. |
| `category` | VARCHAR(50) | None | The category classification of the product. |
| `unit_price` | FLOAT | None | The current standard selling price. |

### 5. `suppliers` Table
This table holds information about the vendors who supply the products.

| Field Name | Data Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `supplier_id` | INT | **Primary Key** | Unique identifier for the supplier. |
| `company_name` | VARCHAR(100) | None | Name of the supplier's company. |
| `contact_name` | VARCHAR(100) | None | Primary contact person at the supplier. |
| `city` | VARCHAR(50) | None | City where the supplier is based. |
| `country` | VARCHAR(50) | None | Country where the supplier is based. |
