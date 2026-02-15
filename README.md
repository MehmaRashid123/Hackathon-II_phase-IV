# 🚀 Todo Chatbot - AI-Powered Task Management

[![Phase IV Complete](https://img.shields.io/badge/Phase%20IV-Complete-success)](./K8S_DEPLOYMENT_COMPLETE.md)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5?logo=kubernetes)](./deploy/README.md)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)](./backend/Dockerfile)
[![Helm](https://img.shields.io/badge/Helm-Charts-0F1689?logo=helm)](./deploy/helm/todo-chatbot)

A modern, AI-powered todo application with intelligent chatbot assistance, built with Next.js, FastAPI, and deployed on Kubernetes.

---

## 🎯 Project Overview

This is a full-stack todo application that combines traditional task management with AI-powered chatbot assistance. Users can manage tasks through a beautiful UI or interact with an intelligent chatbot that understands natural language commands.

### Key Features

- ✅ **Task Management**: Create, update, delete, and organize tasks
- 🤖 **AI Chatbot**: Natural language task management with multiple AI models
- 📊 **Analytics Dashboard**: Track productivity and task completion
- 🎨 **Modern UI**: Beautiful, responsive interface with dark mode
- 🔐 **Authentication**: Secure user authentication with Better Auth
- ☁️ **Cloud Native**: Fully containerized and Kubernetes-ready

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│  - React Components                                          │
│  - Chatbot Interface                                         │
│  - Analytics Dashboard                                       │
│  - Task Management UI                                        │
└──────────────────┬───────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  - REST API                                                  │
│  - AI Model Integration (Gemini, Groq, OpenRouter)          │
│  - Task Management Logic                                     │
│  - Authentication & Authorization                            │
└──────────────────┬───────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                  Database (PostgreSQL)                       │
│  - Neon Serverless PostgreSQL                                │
│  - User Data                                                 │
│  - Tasks & Conversations                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Phase IV: Kubernetes Deployment (COMPLETE)

### ✅ What's Been Accomplished

Phase IV implements **Cloud Native deployment** with Kubernetes, Helm, and Docker:

- ✅ **Containerization**: Multi-stage Docker builds for frontend and backend
- ✅ **Helm Charts**: Complete Helm chart with templating and configuration
- ✅ **Kubernetes Manifests**: Deployments, Services, ConfigMaps, and Secrets
- ✅ **Automated Deployment**: Cross-platform scripts for easy deployment
- ✅ **Comprehensive Documentation**: Step-by-step guides and troubleshooting
- ✅ **Production Ready**: Health checks, resource limits, rolling updates

### 📦 Deliverables

```
deploy/
├── helm/todo-chatbot/          # Complete Helm chart
│   ├── Chart.yaml              # Chart metadata
│   ├── values.yaml             # Default configuration
│   ├── values-local.yaml       # Minikube overrides
│   └── templates/              # Kubernetes manifests
│       ├── backend-deployment.yaml
│       ├── backend-service.yaml
│       ├── frontend-deployment.yaml
│       ├── frontend-service.yaml
│       └── configmap.yaml
├── scripts/                    # Deployment automation
│   ├── deploy-to-minikube.sh  # Full deployment (Linux/macOS)
│   ├── deploy-to-minikube.bat # Full deployment (Windows)
│   ├── create-secrets.sh      # Secret management
│   └── verify-docker-builds.sh
├── README.md                   # Comprehensive deployment guide
├── QUICK_START.md              # 5-minute quick start
└── DEPLOYMENT_STATUS.md        # Current status
```

### 🎯 Quick Deployment

Deploy the entire application to Minikube in 5 minutes:

```bash
# Windows
deploy\scripts\deploy-to-minikube.bat

# Linux/macOS
./deploy/scripts/deploy-to-minikube.sh
```

**What the script does:**
1. ✅ Checks prerequisites (Docker, Minikube, kubectl, Helm)
2. 🚀 Starts Minikube cluster
3. 🏗️ Builds Docker images
4. 📦 Loads images into Minikube
5. 🔐 Creates Kubernetes secrets
6. 🎯 Deploys with Helm
7. ⏳ Waits for pods to be ready
8. 🎉 Displays access information

### 📚 Documentation

- **[Deployment Guide](./deploy/README.md)**: Comprehensive deployment documentation
- **[Quick Start](./deploy/QUICK_START.md)**: Get started in 5 minutes
- **[Deployment Status](./deploy/DEPLOYMENT_STATUS.md)**: Current implementation status
- **[Phase IV Complete](./K8S_DEPLOYMENT_COMPLETE.md)**: Executive summary

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn/ui
- **State Management**: React Hooks
- **Authentication**: Better Auth

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL (Neon)
- **ORM**: SQLAlchemy
- **AI Models**: Google Gemini, Groq, OpenRouter

### DevOps & Deployment
- **Containerization**: Docker (Multi-stage builds)
- **Orchestration**: Kubernetes (Minikube)
- **Package Manager**: Helm 3
- **CI/CD**: GitHub Actions (planned)
- **Monitoring**: Prometheus/Grafana (planned)

---

## 🚀 Getting Started

### Prerequisites

- **Docker**: Container runtime
- **Minikube**: Local Kubernetes cluster
- **kubectl**: Kubernetes CLI
- **Helm**: Kubernetes package manager
- **Node.js**: 18+ (for local development)
- **Python**: 3.11+ (for local development)

### Installation

#### Option 1: Kubernetes Deployment (Recommended)

```bash
# 1. Install prerequisites
# Windows (with Chocolatey):
choco install minikube kubernetes-cli kubernetes-helm -y

# macOS (with Homebrew):
brew install minikube kubectl helm

# 2. Deploy to Minikube
deploy\scripts\deploy-to-minikube.bat  # Windows
./deploy/scripts/deploy-to-minikube.sh # Linux/macOS

# 3. Access the application
minikube service todo-chatbot-frontend
# Or visit: http://localhost:30000
```

#### Option 2: Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 📖 Project Structure

```
.
├── backend/                    # FastAPI backend
│   ├── src/
│   │   ├── main.py            # Application entry point
│   │   ├── models/            # Database models
│   │   ├── routes/            # API routes
│   │   └── services/          # Business logic
│   ├── Dockerfile             # Backend container
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # Next.js frontend
│   ├── app/                   # App router pages
│   ├── components/            # React components
│   │   ├── chatbot/          # Chatbot interface
│   │   ├── analytics/        # Analytics dashboard
│   │   └── ui/               # UI components
│   ├── Dockerfile             # Frontend container
│   └── package.json           # Node dependencies
│
├── deploy/                     # Kubernetes deployment
│   ├── helm/                  # Helm charts
│   ├── scripts/               # Deployment scripts
│   └── README.md              # Deployment guide
│
├── specs/                      # Feature specifications
│   └── 013-k8s-local-deployment/
│       ├── spec.md            # Requirements
│       ├── plan.md            # Implementation plan
│       └── tasks.md           # Task breakdown
│
└── README.md                   # This file
```

---

## 🎨 Features

### 1. Task Management
- Create, read, update, and delete tasks
- Organize tasks by status (Todo, In Progress, Done)
- Drag-and-drop task organization
- Task filtering and search

### 2. AI Chatbot
- Natural language task management
- Multiple AI model support:
  - Google Gemini (gemini-2.0-flash-exp)
  - Groq (llama-3.3-70b-versatile)
  - OpenRouter (various models)
- Context-aware conversations
- Tool calling for task operations

### 3. Analytics Dashboard
- Task completion statistics
- Productivity trends
- Activity tracking
- Visual charts and graphs

### 4. User Authentication
- Secure authentication with Better Auth
- User registration and login
- Session management
- Protected routes

---

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret
BETTER_AUTH_URL=http://localhost:8000
GEMINI_API_KEY=your-gemini-key
GROQ_API_KEY=your-groq-key
OPENROUTER_API_KEY=your-openrouter-key
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://...
```

### Kubernetes Configuration

Helm values can be customized in:
- `deploy/helm/todo-chatbot/values.yaml` (default)
- `deploy/helm/todo-chatbot/values-local.yaml` (Minikube)

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Kubernetes Deployment Tests
```bash
# Check pod status
kubectl get pods

# Check services
kubectl get services

# View logs
kubectl logs -l app.kubernetes.io/component=backend -f
```

---

## 📊 Monitoring & Observability

### Health Checks

**Backend:**
```bash
curl http://localhost:8000/health
# Response: {"status":"healthy","message":"App is running"}
```

**Frontend:**
```bash
curl http://localhost:3000
# Response: HTML page
```

### Kubernetes Health Probes

- **Liveness Probe**: Checks if the application is running
- **Readiness Probe**: Checks if the application is ready to serve traffic

---

## 🚀 Deployment Options

### 1. Local Kubernetes (Minikube)
- ✅ **Status**: Complete and ready
- **Guide**: [deploy/README.md](./deploy/README.md)
- **Time**: 10-15 minutes

### 2. Docker Compose (Development)
- ✅ **Status**: Available
- **Command**: `docker-compose up`
- **Time**: 5 minutes

### 3. Cloud Deployment (Future)
- ⏳ **Status**: Planned
- **Platforms**: AWS EKS, Google GKE, Azure AKS
- **Features**: Auto-scaling, Load balancing, Monitoring

---

## 📈 Roadmap

### Phase I: ✅ Basic Todo App
- Task CRUD operations
- User authentication
- Basic UI

### Phase II: ✅ AI Chatbot Integration
- Chatbot interface
- AI model integration
- Natural language processing

### Phase III: ✅ Enhanced Features
- Analytics dashboard
- Activity tracking
- Improved UI/UX

### Phase IV: ✅ Kubernetes Deployment
- Docker containerization
- Helm charts
- Minikube deployment
- Automated scripts

### Phase V: ⏳ Production Deployment (Planned)
- Cloud deployment (AWS/GCP/Azure)
- CI/CD pipeline
- Monitoring and logging
- Performance optimization

### Phase VI: ⏳ Advanced Features (Planned)
- Real-time collaboration
- Mobile app
- Advanced analytics
- Integration with external tools

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Hackathon II**: Spec-Driven Development methodology
- **Agentic Dev Stack**: Workflow and best practices
- **Claude Code**: AI-assisted development
- **Open Source Community**: Amazing tools and libraries

---

## 📞 Support

For issues, questions, or contributions:

- **Documentation**: [deploy/README.md](./deploy/README.md)
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

---

## 🎯 Quick Links

- **[Deployment Guide](./deploy/README.md)**: Complete deployment documentation
- **[Quick Start](./deploy/QUICK_START.md)**: 5-minute deployment guide
- **[Phase IV Summary](./K8S_DEPLOYMENT_COMPLETE.md)**: Kubernetes deployment details
- **[Deployment Status](./deploy/DEPLOYMENT_STATUS.md)**: Current implementation status
- **[Requirements Analysis](./PHASE_IV_REQUIREMENTS_ANALYSIS.md)**: Phase IV requirements checklist

---

**Built with ❤️ using Spec-Driven Development and Agentic Dev Stack**

**Status**: ✅ Phase IV Complete - Ready for Deployment
**Version**: 0.1.0
**Last Updated**: February 15, 2026
