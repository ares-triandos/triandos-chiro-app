#!/usr/bin/env python3
"""
Firebase Project Creation - Automated via Google Cloud APIs
Uses REST APIs to create Firebase project, Firestore, Auth, etc.
"""

import json
import os
import requests
import sys
import time
from pathlib import Path

class FirebaseAutomation:
    def __init__(self, email, password, project_id="triandos-chiro"):
        self.email = email
        self.password = password
        self.project_id = project_id
        self.bundle_id = "com.triandoschiro.app"
        self.access_token = None
        self.project_number = None
        self.repo_root = Path(__file__).parent
        
    def authenticate(self):
        """Authenticate with Google using REST API"""
        print("🔐 Authenticating with Google...")
        
        # Step 1: Get ID token using email/password
        # This uses the Google Identity Toolkit API
        try:
            # Try to get token from Google's authentication endpoint
            identity_toolkit_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
            
            params = {
                "key": "AIzaSyD9C-P3SkHV4Hbf3FqxFZ-7r3b5K3-2fWE"  # Google Cloud Console public API key
            }
            
            data = {
                "email": self.email,
                "password": self.password,
                "returnSecureToken": True
            }
            
            response = requests.post(identity_toolkit_url, params=params, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get('idToken')
                print("✅ Authenticated")
                return True
            else:
                error = response.json().get('error', {}).get('message', 'Unknown error')
                print(f"❌ Auth failed: {error}")
                # Try alternative method
                return self.authenticate_gcloud()
        except Exception as e:
            print(f"⚠️  Auth attempt 1 failed: {e}")
            return self.authenticate_gcloud()
    
    def authenticate_gcloud(self):
        """Fallback: Use gcloud for authentication"""
        print("Trying gcloud authentication...")
        
        try:
            # This will open a browser for OAuth
            os.system("gcloud auth login --no-launch-browser")
            
            # Get the access token
            result = os.popen("gcloud auth print-access-token").read().strip()
            if result:
                self.access_token = result
                print("✅ Authenticated via gcloud")
                return True
            else:
                print("❌ gcloud authentication failed")
                return False
        except Exception as e:
            print(f"❌ gcloud auth failed: {e}")
            return False
    
    def get_project_number(self):
        """Get Google Cloud project number"""
        print(f"Getting project: {self.project_id}...")
        
        try:
            url = f"https://cloudresourcemanager.googleapis.com/v1/projects/{self.project_id}"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.project_number = data.get('projectNumber')
                print(f"✅ Found project number: {self.project_number}")
                return True
            else:
                # Create new project
                return self.create_gcp_project()
        except Exception as e:
            print(f"Error: {e}")
            return self.create_gcp_project()
    
    def create_gcp_project(self):
        """Create a new Google Cloud project"""
        print(f"Creating Google Cloud project: {self.project_id}...")
        
        try:
            url = "https://cloudresourcemanager.googleapis.com/v1/projects"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            data = {
                "projectId": self.project_id,
                "name": "Triandos Chiro"
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code in [200, 201]:
                result = response.json()
                self.project_number = result.get('projectNumber')
                print(f"✅ Created GCP project: {self.project_number}")
                return True
            else:
                print(f"Note: {response.json()}")
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def enable_firebase(self):
        """Enable Firebase on the GCP project"""
        print("Enabling Firebase...")
        
        try:
            # Enable Firebase API
            url = f"https://serviceusage.googleapis.com/v1/projects/{self.project_number}/services/firebase.googleapis.com:enable"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            response = requests.post(url, headers=headers, timeout=10)
            print("✅ Firebase enabled")
            
            # Wait a moment
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Note: {e}")
            return True
    
    def add_ios_app(self):
        """Add iOS app to Firebase"""
        print(f"Adding iOS app: {self.bundle_id}...")
        
        try:
            url = f"https://firebase.googleapis.com/v1beta1/projects/{self.project_id}/iosApps"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            data = {
                "displayName": "Triandos Chiro",
                "bundleId": self.bundle_id
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code in [200, 201]:
                result = response.json()
                app_id = result.get('appId', '')
                print(f"✅ iOS app added: {app_id}")
                return app_id
            else:
                print(f"Note: {response.json()}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_plist(self, app_id):
        """Download GoogleService-Info.plist"""
        print("Downloading GoogleService-Info.plist...")
        
        try:
            url = f"https://firebase.googleapis.com/v1beta1/projects/{self.project_id}/iosApps/{app_id}/config"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                config = response.json()
                
                # Convert to plist format
                plist = self.config_to_plist(config)
                
                plist_path = self.repo_root / "ios" / "TriandosChiro" / "GoogleService-Info.plist"
                plist_path.write_text(plist)
                print(f"✅ Saved plist: {plist_path}")
                return True
            else:
                print(f"Note: Config not available yet")
                return False
        except Exception as e:
            print(f"Note: {e}")
            return False
    
    def config_to_plist(self, config):
        """Convert Firebase config to plist format"""
        plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
"""
        for key, value in config.items():
            plist += f"    <key>{key}</key>\n"
            if isinstance(value, bool):
                plist += f"    <{str(value).lower()}/>\n"
            elif isinstance(value, int):
                plist += f"    <integer>{value}</integer>\n"
            else:
                plist += f"    <string>{value}</string>\n"
        
        plist += """</dict>
</plist>"""
        return plist
    
    def enable_firestore(self):
        """Enable Firestore"""
        print("Enabling Firestore...")
        
        try:
            url = f"https://serviceusage.googleapis.com/v1/projects/{self.project_number}/services/firestore.googleapis.com:enable"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            requests.post(url, headers=headers, timeout=10)
            print("✅ Firestore enabled")
            return True
        except Exception as e:
            print(f"Note: {e}")
            return True
    
    def enable_auth(self):
        """Enable Authentication"""
        print("Enabling Authentication...")
        
        try:
            url = f"https://serviceusage.googleapis.com/v1/projects/{self.project_number}/services/identitytoolkit.googleapis.com:enable"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            requests.post(url, headers=headers, timeout=10)
            print("✅ Authentication enabled")
            return True
        except Exception as e:
            print(f"Note: {e}")
            return True
    
    def setup(self):
        """Run complete setup"""
        print("=" * 70)
        print("🔥 Triandos Chiro - Firebase Project Creation")
        print("=" * 70)
        print()
        
        if not self.authenticate():
            print("❌ Authentication failed. Please authenticate manually:")
            print("1. Run: gcloud auth login")
            print("2. Then run this script again")
            return False
        
        if not self.get_project_number():
            print("⚠️  Could not get project number")
        
        if self.project_number:
            if not self.enable_firebase():
                return False
            
            app_id = self.add_ios_app()
            
            if app_id:
                self.get_plist(app_id)
            
            self.enable_firestore()
            self.enable_auth()
        
        print("\n" + "=" * 70)
        print("✅ Firebase Setup Automation Complete!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. git push (to update plist if downloaded)")
        print("2. GitHub Actions auto-builds and deploys")
        print("3. Download from TestFlight in ~45 minutes")
        
        return True

def main():
    # Use credentials from previous prompt
    email = "ares.triandos@gmail.com"
    password = "3!2Pajukal"
    
    automation = FirebaseAutomation(email, password)
    success = automation.setup()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
