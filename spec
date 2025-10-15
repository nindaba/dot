# Chat System API Documentation

## Overview

The Travomate Chat System provides real-time messaging between travelers and parcel senders. A chat is automatically created when a booking is paid, enabling both parties to communicate about the delivery.

## Data Models

### Chat
Represents a conversation between two users about a specific booking.

**Fields**:
- `id`: Internal database ID
- `uid`: External UUID for API identification
- `subject`: Chat title (e.g., "Paris -> London")
- `status`: Chat status (OPEN, CLOSED, DELETED)
- `booking`: UUID reference to the associated booking
- `users`: Array of users in the chat (traveler + parcel sender)
- `messages`: Array of messages in the chat
- `createdAt`, `updatedAt`: Audit timestamps

### Message
Represents a single message within a chat.

**Fields**:
- `id`: Internal database ID
- `uid`: External UUID for API identification
- `sender`: UUID of the user who sent the message
- `contentType`: Type of content (TEXT, IMAGE, VIDEO, AUDIO, FILE)
- `content`: Message content or media reference
- `modificationStatus`: Tracks if message was edited/deleted (null, DELETED)
- `status`: Delivery status (SENT, READ)
- `reply`: Optional reference to another message being replied to
- `chat`: Reference to parent chat
- `createdAt`, `updatedAt`: Audit timestamps

### Enumerations

#### ChatStatus
- `OPEN`: Chat is active
- `CLOSED`: Chat is closed
- `DELETED`: Chat is deleted

#### MessageStatus
- `SENT`: Message sent successfully
- `READ`: Message read by recipient

#### MessageContentType
- `TEXT`: Text message
- `IMAGE`: Image file
- `VIDEO`: Video file
- `AUDIO`: Audio file
- `FILE`: Generic file

#### BookingStatus
- `NEW`: Initial booking request
- `CONFIRMED`: Traveler confirmed
- `DECLINED`: Traveler declined
- `CANCELED`: Booking canceled
- `PAID`: Payment completed - **CHAT CREATION TRIGGER**
- `REFUNDED`: Payment refunded
- `RECEIVED`: Traveler received parcel
- `DELIVERED`: Parcel delivered to recipient
- `COMPLETED`: Booking completed

## Chat Creation Flow

### Trigger: Booking Status → PAID

When a booking transitions to `PAID` status, the system automatically creates a chat.

#### Sequence Diagram

```
Client → API: PUT /api/v1/bookings/{uid}/status/PAID
API → BookingService: update booking status
BookingService → ChatService: create chat automatically
ChatService → Database: save chat with 2 users
ChatService → NotificationService: create notification
NotificationService → WebSocket: send notification to users
Client ← WebSocket: receive notification
```

#### Flow Steps

1. **Client updates booking to PAID**
   - Endpoint: `PUT /api/v1/bookings/{booking-uid}/status/PAID`
   - Authorization required

2. **Backend automatically creates chat**
   - Fetches trip details for subject (e.g., "Paris → London")
   - Resolves two participants:
     - Trip owner (traveler)
     - Parcel owner (client)
   - Creates chat with:
     - Status: OPEN
     - Booking reference (UUID)
     - Subject: "FromCity → ToCity"
     - Two users array

3. **Backend sends notifications**
   - Confirmation emails to both parties
   - WebSocket notification with chat details

## API Endpoints

### Base Path
- `/api/chats` or `/api/v1/chats`

### Chat Endpoints

#### 1. Create Chat
**POST** `/api/chats`

Creates a new chat for a booking (alternative to automatic creation).

**Request Body:**
```json
{
  "booking": "550e8400-e29b-41d4-a716-446655440000",
  "subject": "Paris -> London"
}
```

**Response:** `201 Created`
```json
{
  "id": 123,
  "uid": "660e8400-e29b-41d4-a716-446655440001",
  "subject": "Paris -> London",
  "status": "OPEN",
  "booking": "550e8400-e29b-41d4-a716-446655440000",
  "users": [
    {"uValue": "user-uid-1"},
    {"uValue": "user-uid-2"}
  ],
  "createdAt": "2025-10-15T10:30:00Z",
  "updatedAt": "2025-10-15T10:30:00Z"
}
```

#### 2. Get All Chats
**GET** `/api/v1/user-accounts/current/chats?page=0&size=20&eagerload=true`

Returns paginated list of chats for the current user.

