# User Registration Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant RegistrationEndpoint
    participant UserService

    User->>RegistrationEndpoint: Submits registration form
    RegistrationEndpoint->>UserService: Validates input
    UserService-->>RegistrationEndpoint: User created
    RegistrationEndpoint-->>User: Returns user details
```
