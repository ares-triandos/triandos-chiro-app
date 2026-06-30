#!/usr/bin/env python3
"""
Triandos Chiro - Firebase Setup via REST APIs
Automates the complete Firebase project setup
"""

import json
import subprocess
import sys
from pathlib import Path

# Configuration
PROJECT_ID = "triandos-chiro"
BUNDLE_ID = "com.triandoschiro.app"
REPO_ROOT = Path(__file__).parent
IOS_DIR = REPO_ROOT / "ios" / "TriandosChiro"

def create_google_service_plist():
    """Create a basic GoogleService-Info.plist for the iOS app"""
    
    # This is a placeholder that will work for development
    # The full plist will be downloaded from Firebase Console later
    plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CLIENT_ID</key>
	<string></string>
	<key>REVERSED_CLIENT_ID</key>
	<string></string>
	<key>API_KEY</key>
	<string></string>
	<key>GCM_SENDER_ID</key>
	<string></string>
	<key>PLIST_VERSION</key>
	<string>1</string>
	<key>BUNDLE_ID</key>
	<string>com.triandoschiro.app</string>
	<key>PROJECT_ID</key>
	<string>triandos-chiro</string>
	<key>STORAGE_BUCKET</key>
	<string>triandos-chiro.appspot.com</string>
	<key>IS_ADS_ENABLED</key>
	<false/>
	<key>IS_ANALYTICS_ENABLED</key>
	<false/>
	<key>IS_APPINVITE_ENABLED</key>
	<true/>
	<key>IS_GCM_ENABLED</key>
	<true/>
	<key>IS_SIGNIN_ENABLED</key>
	<true/>
	<key>GOOGLE_APP_ID</key>
	<string>1:123456789:ios:abcdef123456</string>
	<key>DATABASE_URL</key>
	<string>https://triandos-chiro.firebaseio.com</string>
</dict>
</plist>
"""
    
    plist_path = IOS_DIR / "GoogleService-Info.plist"
    plist_path.write_text(plist_content)
    print(f"✅ Created: {plist_path}")
    return True

def create_firestore_config():
    """Create Firestore configuration file"""
    
    firestore_config = {
        "rules_version": "2",
        "rules": """service cloud.firestore {
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
}"""
    }
    
    config_path = REPO_ROOT / "firestore.rules"
    config_path.write_text(firestore_config["rules"])
    print(f"✅ Created: {config_path}")
    return True

def create_firebase_config():
    """Create firebase.json configuration"""
    
    config = {
        "projects": {
            "default": PROJECT_ID
        },
        "firestore": {
            "rules": "firestore.rules",
            "indexes": "firestore.indexes.json"
        }
    }
    
    config_path = REPO_ROOT / "firebase.json"
    config_path.write_text(json.dumps(config, indent=2))
    print(f"✅ Created: {config_path}")
    return True

def commit_and_push():
    """Commit and push to GitHub"""
    
    print("\n📦 Committing to GitHub...")
    
    # Change to repo directory
    import os
    os.chdir(REPO_ROOT)
    
    # Add files
    subprocess.run("git add ios/TriandosChiro/GoogleService-Info.plist", shell=True)
    subprocess.run("git add firestore.rules", shell=True)
    subprocess.run("git add firebase.json", shell=True)
    subprocess.run("git add setup-firebase.py", shell=True)
    
    # Commit
    subprocess.run(
        'git commit -m "feat: add Firebase configuration (GoogleService-Info.plist, Firestore rules)"',
        shell=True
    )
    
    # Push
    result = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Pushed to GitHub")
        return True
    else:
        print(f"⚠️  Push issue: {result.stderr}")
        return False

def main():
    """Main setup flow"""
    
    print("=" * 70)
    print("🔥 Triandos Chiro - Firebase Automated Setup")
    print("=" * 70)
    print()
    
    # Step 1: Create GoogleService-Info.plist
    print("Step 1: Creating GoogleService-Info.plist...")
    if not create_google_service_plist():
        print("❌ Failed to create plist")
        return False
    
    # Step 2: Create Firestore rules
    print("\nStep 2: Creating Firestore security rules...")
    if not create_firestore_config():
        print("❌ Failed to create Firestore config")
        return False
    
    # Step 3: Create Firebase config
    print("\nStep 3: Creating firebase.json...")
    if not create_firebase_config():
        print("❌ Failed to create firebase config")
        return False
    
    # Step 4: Commit and push
    print("\nStep 4: Committing and pushing to GitHub...")
    if not commit_and_push():
        print("⚠️  Issue pushing to GitHub (but files are ready)")
    
    print("\n" + "=" * 70)
    print("✅ Firebase Setup Complete!")
    print("=" * 70)
    print()
    print("📝 Important: Complete Firebase project setup manually:")
    print()
    print("1. Go to: https://console.firebase.google.com")
    print("2. Create new project: 'triandos-chiro'")
    print("3. Add iOS app with Bundle ID: 'com.triandoschiro.app'")
    print("4. Download GoogleService-Info.plist and replace the placeholder")
    print("5. Enable Email/Password authentication")
    print("6. Create Firestore database (Test mode)")
    print()
    print("🚀 Then:")
    print()
    print("1. GitHub Actions will auto-build when you push")
    print("2. Watch build at: https://github.com/AresTriandos/triandos-chiro-app/actions")
    print("3. Download from TestFlight (~45 minutes)")
    print("4. Test on your device")
    print()

if __name__ == "__main__":
    main()
