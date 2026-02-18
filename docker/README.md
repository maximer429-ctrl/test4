# Docker Development Environment

## Quick Start

```bash
# Start the development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the environment
docker-compose down
```

Access the application at: **http://localhost:8080**

## What's Included

- **Nginx Alpine** - Lightweight web server (5MB base image)
- **Hot-Reload Support** - Changes to source files are immediately reflected
- **Volume Mounts** - Source code mounted read-only for safety
- **Auto-Indexing** - Browse directories during development
- **CORS Enabled** - For local API testing
- **No Cache** - Ensures you always see latest changes

## Configuration

### Port Mapping

Default port is 8080. To change, create a `.env` file:

```bash
cp .env.example .env
# Edit HOST_PORT in .env
```

Or use environment variable:
```bash
HOST_PORT=3000 docker-compose up -d
```

### File Mounts

The following directories are mounted for hot-reload:
- `./src` → `/usr/share/nginx/html/src`
- `./assets` → `/usr/share/nginx/html/assets`
- `./index.html` → Main page
- `./sprite-example.html` → Sprite demo

## Development Workflow

1. **Start container**
   ```bash
   docker-compose up -d
   ```

2. **Edit files** in your local `src/` or `assets/` directories

3. **Refresh browser** to see changes instantly (no rebuild needed)

4. **View logs** if something goes wrong
   ```bash
   docker-compose logs -f web
   ```

5. **Stop when done**
   ```bash
   docker-compose down
   ```

## Commands

### Building

```bash
# Build image
docker-compose build

# Build without cache
docker-compose build --no-cache

# Pull latest base image
docker-compose pull
```

### Running

```bash
# Start in background
docker-compose up -d

# Start in foreground (see logs)
docker-compose up

# Restart service
docker-compose restart web

# Stop service
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Debugging

```bash
# View logs
docker-compose logs -f

# Execute command in container
docker-compose exec web sh

# Check container status
docker-compose ps

# Inspect container
docker inspect troupo-invaders-dev
```

### Health Check

The container includes a health check:
```bash
# View health status
docker-compose ps
```

Should show "healthy" after startup.

## Troubleshooting

### Port Already in Use

```bash
# Find what's using port 8080
lsof -i :8080

# Use different port
HOST_PORT=3000 docker-compose up -d
```

### Changes Not Showing

```bash
# Hard refresh in browser
Ctrl+Shift+R (Linux/Windows)
Cmd+Shift+R (macOS)

# Restart container
docker-compose restart web

# Clear nginx cache (rare)
docker-compose exec web sh -c "rm -rf /var/cache/nginx/*"
docker-compose restart web
```

### Container Won't Start

```bash
# Check logs
docker-compose logs web

# Check if image is corrupted
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Permission Issues

```bash
# Fix file ownership (Linux)
sudo chown -R $USER:$USER .

# Check Docker socket permissions
ls -l /var/run/docker.sock
```

### Out of Disk Space

```bash
# Clean up Docker
docker system prune -a

# Remove old images
docker image prune -a

# Remove unused volumes
docker volume prune
```

## Production Deployment

For production, you'll want to:

1. Build optimized assets
2. Remove auto-indexing
3. Enable gzip compression
4. Add proper security headers
5. Use production nginx config

Create `docker-compose.prod.yml` for production settings.

## Performance

- **Image Size**: ~10MB (nginx:alpine + config)
- **Memory**: ~10-20MB runtime
- **CPU**: Minimal (nginx is very efficient)
- **Startup**: ~1-2 seconds

## Network

The container uses a bridge network `troupo-network`.

To add more services (backend, database):

```yaml
services:
  backend:
    image: node:18-alpine
    networks:
      - troupo-network
```

## Security Notes

- Volumes are mounted read-only (`:ro`) for safety
- No sensitive data in container
- Development mode only - NOT for production
- CORS is wide open (`*`) - fine for local dev, change for prod

## Extending

### Add Backend Service

Edit `docker-compose.yml`:

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "3000:3000"
    networks:
      - troupo-network
```

Update nginx config to proxy `/api/` to backend.

### Add Database

```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: devpass
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - troupo-network

volumes:
  pgdata:
```

## Tips

- Use `docker-compose logs -f` to watch live logs
- Container restarts automatically unless stopped
- Changes to `.html`, `.js`, `.css`, `.json` are instant
- Changes to `Dockerfile` require rebuild
- Changes to `docker-compose.yml` require `down` + `up`

## Help

If you encounter issues:
1. Check container logs: `docker-compose logs web`
2. Check container status: `docker-compose ps`
3. Try rebuilding: `docker-compose build --no-cache`
4. Create an issue: `bd create "Docker issue description"`
