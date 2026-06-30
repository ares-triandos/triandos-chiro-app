# Deployment Checklist - Triandos Chiro App

## Phase 1: Local Development Setup ✅

- [x] Created fresh React Native 0.75.4 project
- [x] Setup Firebase integration (Auth + Firestore)
- [x] Created patient screens (auth, appointments, scripts, settings)
- [x] Configured TypeScript support
- [x] Created Fastlane setup for iOS builds
- [x] Setup GitHub Actions CI/CD workflow
- [x] Committed to git with clean history

## Phase 2: Firebase Configuration (NEXT)

- [ ] Create Firebase project: https://console.firebase.google.com
- [ ] Add iOS app with bundle ID: `com.triandoschiro.app`
- [ ] Download `GoogleService-Info.plist`
- [ ] Add plist to Xcode project (TriandosChiro target)
- [ ] Enable Email/Password authentication in Firebase
- [ ] Create Firestore database (start in Test mode)
- [ ] Update Firestore rules with security rules (see FIREBASE_SETUP.md)

**Time estimate:** 10 minutes

## Phase 3: Install Dependencies (AFTER Firebase)

```bash
npm install
cd ios && pod install --repo-update && cd ..
```

**Time estimate:** 15 minutes

## Phase 4: Local Testing

```bash
npm run ios
```

Manually test:
- [ ] Signup screen loads
- [ ] Can create account
- [ ] Login works
- [ ] Appointments calendar opens
- [ ] Settings page accessible
- [ ] Logout works

**Time estimate:** 10 minutes

## Phase 5: First GitHub Push (Triggers Automated Build)

```bash
git push origin main
```

GitHub Actions will:
1. ✅ Checkout code
2. ✅ Install dependencies
3. ✅ Install CocoaPods
4. ✅ Build with Xcode
5. ✅ Submit to TestFlight via Fastlane

Monitor at: https://github.com/AresTriandos/triandos-chiro-app/actions

**Time estimate:** 45 minutes

## Phase 6: TestFlight Review

Once build is uploaded (5-10 min after push):
- [ ] Open TestFlight app on your device
- [ ] Install app from TestFlight
- [ ] Test full functionality on real device
- [ ] Check for any crashes/bugs
- [ ] Document any issues

**Time estimate:** 20 minutes

## Phase 7: App Store Submission (Optional)

Once satisfied with TestFlight:
- [ ] Review App Store Connect settings
- [ ] Fill in app description, screenshots
- [ ] Set pricing and availability
- [ ] Submit for App Store review

**Time estimate:** 30 minutes

---

## Quick Start Commands

```bash
# Install everything
npm install && cd ios && pod install --repo-update && cd ..

# Run on simulator
npm run ios

# Manual build for TestFlight
cd ios && bundle exec fastlane ios build_testflight

# Check GitHub Actions status
open https://github.com/AresTriandos/triandos-chiro-app/actions
```

## Important URLs

- Firebase Console: https://console.firebase.google.com
- GitHub Repo: https://github.com/AresTriandos/triandos-chiro-app
- TestFlight: https://testflight.apple.com
- App Store Connect: https://appstoreconnect.apple.com

## Troubleshooting

### CocoaPods Issues
```bash
cd ios && rm -rf Pods Podfile.lock && pod install --repo-update && cd ..
```

### Fastlane Issues
```bash
cd ios && bundle update fastlane && cd ..
```

### Build Stuck?
- Check GitHub Actions logs: https://github.com/AresTriandos/triandos-chiro-app/actions
- Verify `GoogleService-Info.plist` is added to Xcode
- Ensure org secrets are set (APPLE_ID, APPLE_ID_PASSWORD)

---

## Timeline

| Phase | Status | Estimate | Start |
|-------|--------|----------|-------|
| Local Setup | ✅ Done | 30 min | Now |
| Firebase | ⏳ Ready | 10 min | Next |
| Dependencies | ⏳ Ready | 15 min | After Firebase |
| Local Testing | ⏳ Ready | 10 min | After deps |
| GitHub Push | ⏳ Ready | 45 min | After testing |
| TestFlight | ⏳ Ready | 20 min | After push |
| App Store | ⏳ Ready | 30 min | Optional |

**Total time to TestFlight: ~2-3 hours**

---

✅ Scaffold complete. Ready for Firebase setup!
