# 🐾 MokabuLens

See the market through your own lens.

Built with **Next.js**, **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, MokabuLens is a friendly dashboard for investors to record insights, monitor stock indicators, and grow smarter — the Mokabu way.

## ✨ Features

- **🔐 Google OAuth Authentication** - Secure login with Google accounts
- **📱 Responsive Dashboard** - Modern UI built with Next.js and shadcn/ui
- **🏗️ BFF Architecture** - Backend for Frontend pattern for optimized API layer
- **🏗️ Monorepo Architecture** - Organized with pnpm workspaces
- **🐳 Docker Ready** - Easy development and deployment setup
- **📊 FastAPI Backend** - High-performance API with automatic documentation

## 🏗️ Monorepo Structure

This project uses a monorepo structure with pnpm workspaces:

```
MokabuLens/
├── apps/
│   ├── web/                    # Next.js web application
│   │   ├── app/               # Next.js App Router
│   │   │   ├── (auth)/        # Authentication route group
│   │   │   │   └── signin/    # Google OAuth sign-in
│   │   │   ├── (dashboard)/   # Dashboard route group
│   │   │   │   └── page.tsx   # Main dashboard
│   │   │   ├── api/           # Next.js API Routes
│   │   │   │   └── auth/      # Authentication endpoints
│   │   │   └── components/    # UI components (shadcn/ui)
│   │   ├── services/          # BFF business logic layer
│   │   │   └── auth.service.ts
│   │   ├── types/             # TypeScript type definitions
│   │   │   ├── auth.types.ts
│   │   │   └── api.types.ts
│   │   └── Dockerfile         # Docker configuration for web app
│   └── api/                   # FastAPI backend application
│       ├── main.py            # FastAPI main application
│       ├── database.py        # SQLAlchemy database configuration
│       ├── models/            # Database models
│       │   ├── user.py        # User model
│       │   └── product.py     # Product model
│       ├── requirements.txt   # Python dependencies
│       ├── Dockerfile         # Docker configuration for API
│       └── init.sql           # PostgreSQL initialization script
├── docker-compose.yml         # Docker Compose configuration
├── docker-compose.dev.yml     # Development environment
├── docker-compose.prod.yml    # Production environment
├── env.example               # Environment variables template
├── package.json              # Root workspace configuration
└── pnpm-workspace.yaml      # pnpm workspace configuration
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- pnpm (recommended package manager)
- Google Cloud Console account (for OAuth setup)

### 🔐 Google OAuth Setup

Before running the application, you need to set up Google OAuth:

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable Google+ API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it

3. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client ID"
   - Choose "Web application"
   - Add authorized redirect URIs:
     - `http://localhost:3000/api/auth/callback/google` (development)
     - `https://yourdomain.com/api/auth/callback/google` (production)

4. **Configure Environment Variables**:
   ```bash
   # Copy the example environment file
   cp env.example .env.local
   
   # Edit .env.local and add your Google OAuth credentials
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here
   NEXTAUTH_URL=http://localhost:3000
   NEXTAUTH_SECRET=your_nextauth_secret_key_here
   ```

For detailed setup instructions, see [GOOGLE_OAUTH_SETUP.md](./GOOGLE_OAUTH_SETUP.md).

### 🐳 Docker Development (Recommended)

The easiest way to get started is using Docker:

```bash
# Start all services (PostgreSQL, FastAPI, Next.js)
docker-compose up

# Or run in background
docker-compose up -d
```

This will start:
- **PostgreSQL** on `localhost:5432`
- **FastAPI API** on `http://localhost:8000`
- **Next.js Web App** on `http://localhost:3001` (port 3000 might be in use)

### 📱 Access the Applications

