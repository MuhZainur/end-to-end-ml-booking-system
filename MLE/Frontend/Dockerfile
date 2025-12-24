# Stage 1: Build the React Application
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies (cached)
COPY package*.json ./
RUN npm install

# Build the app
COPY . .
RUN npm run build

# Stage 2: Serve the Built App
FROM node:18-alpine

WORKDIR /app

# Install 'serve' package globally to host static files
RUN npm install -g serve

# Copy built assets from Stage 1
COPY --from=build /app/dist /app/dist

# Expose port 3000
EXPOSE 3000

# Start server (SPA mode)
CMD ["serve", "-s", "dist", "-l", "3000"]
