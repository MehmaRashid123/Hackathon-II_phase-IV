# Implementation Plan: Conversational UI with OpenAI ChatKit

**Branch**: `012-conversational-ui-chatkit` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/012-conversational-ui-chatkit/spec.md`

## Summary

Implement a modern conversational UI for task management using OpenAI ChatKit components integrated into the existing SaaS layout. The interface provides users with a natural language chat experience featuring optimistic UI updates, loading states, tool execution indicators, persistent chat history, and comprehensive error handling. The system connects to the backend chat API from Spec 011, enabling seamless AI-powered task management through conversational interaction.

## Technical Context

**Language/Version**: TypeScript 5+, React 18+, Next.js 16+ (App Router)
**Primary Dependencies**: OpenAI ChatKit, React, Next.js, Tailwind CSS, Zustand (state management)
**Storage**: Browser localStorage for conversation ID persistence, backend database for message history
**Testing**: Jest/Vitest (unit), React Testing Library (integration), Playwright (E2E), Lighthouse (performance/accessibility)
**Target Platform**: Modern browsers (Chrome, Firefox, Safari, Edge), mobile responsive (320px+)
**Project Type**: Frontend web application (Next.js App Router)
**Performance Goals**:
- Initial load < 500ms
- Optimistic UI updates < 100ms (perceived instant)
- Chat history load < 1 second (100 messages)
- Smooth scrolling (60fps)
- Memory efficient (1000+ messages)

**Constraints**:
- Must integrate with existing SaaS layout (Spec 005)
- Must connect to chat API from Spec 011
- OpenAI ChatKit components for consistency
- Optimistic UI for instant feel
- WCAG 2.1 AA accessibility compliance
- Mobile responsive (320px minimum width)
- No backend changes (frontend only)

**Scale/Scope**: Production-ready chat UI for multi-user task management, designed for 100-1000 concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development ✅
- **Status**: PASS
- **Evidence**: Specification created in `specs/012-conversational-ui-chatkit/spec.md` with 4 user stories, 14 functional requirements, 8 non-functional requirements, and 8 success criteria before any implementation.

### Principle II: Agentic Workflow ✅
- **Status**: PASS
- **Evidence**: Implementation will be delegated to:
  - `nextjs-ui-builder`: Chat interface components, OpenAI ChatKit integration
  - `react-state-specialist`: State management (Zustand), optimistic UI patterns
  - `accessibility-specialist`: WCAG 2.1 AA compliance, keyboard navigation, ARIA labels
  - `spec-driven-architect`: Integration with Spec 005 (SaaS Layout) and Spec 011 (Chat API)

### Principle III: Security First ✅
- **Status**: PASS
- **Evidence**:
  - JWT authentication for API calls (inherited from Spec 011)
  - User ID validation on all requests
  - No sensitive data in localStorage (only conversation IDs)
  - XSS protection through React's built-in escaping
  - Content Security Policy headers
  - Input sanitization before sending to backend

### Principle IV: Modern Stack with Strong Typing ✅
- **Status**: PASS
- **Evidence**:
  - TypeScript 5+ with strict mode enabled
  - Type-safe API client with typed responses
  - Zod schemas for runtime validation
  - Type-safe state management with Zustand
  - OpenAI ChatKit with TypeScript support

### Principle V: User Isolation ✅
- **Status**: PASS
- **Evidence**:
  - User ID from JWT used in all API calls
  - Conversation history filtered by user on backend
  - No cross-user data access possible
  - localStorage scoped to user session
  - Logout clears all local state

### Principle VI: Responsive Design ✅
- **Status**: PASS
- **Evidence**:
  - Mobile-first design approach
  - Responsive breakpoints (320px, 768px, 1024px, 1920px)
  - Touch-friendly UI elements (44px minimum tap targets)
  - Adaptive layouts for mobile/tablet/desktop
  - Tested on devices from 320px to 1920px width
  - Proper viewport handling for mobile keyboards

### Principle VII: Data Persistence ✅
- **Status**: PASS
- **Evidence**:
  - Chat history persisted on backend (Spec 011)
  - Conversation ID stored in localStorage for continuity
  - Messages fetched from backend on page load
  - Optimistic UI with backend confirmation
  - Automatic retry on network failures

**Gate Decision**: ✅ PASS (All principles satisfied)

## Project Structure

### Documentation (this feature)

```text
specs/012-conversational-ui-chatkit/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (ChatKit best practices)
├── data-model.md        # Phase 1 output (Frontend state schemas)
├── quickstart.md        # Phase 1 output (Setup and testing instructions)
├── contracts/           # Phase 1 output (Component contracts)
│   ├── chat-container.md    # ChatContainer component API
│   ├── message-list.md      # MessageList component API
│   └── chat-input.md        # ChatInput component API
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
frontend/
├── app/
│   └── dashboard/
│       └── ai-assistant/
│           ├── page.tsx              # AI Assistant main page
│           └── layout.tsx            # Optional layout wrapper
├── components/
│   ├── chat/
│   │   ├── AIAssistantView.tsx      # Main container component
│   │   ├── ChatContainer.tsx        # Chat interface wrapper
│   │   ├── ChatHeader.tsx           # Header with title and actions
│   │   ├── MessageList.tsx          # Scrollable message list
│   │   ├── MessageGroup.tsx         # Grouped messages by sender
│   │   ├── Message.tsx              # Individual message component
│   │   ├── MessageContent.tsx       # Message text with markdown
│   │   ├── MessageTimestamp.tsx     # Timestamp display
│   │   ├── ToolExecutionBadge.tsx   # Tool call indicator
│   │   ├── MessageStatus.tsx        # Sending/sent/failed status
│   │   ├── TypingIndicator.tsx      # AI typing animation
│   │   ├── ChatInput.tsx            # Message input field
│   │   ├── SendButton.tsx           # Send message button
│   │   ├── ErrorDisplay.tsx         # Inline error messages
│   │   ├── ConversationSidebar.tsx  # Optional conversation list
│   │   ├── ConversationList.tsx     # List of conversations
│   │   └── ConversationItem.tsx     # Individual conversation preview
│   └── ui/
│       └── ... (existing UI components from Spec 005)
├── lib/
│   ├── api/
│   │   └── chat.ts                  # Chat API client
│   ├── hooks/
│   │   ├── useChat.ts               # Chat state management hook
│   │   ├── useChatHistory.ts        # History loading hook
│   │   └── useOptimisticUI.ts       # Optimistic updates hook
│   ├── stores/
│   │   └── chatStore.ts             # Zustand store for chat state
│   ├── types/
│   │   └── chat.ts                  # TypeScript types for chat
│   └── utils/
│       ├── markdown.ts              # Markdown rendering utilities
│       ├── timestamp.ts             # Timestamp formatting
│       └── conversation.ts          # Conversation ID management
├── styles/
│   └── chat.css                     # Chat-specific styles
├── tests/
│   ├── unit/
│   │   ├── Message.test.tsx
│   │   ├── ChatInput.test.tsx
│   │   └── chatStore.test.ts
│   ├── integration/
│   │   ├── chat-flow.test.tsx       # End-to-end message flow
│   │   └── optimistic-ui.test.tsx   # Optimistic UI behavior
│   ├── e2e/
│   │   └── chat.spec.ts             # Playwright E2E tests
│   └── accessibility/
│       └── chat-a11y.test.tsx       # Accessibility tests
├── package.json                     # Add: @openai/chatkit, zustand
└── README.md                        # Updated with chat UI documentation
```

**Structure Decision**: Frontend Next.js App Router structure (Option 1) selected. This is a pure frontend feature integrating with existing SaaS layout. Uses App Router conventions for routing and layouts.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | All principles pass | N/A |

## Phase 0: Research & Technology Best Practices

### OpenAI ChatKit Integration
- **Decision**: Use OpenAI ChatKit components for chat interface
- **Rationale**: Official OpenAI UI components provide consistent, well-tested chat experience. Reduces custom implementation effort and ensures compatibility with OpenAI design patterns.
- **Alternatives Considered**:
  - Custom chat components: More control but higher development and maintenance cost
  - react-chat-elements: Third-party library but less OpenAI-specific
  - Headless UI with custom styling: More flexible but more work
- **Best Practices**:
  - Use ChatKit's built-in components where possible
  - Customize styling with Tailwind CSS
  - Extend components for tool execution indicators
  - Test ChatKit compatibility early
  - Have fallback to custom components if needed
  - Follow ChatKit documentation for best practices

### Optimistic UI Pattern
- **Decision**: Implement optimistic UI updates for instant feel
- **Rationale**: Users expect instant feedback when sending messages. Optimistic UI shows message immediately while backend processes request, improving perceived performance.
- **Alternatives Considered**:
  - Wait for backend confirmation: Simpler but feels slow
  - Loading spinner only: Doesn't show user's message immediately
  - Pessimistic UI: More reliable but worse UX
- **Best Practices**:
  - Show user message immediately with "sending" status
  - Update to "sent" when backend confirms
  - Show "failed" status with retry option on error
  - Don't duplicate messages on retry
  - Handle race conditions (rapid successive sends)
  - Clear error states after successful retry

### State Management with Zustand
- **Decision**: Use Zustand for chat state management
- **Rationale**: Lightweight, TypeScript-friendly state management without boilerplate. Simpler than Redux, more powerful than useState for complex state.
- **Alternatives Considered**:
  - React Context: Simpler but can cause unnecessary re-renders
  - Redux Toolkit: More powerful but heavier, more boilerplate
  - Jotai/Recoil: Atomic state but less established
  - useState only: Too simple for complex chat state
- **Best Practices**:
  - Single store for all chat state
  - Separate slices for conversations, messages, UI state
  - Persist conversation ID to localStorage
  - Use selectors to prevent unnecessary re-renders
  - Implement middleware for logging and debugging
  - Type-safe actions and state

### Conversation ID Management
- **Decision**: Hybrid approach (URL + localStorage)
- **Rationale**: URL enables deep linking and sharing, localStorage provides fallback and persistence. Best of both worlds.
- **Alternatives Considered**:
  - URL only: Loses state on navigation without query params
  - localStorage only: Can't share or bookmark conversations
  - Session storage: Loses state on tab close
- **Best Practices**:
  - Use URL query param for active conversation
  - Fall back to localStorage if no URL param
  - Update URL when conversation changes
  - Clear localStorage on logout
  - Handle missing/invalid conversation IDs gracefully
  - Support multiple tabs with same conversation

### Markdown Rendering
- **Decision**: Use react-markdown for AI response formatting
- **Rationale**: AI responses may include markdown (bold, italic, lists, code blocks). react-markdown provides safe, customizable rendering.
- **Alternatives Considered**:
  - marked.js: More features but not React-specific
  - Custom parser: Too much work, security risks
  - Plain text only: Loses formatting capabilities
- **Best Practices**:
  - Sanitize markdown to prevent XSS
  - Customize rendering for code blocks (syntax highlighting)
  - Support common markdown features (bold, italic, lists, links)
  - Handle edge cases (malformed markdown)
  - Test with various markdown inputs
  - Limit allowed HTML tags for security

### Accessibility (WCAG 2.1 AA)
- **Decision**: Build accessibility in from the start
- **Rationale**: Accessibility is a requirement, not an afterthought. Easier to build correctly than retrofit.
- **Best Practices**:
  - Semantic HTML (main, article, section, nav)
  - ARIA labels for interactive elements
  - Keyboard navigation (Tab, Enter, Escape)
  - Focus management (trap focus in modals)
  - Screen reader announcements for new messages
  - Color contrast ratios (4.5:1 for text)
  - Skip links for keyboard users
  - Test with screen readers (NVDA, JAWS, VoiceOver)

## Phase 1: Data Models & Component Contracts

### Data Models

See [data-model.md](./data-model.md) for complete entity definitions.

**ChatMessage (Frontend State)**:
```typescript
interface ChatMessage {
  id: string;                    // Unique message ID (temp ID for optimistic, real ID from backend)
  role: 'user' | 'assistant' | 'system';
  content: string;               // Message text
  timestamp: Date;
  status: 'sending' | 'sent' | 'failed';
  toolCalls?: ToolCall[];        // Optional tool execution details
}

