# Dockerfile for Troup'O Invaders Development Environment
FROM nginx:alpine

# Install tools for development
RUN apk add --no-cache \
    curl \
    bash

# Copy nginx configuration for SPA
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# Create working directory
WORKDIR /usr/share/nginx/html

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
