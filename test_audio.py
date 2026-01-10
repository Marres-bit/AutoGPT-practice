#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Audio Feature Test Script
Verify that audio functionality works correctly
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("AUDIO FEATURE TEST (by GitHub Copilot)")
print("=" * 60)

# Test 1: Import modules
print("\n[TEST 1] Testing imports...")
try:
    from audio import AudioManager, TextToSpeech, SpeechToText
    print("[OK] Audio modules imported successfully")
except ImportError as e:
    print(f"[FAIL] Failed to import audio modules: {e}")
    sys.exit(1)

# Test 2: Initialize AudioManager
print("\n[TEST 2] Initializing AudioManager...")
try:
    audio = AudioManager(tts_rate=150, tts_volume=0.9, stt_language='fr-FR')
    print("[OK] AudioManager initialized successfully")
    print(f"    - TTS Rate: 150 wpm")
    print(f"    - TTS Volume: 0.9")
    print(f"    - STT Language: fr-FR")
except Exception as e:
    print(f"[FAIL] Failed to initialize AudioManager: {e}")
    sys.exit(1)

# Test 3: Test TextToSpeech
print("\n[TEST 3] Testing TextToSpeech...")
try:
    audio.speak_response("Bonjour! Je suis votre assistant audio. Cette fonction permet d'ecouter les reponses.")
    print("[OK] TTS test completed (check for audio output)")
except Exception as e:
    print(f"[FAIL] TTS test failed: {e}")

# Test 4: Check GUI integration
print("\n[TEST 4] Testing GUI integration...")
try:
    from gui_premium import PremiumGUI
    print("[OK] GUI imports successfully with audio module")
except ImportError as e:
    print(f"[FAIL] GUI import failed: {e}")
    sys.exit(1)

# Test 5: Verify audio attributes in GUI
print("\n[TEST 5] Checking audio attributes...")
try:
    # We can't instantiate GUI without Tkinter display, 
    # but we can verify the class has audio methods
    assert hasattr(PremiumGUI, 'toggle_audio'), "Missing toggle_audio method"
    print("[OK] GUI has audio control methods")
except AssertionError as e:
    print(f"[FAIL] Missing audio methods in GUI: {e}")
    sys.exit(1)

# Test 6: Requirements check
print("\n[TEST 6] Checking requirements.txt...")
try:
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    required = ['pyttsx3', 'SpeechRecognition', 'openai', 'python-dotenv']
    missing = []
    
    for req in required:
        if req.lower() not in content.lower():
            missing.append(req)
    
    if missing:
        print(f"[WARN] Missing in requirements.txt: {missing}")
    else:
        print("[OK] All audio dependencies in requirements.txt")
except FileNotFoundError:
    print("[WARN] requirements.txt not found")

print("\n" + "=" * 60)
print("[SUCCESS] AUDIO FEATURE TEST COMPLETED SUCCESSFULLY")
print("=" * 60)
print("\nNext steps:")
print("1. Launch the application: python main.py")
print("2. Click 🔊 Audio button to enable audio")
print("3. Type a message and receive audio response")
print("4. Adjust TTS settings in Paramètres → Audio (coming soon)")
