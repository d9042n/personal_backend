# User Login Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant LoginEndpoint
    participant AuthService

    User->>LoginEndpoint: Submits login credentials
    LoginEndpoint->>AuthService: Authenticates user
    AuthService-->>LoginEndpoint: Generates tokens
    LoginEndpoint-->>User: Returns tokens and user details
```
