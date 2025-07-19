# APK Build Instructions for CNC ToolCalc

## Method 1: PWA Builder (Easiest)
1. Go to https://www.pwabuilder.com/
2. Enter your URL: https://cnc-tool-param-calc.onrender.com
3. Click "Build My PWA"
4. Download the generated APK
5. Test on device
6. Upload to Google Play Console

## Method 2: Bubblewrap (Google's TWA)
1. Install Node.js and Java JDK
2. Run: npm install -g @bubblewrap/cli
3. Run: bubblewrap init --manifest https://cnc-tool-param-calc.onrender.com/static/manifest.json
4. Run: bubblewrap build
5. Find APK in: android/app/build/outputs/apk/debug/

## Method 3: Capacitor
1. Install: npm install -g @capacitor/cli
2. Run: npx cap init "CNC ToolCalc" "com.cnctoolcalc.app"
3. Run: npx cap add android
4. Run: npx cap build android
5. Find APK in: android/app/build/outputs/apk/debug/

## Method 4: Manual Android Studio
1. Create new Android project
2. Add WebView component
3. Load your URL: https://cnc-tool-param-calc.onrender.com
4. Build APK

## Google Play Store Requirements:
- APK signed with release key
- Privacy policy
- App description and screenshots
- Content rating
- Developer account ($25 one-time fee)

## Recommended: PWA Builder
This is the easiest method and generates a proper TWA (Trusted Web Activity) APK.
