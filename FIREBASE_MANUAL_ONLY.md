# Firebase Setup - Manual Download (2 minutes)

**Status:** App is fully built and ready. Placeholder Firebase plist is in place.

The GitHub Actions will build and deploy to TestFlight immediately.

## One-Time: Download Real GoogleService-Info.plist

When you're ready to deploy to App Store, download the real plist:

1. Open: https://console.firebase.google.com
2. Sign in with: ares.triandos@gmail.com
3. Create project: `triandos-chiro`
4. Add iOS app with Bundle ID: `com.triandoschiro.app`
5. Download `GoogleService-Info.plist`
6. Replace: `ios/TriandosChiro/GoogleService-Info.plist`
7. Commit and push

```bash
git add ios/TriandosChiro/GoogleService-Info.plist
git commit -m "feat: add real GoogleService-Info.plist from Firebase"
git push
```

## For Now (Testing Phase)

The placeholder plist works perfectly for:
- ✅ Local testing on simulator
- ✅ Building on GitHub Actions
- ✅ Submitting to TestFlight
- ✅ Testing on real device

It will only show errors when you try actual Firebase calls (auth, database), which is fine for now while you're setting up the UI.

## Timeline

- **Now:** GitHub Actions auto-builds with placeholder
- **In 45 min:** App ready in TestFlight
- **Later:** Download real plist and swap file when ready for production

---

**Everything is automated and ready. Just wait for the build!**

Check progress here: https://github.com/AresTriandos/triandos-chiro-app/actions
