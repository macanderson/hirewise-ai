# Authentication System

This document describes the authentication system implemented for the web application.

## Overview

The authentication system integrates with the FastAPI backend at `/api/v1/auth/login` and provides:

- User login with email/password
- JWT token management
- Tenant-based authentication
- Automatic token storage and retrieval
- Protected routes and redirects

## Architecture

### API Client (`src/lib/api.ts`)

- Handles HTTP requests to the FastAPI server
- Implements OAuth2PasswordRequestForm format for login
- Manages tenant ID headers
- Provides typed interfaces for requests/responses

### Authentication Manager (`src/lib/auth.ts`)

- Manages JWT tokens in browser cookies
- Handles tenant ID storage in localStorage
- Provides login/logout functionality
- Automatic token validation and cleanup

### Login Page (`src/app/(auth)/login/page.tsx`)

- Form-based authentication UI
- Email/password validation
- Optional tenant ID input
- Error handling and loading states
- Redirects to dashboard on success

### Dashboard Page (`src/app/dashboard/page.tsx`)

- Protected route example
- Displays user information
- Logout functionality
- Authentication state checking

## Usage

### Login Flow

1. User enters email, password, and optional tenant ID
2. Form submits to FastAPI `/api/v1/auth/login` endpoint
3. On success, JWT token is stored in cookies
4. User is redirected to dashboard
5. Dashboard validates token and displays user info

### API Requirements

The FastAPI server expects:

- **Method**: POST
- **Endpoint**: `/api/v1/auth/login`
- **Content-Type**: `application/x-www-form-urlencoded` (OAuth2PasswordRequestForm)
- **Headers**: `X-Tenant-Id` (optional, but required by server for some operations)
- **Body**: `username` (email) and `password` fields

### Token Management

- Tokens are stored as secure HTTP-only cookies
- Automatic expiration handling
- Token validation on protected routes
- Cleanup on logout or invalid tokens

### Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Security Features

1. **Secure Cookie Storage**: Tokens stored with `secure`, `samesite=strict` flags
2. **Automatic Cleanup**: Invalid tokens are automatically removed
3. **Protected Routes**: Dashboard checks authentication before rendering
4. **Error Handling**: Graceful handling of network and authentication errors
5. **Tenant Isolation**: Support for multi-tenant architecture

## Testing

### Prerequisites

1. FastAPI server running on `http://localhost:8000`
2. Valid user account in the database
3. Tenant ID (if required by your setup)

### Test Flow

1. Navigate to `/login`
2. Enter valid credentials
3. Optionally enter tenant ID
4. Submit form
5. Should redirect to `/dashboard` with user info displayed

### Error Cases

- Invalid credentials → Error message displayed
- Network errors → Error message displayed
- Missing tenant ID (if required) → Server error displayed
- Invalid token → Automatic redirect to login

## Integration with FastAPI

The system is designed to work with the existing FastAPI authentication service:

```python
# FastAPI endpoint expects:
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None
):
    # Handles username/password authentication
    # Returns JWT token
```

### Required Headers

- `X-Tenant-Id`: Required for multi-tenant operations
- `Content-Type`: `application/x-www-form-urlencoded`
- `Accept`: `application/json`

### Response Format

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure FastAPI CORS settings allow the frontend domain
2. **Tenant ID Required**: Some endpoints require `X-Tenant-Id` header
3. **Token Expiration**: Tokens expire and need refresh (not yet implemented)
4. **Network Errors**: Check if FastAPI server is running on correct port

### Debug Tips

1. Check browser Network tab for API requests
2. Verify token storage in browser cookies
3. Check FastAPI logs for authentication errors
4. Ensure environment variables are set correctly