interface ToolCall {
  toolName: string;
  parameters: Record<string, any>;
  result?: string;
}
```

**Conversation (Frontend State)**:
```typescript
interface Conversation {
  id: string;                    // Conversation ID
  title: string;                 // Auto-generated or user-defined
  messages: ChatMessage[];
  lastMessageAt: Date;
  isActive: boolean;
}
```

**ChatState (Zustand Store)**:
```typescript
interface ChatState {
  // Data
  currentConversationId: string | null;
  conversations: Record<string, Conversation>;
  
  // UI State
  isLoading: boolean;
  isSending: boolean;
  error: string | null;
  
  // Actions
  sendMessage: (content: string) => Promise<void>;
  loadConversation: (id: string) => Promise<void>;
  createNewConversation: () => void;
  retryFailedMessage: (messageId: string) => Promise<void>;
  clearError: () => void;
}
```

### Component Contracts

See [contracts/](./contracts/) for complete component specifications.

**AIAssistantView Component**:
```tsx
interface AIAssistantViewProps {
  userId: string;                // From JWT/auth context
  initialConversationId?: string; // From URL or localStorage
}

// Main container component
// Manages conversation loading and state
// Integrates with SaaS layout
```

**ChatContainer Component**:
```tsx
interface ChatContainerProps {
  conversationId: string;
  messages: ChatMessage[];
  isLoading: boolean;
  isSending: boolean;
  error: string | null;
  onSendMessage: (content: string) => void;
  onRetry: (messageId: string) => void;
  onNewConversation: () => void;
}