**Response:** `200 OK`
```json
[
  {
    "id": 123,
    "uid": "660e8400-e29b-41d4-a716-446655440001",
    "subject": "Paris -> London",
    "status": "OPEN",
    "booking": "550e8400-e29b-41d4-a716-446655440000",
    "users": [...],
    "createdAt": "2025-10-15T10:30:00Z",
    "updatedAt": "2025-10-15T10:30:00Z"
  }
]
```

**Headers:**
- `X-Total-Count`: Total number of chats
- `Link`: Pagination links

#### 3. Get Chat by ID
**GET** `/api/chats/{id}`

Returns a specific chat with eager-loaded relationships.

**Response:** `200 OK`
```json
{
  "id": 123,
  "uid": "660e8400-e29b-41d4-a716-446655440001",
  "subject": "Paris -> London",
  "status": "OPEN",
  "booking": "550e8400-e29b-41d4-a716-446655440000",
  "users": [
    {"id": 1, "uValue": "user-uid-1"},
    {"id": 2, "uValue": "user-uid-2"}
  ],
  "createdAt": "2025-10-15T10:30:00Z",
  "updatedAt": "2025-10-15T10:30:00Z"
}
```

#### 4. Update Chat
**PUT** `/api/chats/{id}`

Updates an existing chat (typically for status changes).

**Request Body:**
```json
{
  "id": 123,
  "status": "CLOSED"
}
```

**Response:** `200 OK`

#### 5. Delete Chat
**DELETE** `/api/chats/{id}`

Deletes a chat (soft delete recommended).

**Response:** `204 No Content`

### Message Endpoints

#### 6. Send Message to Chat
**POST** `/api/chats/{id}/messages`

Sends a new message to a specific chat.

**Request Body:**
```json
{
  "content": "Hello! I'm ready to pick up the parcel.",
  "contentType": "TEXT"
}
```

**Optional Content Types:**
- `TEXT`: Plain text message
- `IMAGE`: Image file (content = media UUID)
- `VIDEO`: Video file (content = media UUID)
- `AUDIO`: Audio file (content = media UUID)
- `FILE`: Generic file (content = media UUID)

**Response:** `200 OK`

**Side Effects:**
1. Message is saved with current user as sender
2. Message status set to SENT
3. Notification created and sent via WebSocket
4. Other chat participants receive real-time notification

#### 7. Get Chat Messages
**GET** `/api/chats/{id}/messages?page=0&size=20`

Returns paginated messages for a specific chat, ordered by creation time.

**Response:** `200 OK`
```json
[
  {
    "id": 456,
    "uid": "770e8400-e29b-41d4-a716-446655440002",
    "sender": "user-uid-1",
    "contentType": "TEXT",
    "content": "Hello! I'm ready to pick up the parcel.",
    "modificationStatus": null,
    "status": "SENT",
    "createdAt": "2025-10-15T10:35:00Z",
    "updatedAt": "2025-10-15T10:35:00Z",
    "chat": {
      "id": 123
    },
    "reply": null
  }
]
```

**Headers:**
- `X-Total-Count`: Total message count
- `Link`: Pagination links

#### 8. Create Message (Alternative)
**POST** `/api/messages`

Alternative endpoint for creating messages directly.

**Request Body:**
```json
{
  "chat": {
    "id": 123
  },
  "content": "Thank you!",
  "contentType": "TEXT",
  "status": "SENT"
}
```

**Response:** `201 Created`

#### 9. Update Message
**PUT** `/api/messages/{id}`

Updates a message (e.g., mark as read).

**Request Body:**
```json
{
  "id": 456,
  "status": "READ"
}
```

**Response:** `200 OK`

#### 10. Delete Message
**DELETE** `/api/messages/{id}`

Soft-deletes a message by setting `modificationStatus` to DELETED and clearing content.

**Response:** `204 No Content`

## Complete Example Flow

### Scenario: User pays for booking and starts chatting

#### Step 1: Update Booking to PAID
```http
PATCH /api/bookings/550e8400-e29b-41d4-a716-446655440000
Content-Type: application/json
Authorization: Bearer <token>

{
  "status": "PAID"
}
```

**Backend Actions:**
1. Booking status updated to PAID
2. Trip status updated to BOOKED
3. Trip remaining weight reduced
4. **Chat automatically created** with:
   - Traveler (trip owner)
   - Client (parcel sender)
   - Subject: "Paris -> London"
   - Status: OPEN
