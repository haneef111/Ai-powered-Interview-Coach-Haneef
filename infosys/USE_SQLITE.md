# Switch to SQLite (No MongoDB Required)

If you're having MongoDB connection issues, use the SQLite version instead.

## Steps:

1. **Stop the current backend** (Ctrl+C in the terminal running app.py)

2. **Start the SQLite backend:**
```bash
cd backend
python app_sqlite.py
```

3. **That's it!** Everything else stays the same.

The SQLite version:
- ✅ No MongoDB installation needed
- ✅ No connection string configuration
- ✅ Works exactly the same
- ✅ Stores data in a local file (interview_coach.db)
- ✅ Perfect for development and testing

## Or use the batch file:

Just double-click: `run_backend_sqlite.bat`

The frontend doesn't need any changes - it will work with either backend!
