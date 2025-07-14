# AI Agent v2 - RAG-Powered Conversational AI System

A production-ready AI application combining document management, vector search, and multi-model AI capabilities to provide intelligent, context-aware responses.

This is an application designed for educational purposes. It's likely that we could find better alternatives for all of its functionalities on the internet.

## 🚀 Core Features

### **Chat & AI Integration**
- 🤖 Multi-model AI support (OpenAI GPT-4, Google Gemini family)
- 💬 Persistent conversation history with context management
- 🧠 RAG (Retrieval-Augmented Generation) for context-aware responses
- 📝 Automatic source attribution for transparency

### **Document Management**
- 📄 Markdown document upload and processing
- ✂️ Intelligent token-based text splitting
- 🔍 Semantic search using vector embeddings
- 🗄️ Dual storage: PostgreSQL + Qdrant vector database

### **Infrastructure**
- ⚡ FastAPI with async/await support
- 🐳 Containerized with Docker Compose
- 🛢️ PostgreSQL for relational data
- 🎯 Qdrant for vector similarity search
- ⚛️ React frontend with real-time updates

## 🏃 Quick Start

### Prerequisites

- Docker and Docker Compose
- Make (for simplified commands)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Ai-agent-v2
```

### 2. Environment Configuration

Create `.env` file in `app/API/` directory:

```env
# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO

# Database Configuration (Docker defaults - modify if needed)
DB_HOST=postgres
DB_PORT=5432
DB_NAME=ai_agent_db
DB_USER=ai_agent
DB_PASSWORD=ai_agent_password

# Qdrant Vector Database
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_GRPC_PORT=6334

# Document Processing
DOCUMENT_TOKEN_LIMIT=500
CORPUS_PATH=./Corpus

# OpenAI Embeddings
EMBEDDING_MODEL=text-embedding-ada-002
VECTOR_SIZE=1536
```

### 3. Start the Application

```bash
# Build and start all services (PostgreSQL, Qdrant, API, Frontend)
make build
make up

# Or in one command
make build && make up
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8008
- **API Documentation**: http://localhost:8008/docs

### 4. Verify Installation

```bash
# Check container status
docker-compose ps

# View logs
make logs

# Test API health
curl http://localhost:8008/health
```

## 📡 API Endpoints

### **Chat Management**
- `POST /chat/create` - Create new chat session
- `GET /chat/list` - Get all chats (with pagination)
- `GET /chat/{chat_id}` - Get specific chat with history
- `POST /chat/{chat_id}/message` - Send message in chat
- `DELETE /chat/{chat_id}` - Delete chat and all associated messages

### **Document Management**
- `POST /document/upload` - Upload markdown document
- `GET /document/list` - List all documents
- `GET /document/{document_id}` - Get specific document
- `DELETE /document/{document_id}` - Delete document
- `POST /document/search` - Search documents by prompt

### **User Management**
- `POST /user/create` - Create new user
- `GET /user/list` - List all users
- `GET /user/{user_id}` - Get specific user
- `DELETE /user/{user_id}` - Delete user

### **System**
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

## 🛠️ Make Commands

```bash
# Basic Operations
make help          # Show all available commands
make build         # Build Docker images
make up            # Start all services
make down          # Stop all services
make logs          # View container logs
make shell         # Enter API container shell

# Testing
make test          # Run basic tests
make run-tests     # Run tests with verbose output

# Maintenance
make clean         # Remove containers and volumes

# Production
make build-prod    # Build production image
make up-prod       # Start production services
make down-prod     # Stop production services
```

## 🏗️ Architecture

### **Services Overview**
- **Frontend (React)**: Port 3000 - Interactive web UI
- **API (FastAPI)**: Port 8008 - Core application logic
- **PostgreSQL**: Port 5432 - Relational data storage
- **Qdrant**: Port 6333 - Vector similarity search

### **Data Flow**
1. User uploads documents → API processes & splits text
2. Text chunks → OpenAI embeddings → Qdrant storage
3. User sends chat message → RAG retrieves context
4. Context + prompt → AI model → Response with sources

## 🧪 Testing

```bash
# Run all tests with coverage
make run-tests

# Run specific test file
docker-compose exec web pytest tests/path/to/test.py -v

# Enter container for debugging
make shell
```

## 🚨 Troubleshooting

### **Common Issues**

**1. API Key Errors**
```bash
# Verify .env file exists in app/API/
ls app/API/.env

# Check if keys are set
docker-compose exec web env | grep API_KEY
```

**2. Port Conflicts**
```bash
# Check if ports are in use
lsof -i :3000  # Frontend
lsof -i :8008  # API
lsof -i :5432  # PostgreSQL
lsof -i :6333  # Qdrant
```

**3. Container Issues**
```bash
# View detailed logs
docker-compose logs -f [service_name]

# Restart specific service
docker-compose restart [service_name]

# Full reset
make clean && make build && make up
```

## 📚 Usage Examples

### **Upload a Document**
```bash
curl -X POST http://localhost:8008/document/upload \
  -F "file=@document.md" \
  -F "user_id=123"
```

### **Create a Chat**
```bash
curl -X POST http://localhost:8008/chat/create \
  -H "Content-Type: application/json" \
  -d '{"user_id": "123", "title": "My Chat"}'
```

### **Send a Message**
```bash
curl -X POST http://localhost:8008/chat/{chat_id}/message \
  -H "Content-Type: application/json" \
  -d '{"content": "Tell me about the uploaded document"}'
```

## 🔒 Security Considerations

- Store API keys securely - never commit `.env` files
- Use environment-specific configurations
- Regularly update dependencies
- Monitor API usage and rate limits
- Consider implementing authentication for production

## 📈 Performance Tips

- Adjust `DOCUMENT_TOKEN_LIMIT` based on your needs
- Monitor Qdrant memory usage for large document sets
- Use pagination for listing endpoints
- Consider caching for frequently accessed documents

## 🛣️ Roadmap

- [ ] Support for more document formats (PDF, DOCX)
- [ ] Advanced RAG strategies (HyDE, multi-query)
- [ ] User authentication and authorization
- [ ] Admin dashboard for monitoring
- [ ] Batch document processing
- [ ] Export conversation history

## 📄 License

This project is licensed under the MIT License.
