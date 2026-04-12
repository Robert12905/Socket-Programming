# Socket Programming - Multi-Client Chat Application

## Course Information

COP 3635 - Computer Networking  
Final Project

## Team Members

- Robert Benstine
- Chris Cartaya

---

## Project Overview

This project is a Python-based socket programming application that will evolve into a **multi-client chat system**.

The goal is to allow multiple clients to connect to a server and communicate with each other in real time.

---

## Current Status

- Basic client/server socket communication code is in place
- Project structure has been cleaned and reorganized
- Virtual environment setup has been added
- Shared configuration file (`config.py`) created

This project is currently being refactored into a proper multi-client chat application.

---

## Project Structure

    Socket-Programming/
    ├── README.md
    ├── .gitignore
    ├── client.py
    ├── server.py
    └── config.py

### File Descriptions

- `server.py` - Runs the server. Handles incoming client connections and will eventually manage message broadcasting between clients.

- `client.py` - Connects to the server. Sends user input and receives messages from the server.  
  This single file can be run multiple times (in separate terminals) to simulate multiple clients.

- `config.py` - Stores shared configuration values such as host, port, buffer size, and encoding.  
  This allows both the client and server to use the same settings without duplicating code.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Robert12905/Socket-Programming.git
cd Socket-Programming
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment (Git Bash)

```bash
source .venv/Scripts/activate
```

---

## Running the Application

### Start the server

```bash
python server.py
```

### Start a client (open another terminal)

```bash
python client.py
```

You can run multiple clients by opening multiple terminals.

---

## Planned Features

- Multi-client support (simultaneous connections)
- Username system
- Message broadcasting
- Client join/leave notifications
- Command support (e.g., /quit, /users)
- Improved error handling

---

## Notes

- This project currently uses only Python’s standard library
- Tested with Python 3.12+
