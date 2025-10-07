<h1 style="text-align:center">CubeGame</h1>

# 🚀 Project Setup Guide

## 📦 Installation

Before running the project, make sure you have Python installed.  
Then, install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🖥️ Running the Project

### ▶️ Start the Client
Run the following script to launch the client:
```bash
client.bat
```

### ⚙️ Start the Server
Run the following script to launch the server:
```bash
server.bat
```

---

## ⚙️ Configuration Files

### 🧩 `server.conf`
Contains the server configuration:
```
ip=127.0.0.1
port=44444
```

### 💻 `client.conf`
Contains the client configuration:
```
ip=127.0.0.1
port=44444
username=KGriffon
```

Make sure the client and server IP/port match before running.

---

## 🏗️ Building the Project

To build the project, simply run:
```bash
build.bat
```

The compiled and packaged files will be available in the **`dist/`** directory.