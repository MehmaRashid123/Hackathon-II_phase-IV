# Implementation Tasks: Conversational UI with OpenAI ChatKit

**Branch**: `012-conversational-ui-chatkit` | **Date**: 2026-02-09
**Status**: Ready for Implementation

## Overview
32 tasks organized into 9 phases for implementing modern chat UI with OpenAI ChatKit.

---

## Phase 1: Setup & Dependencies (3 tasks)

### 1.1 Install OpenAI ChatKit and Dependencies (30 min, P0)
- Add @openai/chatkit, zustand, react-markdown to package.json
- Install dependencies
- Verify imports work
- **Commands**: `npm install @openai/chatkit zustand react-markdown`

### 1.2 Create TypeScript Types for Chat (45 min, P0)
- Define ChatMessage, Conversation, ChatState interfaces
- Add ToolCall and MessageStatus types
- **File**: `frontend/lib/types/chat.ts`

### 1.3 Set Up Zustand Store (1 hour, P0)
- Create chat store with state and actions
- Implement sendMessage, loadConversation, createNewConversation actions
- Add localStorage persistence for conversation ID
- **File**: `frontend/lib/stores/chatStore.ts`
- **Depends on**: 1.2

---

## Phase 2: API Integration (2 tasks)

### 2.1 Create Chat API Client (1.5 hours, P0)
- Implement sendMessage, loadConversation, listConversations methods
- Add JWT authentication headers
- Implement retry logic and error handling
- **File**: `frontend/lib/api/chat.ts`
- **Depends on**: 1.2

### 2.2 Create Custom Hooks (1 hour, P0)
- Implement useChat hook (connects store to components)
- Implement useChatHistory hook (loads conversation history)
- Implement useOptimisticUI hook (handles optimistic updates)
- **Files**: `frontend/lib/hooks/useChat.ts`, `useChatHistory.ts`, `useOptimisticUI.ts`
- **Depends on**: 1.3, 2.1

---

## Phase 3: Core Components (8 tasks)

### 3.1 Create ChatContainer Component (1 hour, P0)
- Main wrapper for chat interface
- Integrate OpenAI ChatKit components
- Handle layout and composition
- **File**: `frontend/components/chat/ChatContainer.tsx`
- **Depends on**: 1.1

### 3.2 Create ChatHeader Component (45 min, P0)
- Display conversation title
- Add "New Conversation" button
- **File**: `frontend/components/chat/ChatHeader.tsx`

### 3.3 Create Message Component (1 hour, P0)
- Render individual message
- Support user, assistant, system roles
- Display timestamp
- **File**: `frontend/components/chat/Message.tsx`
- **Depends on**: 1.2

### 3.4 Create MessageContent Component (1 hour, P0)
- Render message text with markdown support
- Use react-markdown for formatting
- Sanitize content for XSS protection
- **File**: `frontend/components/chat/MessageContent.tsx`
- **Depends on**: 3.3

### 3.5 Create MessageList Component (1.5 hours, P0)
- Scrollable message list
- Group consecutive messages by sender
- Auto-scroll to bottom on new messages
- **File**: `frontend/components/chat/MessageList.tsx`
- **Depends on**: 3.3

### 3.6 Create ChatInput Component (1 hour, P0)
- Message input field
- Enter to send, Shift+Enter for new line
- Character count indicator
- Disabled state during sending
- **File**: `frontend/components/chat/ChatInput.tsx`

### 3.7 Create SendButton Component (30 min, P0)
- Send message button
- Loading state
- Disabled state
- **File**: `frontend/components/chat/SendButton.tsx`

### 3.8 Create MessageGroup Component (45 min, P1)
- Group consecutive messages from same sender
- Display sender avatar/name once per group
- **File**: `frontend/components/chat/MessageGroup.tsx`
- **Depends on**: 3.3

---

## Phase 4: UI Feedback Components (5 tasks)

### 4.1 Create TypingIndicator Component (30 min, P0)
- Animated typing indicator for AI responses
- Show when isLoading is true
- **File**: `frontend/components/chat/TypingIndicator.tsx`

### 4.2 Create MessageStatus Component (45 min, P0)
- Display sending/sent/failed status
- Show checkmarks or error icons
- **File**: `frontend/components/chat/MessageStatus.tsx`
- **Depends on**: 1.2

### 4.3 Create ToolExecutionBadge Component (1 hour, P0)
- Display tool execution indicators
- Show tool name and status
- Support multiple tool calls
- **File**: `frontend/components/chat/ToolExecutionBadge.tsx`
- **Depends on**: 1.2

### 4.4 Create ErrorDisplay Component (45 min, P0)
- Inline error messages
- Retry button
- Clear error action
- **File**: `frontend/components/chat/ErrorDisplay.tsx`

