# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# Install prerequisites and Docker
RUN apt-get update && \
    apt-get install -y ca-certificates curl gnupg && \
    # Create directory for Docker's GPG key
    install -m 0755 -d /etc/apt/keyrings && \
    # Download the GPG key
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    # Dynamically add the repository based on the OS version (Trixie, Bookworm, etc.)
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    # Install Docker components
    apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    # Clean up to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add Jenkins user to the Docker group
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Create the Docker directory and volume for DinD
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Switch back to the Jenkins user
USER jenkins