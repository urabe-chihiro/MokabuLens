# 🐾 MokabuLens

See the market through your own lens.

Built with **Next.js**, **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, MokabuLens is a friendly dashboard for investors to record insights, monitor stock indicators, and grow smarter — the Mokabu way.

## 🏗️ Monorepo Structure

This project uses a monorepo structure with pnpm workspaces:

```
MokabuLens/
├── apps/
│   ├── web/                    # Next.js web application
│   │   ├── app/               # App Router pages and components
│   │   ├── components/        # Reusable UI components (shadcn/ui)
│   │   └── Dockerfile         # Docker configuration for web app
│   └── api/                   # FastAPI backend application
│       ├── main.py            # FastAPI main application
│       ├── database.py        # SQLAlchemy database configuration
│       ├── models.py          # Database models
│       ├── requirements.txt   # Python dependencies
│       ├── Dockerfile         # Docker configuration for API
│       └── init.sql           # PostgreSQL initialization script
├── docker-compose.yml         # Docker Compose configuration
├── package.json               # Root workspace configuration
└── pnpm-workspace.yaml       # pnpm workspace configuration
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- pnpm (recommended package manager)

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
- **Next.js Web App** on `http://localhost:3000`

### 📱 Access the Applications

- **Frontend (Next.js)**: [http://localhost:3000](http://localhost:3000)
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
- **Framework**: Next.js 16 (with Turbopack)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui + Radix UI

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

## 📁 Project Structure

- **`apps/web/`** - Main Next.js web application
  - UI components are managed within the web app
  - Uses App Router for routing
  - Configured with shadcn/ui components

- **`packages/`** - Shared packages (ready for future expansion)
  - Can be used for shared utilities, types, or components
  - Currently empty, ready for additional apps/services

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
