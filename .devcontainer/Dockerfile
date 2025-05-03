# Start from the official ROS 2 Humble simulation image
# This includes ROS base, Gazebo, RViz, common tools
FROM ros:humble-perception

# Install GUI streaming components, utilities, and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    fluxbox \
    x11vnc \
    novnc \
    websockify \
    ros-humble-xacro \
    ros-humble-joint-state-publisher \
    ros-humble-joint-state-publisher-gui \
    ros-humble-turtlesim \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-rviz2 \
    python3-colcon-common-extensions \
    git \
    curl \
    terminator \
    && rm -rf /var/lib/apt/lists/*

# --- VNC Startup Script ---
# Create a script to launch the virtual display and VNC services
RUN echo '#!/bin/bash\n\
export DISPLAY=:1\n\
# Start Xvfb virtual display on display :1\n\
Xvfb :1 -screen 0 1600x900x16 & \n\
sleep 2 # Give Xvfb time to start\n\
# Start Fluxbox window manager\n\
fluxbox -display :1 &\n\
sleep 2 # Give Fluxbox time to start\n\
# Start VNC server to share display :1, no password, listening on port 5900\n\
x11vnc -display :1 -nopw -forever -shared -rfbport 5900 &\n\
sleep 2 # Give VNC server time to start\n\
# Start noVNC WebSocket proxy, listening on port 6080, forwarding to VNC server on 5900\n\
# Serve the noVNC web files from /usr/share/novnc/\n\
websockify -D --web=/usr/share/novnc/ 6080 localhost:5900 \n\
# Keep the script running if needed, or just let background processes run\n\
echo "VNC Startup Complete. Access via forwarded port 6080."\n\
# Keep container alive by tailing a log or running another foreground process if needed\n\
# For Codespaces, the postStartCommand often handles keeping it alive\n\
tail -f /dev/null \
' > /usr/local/bin/start-vnc.sh \
&& chmod +x /usr/local/bin/start-vnc.sh

# --- Environment Setup ---
# Add ROS sourcing to the default bashrc for terminals opened *inside* the VNC session
# Note: Codespaces terminal integration usually sources this automatically,
# but it's needed for terminals *within* the Fluxbox/VNC environment.
RUN echo "\nsource /opt/ros/humble/setup.bash" >> /root/.bashrc
RUN echo "export DISPLAY=:1" >> /root/.bashrc # Set display for GUI apps in VNC

# Define the default command (or rely on postStartCommand in devcontainer.json)
# CMD ["/usr/local/bin/start-vnc.sh"]
# Using postStartCommand in devcontainer.json is often preferred for Codespaces background tasks.