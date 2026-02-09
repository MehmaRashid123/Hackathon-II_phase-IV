# Implementation Plan: OpenAI Agents SDK and Stateless Chat API

**Branch**: `011-openai-agents-chat-api` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/011-openai-agents-chat-api/spec.md`

## Summary

Implement a stateless chat API endpoint that integrates OpenAI Agents SDK with MCP server tools to enable natural language task management. The system processes user messages through an AI agent that maintains conversation context via database-stored history, executes MCP tool calls for task operations, and returns friendly natural language responses. The architecture is completely stateless, relying entirely on the database for conversation persistence, enabling horizontal scalability and concurrent multi-user support.

## Technical Context

**Language/Version**: Python 3.11+ (backend), OpenAI Agents SDK 1.0+
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, SQLModel, Neon PostgreSQL, MCP SDK
**Storage**: Neon Serverless PostgreSQL (Conversation and Message tables from Spec 010)
**Testing**: pytest (unit, integration), load testing with locust, property-based testing for agent behavior
**Target Platform**: Linux/macOS server (backend API)
**Project Type**: Backend API service (stateless request-response architecture)
**Performance Goals**:
- P95 response latency < 5 seconds
- Conversation history retrieval < 500ms
- Support 100+ concurrent users
- Agent tool execution < 2 seconds per tool
- Database query optimization for history fetching

**Constraints**:
- Zero global or local state between requests
- All context must be fetched from database per request
- OpenAI Agents SDK for agent orchestration (no custom agent implementation)
- MCP tools from Spec 010 (add_task, list_tasks, complete_task, delete_task, update_task)
- System instructions define "Todo Assistant" persona
- User ID validation on every request
- Stateless architecture for horizontal scaling

**Scale/Scope**: Production-ready chat API for multi-user task management, designed for 100-1000 concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development ✅
- **Status**: PASS
- **Evidence**: Specification created in `specs/011-openai-agents-chat-api/spec.md` with 3 user stories, 10 functional requirements, 6 non-functional requirements, and 7 success criteria before any implementation.

### Principle II: Agentic Workflow ✅
- **Status**: PASS
- **Evidence**: Implementation will be delegated to:
  - `fastapi-backend-architect`: Chat endpoint, request cycle, response handling
  - `ai-integration-specialist`: OpenAI Agents SDK integration, prompt engineering
  - `neon-db-manager`: Conversation history queries, message persistence optimization
  - `spec-driven-architect`: Cross-stack coordination with Spec 010 MCP tools

### Principle III: Security First ✅
- **Status**: PASS
- **Evidence**:
  - JWT authentication required on `/api/{user_id}/chat` endpoint
  - User ID validation (path parameter must match authenticated user)
  - User ID passed to all MCP tool calls for data isolation
  - No cross-user data leakage (conversation history filtered by user_id)
  - Input validation on all request payloads
  - Rate limiting to prevent abuse
  - Logging of all agent interactions for audit trail

### Principle IV: Modern Stack with Strong Typing ✅
- **Status**: PASS
- **Evidence**:
  - Python 3.11+ with type hints throughout
  - Pydantic models for ChatRequest/ChatResponse validation
  - SQLModel for database queries (type-safe ORM)
  - OpenAI Agents SDK with typed tool definitions
  - FastAPI automatic OpenAPI schema generation

### Principle V: User Isolation ✅
- **Status**: PASS
- **Evidence**:
  - Conversation history filtered by user_id on every request
  - User ID extracted from JWT and validated against path parameter
  - All MCP tool calls include user_id for multi-tenant isolation
  - Database queries use WHERE user_id = ? clauses
  - No shared state between users (stateless architecture)

### Principle VI: Responsive Design ⚠️
- **Status**: NOT APPLICABLE
- **Evidence**: This is a backend API feature with no UI components. Responsive design will be addressed in Spec 012 (Conversational UI with ChatKit).

### Principle VII: Data Persistence ✅
- **Status**: PASS
- **Evidence**:
  - Conversation and Message tables from Spec 010
  - Every user message persisted before agent processing
  - Every agent response persisted before returning to client
  - Conversation history fetched from database on every request
  - Transaction support for atomic message saves
  - Indexes on user_id and conversation_id for query performance

**Gate Decision**: ✅ PASS (Principle VI not applicable to backend API)

## Project Structure

### Documentation (this feature)

```text
specs/011-openai-agents-chat-api/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (OpenAI Agents SDK best practices)
├── data-model.md        # Phase 1 output (ChatRequest/ChatResponse schemas)
├── quickstart.md        # Phase 1 output (setup and testing instructions)
├── contracts/           # Phase 1 output (API contracts)
│   └── chat-endpoint.yaml  # POST /api/{user_id}/chat OpenAPI spec
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── chat.py                    # POST /api/{user_id}/chat endpoint
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── todo_assistant.py          # OpenAI Agent configuration
│   │   ├── system_instructions.py     # Agent persona and instructions
│   │   └── tool_definitions.py        # MCP tool schemas for agent
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py            # Stateless request cycle orchestration
│   │   ├── conversation_service.py    # Conversation history management
│   │   └── mcp_client.py              # MCP tool call client
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── chat.py                    # ChatRequest/ChatResponse Pydantic models
│   ├── models/
│   │   ├── __init__.py
│   │   ├── conversation.py            # Conversation SQLModel (from Spec 010)
│   │   └── message.py                 # Message SQLModel (from Spec 010)
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── user_validation.py         # Validate user_id matches JWT
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                  # Configuration (OpenAI API key, etc.)
│   │   └── database.py                # Database connection
│   └── main.py                        # FastAPI app with chat endpoint
├── tests/
│   ├── unit/
│   │   ├── test_chat_service.py       # Stateless cycle unit tests
│   │   ├── test_agent_prompts.py      # System instructions tests
│   │   └── test_tool_mapping.py       # NL to tool mapping tests
│   ├── integration/
│   │   ├── test_chat_endpoint.py      # End-to-end chat flow
│   │   ├── test_mcp_integration.py    # MCP tool call integration
│   │   └── test_context_preservation.py  # Multi-turn conversation tests
│   ├── load/
│   │   └── locustfile.py              # 100 concurrent user load test
│   └── fixtures/
│       ├── sample_conversations.json  # Test conversation data
│       └── sample_messages.json       # Test message data
├── requirements.txt                   # Add: openai-agents-sdk, mcp-sdk
└── README.md                          # Updated with chat API documentation
```

**Structure Decision**: Backend API service structure (Option 1) selected. This is a pure backend feature with no frontend components. The chat endpoint integrates with existing FastAPI application structure from Spec 001-002.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | All applicable principles pass | N/A |

## Phase 0: Research & Technology Best Practices

### OpenAI Agents SDK Integration
- **Decision**: Use OpenAI Agents SDK for agent orchestration
- **Rationale**: Official SDK provides robust agent framework with tool calling, conversation management, and error handling. Reduces custom implementation complexity.
- **Alternatives Considered**:
  - LangChain: More flexible but heavier, adds unnecessary abstraction
  - Custom agent implementation: Full control but high complexity and maintenance burden
  - OpenAI Chat Completions API directly: Lower-level, requires manual tool orchestration
- **Best Practices**:
  - Define system instructions clearly for "Todo Assistant" persona
  - Use structured tool definitions matching MCP tool schemas
  - Implement exponential backoff for OpenAI API rate limits
  - Log all agent interactions for debugging and improvement
  - Set reasonable token limits to control costs
  - Use streaming responses for better UX (future enhancement)

### Stateless Request Cycle Architecture
- **Decision**: Implement pure stateless architecture with database-driven context
- **Rationale**: Enables horizontal scaling, simplifies deployment, prevents state synchronization issues, supports concurrent users without session affinity.
- **Alternatives Considered**:
  - In-memory session storage: Faster but doesn't scale horizontally
  - Redis-based session cache: Adds infrastructure complexity
  - Sticky sessions: Limits scalability and complicates load balancing
- **Best Practices**:
  - Fetch conversation history from DB on every request
  - Save messages to DB before returning response
  - Use database transactions for atomic operations
  - Implement connection pooling for DB performance
  - Add indexes on user_id and conversation_id
  - Cache-aside pattern for frequently accessed conversations (future optimization)

### MCP Tool Integration
- **Decision**: Use MCP SDK client to call tools from Spec 010
- **Rationale**: MCP provides standardized tool interface, enabling agent to execute task operations through well-defined contracts.
- **Alternatives Considered**:
  - Direct database access from agent: Violates separation of concerns
  - REST API calls to task endpoints: Adds HTTP overhead, less efficient
  - Embedded tool implementations: Duplicates logic from Spec 010
- **Best Practices**:
  - Define tool schemas matching MCP tool signatures exactly
  - Pass user_id to every tool call for data isolation
  - Handle tool execution errors gracefully
  - Provide clear error messages to agent for user communication
  - Log tool calls and results for debugging
  - Implement timeout handling for long-running tools

### Natural Language to Tool Mapping
- **Decision**: Rely on OpenAI Agents SDK function calling for intent mapping
- **Rationale**: GPT-4 has strong function calling capabilities, reducing need for custom NLU logic.
- **Alternatives Considered**:
  - Custom intent classification: More control but requires training data and maintenance
  - Rule-based pattern matching: Brittle, doesn't handle variations well
  - Separate NLU service: Adds complexity and latency
- **Best Practices**:
  - Write clear, descriptive tool definitions with examples
  - Include parameter descriptions and constraints
  - Test with diverse natural language inputs
  - Provide fallback responses for ambiguous requests
  - Log misclassifications for prompt improvement
  - Iterate on system instructions based on user feedback

### Conversation Context Management
- **Decision**: Load full conversation history on every request
- **Rationale**: Ensures agent has complete context for accurate responses. Stateless architecture requires DB-driven context.
- **Alternatives Considered**:
  - Sliding window (last N messages): Loses context for long conversations
  - Summarization: Adds complexity, may lose important details
  - Separate context service: Adds infrastructure complexity
- **Best Practices**:
  - Limit history to last 50 messages (configurable)
  - Implement pagination for very long conversations
  - Optimize DB queries with proper indexes
  - Use connection pooling to reduce query latency
  - Consider conversation summarization for 100+ message threads (future)

### Error Handling and User Communication
- **Decision**: Agent translates technical errors into friendly messages
- **Rationale**: Users should never see raw error messages. Agent provides helpful, conversational error explanations.
- **Best Practices**:
  - Catch all exceptions in request cycle
  - Provide agent with error context (not stack traces)
  - Agent generates user-friendly error messages
  - Log full error details for debugging
  - Implement retry logic for transient failures
  - Return 500 errors only for unrecoverable failures

## Phase 1: Data Models & API Contracts

### Data Models

See [data-model.md](./data-model.md) for complete entity definitions.

**ChatRequest Schema** (Pydantic):
```python
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User's natural language message")
    conversation_id: Optional[str] = Field(None, description="Existing conversation ID (null for new conversation)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Add a task to buy groceries",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
```

**ChatResponse Schema** (Pydantic):
```python
class ToolCall(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    result: Optional[str] = None

class ChatResponse(BaseModel):
    conversation_id: str = Field(..., description="Conversation identifier")
    message: str = Field(..., description="Agent's natural language response")
    tool_calls: Optional[List[ToolCall]] = Field(None, description="Tools executed during processing")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "message": "Done! I've added 'buy groceries' to your task list.",
                "tool_calls": [
                    {
                        "tool_name": "add_task",
                        "parameters": {"title": "buy groceries", "description": ""},
                        "result": "success"
                    }
                ],
                "timestamp": "2026-02-09T10:30:00Z"
            }
        }
