# Chat API Documentation

## Overview

The Chat API provides a natural language interface for task management powered by Google Gemini AI. Users can interact with their tasks using conversational language instead of remembering specific commands.

## Base URL

```
http://localhost:8000
```

## Authentication

All endpoints require JWT authentication via Bearer token in the Authorization header.

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Send Chat Message

Send a message to the Todo Assistant and receive a response.

**Endpoint:** `POST /api/{user_id}/chat`

**Path Parameters:**
- `user_id` (string, required): The authenticated user's ID (must match JWT token)

**Request Body:**
```json
{
  "message": "string (1-2000 characters, required)",
  "conversation_id": "string (UUID, optional)"
}
```

**Response:** `200 OK`
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "I've added 'Buy groceries' to your task list!",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "parameters": {
        "title": "Buy groceries",
        "description": ""
      },
      "result": {
        "task_id": "123",
        "title": "Buy groceries"
      }
    }
  ],
  "timestamp": "2026-02-09T10:30:00Z"
}
```

**Error Responses:**

- `400 Bad Request`: Invalid request format
```json
{
  "detail": "Message cannot be empty"
}
```

- `401 Unauthorized`: Missing or invalid authentication token
```json
{
  "detail": "Invalid or expired token"
}
```

- `403 Forbidden`: User ID mismatch
```json
{
  "detail": "You do not have permission to access this user's resources"
}
```

- `500 Internal Server Error`: Server error
```json
{
  "detail": "Sorry, I encountered an error processing your message"
}
```

## Usage Examples

### Example 1: Add a Task

**Request:**
```bash
curl -X POST "http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440000/chat" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

**Response:**
```json
{
  "conversation_id": "650e8400-e29b-41d4-a716-446655440001",
  "message": "I've added 'Buy groceries' to your task list!",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "parameters": {
        "title": "Buy groceries",
        "description": ""
      },
      "result": {
        "task_id": "123",
        "title": "Buy groceries",
        "status": "pending"
      }
    }
  ],
  "timestamp": "2026-02-09T10:30:00.000Z"
}
```

### Example 2: List Tasks

**Request:**
```bash
curl -X POST "http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440000/chat" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me my tasks",
    "conversation_id": "650e8400-e29b-41d4-a716-446655440001"
  }'
```

**Response:**
```json
{
  "conversation_id": "650e8400-e29b-41d4-a716-446655440001",
  "message": "You have 2 tasks:\n1. Buy groceries (pending)\n2. Call mom (pending)",
  "tool_calls": [
    {
      "tool_name": "list_tasks",
      "parameters": {},
      "result": {
        "tasks": [
          {"id": "123", "title": "Buy groceries", "status": "pending"},
          {"id": "124", "title": "Call mom", "status": "pending"}
        ]
      }
    }
  ],
  "timestamp": "2026-02-09T10:31:00.000Z"
}
```

### Example 3: Complete a Task

**Request:**
```bash
curl -X POST "http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440000/chat" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Mark task 123 as done",
    "conversation_id": "650e8400-e29b-41d4-a716-446655440001"
  }'
```

**Response:**
```json
{
  "conversation_id": "650e8400-e29b-41d4-a716-446655440001",
  "message": "Great job! I've marked 'Buy groceries' as completed! 🎉",
  "tool_calls": [
    {
      "tool_name": "complete_task",
      "parameters": {
        "task_id": "123"
      },
      "result": {
        "success": true,
        "task_id": "123"
      }
    }
  ],
  "timestamp": "2026-02-09T10:32:00.000Z"
}
```

## Natural Language Capabilities

The assistant understands various ways to express the same intent:

### Adding Tasks
- "Add a task to buy groceries"
- "Create a new task: Call mom"
- "Remind me to finish the report"
- "I need to buy milk"

### Listing Tasks
- "Show me my tasks"
- "What do I need to do?"
- "List all my tasks"
- "What's on my todo list?"

### Completing Tasks
- "Mark task 123 as done"
- "Complete the grocery task"
- "I finished buying groceries"
- "Task 123 is complete"

### Deleting Tasks
- "Delete task 123"
- "Remove the grocery task"
- "Cancel the meeting task"

### Updating Tasks
- "Change task 123 title to 'Buy milk'"
- "Update the grocery task description"
- "Rename task 123"

## Rate Limits

### Gemini API (Free Tier)
- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per day

If you exceed these limits, you'll receive a `429 Too Many Requests` error.

## Best Practices

1. **Reuse Conversation IDs**: Include the `conversation_id` from previous responses to maintain context
2. **Handle Errors Gracefully**: Always check for error responses and display user-friendly messages
3. **Keep Messages Concise**: While the limit is 2000 characters, shorter messages work better
4. **Monitor Rate Limits**: Track your API usage to avoid hitting limits
5. **Validate User IDs**: Always ensure the user_id in the URL matches the authenticated user

## Security

- All requests must include a valid JWT token
- User IDs are validated against the authenticated user
- Users can only access their own conversations and tasks
- Conversation history is isolated per user

## OpenAPI Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Support

For issues or questions:
- Check the troubleshooting guide in `SETUP_COMPLETE.md`
- Review the implementation status in `specs/011-openai-agents-chat-api/IMPLEMENTATION_STATUS.md`
- Test your setup with `backend/test_gemini_connection.py`
