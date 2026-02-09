# ChatBot Component

AI-powered task management chatbot with floating UI.

## Features

- 🤖 Floating chat button (bottom-right corner)
- 💬 Real-time messaging interface
- 🎨 Beautiful gradient design with animations
- 🌙 Dark mode support
- ⌨️ Keyboard shortcuts (Enter to send)
- 📱 Responsive design

## Usage

The chatbot is automatically included in the dashboard layout. It appears as a floating button in the bottom-right corner of all dashboard pages.

### User Interactions

1. **Open Chat**: Click the floating message icon
2. **Send Message**: Type and press Enter or click Send button
3. **Close Chat**: Click the X button in the header

## Integration with MCP Server

To connect the chatbot to your MCP server backend:

1. Update the `handleSend` function in `ChatBot.tsx`
2. Replace the TODO comment with actual API call:

```typescript
const response = await fetch("http://localhost:8001/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    user_id: userId, // Get from auth context
    message: input,
  }),
});

const data = await response.json();
```

3. The MCP server should handle:
   - Natural language processing
   - Task creation/updates
   - Task queries
   - Conversation history

## Customization

### Colors

Edit the gradient colors in the component:
- Button: `from-blue-600 to-purple-600`
- Header: `from-blue-600 to-purple-600`
- User messages: `bg-blue-600`
- Assistant messages: `bg-gray-100 dark:bg-gray-800`

### Position

Change the floating button position by modifying:
```tsx
className="fixed bottom-6 right-6 z-50"
```

### Size

Adjust chat window dimensions:
```tsx
className="w-96 h-[600px]"
```

## Dependencies

- `framer-motion` - Animations
- `lucide-react` - Icons
- `@radix-ui/react-scroll-area` - Scrollable area
- Shadcn UI components (Button, Input)

## File Structure

```
components/chatbot/
├── ChatBot.tsx       # Main chatbot component
└── README.md         # This file
```

## Next Steps

1. ✅ UI Component created
2. ⏳ Connect to MCP server backend
3. ⏳ Add authentication (user_id)
4. ⏳ Implement conversation history
5. ⏳ Add typing indicators
6. ⏳ Add message timestamps
7. ⏳ Add file attachments support

## API Integration Example

```typescript
// Example API service
export async function sendChatMessage(userId: string, message: string) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getToken()}`,
    },
    body: JSON.stringify({
      user_id: userId,
      message: message,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to send message");
  }

  return response.json();
}
```

## Testing

1. Start the frontend: `npm run dev`
2. Navigate to any dashboard page
3. Click the floating chat button
4. Type a message and press Enter
5. Verify the UI responds correctly

## Troubleshooting

**Chatbot not appearing:**
- Check that LayoutClient includes `<ChatBot />`
- Verify z-index is high enough (z-50)
- Check browser console for errors

**Styling issues:**
- Ensure Tailwind CSS is configured
- Check dark mode is working
- Verify framer-motion is installed

**API errors:**
- Check MCP server is running on port 8001
- Verify CORS is configured
- Check authentication tokens
