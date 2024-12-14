# Use the official NGINX base image
FROM nginx:latest

# Switch to root user to set up the server
USER root

# Copy custom NGINX configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy HTML files to the default directory
COPY html /usr/share/nginx/html

# Set permissions for the HTML directory
RUN chmod -R 755 /usr/share/nginx/html

# Expose the default HTTP port
EXPOSE 80

# Start NGINX in the foreground
CMD ["nginx", "-g", "daemon off;"]
