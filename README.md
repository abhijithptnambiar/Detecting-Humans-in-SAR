
## 🌐 WebApp (Admin & Camera Module)

- Developed using Python (Flask/Django)
- Integrates YOLOv3 and OpenCV for human detection from video feeds
- Admin dashboard to manage rescue teams and view detection history
- Stores data in a MySQL/SQLite database
- Sends detection alerts to the Android app via REST API

## 📱 AndroidApp (Rescue Team Module)

- Developed using Java (Android Studio)
- Receives and displays detection alerts with image and timestamp
- Allows rescue teams to respond and update rescue status

## 🚀 Features

- Human detection using YOLOv3 and OpenCV
- Real-time alerting system
- Web interface for administration
- Mobile app for field operations
- Modular and scalable architecture

## 💻 Technologies Used

- Python, Flask/Django
- YOLOv3, OpenCV
- Java (Android)
- MySQL / SQLite
- RESTful APIs

## 📂 Installation & Setup

> ⚠ Setup instructions will vary based on your environment. General guidelines are:

### WebApp
1. Install required Python packages (`requirements.txt`)
2. Set up YOLOv3 weights and config files
3. Run the Flask/Django server
4. Access the admin dashboard in the browser

### AndroidApp
1. Open the project in Android Studio
2. Configure backend API endpoints
3. Build and install the APK on a device

## 📸 Sample Screenshots

### Detection from Camera Module  
<img src="screenshots/detection_screen.jpg" alt="Detection Screenshot" width="600"/>

### Alert Display in Rescue Team App  
<img src="screenshots/alert_screen.jpg" alt="Alert Screenshot" height="450" width="350"/>
## 🧩 Future Scope

- Integration with drones and GPS-based tracking  
- Advanced thermal detection in low-visibility scenarios  
- Cloud storage and analytics for large-scale deployment  

