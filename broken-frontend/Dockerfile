# Stage 1: Build the React app using Node
FROM node:16-alpine as build

WORKDIR /app

# Copy package files and install dependencies with legacy peer deps flag
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps

# Copy the rest of the app source code
COPY . .

# Build the app for production
RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:alpine

# Copy the build output from the previous stage to Nginx's html directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 in the container
EXPOSE 80

# Run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
