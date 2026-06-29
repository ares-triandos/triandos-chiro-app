# DevContainer Setup - Triandos Chiro App

This DevContainer eliminates environment friction. No more "works on my machine" + no CocoaPods cache issues.

## Quick Start

### VS Code (Recommended)
1. Install "Dev Containers" extension (ms-vscode-remote.remote-containers)
2. Open this repo in VS Code
3. Click **"Reopen in Container"** (bottom-right corner)
4. Wait for build (~2 min first time, instant after)
5. Run `npm start` in the terminal

### Command Line
```bash
# Build and run container
devcontainer up --workspace-folder .

# Or use Docker directly
docker build -f .devcontainer/Dockerfile -t triandos-chiro-dev .
docker run -it -v $(pwd):/workspace triandos-chiro-dev
```

## What's Included

- **Node.js 20** — Latest LTS
- **npm** — Package management
- **Expo CLI** — Expo development
- **EAS CLI** — Managed builds (TestFlight, Play Store)
- **Watchman** — File watching for live reload
- **Git** — Version control
- **Python 3.11** — Automation scripting
- **VS Code Extensions** — TypeScript, Prettier, ESLint, Copilot

## Available Commands

Inside the container:

```bash
# Development
npm start              # Start Expo dev server (tunnel mode)
npm run android       # Start Android emulator
npm run ios          # Start iOS simulator
npm run web          # Start web dev server

# Shortcuts (aliases)
expo-dev              # = expo start --tunnel
eas-preview           # = eas build --platform ios --profile preview --wait
eas-prod              # = eas build --platform ios --profile production --wait

# Git (already authenticated via VS Code)
git push              # Push to GitHub (uses VS Code credentials)
git pull              # Pull latest changes
```

## Ports Forwarded

- **8081** — Expo Web dev server
- **19000** — Expo Dev Server
- **19001** — Expo Debug
- **19002** — Expo Inspector

## Why No CocoaPods Cache Issues?

The container starts **completely fresh** each time. No stale Pod cache from previous builds. When you:

1. Update `expo` version → Pod dependencies update automatically
2. Run `eas build` → Fresh, clean environment every time
3. Change `react-native` version → No cache conflicts

**Before (local machine):**
```
Upgrade Expo 52 → 53
↓
Run build → Pod cache still has old version
↓
Build fails: "Unknown error. See logs..."
↓
Manual: npm ci + pod cache clean + rebuild
```

**After (DevContainer):**
```
Upgrade Expo 52 → 53
↓
Run eas build
↓
Fresh environment, no cache
↓
Build succeeds ✅
```

## First Time Setup Checklist

- [ ] Install "Dev Containers" extension in VS Code
- [ ] Open repo, click "Reopen in Container"
- [ ] Wait for `npm install` to complete
- [ ] Test: `npm start` should start Expo dev server
- [ ] GitHub secrets already available (VS Code handles auth)
- [ ] Push to `main` → GitHub Actions builds automatically

## Troubleshooting

**Container won't start?**
```bash
# Rebuild from scratch
devcontainer rebuild --workspace-folder .
```

**Port already in use?**
- DevContainer forwards ports automatically
- If conflict, edit `devcontainer.json` and change port mappings

**Need to reinstall dependencies?**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Git push not working?**
- VS Code handles authentication inside the container
- If stuck, restart VS Code and retry

## Next Steps

1. **Commit & push** `.devcontainer/` to GitHub
2. **Everyone clones** and "Reopen in Container"
3. **No more environment setup** — fully reproducible

This is your single source of truth for development environment.
