# AI Agent React Frontend

Modern React frontend application for the AI Agent system, built with TypeScript, React Bootstrap, and following the design1-modern style.

## Features

- **Chat Interface**: Create and manage AI conversations
- **Modern Design**: Clean, responsive UI inspired by design1-modern
- **TypeScript**: Full type safety and better developer experience
- **Bootstrap**: Responsive design and UI components
- **Docker**: Containerized deployment with multi-stage builds

## API Endpoints Supported

- `POST /chat` - Create new chat conversation
- `GET /chats` - Get list of user chats
- `GET /chats/{chat_id}` - Get specific chat details

## Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
cd app/Frontend
npm install
```

### Running Locally

```bash
cd app/Frontend
npm start
```

The application will be available at `http://localhost:3000`

### Environment Variables

Create a `.env` file with:

```
REACT_APP_API_URL=http://localhost:8000
```

## Docker Deployment

### Build Docker Image

```bash
cd app/Frontend
docker build -t ai-agent-frontend .
```

### Run with Docker

```bash
cd app/Frontend
docker run -p 3000:80 ai-agent-frontend
```

### Run with Docker Compose

```bash
cd app/Frontend
docker-compose up
```

This will start:
- Frontend on port 3000
- Backend on port 8000
- PostgreSQL on port 5432
- Qdrant on port 6333

## Project Structure

```
app/Frontend/
├── src/
│   ├── components/
│   │   ├── ChatDashboard.tsx    # Main dashboard component
│   │   ├── ChatList.tsx         # Chat history sidebar
│   │   ├── ChatWindow.tsx       # Chat conversation view
│   │   ├── NewChatForm.tsx      # Create new chat form
│   │   └── Navbar.tsx           # Navigation bar
│   ├── services/
│   │   └── chatApi.ts           # API client for chat endpoints
│   ├── types/
│   │   └── chat.ts              # TypeScript type definitions
│   ├── App.tsx                  # Main app component
│   ├── App.css                  # Custom styles
│   └── index.tsx                # App entry point
├── mockups/                     # Original design mockups
├── Dockerfile                   # Docker configuration
├── docker-compose.yml          # Full stack setup
├── nginx.conf                  # Nginx configuration
└── package.json                # Dependencies
```

## Design System

The application follows the design1-modern style with:

- **Color Scheme**: Blue gradients (#667eea to #764ba2)
- **Typography**: System fonts with good hierarchy
- **Components**: Cards, gradients, and modern shadows
- **Responsive**: Mobile-first approach with Bootstrap

## Key Components

### ChatDashboard
Main component that orchestrates the chat experience with sidebar and main content area.

### ChatList
Displays chat history with search and selection capabilities.

### ChatWindow
Shows individual chat conversations with user and AI messages.

### NewChatForm
Form for creating new chat conversations with model selection and system prompts.

## API Integration

The frontend uses Axios for API calls with proper error handling and TypeScript types. The API client is located in `src/services/chatApi.ts`.

## Production Considerations

- Multi-stage Docker build for optimized production images
- Nginx configuration for serving static files
- Environment-based API URL configuration
- Security headers and compression enabled
- Proper error handling and loading states

## Future Enhancements

- Add document and user management features
- Implement real-time chat updates
- Add authentication and user management
- Implement chat search and filtering
- Add export functionality for chat history