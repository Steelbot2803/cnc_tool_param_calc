#!/usr/bin/env python3
"""
APK Builder for CNC Tool Parameter Calculator
Converts the web application to Android APK for Google Play Store
"""

import os
import json
import subprocess
import shutil
from pathlib import Path

def create_bubblewrap_config():
    """Create Bubblewrap configuration for TWA (Trusted Web Activity)"""
    config = {
        "packageId": "com.cnctoolcalc.app",
        "host": "cnc-tool-param-calc.onrender.com",
        "name": "CNC ToolCalc",
        "launcherName": "CNC ToolCalc",
        "display": "standalone",
        "themeColor": "#16a34a",
        "backgroundColor": "#000000",
        "enableNotifications": True,
        "shortcuts": [
            {
                "name": "Calculate",
                "shortName": "Calc",
                "url": "/",
                "chosenIconUrl": "/static/icon-192.png"
            }
        ],
        "iconUrl": "/static/icon-512.png",
        "maskableIconUrl": "/static/icon-512.png",
        "splashScreenFadeOutDuration": 300,
        "signingKey": {
            "path": "android.keystore",
            "alias": "cnc-toolcalc"
        }
    }
    
    with open('bubblewrap-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created bubblewrap-config.json")

def create_capacitor_config():
    """Create Capacitor configuration for hybrid app"""
    config = {
        "appId": "com.cnctoolcalc.app",
        "appName": "CNC ToolCalc",
        "webDir": "dist",
        "bundledWebRuntime": False,
        "server": {
            "url": "https://cnc-tool-param-calc.onrender.com",
            "cleartext": False
        },
        "android": {
            "backgroundColor": "#000000"
        }
    }
    
    with open('capacitor.config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created capacitor.config.json")

def create_pwa_builder_config():
    """Create PWA Builder configuration"""
    config = {
        "name": "CNC ToolCalc",
        "short_name": "CNC ToolCalc",
        "description": "Professional CNC machining calculator",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#000000",
        "theme_color": "#16a34a",
        "orientation": "portrait",
        "scope": "/",
        "lang": "en",
        "categories": ["productivity", "tools"],
        "icons": [
            {
                "src": "/static/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ]
    }
    
    with open('pwa-builder-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created pwa-builder-config.json")

def create_package_json():
    """Create package.json for Node.js dependencies"""
    package = {
        "name": "cnc-toolcalc",
        "version": "1.0.0",
        "description": "CNC Tool Parameter Calculator",
        "main": "app.py",
        "scripts": {
            "start": "python app.py",
            "build:android": "npx @bubblewrap/cli build",
            "build:pwa": "npx pwa-builder",
            "build:capacitor": "npx cap build android"
        },
        "dependencies": {
            "@bubblewrap/cli": "^1.0.0",
            "@capacitor/cli": "^5.0.0",
            "@capacitor/android": "^5.0.0",
            "pwa-builder": "^1.0.0"
        },
        "devDependencies": {
            "@capacitor/core": "^5.0.0"
        }
    }
    
    with open('package.json', 'w') as f:
        json.dump(package, f, indent=2)
    
    print("✅ Created package.json")

def create_android_manifest():
    """Create Android manifest template"""
    manifest = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.cnctoolcalc.app">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">

        <activity
            android:name="com.google.androidbrowserhelper.trusted.LauncherActivity"
            android:exported="true"
            android:launchMode="singleTask">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="https"
                      android:host="cnc-tool-param-calc.onrender.com" />
            </intent-filter>
        </activity>

        <meta-data
            android:name="asset_statements"
            android:resource="@string/asset_statements" />

    </application>

</manifest>'''
    
    os.makedirs('android/app/src/main', exist_ok=True)
    with open('android/app/src/main/AndroidManifest.xml', 'w') as f:
        f.write(manifest)
    
    print("✅ Created AndroidManifest.xml")

def create_build_instructions():
    """Create build instructions file"""
    instructions = '''# APK Build Instructions for CNC ToolCalc

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
'''
    
    with open('BUILD_INSTRUCTIONS.md', 'w') as f:
        f.write(instructions)
    
    print("✅ Created BUILD_INSTRUCTIONS.md")

def main():
    """Main function to set up APK build environment"""
    print("🚀 Setting up APK build environment for CNC ToolCalc...")
    
    # Create all configuration files
    create_bubblewrap_config()
    create_capacitor_config()
    create_pwa_builder_config()
    create_package_json()
    create_android_manifest()
    create_build_instructions()
    
    print("\n✅ APK build environment ready!")
    print("\n📱 Next steps:")
    print("1. Use PWA Builder (recommended): https://www.pwabuilder.com/")
    print("2. Enter your URL: https://cnc-tool-param-calc.onrender.com")
    print("3. Download the generated APK")
    print("4. Test on Android device")
    print("5. Upload to Google Play Console")
    
    print("\n📋 Files created:")
    print("- bubblewrap-config.json (TWA configuration)")
    print("- capacitor.config.json (Capacitor configuration)")
    print("- pwa-builder-config.json (PWA Builder configuration)")
    print("- package.json (Node.js dependencies)")
    print("- android/app/src/main/AndroidManifest.xml (Android manifest)")
    print("- BUILD_INSTRUCTIONS.md (Detailed build guide)")

if __name__ == "__main__":
    main() 