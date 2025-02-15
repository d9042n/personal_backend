# User Profile API

A RESTful API for user profile management focusing on simplicity and security.

## Features

- Public profile viewing
- User management (CRUD)
- Profile customization
- Secure authentication
- Real-time updates

## API Documentation

### Endpoints

| Method | Endpoint                       | Description         | Auth Required |
| ------ | ------------------------------ | ------------------- | ------------- |
| GET    | /api/users/public/{username}/  | View public profile | No            |
| POST   | /api/users/                    | Create user         | No            |
| GET    | /api/users/{username}/         | Get user details    | Yes           |
| PUT    | /api/users/{username}/         | Update user         | Yes           |
| PATCH  | /api/users/{username}/         | Partial update      | Yes           |
| DELETE | /api/users/{username}/         | Delete user         | Yes           |
| GET    | /api/users/{username}/profile/ | Get profile         | Yes           |
| PATCH  | /api/users/{username}/profile/ | Update profile      | Yes           |

### Examples

#### View Public Profile

```http
GET /api/users/public/{username}/
```

#### Create User

```http
POST /api/users/

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "secure_password",
  "profile": {
    "name": "New User",
    "title": "Developer",
    "is_available": true
  }
}
```

#### Update Profile

```http
PATCH /api/users/{username}/profile/

{
  "title": "Senior Developer",
  "badge": "Available"
}
```

## Security

- Authentication required for protected endpoints
- Rate limiting:
  - Public: 100 requests/day
  - Authenticated: 1000 requests/day
- Password requirements:
  - Minimum length: 10 characters
  - Complexity enforced
- CORS, XSS, and CSRF protection
- SSL/HTTPS required in production

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run tests
python manage.py test users
```

## Documentation

For detailed API documentation, visit:

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

Made with ❤️ for the Personal Website Project