// Wrapper for chat interface
// Handles layout and composition
// Integrates ChatKit components
```

**MessageList Component**:
```tsx
interface MessageListProps {
  messages: ChatMessage[];
  isLoading: boolean;
}

// Scrollable message list
// Groups messages by sender
// Handles virtual scrolling for performance
// Shows typing indicator when loading
```

**ChatInput Component**:
```tsx
interface ChatInputProps {
  onSend: (content: string) => void;
  disabled: boolean;
  placeholder?: string;
}

// Message input field
// Enter to send, Shift+Enter for new line
// Character count indicator
// Disabled state during sending
```

### API Integration

**Chat API Client** (`lib/api/chat.ts`):
```typescript
interface ChatAPIClient {
  sendMessage(userId: string, message: string, conversationId?: string): Promise<ChatResponse>;
  loadConversation(userId: string, conversationId: string): Promise<Conversation>;
  listConversations(userId: string): Promise<Conversation[]>;
}

// Handles all API calls to Spec 011 backend
// Includes JWT authentication
// Implements retry logic
// Handles errors gracefully
```

### State Management Flow

```
1. User types message → Update input state
   ↓
2. User presses Enter → Trigger sendMessage action
   ↓
3. Zustand store: Optimistically add message with "sending" status
   ↓
4. API client: POST /api/{user_id}/chat
   ↓
