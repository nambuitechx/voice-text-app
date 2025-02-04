# Use an official Node runtime as the base image
FROM node:20-alpine

# Add a build argument to force rebuild
ARG REBUILD
RUN echo "Rebuild trigger: ${REBUILD:-1}"

# Set the working directory in the container to /app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json package-lock.json ./

# Install the application dependencies
RUN npm ci

# Copy the rest of the application code to the working directory
COPY . .

# Build the application
RUN npm run build

# Expose Vite's production port
EXPOSE 3000

# Set environment variable for production
# ENV NODE_ENV=production

CMD [ "npm", "run", "start" ]
