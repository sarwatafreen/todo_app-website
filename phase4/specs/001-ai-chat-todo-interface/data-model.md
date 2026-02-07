# Data Model: AI-Powered Chat Interface for Todo Management

## Entity: Conversation

**Description**: Represents a continuous interaction session between user and AI assistant, uniquely identified by conversation_id

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the conversation
- `title`: String (Optional) - Auto-generated from first message if not provided
- `user_id`: String - Owner of the conversation (matches JWT authenticated user)
- `created_at`: DateTime - Timestamp when conversation was created
- `updated_at`: DateTime - Timestamp when conversation was last updated

**Relationships**:
- One Conversation to Many Messages (one-to-many relationship)
- One User to Many Conversations (one-to-many relationship)

**Validation Rules**:
- `user_id` must match the authenticated user from JWT token
- `title` is optional, auto-generated from first message content if not provided
- `created_at` is set automatically on creation
- `updated_at` is updated automatically on any change

## Entity: Message

**Description**: Represents individual exchanges in a conversation, containing user_id, conversation_id, role (user/assistant), content, and timestamp

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the message
- `conversation_id`: UUID (Foreign Key) - Links to parent conversation
- `user_id`: String - Owner of the message (matches JWT authenticated user)
- `role`: String (Enum: 'user' | 'assistant') - Identifies who sent the message
- `content`: String - The actual message content
- `timestamp`: DateTime - When the message was created
- `order_index`: Integer - Sequential ordering of messages in conversation

**Relationships**:
- One Message to One Conversation (many-to-one relationship)
- One Message to One User (many-to-one relationship)

**Validation Rules**:
- `conversation_id` must exist in conversations table
- `user_id` must match the authenticated user from JWT token
- `role` must be either 'user' or 'assistant'
- `content` must not be empty
- `order_index` must be sequential within the conversation
- `timestamp` is set automatically on creation

## State Transitions

**Conversation**:
- State: Created → Active → Archived (potential future state)
- Transitions: Created when first message is sent, remains active as long as messages continue

**Message**:
- State: Pending → Processed → Stored
- Transitions: User message created → Agent processes → Agent response stored

## Database Constraints

- Foreign key constraint: messages.conversation_id references conversations.id
- Foreign key constraint: messages.user_id and conversations.user_id reference users table (implicit through authentication)
- Index on conversations.user_id for efficient user-based queries
- Index on messages.conversation_id for efficient conversation-based queries
- Index on messages.timestamp for chronological ordering
- Check constraint: message role must be 'user' or 'assistant'
- Unique constraint: none (messages can have duplicate content)

## Access Control

- All queries must filter by user_id to enforce user isolation
- Conversation access restricted to owner via user_id comparison
- Message access restricted to owner via user_id comparison
- Authentication required for all operations (verified via JWT)