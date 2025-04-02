import tkinter as tk
import time
import pytz
import math
from datetime import datetime
from tkinter import ttk, Canvas
from PIL import Image, ImageTk, ImageDraw, ImageFilter

# Define the time zones to display
time_zones = {
    "New York": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Mumbai": "Asia/Kolkata",
    "Dubai": "Asia/Dubai"
}

# Define color scheme
DARK_BG = "#121212"
ACCENT_COLOR = "#00B4D8"
TEXT_COLOR = "#E0FBFC"
HIGHLIGHT_COLOR = "#3A86FF"
SECONDARY_COLOR = "#8338EC"


class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CHRONOEYE | Global Time Visualizer")
        self.root.geometry("800x600")
        self.root.configure(bg=DARK_BG)
        self.root.resizable(True, True)
        self.animation_angle = 0
        self.globe_rotation = 0
        # Load and set the app icon
        self.create_widgets()


    def create_widgets(self):
        # Create header
        header_frame = tk.Frame(self.root, bg=DARK_BG)
        header_frame.pack(fill="x", pady=10)

        title_label = tk.Label(
            header_frame,
            text="CHRONOEYE",
            font=("Segoe UI", 26, "bold"),
            fg=ACCENT_COLOR,
            bg=DARK_BG
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Global Time Visualizer",
            font=("Segoe UI", 14),
            fg=TEXT_COLOR,
            bg=DARK_BG
        )
        subtitle_label.pack()

        # Create 3D world visualization canvas
        self.globe_canvas = tk.Canvas(
            self.root,
            width=300,
            height=300,
            bg=DARK_BG,
            highlightthickness=0
        )
        self.globe_canvas.pack(pady=10)

        # Create frame for clocks
        clock_frame = tk.Frame(self.root, bg=DARK_BG)
        clock_frame.pack(fill="x", pady=10, padx=20)

        # Create a modern clock for each time zone
        self.clock_widgets = {}
        for i, (city, tz_name) in enumerate(time_zones.items()):
            city_frame = tk.Frame(clock_frame, bg=DARK_BG)
            city_frame.grid(row=0, column=i, padx=10)

            # City name
            city_label = tk.Label(
                city_frame,
                text=city,
                font=("Segoe UI", 14, "bold"),
                fg=HIGHLIGHT_COLOR,
                bg=DARK_BG
            )
            city_label.pack(pady=(0, 5))

            # Clock canvas
            clock_canvas = tk.Canvas(
                city_frame,
                width=100,
                height=100,
                bg=DARK_BG,
                highlightthickness=0
            )
            clock_canvas.pack()

            # Digital time
            time_label = tk.Label(
                city_frame,
                text="00:00:00",
                font=("Segoe UI", 12),
                fg=TEXT_COLOR,
                bg=DARK_BG
            )
            time_label.pack(pady=5)

            # Store references
            self.clock_widgets[city] = {
                "canvas": clock_canvas,
                "time_label": time_label,
                "timezone": tz_name
            }

        # Create status bar
        status_frame = tk.Frame(self.root, bg="#1E1E1E", height=30)
        status_frame.pack(side="bottom", fill="x")

        self.status_label = tk.Label(
            status_frame,
            text="Time synchronized with global servers",
            font=("Segoe UI", 9),
            fg="#AAAAAA",
            bg="#1E1E1E"
        )
        self.status_label.pack(side="left", padx=10)

        # Draw initial clock faces and globe
        self.draw_3d_globe()
        self.draw_clock_faces()

    def draw_3d_globe(self):
        self.globe_canvas.delete("all")

        # Create globe with meridian lines
        cx, cy = 150, 150
        radius = 100

        # Draw the globe background
        self.globe_canvas.create_oval(
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius,
            fill="#1E293B",
            outline=ACCENT_COLOR,
            width=2
        )

        # Draw animated meridian lines
        for i in range(12):
            angle = math.radians(i * 30 + self.globe_rotation)
            x1 = cx + radius * math.cos(angle)
            y1 = cy - radius * math.sin(angle)
            x2 = cx - radius * math.cos(angle)
            y2 = cy + radius * math.sin(angle)
            self.globe_canvas.create_line(
                x1, y1, x2, y2,
                fill=HIGHLIGHT_COLOR,
                width=1,
                dash=(4, 4)
            )

        # Draw equator
        equator_radius = radius * 0.8
        self.globe_canvas.create_oval(
            cx - equator_radius,
            cy - equator_radius * 0.3,
            cx + equator_radius,
            cy + equator_radius * 0.3,
            outline=ACCENT_COLOR,
            width=1,
            dash=(4, 2)
        )

        # Draw city markers on the globe
        positions = {
            "New York": (-60, 40),
            "London": (0, 51),
            "Tokyo": (139, 35),
            "Mumbai": (72, 19),
            "Dubai": (55, 25)
        }

        for city, (lon, lat) in positions.items():
            # Convert to 3D coordinates with rotation
            adjusted_lon = math.radians(lon + self.globe_rotation)
            lat_rad = math.radians(lat)

            # Calculate position (simple projection)
            x = cx + radius * 0.8 * math.cos(lat_rad) * math.sin(adjusted_lon)
            y = cy - radius * 0.8 * math.sin(lat_rad)

            # Only show cities on the "visible" side of the globe
            if math.cos(adjusted_lon) > -0.1:
                # City dot
                self.globe_canvas.create_oval(
                    x - 4, y - 4, x + 4, y + 4,
                    fill=SECONDARY_COLOR,
                    outline=TEXT_COLOR
                )

                # Get current time for this city
                tz = pytz.timezone(time_zones[city])
                current_time = datetime.now(tz).strftime("%H:%M")

                # Time label
                self.globe_canvas.create_text(
                    x, y - 12,
                    text=f"{city}",
                    fill=TEXT_COLOR,
                    font=("Segoe UI", 8, "bold")
                )

    def draw_clock_faces(self):
        for city, widgets in self.clock_widgets.items():
            canvas = widgets["canvas"]
            canvas.delete("all")

            # Get current time for this city
            tz = pytz.timezone(widgets["timezone"])
            now = datetime.now(tz)
            hour, minute, second = now.hour, now.minute, now.second

            # Draw clock face
            cx, cy = 50, 50
            radius = 45

            # Draw outer circle
            canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                outline=ACCENT_COLOR,
                width=2
            )

            # Draw inner circle
            canvas.create_oval(
                cx - radius + 10, cy - radius + 10,
                cx + radius - 10, cy + radius - 10,
                outline=HIGHLIGHT_COLOR,
                width=1
            )

            # Draw hour markers
            for i in range(12):
                angle = math.radians(i * 30)
                x1 = cx + (radius - 5) * math.cos(angle)
                y1 = cy - (radius - 5) * math.sin(angle)
                x2 = cx + (radius - 15) * math.cos(angle)
                y2 = cy - (radius - 15) * math.sin(angle)
                if i % 3 == 0:
                    canvas.create_line(x1, y1, x2, y2, fill=SECONDARY_COLOR, width=2)
                else:
                    canvas.create_line(x1, y1, x2, y2, fill=TEXT_COLOR, width=1)

            # Draw hour hand
            hour_angle = math.radians((hour % 12 + minute / 60) * 30)
            hour_x = cx + 25 * math.cos(hour_angle)
            hour_y = cy - 25 * math.sin(hour_angle)
            canvas.create_line(cx, cy, hour_x, hour_y, fill=HIGHLIGHT_COLOR, width=3)

            # Draw minute hand
            minute_angle = math.radians(minute * 6)
            minute_x = cx + 35 * math.cos(minute_angle)
            minute_y = cy - 35 * math.sin(minute_angle)
            canvas.create_line(cx, cy, minute_x, minute_y, fill=TEXT_COLOR, width=2)

            # Draw second hand
            second_angle = math.radians(second * 6)
            second_x = cx + 40 * math.cos(second_angle)
            second_y = cy - 40 * math.sin(second_angle)
            canvas.create_line(cx, cy, second_x, second_y, fill=ACCENT_COLOR, width=1)

            # Draw center dot
            canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill=SECONDARY_COLOR)

            # Update digital time
            widgets["time_label"].config(text=now.strftime("%H:%M:%S"))

    def update(self):
        self.draw_clock_faces()
        self.animation_angle = (self.animation_angle + 1) % 360
        self.globe_rotation = (self.globe_rotation + 0.5) % 360
        self.draw_3d_globe()

        # Update status bar with current UTC time
        utc_time = datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        self.status_label.config(text=f"Global Sync: {utc_time}")

        self.root.after(100, self.update)


