# 🌍 ChronoEye

ChronoEye is an interactive 3D Globe visualization tool that combines Tkinter and PyWebView to display dynamic geospatial data in a user-friendly desktop application.

## Features
- 3D Globe View with real-time visualization
- Embedded WebView inside Tkinter
- Dynamic Port Selection to prevent conflicts
- Multi-threaded Execution for a smooth user experience
- Local Web Server Integration

## Installation

### Prerequisites
Make sure you have Python 3.8+ installed on your system. Then, install the required dependencies:

```sh
pip install pywebview tk
```

## Getting Started

### Clone the Repository
```sh
git clone https://github.com/KushagraSaxena77/Chronoeye.git
cd Chronoeye
```

### Run the Application
```sh
python main.py
```

## Project Structure
```sh
Chronoeye/
│── web/                 # Web-based 3D visualization assets
│── main.py              # Main Tkinter + PyWebView application
│── server.py            # Local HTTP server
│── README.md            # Project documentation (this file!)
│── requirements.txt     # Python dependencies
```

## How It Works
1. Starts a Local Web Server using Python's `http.server`.
2. Finds an Available Port to prevent conflicts.
3. Launches PyWebView inside a Tkinter UI frame.
4. Displays the 3D Globe Visualization using embedded HTML/CSS/JS.

## Configuration
If you need to change the default port, modify `main.py`:
```python
self.available_port = 8080  # Change this if needed
```

## License
This project is licensed under the MIT License. Feel free to use and modify it!

## Contributing
Pull requests are welcome! If you'd like to contribute:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a Pull Request

## Contact
For any questions or suggestions, feel free to reach out:
- Email: kushagra.saxena@example.com
- Twitter: [@yourhandle](https://twitter.com/yourhandle)
- LinkedIn: [Kushagra Saxena](https://linkedin.com/in/yourname)

Enjoy using ChronoEye! Let us know how it helps your projects!
