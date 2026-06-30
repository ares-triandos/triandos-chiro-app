# Final Setup Steps - Triandos Chiro App

**Status:** ✅ iOS project scaffolding complete. Native iOS build files ready.

## What's Done ✅

- [x] React Native 0.75.4 project initialized
- [x] iOS native project structure created (TriandosChiro.xcodeproj)
- [x] Firebase pods added to Podfile
- [x] App screens created (Auth, Appointments, Scripts, Settings)
- [x] Fastlane configuration ready
- [x] GitHub Actions CI/CD workflow ready
- [x] TypeScript support configured

## What's Left (30 minutes)

### 1. Firebase Project Setup (10 min) 🔥

**On your Mac, in the browser:**

1. Go to: https://console.firebase.google.com
2. Click **"Create a new project"**
3. Project name: `triandos-chiro`
4. Region: **United States**
5. Click **"Create project"** (wait 2-3 min)

### 2. Add iOS App to Firebase (5 min)

1. In Firebase console, click the **iOS icon**
2. **Bundle ID:** `com.triandoschiro.app`
3. **App nickname:** `Triandos Chiro`
4. Click **"Register app"**
5. **IMPORTANT:** Download the `GoogleService-Info.plist` file
   - Save it somewhere accessible

### 3. Add Plist to Xcode Project (5 min)

1. On your Mac, open Xcode
2. Open: `ios/TriandosChiro.xcworkspace` (NOT .xcodeproj)
3. In Xcode, select the **TriandosChiro** project in the left sidebar
4. Right-click → **"Add Files to TriandosChiro..."**
5. Choose the **GoogleService-Info.plist** file you downloaded
6. ⚠️ **Important:** Check these boxes:
   - ☑️ "Copy items if needed"
   - ☑️ "Create groups"
   - ☑️ Target: **TriandosChiro** (must be checked!)
7. Click **"Add"**
8. **Verify:** GoogleService-Info.plist should appear in Xcode navigator

### 4. Enable Email/Password Authentication (3 min)

1. Go back to Firebase console
2. Click **"Authentication"** in the left menu
3. Click **"Sign-in method"** tab
4. Find **"Email/Password"**
5. Click on it, toggle **Enable**, then **Save**

### 5. Create Firestore Database (5 min)

1. In Firebase console, click **"Firestore Database"**
2. Click **"Create database"**
3. **Start mode:** "Test mode" (for development)
4. **Location:** `us-central1`
5. Click **"Create database"** (wait for it to be created)

### 6. Update Firestore Security Rules (2 min)

1. In Firestore, go to the **"Rules"** tab
2. Replace the default rules with this:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Patients can read/write their own data
    match /patients/{userId} {
      allow read, write: if request.auth.uid == userId;
      
      // Nested appointments
      match /appointments/{appointmentId} {
        allow read, write: if request.auth.uid == userId;
      }
      
      // Nested scripts (read-only for patients)
      match /scripts/{scriptId} {
        allow read: if request.auth.uid == userId;
      }
    }
  }
}
```

3. Click **"Publish"**

---

## Next: Install & Test (30 min)

Once Firebase is set up, run these commands on your Mac:

```bash
# Navigate to project
cd triandos-chiro-app

# Install dependencies
npm install

# Install iOS pods
cd ios
pod install --repo-update
cd ..

# Test on simulator
npm run ios
```

**Things to test:**
- ✅ App loads
- ✅ Sign up page works
- ✅ Create new account
- ✅ Login page works
- ✅ Login with that account
- ✅ See appointments screen
- ✅ See scripts screen
- ✅ See settings screen

---

## Then: First Deployment (45 min)

Once local testing works:

```bash
# Commit & push
git add -A
git commit -m "feat: add Firebase configuration and iOS project setup"
git push origin main
```

**This automatically:**
1. Triggers GitHub Actions
2. Builds iOS app
3. Submits to TestFlight
4. You'll see a notification in TestFlight app

---

## URLs to Keep Handy

- **Firebase Console:** https://console.firebase.google.com
- **GitHub Actions:** https://github.com/AresTriandos/triandos-chiro-app/actions
- **TestFlight:** https://testflight.apple.com
- **App Store Connect:** https://appstoreconnect.apple.com

---

## Troubleshooting

### Pod install fails?
```bash
cd ios
rm -rf Pods Podfile.lock
pod install --repo-update
cd ..
```

### GoogleService-Info.plist not found in Xcode?
- Make sure it's in the TriandosChiro.xcodeproj folder
- In Xcode, drag it into the project navigator
- Verify it's under the TriandosChiro target in Build Phases → Copy Bundle Resources

### App crashes on launch?
- Check Console in Xcode (Product → Scheme → Edit Scheme → Run → Diagnostics)
- If it says "GoogleService-Info.plist" not found, verify step 3 above
- Make sure TriandosChiro.xcworkspace is open (not .xcodeproj)

---

## You're Almost There! 🚀

Once you complete these steps, you'll have:
- ✅ iOS app running on your device
- ✅ Patient authentication working
- ✅ Appointment booking functional
- ✅ Automated builds via GitHub Actions
- ✅ Ready for TestFlight & App Store

Estimated total time: **1 hour**
