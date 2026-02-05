---
name: auth-skill
description: Implement secure authentication with signup, signin, password hashing, JWT tokens, and better auth integration.
---

# Authentication Skill

## Instructions

1. **User Management**
   - Implement user signup with validation
   - Secure password storage using hashing (bcrypt or Argon2)
   - Support user signin with email/username and password
   - Implement password reset and recovery flow

2. **Token Management**
   - Generate JWT tokens for session management
   - Include access and refresh tokens
   - Handle token expiration and renewal
   - Ensure secure storage of tokens (HTTP-only cookies or secure headers)

3. **Auth Integration**
   - Support role-based access control (RBAC)
   - Optional integration with OAuth providers (Google, GitHub, etc.)
   - Protect sensitive routes with middleware/auth guards
   - Log authentication events (login, failed attempts, password change)

## Best Practices
- Always hash passwords before storing
- Use environment variables for secret keys
- Validate inputs to prevent injection attacks
- Implement rate limiting to prevent brute-force attacks
- Keep JWT payload minimal and avoid sensitive info
- Mobile-first and API-friendly design

