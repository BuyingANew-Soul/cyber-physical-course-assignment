# Assignment X 

 
> **Environment:** ROS2 Jazzy + Webots R2023b (Docker)

---

## Table of Contents

1. [One-Time Setup](#1-one-time-setup)
   - [Windows](#windows)
   - [macOS (Intel)](#macos-intel)
   - [macOS (Apple Silicon — M1/M2/M3)](#macos-apple-silicon--m1m2m3)
   - [Linux](#linux)
2. [VS Code Setup](#2-vs-code-setup)
3. [Getting Started with This Assignment](#3-getting-started-with-this-assignment)
4. [Daily Workflow](#4-daily-workflow)
5. [Running Your Code](#5-running-your-code)
6. [Submitting Your Work](#6-submitting-your-work)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. One-Time Setup

> ⚠️ **You only do this section once.** After setup, skip straight to [Getting Started](#3-getting-started-with-this-assignment) for every assignment.

---

### Windows

#### Step 1 — Enable WSL2 (Windows Subsystem for Linux)

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

Restart your computer when prompted. This installs WSL2 with Ubuntu automatically.

> **Windows 11** users get WSLg (GUI support) for free — Webots will display without extra steps.  
> **Windows 10** users: after installing WSL2, continue to Step 2.

#### Step 2 — Install Docker Desktop

1. Download from: https://www.docker.com/products/docker-desktop/
2. Run the installer. Make sure **"Use WSL 2 instead of Hyper-V"** is checked.
3. After install, open Docker Desktop and wait for it to say **"Engine running"** in the bottom-left.
4. Open **Settings → Resources → WSL Integration** and enable your Ubuntu distro.

#### Step 3 — Verify installation

Open a terminal (search "Ubuntu" in Start Menu) and run:

```bash
docker run hello-world
```

You should see a message saying `Hello from Docker!` ✅

---

### macOS (Intel)

#### Step 1 — Install Docker Desktop

1. Download from: https://www.docker.com/products/docker-desktop/ (choose **Mac with Intel Chip**)
2. Open the `.dmg` and drag Docker to Applications.
3. Launch Docker Desktop from Applications, wait for **"Engine running"**.

#### Step 2 — Install XQuartz (display server for GUI apps)

Webots needs a display server to render its window on Mac.

1. Download from: https://www.xquartz.org/
2. Install and **restart your Mac**.
3. Open XQuartz → Preferences → Security tab → ✅ Check **"Allow connections from network clients"**
4. Log out and log back in (required for the setting to take effect).

#### Step 3 — Allow display connections

Run this in your Mac terminal every time you start working (or add it to `~/.zshrc` to run automatically):

```bash
xhost +localhost
```

#### Step 4 — Verify

```bash
docker run hello-world
```

---

### macOS (Apple Silicon — M1/M2/M3)

> ⚠️ **Important:** Apple Silicon (ARM) requires one extra step because ROS2 packages are primarily built for Intel (amd64). The container runs via emulation — it works well but is slightly slower.

#### Step 1 — Install Docker Desktop

1. Download from: https://www.docker.com/products/docker-desktop/ (choose **Mac with Apple Silicon**)
2. Install and wait for **"Engine running"**.
3. Open Docker Desktop → Settings → ✅ Enable **"Use Rosetta for x86/amd64 emulation on Apple Silicon"**

#### Step 2 — Install XQuartz (same as Intel Mac)

1. Download from: https://www.xquartz.org/
2. Install and **restart your Mac**.
3. XQuartz → Preferences → Security → ✅ **"Allow connections from network clients"**
4. Log out and log back in.

#### Step 3 — Allow display connections

```bash
xhost +localhost
```

Add this to `~/.zshrc` to run it automatically on every terminal open:

```bash
echo 'xhost +localhost 2>/dev/null' >> ~/.zshrc
```

#### Step 4 — Verify

```bash
docker run hello-world
```

---

### Linux

#### Step 1 — Install Docker Engine

```bash
# Remove old versions if any
sudo apt-get remove docker docker-engine docker.io containerd runc

# Install dependencies
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### Step 2 — Run Docker without sudo

```bash
sudo groupadd docker           # Create docker group (may already exist)
sudo usermod -aG docker $USER  # Add yourself to the group
newgrp docker                  # Apply group change immediately
```

#### Step 3 — Allow GUI (X11 display forwarding)

```bash
xhost +local:docker
```

Add this to `~/.bashrc` to run automatically:

```bash
echo 'xhost +local:docker 2>/dev/null' >> ~/.bashrc
```

#### Step 4 — Verify

```bash
docker run hello-world
```

---

## 2. VS Code Setup

Using VS Code with the Dev Containers extension gives you the smoothest workflow — everything runs inside the container but feels like a normal VS Code session.

#### Step 1 — Install VS Code

Download from: https://code.visualstudio.com/

#### Step 2 — Install two extensions

Open VS Code, press `Ctrl+Shift+X` (or `Cmd+Shift+X` on Mac) to open Extensions, and install:

| Extension | Publisher | Why |
|---|---|---|
| **Dev Containers** | Microsoft | Lets VS Code run inside Docker |
| **Docker** | Microsoft | Sidebar to manage containers |

---

## 3. Getting Started with This Assignment

#### Step 1 — Clone the assignment repo

```bash
git clone https://github.com/your-course-org/assignmentX.git
cd assignmentX
```

#### Step 2 — Open in VS Code

```bash
code .
```

#### Step 3 — Reopen in Container

VS Code will show a popup in the bottom-right corner:

> **"Folder contains a Dev Container configuration file. Reopen folder to develop in a container."**

Click **"Reopen in Container"**.

> If you miss the popup, press `Ctrl+Shift+P` → type **"Reopen in Container"** → Enter.

The first time this runs it will **build the Docker image** (~5–10 minutes). Subsequent opens take only a few seconds.

Once it's done, you'll see **"Dev Container: ROS2 Jazzy + Webots"** in the bottom-left corner of VS Code. ✅  
You are now working inside the container.

---

## 4. Daily Workflow

Once the container is built, your daily workflow is:

```
1. Open the assignment folder in VS Code
2. Click "Reopen in Container" (or it reopens automatically)
3. Write your code in VS Code — files are auto-synced
4. Open a terminal inside VS Code (Ctrl+` ) to run commands
5. All ROS2 and Webots commands run inside that terminal
```

> **Your files are safe.** Everything in the repo folder is stored on your computer, not inside the container. The container is just the execution environment.

---

## 5. Running Your Code

Open a terminal inside VS Code (`Ctrl+`` `) — this terminal is already inside the container.

#### Build the workspace

```bash
cd /ros2_ws
colcon build --symlink-install
source install/setup.bash
```

#### Launch the simulation

```bash
ros2 launch assignments/assignment_X/launch/simulation.launch.py
```

#### Useful commands

```bash
# List running ROS2 nodes
ros2 node list

# See available topics
ros2 topic list

# Echo a topic in real time
ros2 topic echo /topic_name

# Open rqt (graphical ROS2 tools)
ros2 run rqt_gui rqt_gui
```

---

## 6. Submitting Your Work

Your code lives on your host machine (not inside the container), so you submit via Git normally — **from your host machine terminal**, not the container terminal.

```bash
# Stage your changes
git add assignments/assignment_X/

# Commit with a clear message
git commit -m "Assignment X: [brief description of what you did]"

# Push to your fork / assigned branch
git push origin main
```

> **What to submit:** Only your code files inside `assignments/assignment_X/src/`. Do not commit build artifacts (`build/`, `install/`, `log/` directories — these are in `.gitignore` already).

---

## 7. Troubleshooting

#### ❌ "Cannot connect to the Docker daemon"
Docker Desktop is not running. Open Docker Desktop and wait for "Engine running".

#### ❌ Webots opens but shows a black/blank window (Mac)
XQuartz is not running or `xhost +localhost` hasn't been run.
```bash
# Make sure XQuartz is open, then:
xhost +localhost
```

#### ❌ "Reopen in Container" option doesn't appear in VS Code
The Dev Containers extension is not installed. Go to Extensions (`Ctrl+Shift+X`) and install **"Dev Containers"** by Microsoft.

#### ❌ Container builds but ROS2 commands say "command not found"
The ROS2 environment isn't sourced. Run:
```bash
source /opt/ros/jazzy/setup.bash
source /ros2_ws/install/setup.bash
```
Or close and reopen the terminal — `.bashrc` sources these automatically.

#### ❌ Very slow performance on Apple Silicon Mac
This is expected — the container runs via x86 emulation. It should still be usable. For heavy simulations, reduce the Webots rendering quality in Preferences → OpenGL.

#### ❌ `colcon build` fails with missing dependencies
Run rosdep inside the container:
```bash
rosdep install --from-paths src --ignore-src -r -y
```

---

## Need Help?

Post in the course forum with:
1. Your operating system and version
2. The exact error message (copy-paste, not a screenshot)
3. What you already tried

---

*Environment: ROS2 Jazzy Jalisco · Webots R2023b · Docker*
