# ============================================================
# ROS2 Jazzy + Webots Course Environment
# Platform: linux/amd64 (forced in docker-compose.yml)
# Works on: Linux x86, Mac Intel, Mac Apple Silicon (Rosetta),
#           Windows WSL2
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

# ── Webots dependencies ──────────────────────────────────────
# Install libraries required by the Webots .deb on Ubuntu 24.04
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

# ── Webots R2025a (amd64 only) ───────────────────────────────
# NOTE: Cyberbotics does not provide an arm64 Linux .deb.
# Apple Silicon users run this amd64 image via Rosetta emulation
# (set platform: linux/amd64 in docker-compose.yml).
RUN apt-get update && \
    wget -q "https://github.com/cyberbotics/webots/releases/download/R2025a/webots_2025a_amd64.deb" \
        -O /tmp/webots.deb && \
    apt-get install -y /tmp/webots.deb && \
    rm /tmp/webots.deb && \
    rm -rf /var/lib/apt/lists/*

# ── Environment setup ────────────────────────────────────────
ENV WEBOTS_HOME=/usr/local/webots
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# ── NVIDIA GPU (used only when docker-compose.nvidia.yml is active)
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=graphics,utility,compute
ENV __GLX_VENDOR_LIBRARY_NAME=nvidia

# Source ROS2 automatically in every new shell
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc && \
    echo "source /ros2_ws/install/setup.bash 2>/dev/null || true" >> /root/.bashrc && \
    echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> /root/.bashrc

# ── Display environment ──────────────────────────────────────
# DISPLAY is passed in at runtime via docker-compose
ENV DISPLAY=:0

# ── Workspace ────────────────────────────────────────────────
WORKDIR /ros2_ws

# Pre-initialize rosdep (speeds up first run for students)
RUN rosdep update

# Default command: interactive bash
CMD ["/bin/bash"]