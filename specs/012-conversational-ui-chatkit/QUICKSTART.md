# Quick Start Guide: Conversational UI

Get started with the AI Assistant chat interface in 5 minutes.

## Prerequisites

- Node.js 18+ installed
- Frontend development server running
- Backend API running on `http://localhost:8000`
- User authenticated with JWT token

## Installation

Dependencies are already installed. If you need to reinstall:

```bash
cd frontend
npm install zustand react-markdown remark-gfm rehype-highlight
```

## Usage

### 1. Access the AI Assistant

Navigate to the AI Assistant page:
```
http://localhost:3000/dashboard/ai-assistant
```

Or click "AI Assistant" in the sidebar navigation.

### 2. Send Your First Message

Type a message in the input field and press Enter:
```
"Add a task to buy groceries"
```

The AI will respond and execute the task creation tool.

### 3. View Tool Execution

When the AI executes tools (like creating tasks), you'll see badges showing:
- Tool name (e.g., "add_task")
- Completion status (checkmark)

### 4. Handle Errors

If a message fails to send:
1. You'll see a "Failed" status with a red icon
2. Click the "Retry" button to resend
3. The error message will explain what went wrong

### 5. Start New Conversations

Click the "New Chat" button in the header to start a fresh conversation.

## Code Examples

### Using the Chat Store

```typescript
import { useChatStore } from "@/lib/stores/chatStore";

function MyComponent() {
  const {
    sendMessage,
    messages,
    isLoading,
    isSending,
    error,
    clearError,
  } = useChatStore();

  const handleSend = async () => {
    await sendMessage("Show me all my tasks");
  };

  return (
    <div>
      {error && <div className="error">{error}</div>}
      {messages.map((msg) => (
        <div key={msg.id}>
          <strong>{msg.role}:</strong> {msg.content}
        </div>
      ))}
      <button onClick={handleSend} disabled={isSending}>
        Send
      </button>
    </div>
  );
}
```

### Creating Custom Message Components

```typescript
import { ChatMessage } from "@/lib/types/chat";
import { Message } from "@/components/chat/Message";

function CustomMessageList({ messages }: { messages: ChatMessage[] }) {
  return (
    <div className="space-y-4">
      {messages.map((message) => (
        <Message
          key={message.id}
          message={message}
          onRetry={(id) => console.log("Retry:", id)}
        />
      ))}
    </div>
  );
}
```

### Accessing Conversation State

```typescript
import { useChatStore } from "@/lib/stores/chatStore";

function ConversationInfo() {
  const { currentConversationId, conversations } = useChatStore();

  const currentConversation = currentConversationId
    ? conversations[currentConversationId]
    : null;

  return (
    <div>
      <h3>Current Conversation</h3>
      <p>ID: {currentConversation?.id}</p>
      <p>Title: {currentConversation?.title}</p>
      <p>Messages: {currentConversation?.messages.length}</p>
    </div>
  );
}
```

## Common Tasks

### Add a Welcome Message

```typescript
const welcomeMessage: ChatMessage = {
  id: "welcome",
  role: "assistant",
  content: "Hi! How can I help you today?",
  timestamp: new Date(),
  status: "sent",
};

useChatStore.getState().addMessage(welcomeMessage);
```

### Clear All Messages

```typescript
useChatStore.getState().createNewConversation();
```

### Handle Authentication Errors

```typescript
const { error } = useChatStore();

if (error?.includes("Not authenticated")) {
  // Redirect to login
  router.push("/login");
}
```

### Customize Message Rendering

```typescript
import { MessageContent } from "@/components/chat/MessageContent";

function CustomMessage({ content }: { content: string }) {
  return (
    <div className="custom-message">
      <MessageContent content={content} />
    </div>
  );
}
```

## Markdown Support

The chat supports GitHub Flavored Markdown:

### Text Formatting
```
**bold text**
*italic text*
~~strikethrough~~
`inline code`
```

### Lists
```
- Bullet point 1
- Bullet point 2

1. Numbered item 1
2. Numbered item 2
```

### Code Blocks
````
```javascript
function hello() {
  console.log("Hello, world!");
}
```
````

### Links
```
[Link text](https://example.com)
```

## Troubleshooting

### Messages Not Sending

**Problem**: Messages fail to send with "Not authenticated" error.

**Solution**: Check that user is logged in and JWT token is valid:
```typescript
import { auth } from "@/lib/api/auth";

const user = auth.getUser();
const token = auth.getToken();

console.log("User:", user);
console.log("Token:", token);
```

### Backend Connection Failed

**Problem**: Messages fail with "backend connection" error.

**Solution**: Ensure backend is running on `http://localhost:8000`:
```bash
cd backend
python -m uvicorn src.main:app --reload
```

### Conversation Not Persisting

**Problem**: Conversation resets on page refresh.

**Solution**: Check localStorage for conversation ID:
```typescript
const conversationId = localStorage.getItem("currentConversationId");
console.log("Stored conversation ID:", conversationId);
```

### Markdown Not Rendering

**Problem**: Markdown appears as plain text.

**Solution**: Ensure `react-markdown` is installed:
```bash
npm install react-markdown remark-gfm rehype-highlight
```

### Dark Mode Issues

**Problem**: Colors don't look right in dark mode.

**Solution**: Check that dark mode classes are applied:
```typescript
// In your component
<div className="bg-white dark:bg-gray-900">
  {/* Content */}
</div>
```

## API Reference

### Chat Store Actions

#### `sendMessage(content: string): Promise<void>`
Sends a message to the AI assistant.

```typescript
await useChatStore.getState().sendMessage("Hello!");
```

#### `retryFailedMessage(messageId: string): Promise<void>`
Retries a failed message.

```typescript
await useChatStore.getState().retryFailedMessage("msg-123");
```

#### `createNewConversation(): void`
Creates a new conversation.

```typescript
useChatStore.getState().createNewConversation();
```

#### `loadConversation(id: string): Promise<void>`
Loads a conversation by ID (placeholder for future backend support).

```typescript
await useChatStore.getState().loadConversation("conv-123");
```

#### `clearError(): void`
Clears the current error state.

```typescript
useChatStore.getState().clearError();
```

#### `addMessage(message: ChatMessage): void`
Adds a message to the current conversation.

```typescript
useChatStore.getState().addMessage({
  id: "msg-123",
  role: "assistant",
  content: "Hello!",
  timestamp: new Date(),
  status: "sent",
});
```

#### `updateMessage(id: string, updates: Partial<ChatMessage>): void`
Updates an existing message.

```typescript
useChatStore.getState().updateMessage("msg-123", {
  status: "sent",
});
```

## Next Steps

1. **Test the interface**: Send various messages and test error handling
2. **Customize styling**: Modify components to match your brand
3. **Add features**: Implement conversation sidebar, search, etc.
4. **Write tests**: Add unit and integration tests
5. **Deploy**: Build and deploy to production

## Resources

- [Spec 012 Documentation](./spec.md)
- [Implementation Complete](./IMPLEMENTATION_COMPLETE.md)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
- [React Markdown Documentation](https://github.com/remarkjs/react-markdown)
- [Gemini API Documentation](https://ai.google.dev/docs)

## Support

For issues or questions:
1. Check the [Implementation Complete](./IMPLEMENTATION_COMPLETE.md) document
2. Review the [Spec 012](./spec.md) requirements
3. Check the backend logs for API errors
4. Verify authentication and JWT tokens

---

**Last Updated**: February 9, 2026  
**Version**: 1.0