- **Frontend (Next.js)**: [http://localhost:3001](http://localhost:3001) or [http://localhost:3000](http://localhost:3000)
- **Sign In Page**: [http://localhost:3001/signin](http://localhost:3001/signin)
- **Backend API (FastAPI)**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Database**: PostgreSQL on `localhost:5432`

### 🛠️ Local Development (Without Docker)

If you prefer to run locally without Docker:

```bash
# Install dependencies
pnpm install

# Start the development server
pnpm dev

# Or start a specific app
pnpm --filter web dev
```

### Other Commands

```bash
# Build for production
pnpm build

# Run linting
pnpm lint

# Start production server
pnpm start
```

### 🐳 Docker Commands

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up --build

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs api
docker-compose logs web
docker-compose logs postgres

# Execute commands in running container
docker-compose exec api bash
docker-compose exec web sh

# Remove all containers and volumes
docker-compose down -v
```

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui + Radix UI
- **Authentication**: NextAuth.js with Google OAuth
- **State Management**: React hooks + Context API
- **BFF Pattern**: Next.js API Routes as Backend for Frontend layer

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Migration**: Alembic

### Development
- **Package Manager**: pnpm
- **Monorepo**: pnpm workspaces
- **Containerization**: Docker & Docker Compose

## 📁 Project Architecture

### Next.js App Router Structure

The web application follows Next.js App Router conventions with route groups for better organization:

- **`(auth)/`** - Authentication route group
  - `/signin` - Google OAuth sign-in page
  - Dedicated layout for authentication flows

- **`(dashboard)/`** - Dashboard route group
  - `/` - Main dashboard page
  - Dedicated layout with navigation and user controls

- **`api/`** - Next.js API Routes
  - `/api/auth/[...nextauth]` - NextAuth.js authentication endpoints
  - BFF (Backend for Frontend) pattern implementation

### BFF (Backend for Frontend) Architecture

This application implements the **BFF pattern** to provide a dedicated backend layer specifically optimized for the frontend needs:

- **`app/api/`** - Next.js API Routes (BFF Layer)
  - `/api/auth/[...nextauth]` - Authentication endpoints
  - Acts as a proxy between frontend and external services
  - Handles authentication, data transformation, and business logic

- **`services/`** - Business logic layer
  - `auth.service.ts` - Authentication service with NextAuth.js integration
  - Encapsulates complex business logic and API interactions
  - Provides clean interfaces for UI components

- **`types/`** - TypeScript type definitions
  - `auth.types.ts` - Authentication-related types
  - `api.types.ts` - API response and request types
  - Ensures type safety across the BFF layer

- **`components/`** - Reusable UI components
  - `ui/` - shadcn/ui base components
  - `layout/` - Layout-specific components

#### BFF Benefits

- **Frontend Optimization**: API responses tailored specifically for UI needs
- **Security**: Sensitive operations handled server-side
- **Performance**: Reduced client-side processing and network calls
- **Maintainability**: Clear separation between UI and business logic
- **Scalability**: Independent scaling of frontend and backend concerns

## 🔐 Authentication Flow

The application implements a secure authentication system using NextAuth.js with Google OAuth:

1. **User visits `/signin`** - Redirected to Google OAuth
2. **Google authentication** - User authorizes the application
3. **Callback handling** - NextAuth.js processes the OAuth response
4. **Session creation** - User session is established
5. **Dashboard access** - Authenticated user can access the main dashboard
6. **Session management** - Automatic session refresh and logout functionality

### Security Features

- **JWT-based sessions** - Secure session management
- **CSRF protection** - Built-in CSRF protection via NextAuth.js
- **Secure cookies** - HttpOnly cookies for session storage
- **Environment-based configuration** - Secure credential management

## 🔧 Development

### Adding New Apps

To add a new application to the monorepo:

```bash
# Create new app directory
mkdir apps/new-app

# Add package.json with appropriate name
# Update pnpm-workspace.yaml if needed
```

### Adding Shared Packages

To add a shared package:

```bash
# Create new package directory
mkdir packages/shared-utils

# Add package.json with appropriate configuration
```

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API
- [pnpm Workspaces](https://pnpm.io/workspaces) - learn about pnpm workspace management
- [shadcn/ui](https://ui.shadcn.com/) - learn about the UI component library

## 🚀 Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

### Monorepo Deployment Setup

Since this is a monorepo, you need to configure Vercel properly:

1. **Import your project** to Vercel
2. **Set the Root Directory** to `apps/web` in your project settings
3. **Build Command**: `pnpm --filter web build`
4. **Output Directory**: `.next` (automatically detected by Next.js)
5. **Install Command**: `pnpm install`

**Important**: Make sure to set the Root Directory to `apps/web` in your Vercel project settings.

### Manual Configuration (if needed)

If you need to configure manually in Vercel dashboard:

- **Root Directory**: `apps/web`
- **Framework Preset**: Next.js
- **Build Command**: `pnpm --filter web build`
- **Output Directory**: `.next` (leave empty for auto-detection)
- **Install Command**: `pnpm install`

### Troubleshooting

If you encounter path duplication errors (like `/vercel/path0/apps/web/apps/web/.next/`):

**Method 1: Fix existing project**
1. Go to your Vercel project settings
2. Set **Root Directory** to `apps/web`
3. Set **Output Directory** to `.next`
4. Redeploy the project

**Method 2: Create new project (recommended)**
1. **Delete the existing Vercel project**
2. **Create a new project** from the same repository
3. **During project creation, set Root Directory to `apps/web`**
4. **Use the build command**: `pnpm --filter web build`
5. **Set Output Directory**: `.next`

**Important**: The Root Directory must be set to `apps/web` for the monorepo to work correctly.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