```

**Agent Context** (Ephemeral, not persisted):
```python
class AgentContext:
    user_id: str
    conversation_history: List[Message]  # From DB
    system_instructions: str
    available_tools: List[ToolDefinition]
    mcp_client: MCPClient
```

### API Contracts

See [contracts/](./contracts/) for OpenAPI specifications.

**Chat Endpoint**: `POST /api/{user_id}/chat`
- **Method**: POST
- **Authentication**: Required (JWT Bearer token)
- **Path Parameters**:
  - `user_id`: String (UUID, must match authenticated user)
- **Request Headers**:
  - `Authorization: Bearer <jwt_token>` (required)
  - `Content-Type: application/json` (required)
- **Request Body**: ChatRequest schema
- **Responses**:
  - **200 OK** (successful chat):
    ```json
    {
      "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
      "message": "Done! I've added 'buy groceries' to your task list.",
      "tool_calls": [
        {
          "tool_name": "add_task",
          "parameters": {"title": "buy groceries", "description": ""},
          "result": "success"
        }
      ],
      "timestamp": "2026-02-09T10:30:00Z"
    }
    ```
  - **400 Bad Request** (invalid input):
    ```json
    {
      "detail": "Message cannot be empty"
    }
    ```
  - **401 Unauthorized** (missing/invalid JWT):
    ```json
    {
      "detail": "Invalid or expired token"
    }
    ```
  - **403 Forbidden** (user_id mismatch):
    ```json
    {
      "detail": "User ID in path does not match authenticated user"
    }
    ```
  - **500 Internal Server Error** (unrecoverable failure):
    ```json
    {
      "detail": "An error occurred processing your request. Please try again."
    }
    ```

### Stateless Request Cycle Flow

```
1. Client → POST /api/{user_id}/chat
   ↓
