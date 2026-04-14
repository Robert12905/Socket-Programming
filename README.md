# Socket Programming - Multi-Client Chat Application

## Course Information

Florida Gulf Coast University (FGCU)  
COP 3635 - Computer Networking  
Final Project

Instructor: Dr. Deepa Devasenapathy

Project Start Date: April 11, 2026  
Due Date: April 14, 2026

## Team Members

- [Robert Benstine](https://github.com/Robert12905)
- [Chris Cartaya](https://github.com/chris-cartaya)

---

## Project Overview

This project is a Python-based socket programming application that implements a **multi-client chat system**.

The goal is to allow multiple clients to connect to a server and communicate with each other in real time.

---

## Current Status

- Multi-client server with concurrent connections (threaded)
- Real-time message broadcasting between clients
- Username system implemented
- Join/leave notifications
- Duplicate username protection (server-side validation)
- Graceful client disconnect and server shutdown handling
- Color-coded server terminal output per username
- Shared configuration file (`config.py`)

---

## Project Structure

    Socket-Programming/
    ├── README.md
    ├── .gitignore
    ├── client.py
    ├── server.py
    └── config.py

### File Descriptions

- `server.py` - Runs the server. Handles client connections, message broadcasting, usernames, and server-side validation logic.

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

### 3. Activate virtual environment

#### Git Bash (Windows)

```bash
source .venv/Scripts/activate
```

#### PowerShell (Windows)

```pwsh
.venv\Scripts\Activate.ps1
```

#### Command Prompt (Windows)

```cmd
.venv\Scripts\activate.bat
```

#### macOS / Linux

```bash
source .venv/bin/activate
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

### Notes

- You can run multiple clients by opening multiple terminals.
- Each client must enter a unique username.
- Type `quit` to disconnect from the chat.

---

## Current Features

- Multi-client support (simultaneous connections)
- Username system
- Message broadcasting
- Client join/leave notifications
- Duplicate username protection
- Graceful disconnect handling

---

## Future Improvements

- Retry username selection without disconnecting
- Timestamps for messages
- Private messaging
- Active user list command (`/users`)

---

## Notes

- This project currently uses only Python’s standard library
- Tested with Python 3.12+
