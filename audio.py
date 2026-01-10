"""
Audio Module - Text-to-Speech and Speech-to-Text
Enables voice interaction with the AI Agent
"""
import threading
import pyttsx3
import speech_recognition as sr
from queue import Queue


class TextToSpeech:
    """Convert text responses to speech"""
    """Convert text responses to speech

    Improvements:
    - Try to auto-select a higher-quality Windows SAPI voice (Zira/David/etc.)
    - Provide methods to list and set available voices
    - Slightly higher default rate and volume for more natural tempo
    """

    def __init__(self, rate=180, volume=1.0):
        self.engine = pyttsx3.init()
        self.is_speaking = False

        # Initialize properties
        try:
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
        except Exception:
            pass

        # Cache available voices
        try:
            self.voices = self.engine.getProperty('voices') or []
        except Exception:
            self.voices = []

        # Attempt to choose a preferred voice (Windows SAPI common names)
        preferred_keywords = [
            'Zira', 'David', 'Mark', 'Anna', 'Salli', 'Joanna', 'Alloy', 'Microsoft', 'EVA', 'Ivona'
        ]
        chosen = None
        for v in self.voices:
            name = (v.name or '') + ' ' + (v.id or '')
            for kw in preferred_keywords:
                if kw.lower() in name.lower():
                    chosen = v
                    break
            if chosen:
                break

        # As fallback, prefer any voice with 'female' or 'male' in description
        if not chosen:
            for v in self.voices:
                n = (v.name or '').lower()
                if 'female' in n or 'female' in (v.id or '').lower():
                    chosen = v
                    break

        # Apply chosen voice if found
        if chosen:
            try:
                self.engine.setProperty('voice', chosen.id)
            except Exception:
                pass
    
    def speak(self, text, on_start=None, on_end=None):
        """
        Speak text asynchronously
        
        Args:
            text (str): Text to speak
            on_start (callable): Callback when speech starts
            on_end (callable): Callback when speech ends
        """
        def speak_thread():
            try:
                self.is_speaking = True
                if on_start:
                    on_start()
                
                # Slight preprocessing to improve cadence: ensure punctuation ends sentences
                processed = text.replace('\n', '. ').strip()
                self.engine.say(processed)
                self.engine.runAndWait()
                
                if on_end:
                    on_end()
            except Exception as e:
                print(f"TTS Error: {e}")
            finally:
                self.is_speaking = False
        
        # Run in separate thread to avoid blocking
        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()
    
    def stop(self):
        """Stop current speech"""
        try:
            self.engine.stop()
            self.is_speaking = False
        except Exception as e:
            print(f"Error stopping speech: {e}")
    
    def set_rate(self, rate):
        """Set speech rate (50-300, default 150)"""
        self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume):
        """Set volume (0.0-1.0)"""
        self.engine.setProperty('volume', volume)

    def list_voices(self):
        """Return list of available voices as (index, name, id) tuples"""
        out = []
        for i, v in enumerate(self.voices):
            out.append((i, getattr(v, 'name', ''), getattr(v, 'id', '')))
        return out

    def set_voice(self, name_or_index):
        """Set voice by name substring or by index

        Args:
            name_or_index (str|int): substring to match in voice name or integer index
        Returns:
            bool: True if set, False otherwise
        """
        try:
            if isinstance(name_or_index, int):
                v = self.voices[name_or_index]
                self.engine.setProperty('voice', v.id)
                return True

            needle = str(name_or_index).lower()
            for v in self.voices:
                if needle in (v.name or '').lower() or needle in (v.id or '').lower():
                    self.engine.setProperty('voice', v.id)
                    return True
        except Exception:
            return False
        return False


class SpeechToText:
    """Convert speech to text"""
    
    def __init__(self, language='fr-FR'):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.is_listening = False
    
    def listen(self, timeout=10, callback=None):
        """
        Listen for speech input
        
        Args:
            timeout (int): Seconds to listen
            callback (callable): Function to call with recognized text
            
        Returns:
            str: Recognized text or empty string if failed
        """
        def listen_thread():
            try:
                self.is_listening = True
                print("🎤 Listening...")
                
                with sr.Microphone() as source:
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                    # Listen with timeout
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
                
                print("🔍 Processing audio...")
                
                # Try Google Speech Recognition (free API)
                try:
                    text = self.recognizer.recognize_google(audio, language=self.language)
                    print(f"✓ Recognized: {text}")
                    
                    if callback:
                        callback(text)
                    
                    return text
                
                except sr.UnknownValueError:
                    error_msg = "Could not understand audio"
                    print(f"❌ {error_msg}")
                    if callback:
                        callback(None)
                    return ""
                
                except sr.RequestError as e:
                    error_msg = f"API error: {e}"
                    print(f"❌ {error_msg}")
                    if callback:
                        callback(None)
                    return ""
            
            except sr.MicrophoneError:
                print("❌ Microphone not found or access denied")
                if callback:
                    callback(None)
                return ""
            
            except Exception as e:
                print(f"❌ Error: {e}")
                if callback:
                    callback(None)
                return ""
            
            finally:
                self.is_listening = False
        
        # Run in separate thread
        thread = threading.Thread(target=listen_thread, daemon=True)
        thread.start()
    
    def set_language(self, language):
        """
        Set language for recognition
        
        Args:
            language (str): Language code (e.g., 'fr-FR', 'en-US', 'es-ES')
        """
        self.language = language


class AudioManager:
    """Manages both TTS and STT"""
    
    def __init__(self, tts_rate=180, tts_volume=1.0, stt_language='fr-FR'):
        self.tts = TextToSpeech(rate=tts_rate, volume=tts_volume)
        self.stt = SpeechToText(language=stt_language)
        self.audio_enabled = True
    
    def speak_response(self, text, on_start=None, on_end=None):
        """Speak an AI response"""
        if self.audio_enabled:
            self.tts.speak(text, on_start=on_start, on_end=on_end)
    
    def listen_for_input(self, callback=None):
        """Listen for user speech input"""
        if self.audio_enabled and not self.stt.is_listening:
            self.stt.listen(callback=callback)
    
    def stop_speaking(self):
        """Stop current speech"""
        self.tts.stop()
    
    def toggle_audio(self):
        """Enable/disable audio"""
        self.audio_enabled = not self.audio_enabled
        return self.audio_enabled
    
    def set_tts_rate(self, rate):
        """Set TTS speech rate"""
        self.tts.set_rate(rate)
    
    def set_tts_volume(self, volume):
        """Set TTS volume"""
        self.tts.set_volume(volume)
    
    def set_stt_language(self, language):
        """Set STT language"""
        self.stt.set_language(language)

    def list_voices(self):
        """Return available TTS voices via underlying engine"""
        try:
            return self.tts.list_voices()
        except Exception:
            return []

    def set_voice(self, name_or_index):
        """Set the TTS voice by name substring or index"""
        try:
            return self.tts.set_voice(name_or_index)
        except Exception:
            return False
