# 📊 API Flow Diagrams

[![API Status](https://img.shields.io/badge/API-Active-success)](https://github.com/yourusername/personal_backend)
[![Mermaid](https://img.shields.io/badge/Mermaid.js-Diagrams-blue)](https://mermaid.js.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This directory contains flow diagrams illustrating the API request/response cycles and data flow for key features of the Personal Backend API. These diagrams help visualize the interactions between different components of the system.

## 📑 Table of Contents

1. [Authentication Flow](#authentication-flow)
2. [User Registration Flow](#user-registration-flow)
3. [Real-time Notifications Flow](#real-time-notifications-flow)
4. [Session Management Flow](#session-management-flow)
5. [Data Flow Patterns](#data-flow-patterns)
6. [System Architecture](#system-architecture)

## 🔐 Authentication Flow

The following diagram illustrates the JWT authentication flow:

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Database

    Client->>API: POST /api/login/ (credentials)
    API->>Database: Validate credentials
    Database-->>API: User data
    API-->>Client: JWT tokens + user data

    Note over Client,API: For subsequent requests
    Client->>API: Request with Bearer token
    API->>API: Validate token
    API-->>Client: Protected resource
```

## 👤 User Registration Flow

The following diagram illustrates the user registration process:

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Database

    Client->>API: POST /api/users/ (user data)
    API->>API: Validate input
    API->>Database: Create user
    Database-->>API: User created
    API-->>Client: 201 Created + user data
```

## 🔔 Real-time Notifications Flow

The following diagram illustrates the WebSocket-based real-time notification system:

```mermaid
sequenceDiagram
    participant Client
    participant WebSocket
    participant API
    participant Database

    Client->>WebSocket: Connect (with token)
    WebSocket->>API: Authenticate connection
    API-->>WebSocket: Connection accepted
    WebSocket-->>Client: Connection established

    Note over API,Database: When notification created
    API->>Database: Create notification
    Database-->>API: Notification created
    API->>WebSocket: Push notification
    WebSocket-->>Client: Notification received

    Client->>API: PATCH /notifications/{id}/read/
    API->>Database: Update notification
    Database-->>API: Notification updated
    API-->>Client: 200 OK
```

## 📱 Session Management Flow

The following diagram illustrates the session management process:

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Cache
    participant Database

    Client->>API: GET /api/session/
    API->>Cache: Check session
    Cache-->>API: Session data
    API->>Database: Get user data
    Database-->>API: User data
    API-->>Client: Session + user data
```

## 🔄 Data Flow Patterns

### Request Flow

The standard request flow follows these steps:

1. Client sends request with authentication
2. API validates authentication
3. API processes request
4. Database operations (if needed)
5. Response returned to client

```mermaid
flowchart LR
    A[Client] -->|Request| B[API Gateway]
    B -->|Validate| C[Authentication]
    C -->|Process| D[API Endpoint]
    D -->|Query/Update| E[Database]
    E -->|Data| D
    D -->|Response| A
```

### WebSocket Flow

The WebSocket communication flow:

1. Client establishes WebSocket connection
2. Real-time events pushed to client
3. Client acknowledges events
4. Connection maintained for continuous updates

```mermaid
flowchart LR
    A[Client] -->|Connect| B[WebSocket Server]
    B -->|Authenticate| C[Auth Service]
    C -->|Validated| B
    B -->|Accept| A
    D[Event Source] -->|New Event| B
    B -->|Push Event| A
    A -->|Acknowledge| B
```

### Error Flow

The error handling flow:

1. Client sends invalid request
2. API validates and catches error
3. Error response returned with appropriate status code
4. Client handles error appropriately

```mermaid
flowchart LR
    A[Client] -->|Invalid Request| B[API Gateway]
    B -->|Validate| C[Validation Layer]
    C -->|Error| D[Error Handler]
    D -->|Format Error| E[Response Formatter]
    E -->|Error Response| A
```

## 🏗️ System Architecture

The overall system architecture:

```mermaid
flowchart TB
    Client[Client Applications]
    API[Django REST API]
    WS[WebSocket Server]
    DB[(PostgreSQL)]
    Cache[(Redis)]
    Celery[Celery Workers]

    Client <--> API
    Client <--> WS
    API <--> DB
    API <--> Cache
    WS <--> Cache
    API --> Celery
    Celery <--> DB
    Celery <--> Cache

    subgraph Backend
        API
        WS
        DB
        Cache
        Celery
    end
```

## 📝 Notes

- All diagrams are created using Mermaid.js syntax
- Diagrams show simplified flows, actual implementations may have additional steps
- Authentication is required for most endpoints (except public ones)
- WebSocket connections require valid JWT token
- Error handling is implemented at each step

## 🔍 Viewing the Diagrams

These diagrams can be viewed in any Markdown viewer that supports Mermaid.js, including:

- GitHub (natively supports Mermaid)
- VS Code with Markdown Preview Enhanced
- Mermaid Live Editor: https://mermaid.live/

---

For more information about the API, refer to the [main documentation](../README.md).