5. On success:
   - Update message status to "sent"
   - Add AI response to messages
   - Update conversation in store
   - Persist conversation ID to localStorage
   ↓
6. On failure:
   - Update message status to "failed"
   - Show error message
   - Provide retry option
```

### Integration with Existing Layout

```tsx
// app/dashboard/ai-assistant/page.tsx
import { AIAssistantView } from '@/components/chat/AIAssistantView';

export default function AIAssistantPage() {
  return <AIAssistantView userId={getUserId()} />;
}

// Sidebar navigation (update existing Sidebar component)
<NavItem href="/dashboard/ai-assistant" icon={MessageSquare}>
  AI Assistant
</NavItem>
```

## Architectural Decisions Requiring Documentation

### ADR 1: OpenAI ChatKit vs. Custom Components
- **Context**: Need chat UI components for conversational interface
- **Decision**: Use OpenAI ChatKit components with custom extensions
- **Alternatives**:
  - Custom components: More control but higher cost
  - react-chat-elements: Third-party but less OpenAI-specific
  - Headless UI: More flexible but more work
- **Consequences**:
  - ✅ Consistent OpenAI design patterns
  - ✅ Well-tested, maintained components
  - ✅ Reduced development time
  - ⚠️ Dependency on ChatKit updates
  - ⚠️ May need custom extensions for tool indicators
- **Status**: Approved
- **Suggest ADR**: 📋 Architectural decision detected: OpenAI ChatKit for chat UI. Document? Run `/sp.adr chatkit-component-choice`

### ADR 2: Optimistic UI with Backend Confirmation
- **Context**: Need instant feel for message sending
- **Decision**: Implement optimistic UI updates with backend confirmation
- **Alternatives**:
  - Wait for backend: Simpler but feels slow
  - Loading spinner only: Doesn't show message immediately
  - Pessimistic UI: More reliable but worse UX
- **Consequences**:
  - ✅ Instant perceived performance (< 100ms)
  - ✅ Better user experience
  - ✅ Clear error states with retry
  - ⚠️ Complexity in handling failures
  - ⚠️ Race conditions with rapid sends
- **Status**: Approved
- **Suggest ADR**: 📋 Architectural decision detected: Optimistic UI pattern. Document? Run `/sp.adr optimistic-ui-pattern`

### ADR 3: Zustand for State Management
- **Context**: Need state management for complex chat state
- **Decision**: Use Zustand for lightweight, TypeScript-friendly state management
- **Alternatives**:
  - React Context: Simpler but re-render issues
  - Redux Toolkit: More powerful but heavier
  - Jotai/Recoil: Atomic state but less established
- **Consequences**:
  - ✅ Lightweight and performant
  - ✅ TypeScript-friendly
  - ✅ Less boilerplate than Redux
  - ✅ Easy to test
  - ⚠️ Less ecosystem than Redux
- **Status**: Approved
- **Suggest ADR**: 📋 Architectural decision detected: Zustand for state management. Document? Run `/sp.adr zustand-state-management`

## Testing Strategy

### Unit Tests
- **Message Rendering**: Test with various content types (text, markdown, code blocks)
- **Input Validation**: Test empty messages, long messages, special characters
- **Error State Handling**: Test error display and retry logic
- **Timestamp Formatting**: Test various date formats and timezones
- **Tool Execution Badge**: Test display with different tool types

### Integration Tests
- **End-to-End Message Flow**: Send message → optimistic UI → backend → confirmation
- **Chat History Loading**: Load conversation → display messages → scroll to bottom
- **Conversation Switching**: Switch between conversations → load history → update URL
- **Error Recovery**: Network failure → error display → retry → success
- **Optimistic UI Updates**: Rapid sends → no duplicates → correct order

### E2E Tests (Playwright)
- **Complete Chat Flow**: Login → open AI Assistant → send message → receive response
- **Conversation Persistence**: Send messages → refresh page → history restored
- **Multi-Device**: Login on different device → history available
- **Error Scenarios**: Disconnect network → send message → error → reconnect → retry

### Accessibility Tests
- **Keyboard Navigation**: Tab through interface → Enter to send → Escape to close
- **Screen Reader**: Announce new messages → read message content → tool indicators
- **Focus Management**: Focus input after send → focus error on failure
- **Color Contrast**: Test all text against backgrounds (4.5:1 ratio)
- **ARIA Labels**: Verify all interactive elements have labels

### Performance Tests
- **Initial Load Time**: Measure time to first render (target < 500ms)
- **Message Rendering**: Test with 100+ messages (target < 1s)
- **Scroll Performance**: Measure FPS during scrolling (target 60fps)
- **Memory Usage**: Monitor memory over extended session (1000+ messages)

### Visual Regression Tests
- **Chat Interface Layout**: Desktop, tablet, mobile views
- **Message Grouping**: Consecutive messages from same sender
- **Loading States**: Typing indicator, sending status
- **Error Display**: Inline errors, retry buttons
- **Tool Indicators**: Tool execution badges

## Next Steps

This plan will be followed by:
1. **Phase 2: Task Generation** (`/sp.tasks`) - Break down this plan into actionable, ordered tasks
2. **Phase 3: Implementation** (`/sp.implement`) - Execute tasks via specialized agents
3. **Phase 4: Testing & Validation** - Verify all acceptance scenarios pass
4. **Phase 5: Accessibility Audit** - WCAG 2.1 AA compliance verification
5. **Phase 6: Performance Optimization** - Lighthouse audit and optimization
6. **Phase 7: Documentation** - Complete component documentation and quickstart guide
7. **Phase 8: Commit & PR** (`/sp.git.commit_pr`) - Create pull request for review

**Implementation Sequence**:
1. Set up OpenAI ChatKit dependencies
2. Create Zustand store for chat state
3. Implement API client for Spec 011 backend
4. Build core components (ChatContainer, MessageList, ChatInput)
5. Implement optimistic UI pattern
6. Add loading states and typing indicators
7. Implement tool execution badges
8. Add error handling and retry logic
9. Implement conversation ID management (URL + localStorage)
10. Add markdown rendering for AI responses
11. Integrate with SaaS layout (Spec 005)
12. Implement accessibility features (keyboard nav, ARIA labels)
13. Add responsive design for mobile
14. Write unit tests for components
15. Write integration tests for flows
16. Write E2E tests with Playwright
17. Conduct accessibility audit
18. Optimize performance (virtual scrolling, lazy loading)
19. Document components and usage

**Critical Path**:
- Zustand store must be set up before components
- API client must be implemented before message sending
- Optimistic UI must be working before error handling
- Core components must be built before integration with layout
- Accessibility features must be built in (not retrofitted)
- Testing must be done incrementally (not all at end)

**Agent Assignments**:
- `nextjs-ui-builder`: Chat components, OpenAI ChatKit integration, responsive design
- `react-state-specialist`: Zustand store, optimistic UI, state management patterns
- `accessibility-specialist`: WCAG 2.1 AA compliance, keyboard navigation, ARIA labels, screen reader testing
- `spec-driven-architect`: Integration with Spec 005 (SaaS Layout) and Spec 011 (Chat API)

**Estimated Complexity**: High (Complex UI, optimistic updates, accessibility, performance, multiple integrations)

**Dependencies**:
- **Spec 011 (Chat API)**: MUST be completed and deployed before frontend implementation
  - Requires: POST /api/{user_id}/chat endpoint
  - Requires: ChatRequest/ChatResponse schemas
  - Requires: Conversation and message persistence
- **Spec 005 (SaaS Layout)**: MUST be completed for layout integration
  - Requires: Dashboard layout structure
  - Requires: Sidebar navigation
  - Requires: Responsive design system

**Risk Mitigation**:
- OpenAI ChatKit compatibility: Evaluate early, have fallback to custom components
- Performance with large history: Implement virtual scrolling and pagination
- Optimistic UI confusion: Clear error states and automatic retry
- State management complexity: Use established Zustand patterns
- Accessibility compliance: Build in from start, test with screen readers
- Mobile keyboard issues: Proper viewport handling and scroll-to-input

