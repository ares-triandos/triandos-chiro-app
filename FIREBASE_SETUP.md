# Firebase Setup Guide

## 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Click "Create a new project"
3. Name: `triandos-chiro`
4. Location: Select your region (US)
5. Create project

## 2. Add iOS App

1. Click iOS icon in project overview
2. Bundle ID: `com.triandoschiro.app`
3. App nickname: `Triandos Chiro`
4. Download `GoogleService-Info.plist`

## 3. Add GoogleService-Info.plist to Xcode

1. In Xcode, right-click `TriandosChiro` project
2. Select "Add Files to TriandosChiro"
3. Choose `GoogleService-Info.plist`
4. Ensure "Copy items if needed" is checked
5. Add to TriandosChiro target

## 4. Enable Authentication

### Email/Password Auth

1. Firebase Console → Authentication
2. Click "Get started"
3. Select "Email/Password"
4. Click "Enable"

### (Optional) Google Sign-In

1. Click "Google"
2. Enable and add support email

## 5. Setup Firestore Database

1. Firebase Console → Firestore Database
2. Click "Create database"
3. Start in **Test mode** (for development)
4. Region: `us-central1`
5. Create database

### Firestore Security Rules

Replace with:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Patients can read/write their own documents
    match /patients/{userId} {
      allow read, write: if request.auth.uid == userId;
      
      // Nested appointments
      match /appointments/{appointmentId} {
        allow read, write: if request.auth.uid == userId;
      }
      
      // Nested scripts
      match /scripts/{scriptId} {
        allow read: if request.auth.uid == userId;
      }
    }
    
    // Admin only (for uploading scripts)
    match /patients/{userId}/scripts/{scriptId} {
      allow write: if request.auth.uid == "ADMIN_UID_HERE";
    }
  }
}
```

## 6. Install iOS Dependencies

```bash
cd ios
pod install --repo-update
cd ..
```

## 7. Test Firebase Connection

Run the app:
```bash
npm run ios
```

Try signing up → Should create user in Firebase Auth + Firestore

## Next: Admin Dashboard (Optional)

For managing appointments and uploading scripts:
- Create web dashboard with Next.js
- Use Firebase Admin SDK for admin operations
- Access at: `dashboard.triandoschiro.com`

## Firestore Structure

```
patients/
├── {userId}/
│   ├── name: string
│   ├── email: string
│   ├── createdAt: timestamp
│   ├── appointments/
│   │   └── {appointmentId}/
│   │       ├── dateTime: string
│   │       ├── status: "scheduled" | "completed" | "cancelled"
│   │       ├── notes: string
│   │       └── createdAt: timestamp
│   └── scripts/
│       └── {scriptId}/
│           ├── title: string
│           ├── description: string
│           ├── url: string (Google Drive link)
│           └── createdAt: timestamp
```

## Troubleshooting

### Build fails: CocoaPods issues

```bash
cd ios
rm -rf Pods Podfile.lock
pod install --repo-update
cd ..
```

### Firebase not initializing

Check `GoogleService-Info.plist` is in Xcode target "Copy Bundle Resources"

### Auth not working

Verify Email/Password is enabled in Firebase Console → Authentication

---

Once Firebase is set up, push to main branch to trigger TestFlight build!
