# ============================================================
# ROS2 Jazzy + Webots Course Environment
# Supports: amd64 (x86_64) and arm64 (Apple Silicon M1/M2/M3)
# ============================================================

FROM ros:jazzy-ros-base

# Avoid interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive

# ── System dependencies ──────────────────────────────────────
RUN apt-get update && apt-get install -y \
    # ROS2 tools
    ros-jazzy-webots-ros2 \
    ros-jazzy-rmw-cyclonedds-cpp \
    ros-jazzy-rqt \
    ros-jazzy-rqt-common-plugins \
    ros-jazzy-rviz2 \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-pip \
    # Utilities
    wget \
    curl \
    git \
    nano \
    vim \
    bash-completion \
    # GUI / display support
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    libxcb-cursor0 \
    libxcb-util1 \
    libdbus-1-3 \
    libegl1 \
    libgl1 \
    x11-apps \
    mesa-utils \
    && rm -rf /var/lib/apt/lists/*

# ── Webots ───────────────────────────────────────────────────
# Install dependencies that Webots R2025a requires on Ubuntu 24.04 Noble.
# These were not available or named differently in older Ubuntu releases,
# which is why the R2023b .deb failed with unmet dependencies.
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libfreeimage3 \
    libssh-4 \
    libzip4t64 \
    xserver-xorg-core \
    xvfb \
    libglu1-mesa \
    libavcodec60 \
    libavformat60 \
    libavutil58 \
    libswscale7 \
    && rm -rf /var/lib/apt/lists/*

# Download and install Webots R2025a — first release with full Ubuntu 24.04 support.
# R2023b does NOT support Ubuntu 24.04 (which ros:jazzy-ros-base is based on).
RUN apt-get update && \
    ARCH=$(dpkg --print-architecture) && \
    echo "Detected architecture: $ARCH" && \
    if [ "$ARCH" = "amd64" ]; then \
        WEBOTS_DEB="webots_2025a_amd64.deb"; \
    elif [ "$ARCH" = "arm64" ]; then \
        WEBOTS_DEB="webots_2025a_arm64.deb"; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    wget -q "https://github.com/cyberbotics/webots/releases/download/R2025a/${WEBOTS_DEB}" \
        -O /tmp/webots.deb && \
    apt-get install -y /tmp/webots.deb && \
    rm /tmp/webots.deb && \
    rm -rf /var/lib/apt/lists/*

# ── Environment setup ────────────────────────────────────────
ENV WEBOTS_HOME=/usr/local/webots
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Source ROS2 automatically in every new shell
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc && \
    echo "source /ros2_ws/install/setup.bash 2>/dev/null || true" >> /root/.bashrc && \
    echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> /root/.bashrc

# ── Display environment ──────────────────────────────────────
# DISPLAY is passed in at runtime via docker-compose
ENV DISPLAY=:0

# ── NVIDIA GPU ───────────────────────────────────────────────
# These tell the NVIDIA container runtime to expose the GPU,
# and tell Webots/OpenGL to use it instead of software Mesa.
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=graphics,utility,compute
ENV __GLX_VENDOR_LIBRARY_NAME=nvidia

# ── Workspace ────────────────────────────────────────────────
WORKDIR /ros2_ws

# Pre-initialize rosdep (speeds up first run for students)
RUN rosdep update

# Default command: interactive bash
CMD ["/bin/bash"]