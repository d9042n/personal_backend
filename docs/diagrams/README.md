# API Flow Diagrams

This directory contains flow diagrams illustrating the API request/response cycles and data flow for key features of the Personal Backend API.

## Authentication Flow

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

## User Registration Flow

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

## Real-time Notifications Flow

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

## Session Management Flow

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

## Data Flow Patterns

### Request Flow

1. Client sends request with authentication
2. API validates authentication
3. API processes request
4. Database operations (if needed)
5. Response returned to client

### WebSocket Flow

1. Client establishes WebSocket connection
2. Real-time events pushed to client
3. Client acknowledges events
4. Connection maintained for continuous updates

### Error Flow

1. Client sends invalid request
2. API validates and catches error
3. Error response returned with appropriate status code
4. Client handles error appropriately

## Notes

- All diagrams are created using Mermaid.js syntax
- Diagrams show simplified flows, actual implementations may have additional steps
- Authentication is required for most endpoints (except public ones)
- WebSocket connections require valid JWT token
- Error handling is implemented at each step
