# Development Guide - Troup'O Invaders

## Overview

Troup'O Invaders is a WebGL-based Space Invaders clone featuring ruminant enemies (cows, sheep, goats, and alpacas). This project uses a **containerized development environment** to ensure consistency across all development machines.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **Git** (version 2.30 or higher)

### Installing Prerequisites

#### Linux (Ubuntu/Debian)
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Logout and login for group changes to take effect
```

#### macOS
```bash
# Install Docker Desktop
brew install --cask docker

# Docker Compose is included with Docker Desktop
```

#### Windows
Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone git@github.com:maximer429-ctrl/test4.git
   cd test4
   ```

2. **Start the development environment**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   Open your browser and navigate to: `http://localhost:8080`

4. **View logs**
   ```bash
   docker-compose logs -f
   ```

5. **Stop the environment**
   ```bash
   docker-compose down
   ```

## Container Architecture

The development environment consists of:

- **Web Server Container**: Serves the HTML/WebGL application with hot-reload support
- **Volume Mounts**: Source code is mounted for live development
- **Port Mapping**: Container port 80 mapped to host port 8080

## Development Workflow

### Making Changes

1. **Claim an issue** (ensure work is tracked)
   ```bash
   bd update <issue-id> --claim
   ```

2. **Make your changes** in the project files
   - HTML files in `/src`
   - JavaScript/WebGL code in `/src/js`
   - Assets (sprites, sounds) in `/assets`

3. **Test your changes**
   - Changes are automatically reflected in the browser (hot-reload)
   - Refresh the browser if needed

4. **Complete your work**
   ```bash
   bd close <issue-id>
   bd sync
   git add .
   git commit -m "Description of changes"
   git push
   ```

### Running Commands in the Container

If you need to execute commands inside the container:

```bash
# Enter the container shell
docker-compose exec web sh

# Or run a single command
docker-compose exec web <command>
```

## Common Tasks

### Rebuild the Container

After modifying the Dockerfile or dependencies:

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### View Real-time Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
```

### Clean Up

Remove all containers, volumes, and images:

```bash
docker-compose down -v
docker system prune -a
```

### Check Container Status

```bash
docker-compose ps
```

## Project Structure

```
test4/
├── .beads/              # Issue tracking database
├── .github/             # GitHub configuration
├── assets/              # Game assets (sprites, sounds)
│   ├── sprites/         # Enemy and player sprites
│   ├── sounds/          # Sound effects and music
│   └── fonts/           # Game fonts
├── src/                 # Source code
│   ├── index.html       # Main HTML file
│   ├── js/              # JavaScript/WebGL code
│   │   ├── main.js      # Entry point
│   │   ├── engine/      # WebGL rendering engine
│   │   ├── game/        # Game logic
│   │   └── utils/       # Utility functions
│   └── css/             # Stylesheets
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile           # Container definition
├── DEVELOPMENT.md       # This file
├── AGENTS.md            # Agent instructions
└── README.md            # Project overview
```

## Development Tools

### Browser DevTools

- **Console**: View logs and errors
- **Network Tab**: Monitor asset loading
- **Performance Tab**: Profile WebGL rendering
- **Application Tab**: Inspect storage and cache

### Recommended Browser Extensions

- WebGL Inspector - Debug WebGL calls
- React Developer Tools (if using React)
- Performance Monitor - Track FPS and memory

## Troubleshooting

### Container Won't Start

```bash
# Check if port 8080 is already in use
lsof -i :8080  # Linux/macOS
netstat -ano | findstr :8080  # Windows

# Kill the process or change the port in docker-compose.yml
```

### Changes Not Reflecting

```bash
# Hard reload in browser
Ctrl+Shift+R (Linux/Windows)
Cmd+Shift+R (macOS)

# Restart the container
docker-compose restart web
```

### Permission Issues (Linux)

```bash
# Fix file ownership
sudo chown -R $USER:$USER .

# Ensure Docker socket permissions
sudo chmod 666 /var/run/docker.sock
```

### Container Build Fails

```bash
# Clean Docker cache
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
```

### Out of Memory

```bash
# Increase Docker memory limit in Docker Desktop settings
# Or add to docker-compose.yml:
services:
  web:
    mem_limit: 2g
```

## Performance Optimization

### Development Mode

- Hot-reload enabled for rapid iteration
- Source maps for easier debugging
- Verbose logging enabled

### Production Build

For production deployment (to be configured):

```bash
# Build optimized assets
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## Testing

### Manual Testing

1. Start the development environment
2. Open `http://localhost:8080` in multiple browsers
3. Test game controls, sprites, and collision detection
4. Check browser console for errors

### Automated Testing

```bash
# Run tests (when test suite is implemented)
docker-compose exec web npm test
```

## Issue Tracking with bd

This project uses **bd (beads)** for issue tracking. Key commands:

```bash
bd ready              # View available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim an issue
bd close <id>         # Complete work
bd sync               # Sync with git
```

See [AGENTS.md](AGENTS.md) for complete bd workflow.

## Best Practices

1. **Always work in the container** - Ensures consistent environment
2. **Claim issues before coding** - Prevents duplicate work
3. **Test in multiple browsers** - Chrome, Firefox, Safari, Edge
4. **Commit frequently** - Small, focused commits with clear messages
5. **Keep containers updated** - Rebuild after dependency changes
6. **Monitor performance** - Target 60 FPS for smooth gameplay
7. **Sync issues regularly** - Run `bd sync` at session end

## Getting Help

- Check this document first
- Review [AGENTS.md](AGENTS.md) for workflow questions
- Check Docker logs: `docker-compose logs`
- View issue details: `bd show <issue-id>`

## Contributing

1. Find available work: `bd ready`
2. Claim an issue: `bd update <id> --claim`
3. Develop in the containerized environment
4. Test thoroughly
5. Complete work: `bd close <id>`
6. Sync and push: `bd sync && git push`

## Environment Variables

Create a `.env` file in the project root for custom configuration:

```bash
# Port mapping
HOST_PORT=8080

# Development mode
DEBUG=true

# Log level
LOG_LEVEL=debug
```

## Security Notes

- Never commit sensitive data (API keys, passwords)
- Keep Docker and dependencies updated
- Review container security best practices
- Use `.dockerignore` to exclude unnecessary files

---

**Happy Coding! 🚀**

For questions or issues with the development environment, please create an issue using `bd create`.