2. Middleware: Validate JWT and user_id match
   ↓
3. Service: Fetch conversation history from DB
   - Query: SELECT * FROM messages WHERE conversation_id = ? AND user_id = ? ORDER BY timestamp
   ↓
4. Service: Build agent context
   - Load system instructions
   - Load MCP tool definitions
   - Attach conversation history
   ↓
5. Service: Initialize OpenAI Agent
   - Pass system instructions
   - Register MCP tools
   - Provide conversation history
   ↓
6. Service: Process user message through agent
   - Agent analyzes intent
   - Agent calls MCP tools as needed (with user_id)
   - Agent generates natural language response
   ↓
7. Service: Save messages to DB (transaction)
   - INSERT user message
   - INSERT agent response
   - COMMIT transaction
   ↓
8. Service: Return ChatResponse to client
   ↓
9. Client receives response
```

### System Instructions Template

```text
You are a friendly Todo Assistant helping users manage their tasks through natural conversation.

Your capabilities:
- Add new tasks when users describe things they need to do
- List all tasks when users want to see what's on their plate
- Mark tasks as complete when users finish them
- Delete tasks when users no longer need them
- Update task details when users want to make changes

Available tools:
- add_task(title: str, description: str = "") → Creates a new task
- list_tasks() → Returns all user's tasks
- complete_task(task_id: str) → Marks a task as complete
- delete_task(task_id: str) → Removes a task
- update_task(task_id: str, title: str = None, description: str = None) → Updates task details

