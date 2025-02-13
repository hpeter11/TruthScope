# Build vite app
FROM node:18-alpine AS builder
WORKDIR /app

# Copy package files and install deps
COPY package*.json ./
RUN npm install

# Copy all src files and build app
COPY . .
RUN npm run build

# Serve w Nginx
FROM nginx:alpine
# Copy the production build (by default, Vite outputs to "dist") to Nginx's html folder
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
