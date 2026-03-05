# MongoDB Installation Guide for Windows

## Quick Install Steps:

1. **Download MongoDB Community Server**
   - Go to: https://www.mongodb.com/try/download/community
   - Select: Windows x64
   - Click "Download"

2. **Install MongoDB**
   - Run the installer
   - Choose "Complete" installation
   - Check "Install MongoDB as a Service" (IMPORTANT!)
   - Check "Install MongoDB Compass" (optional GUI tool)
   - Click Install

3. **Verify MongoDB is Running**
   Open Command Prompt and run:
   ```bash
   mongosh
   ```
   
   If you see a MongoDB shell, it's working!
   Type `exit` to quit.

## If MongoDB Service is Not Running:

### Method 1: Start via Services
1. Press `Win + R`
2. Type `services.msc` and press Enter
3. Find "MongoDB Server"
4. Right-click → Start

### Method 2: Start via Command Prompt (Run as Administrator)
```bash
net start MongoDB
```

## Verify Connection:
```bash
mongosh "mongodb://localhost:27017"
```

If successful, you'll see:
```
Current Mongosh Log ID: ...
Connecting to: mongodb://localhost:27017/
```