### 4.5 Create MessageTimestamp Component (30 min, P1)
- Format and display timestamps
- Relative time (e.g., "2 minutes ago")
- **File**: `frontend/components/chat/MessageTimestamp.tsx`

---

## Phase 5: Optimistic UI Implementation (2 tasks)

### 5.1 Implement Optimistic Message Sending (1.5 hours, P0)
- Add message with "sending" status immediately
- Send to backend
- Update status to "sent" on success
- Update status to "failed" on error
- **File**: `frontend/lib/stores/chatStore.ts` (update sendMessage action)
- **Depends on**: 1.3, 2.1

### 5.2 Implement Retry Logic (1 hour, P0)
- Add retryFailedMessage action to store
- Handle retry button clicks
- Prevent message duplication
- **File**: `frontend/lib/stores/chatStore.ts`
- **Depends on**: 5.1

---

## Phase 6: Conversation Management (3 tasks)

### 6.1 Implement Conversation ID Management (1 hour, P0)
- Store conversation ID in URL query param
- Fall back to localStorage
- Update URL when conversation changes
- **File**: `frontend/lib/utils/conversation.ts`

### 6.2 Create ConversationSidebar Component (1.5 hours, P2)
- List of conversations
- Conversation preview and timestamp
- Switch between conversations
- **File**: `frontend/components/chat/ConversationSidebar.tsx`
- **Depends on**: 1.3

### 6.3 Create ConversationList and ConversationItem Components (1 hour, P2)
- Display conversation list
- Individual conversation preview
- Active conversation highlighting
- **Files**: `frontend/components/chat/ConversationList.tsx`, `ConversationItem.tsx`
- **Depends on**: 6.2

---

## Phase 7: Main View & Integration (2 tasks)

### 7.1 Create AIAssistantView Component (1.5 hours, P0)
- Main container component
- Load conversation on mount
- Handle conversation switching
- Integrate all chat components
- **File**: `frontend/components/chat/AIAssistantView.tsx`
- **Depends on**: 3.1, 3.5, 3.6, 4.1, 4.4

### 7.2 Create AI Assistant Page (45 min, P0)
- Create Next.js page at /dashboard/ai-assistant
- Integrate AIAssistantView
- Add to sidebar navigation
- **File**: `frontend/app/dashboard/ai-assistant/page.tsx`
- **Depends on**: 7.1

---

## Phase 8: Accessibility & Responsive Design (3 tasks)

### 8.1 Implement Keyboard Navigation (1 hour, P1)
- Tab navigation through interface
- Enter to send message
- Escape to clear input
- Focus management
- **Files**: Update ChatInput.tsx, ChatContainer.tsx

### 8.2 Add ARIA Labels and Screen Reader Support (1 hour, P1)
- Add ARIA labels to all interactive elements
- Announce new messages to screen readers
- Proper semantic HTML
- **Files**: Update all chat components

### 8.3 Implement Responsive Design (1.5 hours, P1)
- Mobile-first design (320px+)
- Responsive breakpoints (768px, 1024px, 1920px)
- Touch-friendly UI (44px tap targets)
- Mobile keyboard handling
- **File**: `frontend/styles/chat.css`
- **Files**: Update all chat components

---

## Phase 9: Testing & Documentation (4 tasks)

### 9.1 Write Unit Tests (2 hours, P1)
- Test Message, ChatInput, MessageStatus components
- Test chatStore actions
- Test API client methods
- **Files**: `frontend/tests/unit/*.test.tsx`
- **Depends on**: All component tasks

### 9.2 Write Integration Tests (2 hours, P1)
- Test end-to-end message flow
- Test optimistic UI behavior
- Test error recovery
- **Files**: `frontend/tests/integration/*.test.tsx`
- **Depends on**: 7.1

### 9.3 Write E2E Tests with Playwright (1.5 hours, P1)
- Test complete chat flow
- Test conversation persistence
- Test error scenarios
- **File**: `frontend/tests/e2e/chat.spec.ts`
- **Depends on**: 7.2

### 9.4 Create Component Documentation (1 hour, P2)
- Document all chat components
- Add usage examples
- Create quickstart guide
- **Files**: `specs/012-conversational-ui-chatkit/contracts/*.md`, `quickstart.md`

---

## Summary
- **Total**: 32 tasks, ~28 hours
- **Critical Path**: Setup → API → Core Components → Optimistic UI → Main View → Testing
- **Parallel Work**: Core components (3.1-3.8), UI feedback (4.1-4.5), Conversation management (6.2-6.3)
- **Dependencies**: Spec 011 (Chat API) and Spec 005 (SaaS Layout) must be completed first
