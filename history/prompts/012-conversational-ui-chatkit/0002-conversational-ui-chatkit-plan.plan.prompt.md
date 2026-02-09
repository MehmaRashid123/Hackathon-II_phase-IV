---
id: 0002
title: Conversational UI with ChatKit Implementation Plan
stage: plan
date: 2026-02-09
surface: agent
model: kiro-sonnet
feature: 012-conversational-ui-chatkit
branch: 012-conversational-ui-chatkit
user: developer
command: /sp.plan
labels: ["conversational-ui", "openai-chatkit", "react", "nextjs", "frontend", "optimistic-ui", "implementation-plan"]
links:
  spec: specs/012-conversational-ui-chatkit/spec.md
  plan: specs/012-conversational-ui-chatkit/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/012-conversational-ui-chatkit/plan.md
tests:
  - None (planning phase)
---

## Prompt

/sp.plan

Create: architecture sketch, section structure, research approach, quality validation.
Decisions needing documentation: list important choices with options and tradeoffs.
Testing strategy: validation checks based on acceptance criteria.

Technical details:
- Use research-concurrent approach (research while writing, not all upfront)
- Follow APA citation style from Constitution
- Organize by phases: Research → Foundation → Analysis → Synthesis

## Response snapshot

Created comprehensive implementation plan for Conversational UI with OpenAI ChatKit feature (Spec 012).

**Key Components:**

1. **Technical Context**
   - TypeScript 5+, React 18+, Next.js 16+ App Router, OpenAI ChatKit, Zustand
   - Performance goals: Initial load < 500ms, optimistic UI < 100ms, history load < 1s
   - Constraints: Integrate with SaaS layout, connect to Spec 011 API, WCAG 2.1 AA compliance

2. **Constitution Check** (All Principles Pass)
   - ✅ Spec-Driven Development: Complete specification before implementation
   - ✅ Agentic Workflow: Delegated to specialized agents
   - ✅ Security First: JWT auth, user ID validation, XSS protection
   - ✅ Modern Stack: TypeScript 5+ strict mode, type-safe state management
   - ✅ User Isolation: User ID in all API calls, no cross-user access
   - ✅ Responsive Design: Mobile-first, 320px-1920px, touch-friendly
   - ✅ Data Persistence: Backend persistence, localStorage for conversation ID

3. **Project Structure**
   - Documentation: plan.md, research.md, data-model.md, quickstart.md, contracts/
   - Source code: components/chat/, lib/api/, lib/hooks/, lib/stores/, tests/
   - Frontend Next.js App Router structure

4. **Phase 0: Research & Technology Best Practices**
   - OpenAI ChatKit integration (vs. custom components, react-chat-elements)
   - Optimistic UI pattern (vs. wait for backend, loading spinner only)
   - State management with Zustand (vs. Context, Redux, Jotai)
   - Conversation ID management (hybrid URL + localStorage)
   - Markdown rendering with react-markdown
   - Accessibility (WCAG 2.1 AA from start)

5. **Phase 1: Data Models & Component Contracts**
   - ChatMessage (id, role, content, timestamp, status, toolCalls)
   - Conversation (id, title, messages, lastMessageAt, isActive)
   - ChatState (Zustand store with actions)
   - Component hierarchy: AIAssistantView → ChatContainer → MessageList/ChatInput
   - API client for Spec 011 backend integration

6. **Architectural Decisions Requiring Documentation (3 ADRs)**
   - ADR 1: OpenAI ChatKit vs. custom components
   - ADR 2: Optimistic UI with backend confirmation
   - ADR 3: Zustand for state management

7. **Testing Strategy**
   - Unit tests: Message rendering, input validation, error handling
   - Integration tests: End-to-end flow, history loading, conversation switching
   - E2E tests (Playwright): Complete chat flow, persistence, multi-device
   - Accessibility tests: Keyboard nav, screen reader, focus management
   - Performance tests: Load time, rendering, scroll, memory
   - Visual regression tests: Layouts, loading states, error display

8. **Implementation Sequence** (19 steps)
   - ChatKit setup → Zustand store → API client → Core components → Optimistic UI → Loading states → Tool badges → Error handling → Conversation ID → Markdown → Layout integration → Accessibility → Responsive → Testing → Optimization → Documentation

9. **Critical Path**
   - Zustand store before components
   - API client before message sending
   - Optimistic UI before error handling
   - Core components before layout integration
   - Accessibility built in (not retrofitted)
   - Incremental testing (not all at end)

10. **Agent Assignments**
    - nextjs-ui-builder: Chat components, ChatKit integration, responsive design
    - react-state-specialist: Zustand store, optimistic UI, state patterns
    - accessibility-specialist: WCAG 2.1 AA, keyboard nav, ARIA labels, screen reader
    - spec-driven-architect: Integration with Spec 005 and Spec 011

11. **Dependencies**
    - Spec 011 (Chat API) MUST be completed first
    - Spec 005 (SaaS Layout) MUST be completed for integration
    - Requires: POST /api/{user_id}/chat endpoint, ChatRequest/ChatResponse schemas

12. **Risk Mitigation**
    - ChatKit compatibility → Evaluate early, fallback to custom
    - Performance with large history → Virtual scrolling, pagination
    - Optimistic UI confusion → Clear error states, auto-retry
    - State complexity → Established Zustand patterns
    - Accessibility compliance → Build in from start, test with screen readers
    - Mobile keyboard issues → Proper viewport handling

## Outcome

- ✅ Impact: Complete architectural plan for modern conversational UI with OpenAI ChatKit
- 🧪 Tests: Comprehensive testing strategy (unit, integration, E2E, accessibility, performance, visual)
- 📁 Files: Created specs/012-conversational-ui-chatkit/plan.md
- 🔁 Next prompts: /sp.tasks to break down into actionable implementation tasks
- 🧠 Reflection: Plan emphasizes optimistic UI for instant feel, proper accessibility from start, and integration with existing SaaS layout and chat API

## Evaluation notes (flywheel)

- Failure modes observed: None (planning phase)
- Graders run and results (PASS/FAIL): N/A (planning phase)
- Prompt variant (if applicable): Standard plan creation following Claude Code SDD methodology with research-concurrent approach
- Next experiment (smallest change to try): Proceed to task breakdown phase with /sp.tasks command

