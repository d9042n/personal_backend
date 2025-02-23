# Real-time Notifications Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant WebSocketEndpoint
    participant NotificationService

    User->>WebSocketEndpoint: Establishes connection
    WebSocketEndpoint-->>User: Connection established
    NotificationService->>WebSocketEndpoint: Sends notifications
    WebSocketEndpoint-->>User: Delivers notifications
```
