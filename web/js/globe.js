// Globe visualization using Three.js
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
window.addEventListener('load', init);