5. Emails sent to both parties
6. Notification sent via WebSocket

#### Step 2: Client Receives WebSocket Notification
```json
{
  "type": "BOOKING_PAID",
  "booking": {
    "uid": "550e8400-e29b-41d4-a716-446655440000",
    "status": "PAID"
  },
  "chat": {
    "uid": "660e8400-e29b-41d4-a716-446655440001",
    "subject": "Paris -> London"
  }
}
```

#### Step 3: Client Fetches Available Chats
```http
GET /api/chats?page=0&size=20&eagerload=true
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 123,
    "uid": "660e8400-e29b-41d4-a716-446655440001",
    "subject": "Paris -> London",
    "status": "OPEN",
    "booking": "550e8400-e29b-41d4-a716-446655440000",
    "users": [
      {"uValue": "traveler-uid"},
      {"uValue": "client-uid"}
    ],
    "createdAt": "2025-10-15T10:30:00Z",
    "updatedAt": "2025-10-15T10:30:00Z"
  }
]
```

#### Step 4: Client Opens Chat and Fetches Messages
```http
GET /api/chats/123/messages?page=0&size=20
Authorization: Bearer <token>
```

**Response:** `200 OK` (empty initially)
```json
[]
```

#### Step 5: Client Sends First Message
```http
POST /api/chats/123/messages
Content-Type: application/json
Authorization: Bearer <token>

{
  "content": "Hi! I'm available to drop off the parcel tomorrow at 2 PM. Does that work?",
  "contentType": "TEXT"
}
```

**Response:** `200 OK`

**Backend Actions:**
1. Message created with sender = current user UID
2. Message status set to SENT
3. Notification created
4. WebSocket notification sent to traveler

#### Step 6: Traveler Receives WebSocket Notification
```json
{
  "type": "NEW_MESSAGE",
  "chat": {
    "id": 123,
    "uid": "660e8400-e29b-41d4-a716-446655440001"
  },
  "message": {
    "uid": "770e8400-e29b-41d4-a716-446655440002",
    "sender": "client-uid",
    "content": "Hi! I'm available to drop off the parcel tomorrow at 2 PM. Does that work?",
    "status": "SENT"
  }
}
```

#### Step 7: Traveler Replies
```http
POST /api/chats/123/messages
Content-Type: application/json
Authorization: Bearer <token>

{
  "content": "Perfect! I'll meet you at the agreed location. See you then!",
  "contentType": "TEXT"
}
```

**Response:** `200 OK`

#### Step 8: Both Users Fetch Message History
```http
GET /api/chats/123/messages?page=0&size=20
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 456,
    "uid": "770e8400-e29b-41d4-a716-446655440002",
    "sender": "client-uid",
    "contentType": "TEXT",
    "content": "Hi! I'm available to drop off the parcel tomorrow at 2 PM. Does that work?",
    "modificationStatus": null,
    "status": "READ",
    "createdAt": "2025-10-15T10:35:00Z",
    "updatedAt": "2025-10-15T10:35:30Z",
    "chat": {"id": 123},
    "reply": null
  },
  {
    "id": 457,
    "uid": "880e8400-e29b-41d4-a716-446655440003",
    "sender": "traveler-uid",
    "contentType": "TEXT",
    "content": "Perfect! I'll meet you at the agreed location. See you then!",
    "modificationStatus": null,
    "status": "SENT",
    "createdAt": "2025-10-15T10:37:00Z",
    "updatedAt": "2025-10-15T10:37:00Z",
    "chat": {"id": 123},
    "reply": null
  }
]
```

#### Step 9: Mark Message as Read
```http
PUT /api/messages/456
Content-Type: application/json
Authorization: Bearer <token>

{
  "id": 456,
  "status": "READ"
}
```

**Response:** `200 OK`

#### Step 10: Send Image
```http
POST /api/chats/123/messages
Content-Type: application/json
Authorization: Bearer <token>

{
  "content": "990e8400-e29b-41d4-a716-446655440004",
  "contentType": "IMAGE"
}
```

**Note:** For non-TEXT content types, the `content` field contains the UUID of a media file uploaded via the Media API.

## WebSocket Integration

### Connection
**Endpoint:** `/websocket/tracker`

**Protocol:** STOMP over SockJS