Communication style:
- Be friendly, warm, and conversational
- Provide clear confirmations after actions (e.g., "Done! I've added 'buy groceries' to your list.")
- Ask for clarification when requests are ambiguous (e.g., "Which task did you want to complete?")
- Explain errors in user-friendly language (e.g., "I couldn't find that task. Could you describe it differently?")
- Use natural language, not technical jargon

Important rules:
- Always use the provided tools to interact with the user's task list
- Never make up task IDs or data - only use what the tools return
- If a tool fails, explain the issue clearly and suggest alternatives
- Keep responses concise but friendly
- When listing tasks, format them clearly with numbers or bullets

Example interactions:
User: "Add a task to buy groceries"
You: "Done! I've added 'buy groceries' to your task list."

User: "Show me my tasks"
You: "Here are your tasks:
1. Buy groceries
2. Finish project report
3. Call dentist"

User: "I'm done with the groceries"
You: "Great! I've marked 'buy groceries' as complete. Nice work!"

User: "Delete the dentist task"
You: "Got it! I've removed 'call dentist' from your list."
```

### Quickstart

See [quickstart.md](./quickstart.md) for complete setup instructions.

**Summary**:
1. Ensure Spec 010 (MCP Server) is deployed and running
2. Set up environment variables in `.env`:
   - `OPENAI_API_KEY`: OpenAI API key for Agents SDK
   - `DATABASE_URL`: Neon PostgreSQL connection string
   - `MCP_SERVER_URL`: MCP server endpoint from Spec 010
   - `BETTER_AUTH_SECRET`: JWT verification secret
3. Install dependencies:
   - `pip install openai-agents-sdk mcp-sdk`
4. Run database migrations (if needed for indexes)
5. Start FastAPI server:
   - `uvicorn src.main:app --reload`
6. Test chat endpoint:
   - Obtain JWT token from auth endpoint
   - Send POST request to `/api/{user_id}/chat`
   - Verify agent response and tool execution

## Architectural Decisions Requiring Documentation

### ADR 1: Stateless Architecture with Database-Driven Context
- **Context**: Need to support horizontal scaling and concurrent users
- **Decision**: Implement pure stateless architecture, fetching all context from database per request
- **Alternatives**:
  - In-memory session storage: Doesn't scale horizontally
  - Redis cache: Adds infrastructure complexity
  - Sticky sessions: Limits scalability
- **Consequences**:
  - ✅ Horizontal scaling without session affinity
  - ✅ Simplified deployment (no state synchronization)
  - ✅ Concurrent user support without conflicts
  - ⚠️ Database query on every request (mitigated with connection pooling and indexes)
  - ⚠️ Slightly higher latency vs. in-memory (acceptable for 500ms target)
- **Status**: Approved
- **Suggest ADR**: 📋 Architectural decision detected: Stateless architecture with database-driven context. Document? Run `/sp.adr stateless-chat-architecture`

### ADR 2: OpenAI Agents SDK vs. Custom Agent Implementation
- **Context**: Need agent orchestration for tool calling and conversation management
- **Decision**: Use OpenAI Agents SDK for agent implementation
- **Alternatives**:
  - LangChain: More flexible but heavier
  - Custom implementation: Full control but high complexity
  - Direct Chat Completions API: Lower-level, manual tool orchestration
- **Consequences**:
  - ✅ Robust, well-tested agent framework
  - ✅ Built-in tool calling and error handling
  - ✅ Reduced custom code and maintenance
  - ⚠️ Dependency on OpenAI SDK updates
  - ⚠️ Less flexibility for custom agent behaviors
- **Status**: Approved
- **Suggest ADR**: 📋 Architectural decision detected: OpenAI Agents SDK for agent orchestration. Document? Run `/sp.adr openai-agents-sdk-choice`

### ADR 3: Full Conversation History vs. Sliding Window
- **Context**: Need to provide agent with conversation context
- **Decision**: Load full conversation history (up to 50 messages) on every request
- **Alternatives**:
  - Sliding window (last 10 messages): Loses context
  - Summarization: Adds complexity, may lose details
  - Separate context service: Infrastructure overhead
- **Consequences**:
  - ✅ Complete context for accurate responses
  - ✅ Simple implementation (single DB query)
  - ✅ No context loss for multi-turn conversations
  - ⚠️ Higher token usage for long conversations (mitigated with 50 message limit)
  - ⚠️ Larger DB queries (mitigated with indexes and pagination)
- **Status**: Approved
- **Suggest ADR**: 📋 Architectural decision detected: Full conversation history loading. Document? Run `/sp.adr conversation-history-strategy`

## Testing Strategy

### Unit Tests
- **Agent Prompt Construction**: Verify system instructions are correctly formatted
- **Tool Call Parameter Extraction**: Test NL to tool parameter mapping
- **Error Handling**: Test each failure mode (DB error, OpenAI API error, MCP tool error)
- **User ID Validation**: Verify user_id matching logic
- **Message Persistence**: Test transaction handling for message saves

### Integration Tests
- **End-to-End Chat Flow**: Send message → agent processes → tool executes → response returns
- **MCP Tool Integration**: Verify all 5 MCP tools are callable and return expected results
- **Database Persistence**: Verify messages are saved and retrievable
- **Conversation Context Retrieval**: Test history loading with various conversation lengths
- **Multi-Turn Conversations**: Test context preservation across multiple messages

### Load Tests
- **100 Concurrent Users**: Use locust to simulate 100 users sending messages simultaneously
- **Sustained Load**: Run for 10 minutes to detect memory leaks or performance degradation
- **Random Server Restarts**: Verify stateless architecture by restarting server mid-test
- **Cross-Talk Detection**: Verify no user data leakage between concurrent requests

### Acceptance Tests
- **Natural Language Command Mapping**: Test 20+ diverse NL inputs for correct tool mapping
- **Context Preservation**: Test 5-turn conversations to verify context is maintained
- **Friendly Response Generation**: Verify agent provides confirmations in 100% of successful tool executions
- **Error Message Clarity**: Test error scenarios and verify user-friendly messages

### Property-Based Tests
- **Stateless Property**: For any request sequence, restarting server should not affect results
- **User Isolation Property**: For any two users, user A's messages should never appear in user B's history
- **Idempotency Property**: Sending same message twice should produce consistent results (with different timestamps)

## Next Steps

This plan will be followed by:
1. **Phase 2: Task Generation** (`/sp.tasks`) - Break down this plan into actionable, ordered tasks
2. **Phase 3: Implementation** (`/sp.implement`) - Execute tasks via specialized agents
3. **Phase 4: Testing & Validation** - Verify all acceptance scenarios pass
4. **Phase 5: Load Testing** - Validate 100 concurrent user support
5. **Phase 6: Documentation** - Complete API documentation and quickstart guide
6. **Phase 7: Commit & PR** (`/sp.git.commit_pr`) - Create pull request for review

**Implementation Sequence**:
1. Set up OpenAI Agents SDK integration (agent initialization, system instructions)
2. Implement MCP tool definitions for agent (tool schemas matching Spec 010)
3. Build stateless request cycle service (fetch history → run agent → save messages → return)
4. Create chat endpoint with user validation middleware
5. Implement conversation history service (DB queries with indexes)
6. Add error handling and user-friendly error messages
7. Write unit tests for each component
8. Write integration tests for end-to-end flow
9. Implement load testing with locust
10. Optimize database queries and connection pooling
11. Document API and create quickstart guide

**Critical Path**:
- OpenAI Agents SDK must be configured before agent can process messages
- MCP tool definitions must match Spec 010 tool signatures exactly
- Conversation history service must be optimized before load testing
- User validation middleware must be in place before endpoint is exposed
- Database indexes must be created before performance testing

**Agent Assignments**:
- `fastapi-backend-architect`: Chat endpoint, request cycle orchestration, response handling
- `ai-integration-specialist`: OpenAI Agents SDK integration, system instructions, prompt engineering
- `neon-db-manager`: Conversation history queries, message persistence, index optimization
- `spec-driven-architect`: Cross-stack coordination with Spec 010 MCP tools

**Estimated Complexity**: High (AI agent integration, stateless architecture, MCP tool orchestration, multi-user concurrency)

**Dependencies**:
- **Spec 010 (MCP Server)**: MUST be completed and deployed before implementation
  - Requires: Conversation and Message tables
  - Requires: MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
  - Requires: User authentication and authorization

**Risk Mitigation**:
- OpenAI API rate limits: Implement exponential backoff and request queuing
- Database latency: Use connection pooling and query optimization
- Agent misinterpretation: Comprehensive prompt engineering and testing
- Concurrent request race conditions: Use database transactions and proper isolation levels
- Tool execution failures: Graceful error handling and user-friendly messages

