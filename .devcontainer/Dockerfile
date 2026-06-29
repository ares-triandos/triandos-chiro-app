FROM mcr.microsoft.com/devcontainers/javascript-node:20

# Install system dependencies for Expo/React Native development
RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    git \
    curl \
    watchman \
    && rm -rf /var/lib/apt/lists/*

# Install Expo CLI and EAS CLI globally
RUN npm install -g expo-cli eas-cli

# Install Python dependencies (useful for automation scripts)
RUN pip3 install requests pyyaml

# Set up bash aliases for convenience
RUN echo 'alias expo-dev="expo start --tunnel"' >> /home/node/.bashrc && \
    echo 'alias eas-preview="eas build --platform ios --profile preview --wait"' >> /home/node/.bashrc && \
    echo 'alias eas-prod="eas build --platform ios --profile production --wait"' >> /home/node/.bashrc

# Create a non-root user 'node' is already created by the base image
USER node

# Set working directory
WORKDIR /workspace
