# Edit User Profile Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant ProfileEndpoint
    participant UserService

    User->>ProfileEndpoint: Requests current profile
    ProfileEndpoint-->>User: Returns profile data
    User->>ProfileEndpoint: Submits updated profile
    ProfileEndpoint->>UserService: Validates input
    UserService-->>ProfileEndpoint: Updates user profile
    ProfileEndpoint-->>User: Returns updated profile
```
