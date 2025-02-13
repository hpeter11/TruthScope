# Stage 1: Build the Vite app
FROM node:18-alpine AS builder
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy all source files and build the app
COPY . .
RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:alpine
# Copy the production build (by default, Vite outputs to "dist") to Nginx's html folder
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 (default Nginx port)
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
