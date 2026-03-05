# MongoDB Atlas Setup (Free Cloud Database)

## Step 1: Create Free Account
1. Go to: https://www.mongodb.com/cloud/atlas/register
2. Sign up with email or Google
3. Choose "Free" tier (M0 Sandbox)

## Step 2: Create a Cluster
1. Choose a cloud provider (AWS recommended)
2. Select a region close to you
3. Click "Create Cluster" (takes 3-5 minutes)

## Step 3: Create Database User
1. Click "Database Access" in left menu
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Username: `admin`
5. Password: Create a strong password (save it!)
6. Database User Privileges: "Read and write to any database"
7. Click "Add User"

## Step 4: Allow Network Access
1. Click "Network Access" in left menu
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (for development)
4. Click "Confirm"

## Step 5: Get Connection String
1. Click "Database" in left menu
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string (looks like):
   ```
   mongodb+srv://admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

## Step 6: Update Your .env File
Replace `<password>` with your actual password:
```
MONGO_URI=mongodb+srv://admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/interview_coach?retryWrites=true&w=majority
```

Save the file and restart your backend server!
