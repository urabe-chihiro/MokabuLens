# 🐾 MokabuLens

See the market through your own lens.

Built with **Next.js**, **Python**, and **Prisma**, MokabuLens is a friendly dashboard for investors to record insights, monitor stock indicators, and grow smarter — the Mokabu way.

## 🏗️ Monorepo Structure

This project uses a monorepo structure with pnpm workspaces:

```
MokabuLens/
├── apps/
│   └── web/                    # Next.js web application
│       ├── app/               # App Router pages and components
│       ├── components/        # Reusable UI components (shadcn/ui)
│       └── ...
├── packages/                   # Shared packages (future)
├── package.json               # Root workspace configuration
└── pnpm-workspace.yaml       # pnpm workspace configuration
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- pnpm (recommended package manager)

### Installation

```bash
# Install dependencies
pnpm install
```

### Development

```bash
# Start the development server
pnpm dev

# Or start a specific app
pnpm --filter web dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Other Commands

```bash
# Build for production
pnpm build

# Run linting
pnpm lint

# Start production server
pnpm start
```

## 🛠️ Tech Stack

- **Framework**: Next.js 16 (with Turbopack)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui + Radix UI
- **Package Manager**: pnpm
- **Monorepo**: pnpm workspaces

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

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