**Example (JavaScript):**
```javascript
import SockJS from 'sockjs-client';
import Stomp from 'stompjs';

const socket = new SockJS('http://localhost:8080/websocket/tracker');
const stompClient = Stomp.over(socket);

stompClient.connect(
  { Authorization: `Bearer ${token}` },
  () => {
    console.log('Connected to WebSocket');

    // Subscribe to user-specific notifications
    stompClient.subscribe('/user/topic/notifications', (message) => {
      const notification = JSON.parse(message.body);
      console.log('Received notification:', notification);

      // Handle new message notification
      if (notification.type === 'NEW_MESSAGE') {
        // Update chat UI
        loadMessages(notification.chat.id);
      }
    });
  },
  (error) => {
    console.error('WebSocket connection error:', error);
  }
);
```

### Topics
- `/topic/notifications`: Broadcast notifications (all users)
- `/user/topic/notifications`: User-specific notifications (targeted)

### Notification Flow
1. User sends message via REST API
2. Backend persists message
3. Backend creates notification
4. `NotificationWebSocketService` sends notification to recipient via WebSocket
5. Recipient's client receives notification in real-time
6. Client updates UI without polling

## Security & Access Control

### Authentication
- All endpoints require JWT authentication (AWS Cognito)
- Include JWT token in `Authorization` header: `Bearer <token>`

### Authorization
- Users can only access their own chats
- Message sender is automatically set to the authenticated user
- Access denied errors return HTTP 403

## Error Handling

### Common Exceptions
- `EntityStatusNotFoundException`: Chat or booking not found
- `AccessDeniedException`: User lacks permission to access chat
- `BadRequestAlertException`: Invalid request (e.g., missing ID, invalid status)

### Example Error Response
```json
{
  "type": "https://www.jhipster.tech/problem/entity-not-found",
  "title": "Entity not found",
  "status": 404,
  "detail": "Chat 999 not found",
  "entityName": "chat",
  "errorKey": "idnotfound"
}
```

## Best Practices

### Client Implementation
1. **Establish WebSocket connection on login** to receive real-time notifications
2. **Subscribe to user-specific topic** `/user/topic/notifications`
3. **Handle reconnection logic** for dropped connections
4. **Implement message pagination** for long chat histories
5. **Cache chat list** and update on notifications
6. **Mark messages as read** when chat is opened
7. **Handle media content** by fetching media URLs from Media API

## Troubleshooting

### Chat not created when booking is paid
- Verify the booking UID is correct
- Ensure both trip owner and parcel owner users exist
- Check that booking status successfully transitions to PAID
- Review API response for error messages

### Messages not received in real-time
- Verify WebSocket connection is established (check browser console)
- Ensure correct subscription to `/user/topic/notifications`
- Check CORS configuration allows WebSocket connections
- Inspect network tab for WebSocket frames

### Cannot send messages
- Verify JWT token is valid and not expired
- Confirm the chat exists and user is a participant
- Check that the chat status is OPEN
- Review HTTP response status codes (403 = unauthorized, 404 = chat not found)

## Summary

The Travomate Chat System provides seamless real-time communication between travelers and parcel senders:

1. **Automatic Creation**: Chat is created automatically when a booking reaches PAID status
2. **Two Participants**: Each chat includes the traveler (trip owner) and client (parcel sender)
3. **Real-time Messaging**: WebSocket integration enables instant message delivery
4. **Rich Content**: Supports text, images, videos, audio, and files
5. **Notifications**: All message events trigger notifications to recipients
6. **Security**: JWT authentication and user-specific access control
7. **RESTful API**: Simple and consistent API endpoints for all operations

## Quick Start Example

```javascript
// 1. Update booking to PAID (triggers chat creation)
PUT /api/v1/bookings/{{booking-uid}}/status/PAID
Authorization: Bearer {{token}}

// 2. Fetch user's chats
GET /api/v1/user-accounts/current/chats
Authorization: Bearer {{token}}

// 3. Get messages for specific chat
GET /api/chats/{{chat-id}}/messages?page=0&size=20
Authorization: Bearer {{token}}

// 4. Send a message
POST /api/chats/{{chat-id}}/messages
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "content": "Hello! When can we arrange pickup?",
  "contentType": "TEXT"
}

// 5. Mark message as read
PUT /api/messages/{{message-id}}
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "id": {{message-id}},
  "status": "READ"
}
```
