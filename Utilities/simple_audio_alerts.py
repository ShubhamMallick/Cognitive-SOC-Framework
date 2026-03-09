"""
Enhanced Audio Alert System - SOC Framework
Supports text-to-speech, sound files, sirens, and combined alerts
"""

import os
import threading
import time
from typing import Dict, Optional, List
import pyttsx3
from playsound import playsound
import queue

class EnhancedAudioAlerts:
    """
    Enhanced Audio Alert Intelligence System
    Fixed threading issues with proper TTS engine management
    """

    def __init__(self, sound_directory: str = "static/sounds/"):
        """
        Initialize enhanced audio alert system with proper threading
        """
        self.sound_dir = sound_directory
        self.is_playing = False
        self.alert_queue = queue.Queue()

        # TTS Engine with proper management
        self.tts_lock = threading.Lock()
        self.tts_engine = None
        self.tts_available = False
        self._init_tts_engine()

        # Sound File Mappings (enhanced)
        self.sound_files = {
            # Sirens and Emergency Sounds
            "CRITICAL_SIREN": "critical_siren.wav",
            "HIGH_ALERT_SIREN": "high_alert_siren.wav",
            "EMERGENCY_SIREN": "emergency_siren.wav",

            # Alert Noises
            "WARNING_BEEP": "warning_beep.wav",
            "ATTENTION_CHIME": "attention_chime.wav",
            "NOTIFICATION_PING": "notification_ping.wav",
            "SUCCESS_CHIME": "success_chime.wav",

            # Combined Alert Packs
            "CRITICAL_PACK": ["critical_siren.wav", "warning_beep.wav"],
            "HIGH_PACK": ["high_alert_siren.wav", "attention_chime.wav"],
            "MEDIUM_PACK": ["warning_beep.wav", "notification_ping.wav"],
            "LOW_PACK": ["notification_ping.wav"],
            "SUCCESS_PACK": ["success_chime.wav"]
        }

        # Alert Type Configurations
        self.alert_types = {
            "CRITICAL": {
                "speech": True,
                "sound": "CRITICAL_PACK",
                "priority": "HIGHEST",
                "blocking": True,
                "repeat": 2
            },
            "HIGH": {
                "speech": True,
                "sound": "HIGH_PACK",
                "priority": "HIGH",
                "blocking": False,
                "repeat": 1
            },
            "MEDIUM": {
                "speech": True,
                "sound": "MEDIUM_PACK",
                "priority": "MEDIUM",
                "blocking": False,
                "repeat": 1
            },
            "LOW": {
                "speech": False,
                "sound": "LOW_PACK",
                "priority": "LOW",
                "blocking": False,
                "repeat": 1
            },
            "SUCCESS": {
                "speech": True,
                "sound": "SUCCESS_PACK",
                "priority": "LOW",
                "blocking": False,
                "repeat": 1
            }
        }

    def _init_tts_engine(self):
        """Safely initialize TTS engine with proper error handling"""
        try:
            with self.tts_lock:
                if self.tts_engine is None:
                    self.tts_engine = pyttsx3.init()
                    # Configure voice settings
                    voices = self.tts_engine.getProperty('voices')
                    self.tts_engine.setProperty('rate', 180)  # Speed of speech
                    self.tts_engine.setProperty('volume', 0.8)  # Volume level
                    if voices:
                        self.tts_engine.setProperty('voice', voices[0].id)
                    self.tts_available = True
        except Exception as e:
            print(f"TTS initialization failed: {e}")
            self.tts_available = False

    def speak_alert(self, message: str, blocking: bool = False) -> bool:
        """
        Speak an alert message using TTS

        Args:
            message: Text to speak
            blocking: Whether to wait for speech to complete

        Returns:
            bool: Success status
        """
        if not self.tts_available:
            print("TTS not available, cannot speak alert")
            return False

        try:
            if blocking:
                # Blocking speech
                with self.tts_lock:
                    self.tts_engine.say(message)
                    self.tts_engine.runAndWait()
                return True
            else:
                # Non-blocking speech in background thread
                thread = threading.Thread(target=self._speak_thread, args=(message,))
                thread.daemon = True
                thread.start()
                return True

        except Exception as e:
            print(f"Speech failed: {e}")
            return False

    def _speak_thread(self, message: str):
        """Background thread for non-blocking speech"""
        try:
            with self.tts_lock:
                self.tts_engine.say(message)
                self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Background speech error: {e}")

    def play_sound_file(self, sound_key: str, blocking: bool = False) -> bool:
        """
        Play a sound file by key

        Args:
            sound_key: Key from sound_files mapping
            blocking: Whether to wait for sound to complete

        Returns:
            bool: Success status
        """
        try:
            sound_file = self.sound_files.get(sound_key)
            if not sound_file:
                print(f"Sound key not found: {sound_key}")
                return False

            # Handle single files
            if isinstance(sound_file, str):
                full_path = os.path.join(self.sound_dir, sound_file)
                if not os.path.exists(full_path):
                    print(f"Sound file not found: {full_path}")
                    return False

                if blocking:
                    playsound(full_path)
                else:
                    thread = threading.Thread(target=playsound, args=(full_path,))
                    thread.daemon = True
                    thread.start()
                return True

            # Handle sound packs (multiple files)
            elif isinstance(sound_file, list):
                if blocking:
                    for sf in sound_file:
                        full_path = os.path.join(self.sound_dir, sf)
                        if os.path.exists(full_path):
                            playsound(full_path)
                            time.sleep(0.2)  # Small gap between sounds
                else:
                    thread = threading.Thread(target=self._play_sound_pack, args=(sound_file,))
                    thread.daemon = True
                    thread.start()
                return True

        except Exception as e:
            print(f"Sound playback failed: {e}")
            return False

    def _play_sound_pack(self, sound_files: List[str]):
        """Play a pack of sound files sequentially"""
        try:
            for sf in sound_files:
                full_path = os.path.join(self.sound_dir, sf)
                if os.path.exists(full_path):
                    playsound(full_path)
                    time.sleep(0.2)  # Gap between sounds
        except Exception as e:
            print(f"Sound pack playback error: {e}")

    def play_combined_alert(self, severity: str, message: str = None, blocking: bool = None) -> bool:
        """
        Play combined speech + sound alert PARALLELY (simultaneously)
        Both sound and speech start at the same time for maximum impact
        """
        try:
            alert_config = self.alert_types.get(severity, self.alert_types["LOW"])

            # Determine blocking behavior
            if blocking is None:
                blocking = alert_config["blocking"]

            success = True

            # Create threads for parallel execution
            sound_thread = None
            speech_thread = None

            # Start sound playback thread (if configured)
            if alert_config.get("sound"):
                sound_thread = threading.Thread(
                    target=self.play_sound_file,
                    args=(alert_config["sound"], False),
                    daemon=True
                )
                sound_thread.start()

            # Start speech thread (if configured and available)
            if alert_config.get("speech", False) and message and self.tts_available:
                speech_thread = threading.Thread(
                    target=self.speak_alert,
                    args=(message, False),
                    daemon=True
                )
                speech_thread.start()

            # For blocking alerts, wait for completion
            if blocking:
                if sound_thread:
                    sound_thread.join()  # Wait for sound to complete
                if speech_thread:
                    speech_thread.join()  # Wait for speech to complete
            else:
                # For non-blocking alerts, let them run in background
                # Don't wait, just return success
                pass

            # Handle repeats for critical alerts (sequential repeats)
            repeat_count = alert_config.get("repeat", 1)
            if repeat_count > 1 and success:
                for i in range(repeat_count - 1):
                    time.sleep(2.0)  # Wait between repeats
                    if alert_config.get("sound"):
                        # Play sound again (non-blocking)
                        repeat_thread = threading.Thread(
                            target=self.play_sound_file,
                            args=(alert_config["sound"], False),
                            daemon=True
                        )
                        repeat_thread.start()

            return success

        except Exception as e:
            print(f"Combined alert failed: {e}")
            return False

    def _delayed_speech(self, message: str, delay: float):
        """Speak message after delay"""
        time.sleep(delay)
        self.speak_alert(message, blocking=False)

    def alert_pipeline_complete(self, final_decision: str, confidence: float = None) -> bool:
        """
        Enhanced alert for pipeline completion with speech + sound
        """
        # Generate message
        if final_decision == "EXECUTE_AUTOMATED_CONTAINMENT":
            message = "Alert: Automated containment initiated. Security threat contained."
            severity = "CRITICAL"
        elif final_decision == "HUMAN_ANALYST_REVIEW":
            message = "Alert: Incident requires human analyst review. Please investigate immediately."
            severity = "HIGH"
        elif final_decision == "ADAPTIVE_MONITORING_MODE":
            message = "Alert: Adaptive monitoring activated. System under enhanced surveillance."
            severity = "MEDIUM"
        else:  # SAFE_PASS
            message = "System status: Normal operation. No security threats detected."
            severity = "SUCCESS"

        # Add confidence level if available
        if confidence is not None:
            confidence_text = f"{confidence:.2f}"
            message = f"{message} Confidence level: {confidence_text}"

        return self.play_combined_alert(severity, message)

    def alert_high_priority_threat(self, threat_type: str = "unknown") -> bool:
        """Speak high-priority threat alert"""
        message = f"High priority security threat detected. Threat type: {threat_type}. Immediate attention required."
        return self.speak_alert(message, blocking=False)

    def alert_system_status(self, status: str) -> bool:
        """Speak system status updates"""
        status_messages = {
            "starting": "Security analysis system starting",
            "running": "Security analysis in progress",
            "completed": "Security analysis completed successfully",
            "error": "Security analysis encountered an error",
            "maintenance": "System entering maintenance mode"
        }

        message = status_messages.get(status, f"System status: {status}")
        return self.speak_alert(message, blocking=False)

    def get_status(self) -> Dict:
        """Get system status"""
        return {
            "tts_initialized": self.tts_available,
            "engine_available": self.tts_engine is not None,
            "voice_rate": self.tts_engine.getProperty('rate') if self.tts_available else None,
            "voice_volume": self.tts_engine.getProperty('volume') if self.tts_available else None
        }


# Global instance for easy access
audio_alerts = EnhancedAudioAlerts()