# Create the main window
root = tk.Tk()
app = ClockApp(root)
app.update()

# Run the application
root.mainloop()
'''
STILL IN DEVELOPMENT
import tkinter as tk
import time
import pytz
import math
import json
import os
import threading
import http.server
import socketserver
import webbrowser
from datetime import datetime
from tkinter import ttk, Frame
from PIL import Image, ImageTk
import webview
from bottle import app


def find_available_port(start_port=8080):
    """Find an available port starting from start_port"""
    port = start_port
    max_port = start_port + 100  # Try 100 ports

    while port < max_port:
        try:
            with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as server:
                # If we get here, the port is available
                server.server_close()
                return port
        except OSError:
            # Port not available, try the next one
            port += 1

    raise RuntimeError("No available ports found")


# Define the time zones to display
time_zones = {
    "New York": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Mumbai": "Asia/Kolkata",
    "Dubai": "Asia/Dubai",
    "Sydney": "Australia/Sydney",
    "Rio": "America/Sao_Paulo",
    "Moscow": "Europe/Moscow"
}

# Define color scheme
DARK_BG = "#0F172A"
ACCENT_COLOR = "#06B6D4"
TEXT_COLOR = "#F1F5F9"
HIGHLIGHT_COLOR = "#3B82F6"
SECONDARY_COLOR = "#8B5CF6"


class TimeDataAPI:
    """Class to provide time data to the web component"""

    def __init__(self, time_zones):
        self.time_zones = time_zones

    def get_time_data(self):
        """Returns current time data for all time zones"""
        time_data = {}
        for city, tz_name in self.time_zones.items():
            timezone = pytz.timezone(tz_name)
            now = datetime.now(timezone)

            # Get coordinates (approximate for visualization)
            coords = {
                "New York": [-74.006, 40.7128, -5],
                "London": [0.1278, 51.5074, 0],
                "Tokyo": [139.6503, 35.6762, 9],
                "Mumbai": [72.8777, 19.0760, 5.5],
                "Dubai": [55.2708, 25.2048, 4],
                "Sydney": [151.2093, -33.8688, 10],
                "Rio": [-43.1729, -22.9068, -3],
                "Moscow": [37.6173, 55.7558, 3]
            }

            time_data[city] = {
                "time": now.strftime("%H:%M:%S"),
                "hour": now.hour,
                "minute": now.minute,
                "second": now.second,
                "timezone": tz_name,
                "offset": now.strftime("%z"),
                "date": now.strftime("%Y-%m-%d"),
                "daylight": True if 6 <= now.hour < 18 else False,
                "coords": coords.get(city, [0, 0, 0])
            }
        return time_data


class WebServer:
    """Simple HTTP server to serve the HTML/JS files"""

    def __init__(self, port=8000):
        self.port = port
        self.httpd = None

    def start(self):
        """Start the web server in a separate thread"""
        handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", self.port), handler)

        server_thread = threading.Thread(target=self.httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print(f"Server started at http://localhost:{self.port}")

    def stop(self):
        """Stop the web server"""
        if self.httpd:
            self.httpd.shutdown()


class ChronoEyeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CHRONOEYE | Advanced Global Time Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg=DARK_BG)
        self.root.resizable(True, True)

        # Create the API and web server
        self.time_api = TimeDataAPI(time_zones)

        # Create directory structure if it doesn't exist
        self.setup_files()

        # Start the web server
        available_port = find_available_port()

        # Start the web server on the available port
        self.server = WebServer(port=available_port)

        # Store the available port for later use in the webview
        self.available_port = available_port

        # Create UI elements
        self.create_widgets()

        # Start update loop
        self.update_data()

    def setup_files(self):
        """Create necessary files and directories"""
        # Create web directory if it doesn't exist
        if not os.path.exists("web"):
            os.makedirs("web")
            os.makedirs("web/js")
            os.makedirs("web/css")

        # Create HTML file
        with open("web/index.html", "w") as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChronoEye 3D Globe</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <div id="globe-container"></div>
    <div id="time-display">
        <div id="current-city">
            <h2>Select a city</h2>
            <div class="time">--:--:--</div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="js/globe.js"></script>
</body>
</html>""")

        # Create CSS file
        with open("web/css/styles.css", "w") as f:
            f.write("""body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: #0F172A;
    color: #F1F5F9;
    font-family: 'Segoe UI', Arial, sans-serif;
}

#globe-container {
    position: absolute;
    width: 100%;
    height: 100%;
}

#time-display {
    position: absolute;
    bottom: 20px;
    left: 20px;
    background-color: rgba(15, 23, 42, 0.7);
    border-radius: 10px;
    padding: 15px;
    backdrop-filter: blur(10px);
    border: 1px solid #3B82F6;
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.3);
}

#current-city h2 {
    margin: 0 0 10px 0;
    font-size: 24px;
    color: #06B6D4;
}

.time {
    font-size: 36px;
    font-weight: bold;
    color: #F1F5F9;
}""")

        # Create JavaScript file for 3D globe
        with open("web/js/globe.js", "w") as f:
            f.write("""// Globe visualization using Three.js
let scene, camera, renderer, globe, cityMarkers = {}, timeData = {};
let raycaster = new THREE.Raycaster();
let mouse = new THREE.Vector2();
let selectedCity = null;

// Initialize the 3D scene
function init() {
    // Create scene
    scene = new THREE.Scene();

    // Create camera
    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 4;

    // Create renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.getElementById('globe-container').appendChild(renderer.domElement);

    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0x404040, 1);
    scene.add(ambientLight);

    // Add directional light
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 3, 5);
    scene.add(directionalLight);

    // Create earth globe
    const earthGeometry = new THREE.SphereGeometry(2, 64, 64);

    // Create two-tone earth material
    const earthMaterial = new THREE.MeshPhongMaterial({
        color: 0x1e3a8a, // Deep blue
        emissive: 0x072655,
        specular: 0x3b82f6,
        shininess: 15,
        transparent: true,
        opacity: 0.9
    });

    globe = new THREE.Mesh(earthGeometry, earthMaterial);
    scene.add(globe);

    // Add grid lines (longitude/latitude)
    addGridLines();

    // Handle window resize
    window.addEventListener('resize', onWindowResize);

    // Add mouse interaction
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('click', onMouseClick);

    // Fetch initial time data
    updateTimeData();

    // Start animation loop
    animate();
}

// Add grid lines to represent longitude and latitude
function addGridLines() {
    // Add longitude lines
    for (let i = 0; i < 24; i++) {
        const material = new THREE.LineBasicMaterial({ 
            color: 0x3b82f6,
            transparent: true,
            opacity: 0.3
        });

        const points = [];
        const angle = (i / 24) * Math.PI * 2;

        for (let j = 0; j <= 180; j++) {
            const latitude = (j - 90) * Math.PI / 180;
            const x = 2 * Math.cos(latitude) * Math.cos(angle);
            const y = 2 * Math.sin(latitude);
            const z = 2 * Math.cos(latitude) * Math.sin(angle);

            points.push(new THREE.Vector3(x, y, z));
        }

        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const line = new THREE.Line(geometry, material);
        scene.add(line);
    }

    // Add latitude lines
    for (let i = -80; i <= 80; i += 20) {
        const material = new THREE.LineBasicMaterial({ 
            color: 0x06b6d4,
            transparent: true,
            opacity: 0.3
        });

        const points = [];
        const latitude = i * Math.PI / 180;

        for (let j = 0; j <= 360; j++) {
            const angle = j * Math.PI / 180;
            const radius = 2 * Math.cos(latitude);
            const x = radius * Math.cos(angle);
            const y = 2 * Math.sin(latitude);
            const z = radius * Math.sin(angle);

            points.push(new THREE.Vector3(x, y, z));
        }

        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const line = new THREE.Line(geometry, material);
        scene.add(line);
    }

    // Add equator with special styling
    const equatorMaterial = new THREE.LineBasicMaterial({ 
        color: 0x8b5cf6,
        transparent: true,
        opacity: 0.6,
        linewidth: 2
    });

    const equatorPoints = [];
    for (let j = 0; j <= 360; j++) {
        const angle = j * Math.PI / 180;
        const x = 2 * Math.cos(angle);
        const y = 0;
        const z = 2 * Math.sin(angle);

        equatorPoints.push(new THREE.Vector3(x, y, z));
    }

    const equatorGeometry = new THREE.BufferGeometry().setFromPoints(equatorPoints);
    const equator = new THREE.Line(equatorGeometry, equatorMaterial);
    scene.add(equator);
}

// Update the globe rotation and city markers
function animate() {
    requestAnimationFrame(animate);

    // Rotate the globe slowly
    globe.rotation.y += 0.001;

    // Update city markers
    updateCityMarkers();

    renderer.render(scene, camera);
}

// Handle window resize
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Fetch time data from Python backend
function updateTimeData() {
    // In a real implementation, this would be an API call
    // For now, we'll manually update with some sample data
    fetch('/api/time-data')
        .then(response => response.json())
        .then(data => {
            timeData = data;

            // Update city markers if they exist
            if (Object.keys(cityMarkers).length === 0) {
                createCityMarkers();
            }

            // Update selected city display
            updateSelectedCityDisplay();
        })
        .catch(error => {
            console.error('Error fetching time data:', error);
            // Use fallback data for demo
            // This would be provided by the Python backend in real implementation
        });

    // Update every second
    setTimeout(updateTimeData, 1000);
}

// Create markers for each city
function createCityMarkers() {
    // Clear existing markers
    Object.values(cityMarkers).forEach(marker => {
        scene.remove(marker);
    });
    cityMarkers = {};

    // Create new markers
    Object.entries(timeData).forEach(([city, data]) => {
        const [longitude, latitude, timezone] = data.coords;

        // Convert coordinates to 3D position
        const phi = (90 - latitude) * Math.PI / 180;
        const theta = (longitude + 180) * Math.PI / 180;

        const x = -2.1 * Math.sin(phi) * Math.cos(theta);
        const y = 2.1 * Math.cos(phi);
        const z = 2.1 * Math.sin(phi) * Math.sin(theta);

        // Create marker
        const markerGeometry = new THREE.SphereGeometry(0.05, 16, 16);
        const markerMaterial = new THREE.MeshBasicMaterial({ 
            color: data.daylight ? 0xf59e0b : 0x8b5cf6
        });

        const marker = new THREE.Mesh(markerGeometry, markerMaterial);
        marker.position.set(x, y, z);
        marker.userData = { city: city };
        scene.add(marker);

        // Add pulsing light effect
        const pulseLight = new THREE.PointLight(
            data.daylight ? 0xf59e0b : 0x8b5cf6, 
            0.5, 
            0.5
        );
        pulseLight.position.set(x, y, z);
        scene.add(pulseLight);

        // Store reference to marker
        cityMarkers[city] = {
            marker: marker,
            light: pulseLight,
            position: new THREE.Vector3(x, y, z)
        };
    });
}

// Update city markers (colors, positions based on rotation)
function updateCityMarkers() {
    Object.entries(cityMarkers).forEach(([city, markerObj]) => {
        const { marker, light, position } = markerObj;

        // Check if the marker is on the visible side of the globe
        const dotProduct = new THREE.Vector3(0, 0, 1).dot(
            position.clone().applyMatrix4(globe.matrixWorld).normalize()
        );

        // Make visible only if facing the camera
        if (dotProduct > 0) {
            marker.visible = true;
            light.visible = true;

            // Pulse effect
            const time = Date.now() * 0.001;
            const pulse = (Math.sin(time * 2) + 1) / 4 + 0.5;
            light.intensity = pulse;
        } else {
            marker.visible = false;
            light.visible = false;
        }
    });
}

// Handle mouse move for interactions
function onMouseMove(event) {
    // Calculate mouse position in normalized device coordinates
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    // Check for intersections with city markers
    raycaster.setFromCamera(mouse, camera);

    // Get all city markers for intersection test
    const markerObjects = Object.values(cityMarkers).map(m => m.marker);
    const intersects = raycaster.intersectObjects(markerObjects);

    // Reset all markers to normal size
    markerObjects.forEach(marker => {
        marker.scale.set(1, 1, 1);
    });

    // If intersection found, highlight the marker
    if (intersects.length > 0) {
        const marker = intersects[0].object;
        marker.scale.set(1.5, 1.5, 1.5);
        document.body.style.cursor = 'pointer';
    } else {
        document.body.style.cursor = 'default';
    }
}

// Handle mouse click for selecting cities
function onMouseClick(event) {
    // Calculate mouse position in normalized device coordinates
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    // Check for intersections with city markers
    raycaster.setFromCamera(mouse, camera);

    // Get all city markers for intersection test
    const markerObjects = Object.values(cityMarkers).map(m => m.marker);
    const intersects = raycaster.intersectObjects(markerObjects);

    // If intersection found, select the city
    if (intersects.length > 0) {
        const marker = intersects[0].object;
        selectedCity = marker.userData.city;
        updateSelectedCityDisplay();
    }
}

// Update the display for the selected city
function updateSelectedCityDisplay() {
    if (selectedCity && timeData[selectedCity]) {
        const cityData = timeData[selectedCity];
        const cityElement = document.getElementById('current-city');
        cityElement.innerHTML = `
            <h2>${selectedCity}</h2>
            <div class="time">${cityData.time}</div>
            <div>${cityData.date}</div>
            <div>${cityData.timezone} (UTC${cityData.offset})</div>
        `;
    }
}

// Initialize the scene when the page loads
window.addEventListener('load', init);""")

    def create_widgets(self):
        """Create the UI elements"""
        # Create header
        header_frame = tk.Frame(self.root, bg=DARK_BG)
        header_frame.pack(fill="x", pady=10)

        title_label = tk.Label(
            header_frame,
            text="CHRONOEYE",
            font=("Segoe UI", 32, "bold"),
            fg=ACCENT_COLOR,
            bg=DARK_BG
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Advanced Global Time Visualizer",
            font=("Segoe UI", 16),
            fg=TEXT_COLOR,
            bg=DARK_BG
        )
        subtitle_label.pack()

        # Create web view for 3D visualization
        self.webview_frame = Frame(self.root, bg=DARK_BG)
        self.webview_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Create webview using pywebview
        self.webview = webview.create_window(
            "3D Globe",
            f"http://localhost:{self.available_port}/web/index.html",
            width=900,
            height=500,

        )

        # Create bottom panel for analog clocks
        bottom_frame = tk.Frame(self.root, bg=DARK_BG)
        bottom_frame.pack(fill="x", pady=10, padx=20)

        # Create a modern clock for each time zone (limited to 5 to fit)
        selected_cities = list(time_zones.keys())[:5]
        self.clock_widgets = {}

        for i, city in enumerate(selected_cities):
            city_frame = tk.Frame(bottom_frame, bg=DARK_BG)
            city_frame.grid(row=0, column=i, padx=15)

            # City name
            city_label = tk.Label(
                city_frame,
                text=city,
                font=("Segoe UI", 14, "bold"),
                fg=HIGHLIGHT_COLOR,
                bg=DARK_BG
            )
            city_label.pack(pady=(0, 5))

            # Clock canvas
            clock_canvas = tk.Canvas(
                city_frame,
                width=100,
                height=100,
                bg=DARK_BG,
                highlightthickness=0
            )
            clock_canvas.pack()

            # Digital time
            time_label = tk.Label(
                city_frame,
                text="00:00:00",
                font=("Segoe UI", 12),
                fg=TEXT_COLOR,
                bg=DARK_BG
            )
            time_label.pack(pady=5)

            # Store references
            self.clock_widgets[city] = {
                "canvas": clock_canvas,
                "time_label": time_label,
                "timezone": time_zones[city]
            }

        # Create status bar
        status_frame = tk.Frame(self.root, bg="#1E1E1E", height=30)
        status_frame.pack(side="bottom", fill="x")

        self.status_label = tk.Label(
            status_frame,
            text="Time synchronized with global servers",
            font=("Segoe UI", 9),
            fg="#AAAAAA",
            bg="#1E1E1E"
        )
        self.status_label.pack(side="left", padx=10)

        # Draw initial clock faces
        self.draw_clock_faces()

    def draw_clock_faces(self):
        """Draw analog clocks for each city"""
        for city, widgets in self.clock_widgets.items():
            canvas = widgets["canvas"]
            canvas.delete("all")

            # Get current time for this city
            tz = pytz.timezone(widgets["timezone"])
            now = datetime.now(tz)
            hour, minute, second = now.hour, now.minute, now.second

            # Draw clock face
            cx, cy = 50, 50
            radius = 45

            # Draw outer circle
            canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                outline=ACCENT_COLOR,
                width=2
            )

            # Draw inner circle
            canvas.create_oval(
                cx - radius + 10, cy - radius + 10,
                cx + radius - 10, cy + radius - 10,
                outline=HIGHLIGHT_COLOR,
                width=1
            )

            # Draw hour markers
            for i in range(12):
                angle = math.radians(i * 30)
                x1 = cx + (radius - 5) * math.cos(angle)
                y1 = cy - (radius - 5) * math.sin(angle)
                x2 = cx + (radius - 15) * math.cos(angle)
                y2 = cy - (radius - 15) * math.sin(angle)
                if i % 3 == 0:
                    canvas.create_line(x1, y1, x2, y2, fill=SECONDARY_COLOR, width=2)
                else:
                    canvas.create_line(x1, y1, x2, y2, fill=TEXT_COLOR, width=1)

            # Draw hour hand
            hour_angle = math.radians((hour % 12 + minute / 60) * 30)
            hour_x = cx + 25 * math.cos(hour_angle)
            hour_y = cy - 25 * math.sin(hour_angle)
            canvas.create_line(cx, cy, hour_x, hour_y, fill=HIGHLIGHT_COLOR, width=3)

            # Draw minute hand
            minute_angle = math.radians(minute * 6)
            minute_x = cx + 35 * math.cos(minute_angle)
            minute_y = cy - 35 * math.sin(minute_angle)
            canvas.create_line(cx, cy, minute_x, minute_y, fill=TEXT_COLOR, width=2)

            # Draw second hand
            second_angle = math.radians(second * 6)
            second_x = cx + 40 * math.cos(second_angle)
            second_y = cy - 40 * math.sin(second_angle)
            canvas.create_line(cx, cy, second_x, second_y, fill=ACCENT_COLOR, width=1)

            # Draw center dot
            canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill=SECONDARY_COLOR)

            # Update digital time
            widgets["time_label"].config(text=now.strftime("%H:%M:%S"))

    def update_data(self):
        """Update time data and UI"""
        # Update clock faces
        self.draw_clock_faces()

        # Update status bar with current UTC time
        utc_time = datetime.now(pytz.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        self.status_label.config(text=f"Global Sync: {utc_time}")

        # Schedule next update
        self.root.after(1000, self.update_data)

    def create_api_endpoints(self):
        """Create API endpoints for the web interface"""

        class TimeDataHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/api/time-data':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()

                    # Get time data from the app instance
                    data = app.time_api.get_time_data()
                    self.wfile.write(json.dumps(data).encode())
                else:
                    # Serve static files
                    try:
                        if self.path == '/':
                            self.path = '/web/index.html'
                        elif not self.path.startswith('/web'):
                            self.path = f'/web{self.path}'

                        file_to_open = open(self.path[1:], 'rb')
                        self.send_response(200)

                        # Set content type based on file extension
                        if self.path.endswith('.html'):
                            self.send_header('Content-type', 'text/html')
                        elif self.path.endswith('.css'):
                            self.send_header('Content-type', 'text/css')
                        elif self.path.endswith('.js'):
                            self.send_header('Content-type', 'application/javascript')
                        else:
                            self.send_header('Content-type', 'application/octet-stream')

                        self.end_headers()
                        self.wfile.write(file_to_open.read())
                        file_to_open.close()

                    except FileNotFoundError:
                        self.send_response(404)
                        self.end_headers()
                        self.wfile.write(b'File not found')

        return TimeDataHandler

    def __del__(self):
        """Clean up resources when app is closed"""
        if hasattr(self, 'server') and self.server:
            self.server.stop()


# Create custom handler for the web server
class AppHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/time-data':
            # This is the API endpoint for time data
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Create time data
            time_api = TimeDataAPI(time_zones)
            data = time_api.get_time_data()
            self.wfile.write(json.dumps(data).encode())
        else:
            # Serve static files
            return http.server.SimpleHTTPRequestHandler.do_GET(self)


def main():
    # Start the web server in a separate thread
    handler = AppHandler
    httpd = socketserver.TCPServer(("", 8081), handler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # Create the main window and app
    root = tk.Tk()
    app = ChronoEyeApp(root)

    # Run the application
    root.mainloop()

    # Clean up
    httpd.shutdown()


if __name__ == "__main__":
    main()
    '''

