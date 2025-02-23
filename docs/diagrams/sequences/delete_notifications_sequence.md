# Delete Notifications Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant NotificationList
    participant NotificationEndpoint

    User->>NotificationList: Views notifications
    User->>NotificationEndpoint: Selects notification to delete
    NotificationEndpoint-->>User: Removes notification
```
