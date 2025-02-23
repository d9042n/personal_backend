# Mark Notifications as Read Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant NotificationList
    participant NotificationEndpoint

    User->>NotificationList: Views notifications
    User->>NotificationEndpoint: Selects notification to mark as read
    NotificationEndpoint-->>User: Updates read status
```
