# Assignment X — [Title]

> **Environment:** ROS2 Jazzy (Docker) + Webots (native on your OS)

---

## How it works

```
Your computer
├── Webots  ← runs natively (full GPU, no display issues)
└── Docker container
    └── ROS2 Jazzy  ← all your code runs here
            ↕ TCP port 1234
        webots_ros2 driver bridges them
```

You write and edit code on your host machine using VS Code.
The code runs and builds inside the container.
Git is always used from your host machine terminal — never from inside the container.

---

## 1. Install prerequisites

### Webots (on your host OS — do this once)

Download and install **Webots R2025a** for your OS:
https://github.com/cyberbotics/webots/releases/tag/R2025a

| OS | File to download |
|---|---|
| Windows | `webots_2025a_setup.exe` |
| macOS | `webots_2025a.dmg` |
| Linux | `webots_2025a_amd64.deb` |

### Docker Desktop (do this once)

| OS | Instructions |
|---|---|
| Windows | Install Docker Desktop. During install ensure **"Use WSL2"** is checked. |
| macOS Intel | Install Docker Desktop for Mac (Intel). |
| macOS Apple Silicon | Install Docker Desktop for Mac (Apple Silicon). Then go to **Settings → General** and enable **"Use Rosetta for x86/amd64 emulation"**. |
| Linux | Install Docker Engine + Compose plugin via apt (see README setup section). Then run `sudo usermod -aG docker $USER` and log out/in. |

### VS Code extensions (do this once)

Install these two extensions in VS Code (`Ctrl+Shift+X`):
- **Dev Containers** — by Microsoft (`ms-vscode-remote.remote-containers`)
- **Docker** — by Microsoft (`ms-azuretools.vscode-docker`)

---

## 2. One-time environment setup

### Step 1 — Clone the repo

```bash
git clone git@github.com:BuyingANew-Soul/cyber-physical-course-assignment.git
cd cyber-physical-course-assignment
```

### Step 2 — Create your .env file

```bash
cp .env.example .env
```

Now open `.env` and uncomment the lines for **your OS**:

**Linux:**
```
NETWORK_MODE=host
WEBOTS_HOST=localhost
```

**Mac or Windows:**
```
NETWORK_MODE=bridge
WEBOTS_HOST=host.docker.internal
```

> `.env` is gitignored — it stays on your machine only. Never commit it.

### Step 3 — Open in VS Code

```bash
code .
```

VS Code will show a popup: **"Reopen in Container"** — click it.

> If you miss the popup: `Ctrl+Shift+P` → **Dev Containers: Reopen in Container**

The first build takes **3–5 minutes**. After that it's instant.

When the bottom-left corner of VS Code shows **"Dev Container: ROS2 Jazzy"** you are inside the container. ✅

---

## 3. Daily workflow

```
1. Open Webots on your host OS, open the assignment world file
2. Open VS Code → Reopen in Container (instant after first build)
3. Edit code in VS Code as normal
4. Open terminal in VS Code (Ctrl+`) — this is inside the container
5. Build and run your ROS2 code from that terminal
6. When done, push your code from a HOST terminal (not container)
```

---

## 4. Building and running

All commands below are run **inside the container terminal** (`Ctrl+`` in VS Code).

### Build the workspace

```bash
cb          # alias for: colcon build --symlink-install
src         # alias for: source install/setup.bash
```

Or the full commands:
```bash
cd /ros2_ws
colcon build --symlink-install
source install/setup.bash
```

> `--symlink-install` means Python files are symlinked rather than copied —
> you don't need to rebuild after editing a `.py` file, only after adding new
> nodes or changing `setup.py`.

### Build a single package (faster)

```bash
cbs my_package    # alias for: colcon build --symlink-install --packages-select
```

### Launch the full simulation

```bash
ros2 launch my_package robot.launch.py
```

> Make sure Webots is already open with the correct world before running this.

<!-- ### Run a single node

```bash
ros2 run my_package example_node
``` -->

### Useful debugging commands

```bash
rn                          # alias: ros2 node list
rt                          # alias: ros2 topic list
ros2 topic echo /chatter    # print messages on a topic
ros2 topic hz /cmd_vel      # check publish rate
ros2 node info /example_node
ros2 run rqt_graph rqt_graph   # visual node/topic graph (needs display)
```

---

## 5. Project structure

```
assignmentX/
├── .devcontainer/
│   └── devcontainer.json       # VS Code container config
├── docker/
│   └── Dockerfile              # ROS2 environment definition
├── src/
│   └── my_package/           # ← YOUR CODE LIVES HERE
│       ├── my_package/
│       │   ├── __init__.py
│       │   └── example_node.py # starter node — copy & modify
│       ├── launch/
│       │   └── robot.launch.py # launch file
│       ├── resource/
│       ├── package.xml
│       ├── setup.py            # register new nodes here
│       └── setup.cfg
        └── worlds
├── worlds/                     # Webots .wbt world files
├── docker-compose.yml
├── .env.example                # copy to .env, set your OS values
├── .env                        # gitignored — your local settings
├── .gitignore
└── README.md
```

---

## 6. Adding a new node

1. Create `src/my_package/my_package/my_new_node.py`
2. Register it in `setup.py` under `entry_points`:
   ```python
   'my_new_node = my_package.my_new_node:main',
   ```
3. Rebuild:
   ```bash
   cb && src
   ```
4. Run it:
   ```bash
   ros2 run my_package my_new_node
   ```

---

## 7. Submitting your work

Git is always used from your **host machine terminal** — not from inside the container.

```bash
# In a normal terminal on your host machine:
git add src/
git commit -m "Assignment X: describe what you implemented"
git push origin main
```

> Never commit: `build/`, `install/`, `log/` — these are in `.gitignore`.
> Never commit: `.env` — it contains your local OS settings.

---

## 8. Troubleshooting

**"Reopen in Container" doesn't appear**
→ Install the **Dev Containers** extension by Microsoft in VS Code.

**Build fails with "package not found"**
→ Run `rosdep install --from-paths src --ignore-src -r -y` inside the container terminal.

**`ros2 launch` can't connect to Webots**
→ Check Webots is open on your host with the correct world loaded.
→ Check your `.env` has the right `WEBOTS_HOST` for your OS.
→ On Linux, verify `NETWORK_MODE=host` is set in `.env`.

**Changes to Python files not reflected after rebuild**
→ Run `src` (re-source the workspace) in your container terminal.
→ If that doesn't work, run `cb` to rebuild.

**Mac Apple Silicon: container build fails**
→ Go to Docker Desktop → Settings → General → enable **"Use Rosetta for x86/amd64 emulation"**.

**"colcon: command not found"**
→ The ROS2 environment isn't sourced. Run:
```bash
source /opt/ros/jazzy/setup.bash
```

---

*ROS2 Jazzy Jalisco · Webots R2025a · Docker*
