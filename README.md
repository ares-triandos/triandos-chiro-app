# Triandos Chiro - Patient Portal App

iOS app for Triandos Chiropractic Office. Patients can schedule appointments and access treatment scripts.

## Tech Stack

- **React Native** 0.75.4 - Native iOS app
- **Firebase** - Authentication, Firestore database
- **React Navigation** - Tab-based navigation
- **Fastlane** - Automated TestFlight builds
- **GitHub Actions** - CI/CD automation

## Features

- **Patient Authentication** - Secure login/signup
- **Appointment Booking** - Calendar-based scheduling
- **Patient Portal** - Access treatment scripts and records
- **Settings** - Profile management and logout

## Setup

### Prerequisites

- Node 22+
- macOS with Xcode 15+
- CocoaPods
- Ruby 3.2+
- Fastlane gem

### Local Development

```bash
# Install dependencies
npm install

# Install iOS pods
cd ios && pod install && cd ..

# Run on iOS simulator
npm run ios
```

### Firebase Setup

1. Create Firebase project at console.firebase.google.com
2. Add iOS app with bundle ID: `com.triandoschiro.app`
3. Download `GoogleService-Info.plist`
4. Add to Xcode project

### Fastlane Setup

```bash
cd ios
bundle install
fastlane ios build_testflight
```

### GitHub Secrets (Already Configured)

Organization-level secrets:
- `APPLE_ID` - Apple ID email
- `APPLE_ID_PASSWORD` - App-specific password
- `EXPO_TOKEN` - (for future EAS builds if needed)

## Build & Deploy

### Automatic (via Git Push)

```bash
git push origin main
```

This triggers GitHub Actions → Builds → TestFlight submission

### Manual Build

```bash
cd ios
bundle exec fastlane ios build_testflight
```

## Directory Structure

```
triandos-chiro-app/
├── src/
│   ├── screens/
│   │   ├── auth/
│   │   │   ├── LoginScreen.tsx
│   │   │   └── SignupScreen.tsx
│   │   └── patient/
│   │       ├── AppointmentsScreen.tsx
│   │       ├── ScriptsScreen.tsx
│   │       └── SettingsScreen.tsx
│   └── App.tsx
├── ios/
│   ├── Fastfile
│   ├── Gemfile
│   └── TriandosChiro.xcworkspace
├── .github/workflows/
│   └── build-ios.yml
├── package.json
├── tsconfig.json
└── index.js
```

## Key Files

- **App.tsx** - Main app component with navigation
- **Fastfile** - Fastlane build automation
- **.github/workflows/build-ios.yml** - GitHub Actions CI/CD

## Troubleshooting

### Build Issues

If `pod install` fails:
```bash
cd ios
rm -rf Pods Podfile.lock
pod install --repo-update
cd ..
```

If Fastlane fails:
```bash
cd ios
bundle update fastlane
bundle exec fastlane ios build_testflight --verbose
```

## Next Steps

1. ✅ Initialize project
2. ✅ Setup Firebase
3. ✅ Create screens
4. ✅ Configure Fastlane
5. ⏭️ Test locally on simulator
6. ⏭️ First GitHub push triggers TestFlight build
7. ⏭️ Review in TestFlight → Submit to App Store

## Support

For issues or questions, check the GitHub Actions logs or contact support.
