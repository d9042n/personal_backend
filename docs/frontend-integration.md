# 🖥 Frontend Integration Guide

## Overview

This guide provides instructions on how to integrate the Personal Backend API and WebSocket services into a frontend application. It covers authentication, user management, and real-time notifications.

## API Integration

### Setting Up API Calls

Use a library like Axios or Fetch API to make HTTP requests to the backend.

```javascript
import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://your-domain/api/",
  timeout: 1000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Example: User Login
async function login(usernameOrEmail, password) {
  const response = await apiClient.post("/login/", {
    username_or_email: usernameOrEmail,
    password,
  });
  return response.data;
}

// Usage example
async function handleLogin() {
  try {
    // Can use either username or email
    const { access, refresh } = await login(
      "john@example.com",
      "SecurePass123!"
    );
    // Or
    // const { access, refresh } = await login("johndoe", "SecurePass123!");
    accessToken = access;
    refreshToken = refresh;
  } catch (error) {
    // Handle login error
  }
}
```

### Handling Authentication

Store the access and refresh tokens securely (e.g., in memory or secure storage).

```javascript
let accessToken = "";
let refreshToken = "";

async function handleLogin() {
  const { access, refresh } = await login("johndoe", "SecurePass123!");
  accessToken = access;
  refreshToken = refresh;
}
```

### Making Authenticated Requests

Include the access token in the Authorization header for protected routes.

```javascript
async function fetchUserProfile() {
  const response = await apiClient.get("/users/johndoe/profile/", {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  return response.data;
}
```

## WebSocket Integration

### Setting Up WebSocket Connection

Establish a WebSocket connection to receive real-time notifications.

```javascript
const socket = new WebSocket("ws://your-domain/ws/notifications/");

socket.onopen = () => {
  console.log("WebSocket connection established");
};

socket.onmessage = (event) => {
  const notification = JSON.parse(event.data);
  handleNotification(notification);
};
```

### Handling Notifications

Implement a function to handle incoming notifications and update the UI accordingly.

```javascript
function handleNotification(notification) {
  switch (notification.type) {
    case "profile_update":
      updateProfileUI(notification.data);
      break;
    // Handle other notification types...
  }
}
```

## UI Components

### Notification Bell Component

Create a notification bell component to display the number of unread notifications.

```jsx
function NotificationBell({ count }) {
  return (
    <div className="notification-bell">
      <BellIcon />
      {count > 0 && <span className="badge">{count}</span>}
    </div>
  );
}
```

### Notification List Component

Display a list of notifications for the user.

```jsx
function NotificationList({ notifications }) {
  return (
    <div className="notification-list">
      {notifications.map((notification) => (
        <NotificationItem key={notification.id} notification={notification} />
      ))}
    </div>
  );
}
```

## Conclusion

Integrating the Personal Backend API and WebSocket services into your frontend application allows for a seamless user experience with real-time updates and secure user management. Follow the guidelines provided to ensure a smooth integration process.
