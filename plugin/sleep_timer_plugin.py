# Jellyfin Sleep Timer Plugin
# This script extends Jellyfin with a sleep timer accessible directly in the video player settings.
# It is intended for educational purposes and assumes familiarity with Jellyfin's plugin development.

import time
import threading
from jellyfin_api import Jellyfin

class SleepTimerPlugin:
    def __init__(self, jellyfin_url, api_key):
        self.jellyfin = Jellyfin(jellyfin_url, api_key)
        self.timer_thread = None

    def start_timer(self, duration_minutes):
        """
        Start the sleep timer.

        :param duration_minutes: The time in minutes before stopping playback.
        """
        duration_seconds = duration_minutes * 60

        if self.timer_thread and self.timer_thread.is_alive():
            print("A timer is already running. Please stop it first.")
            return

        self.timer_thread = threading.Thread(target=self._stop_playback_after_delay, args=(duration_seconds,))
        self.timer_thread.daemon = True
        self.timer_thread.start()
        print(f"Sleep timer started for {duration_minutes} minutes.")

    def stop_timer(self):
        """
        Stop the sleep timer if it is running.
        """
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread = None
            print("Sleep timer stopped.")
        else:
            print("No sleep timer is currently running.")

    def _stop_playback_after_delay(self, duration_seconds):
        time.sleep(duration_seconds)
        if self.timer_thread:
            self._stop_playback()

    def _stop_playback(self):
        """
        Stop all active playback sessions on the Jellyfin server.
        """
        sessions = self.jellyfin.get_sessions()
        for session in sessions:
            if session.get("NowPlayingItem"):
                session_id = session.get("Id")
                self.jellyfin.stop_playback(session_id)
                print(f"Playback stopped for session {session_id}.")

if __name__ == "__main__":
    # Replace with your Jellyfin server details
    JELLYFIN_URL = "http://your-jellyfin-server"
    API_KEY = "your-api-key"

    # Initialize plugin (to be extended for Jellyfin video player integration)
    plugin = SleepTimerPlugin(JELLYFIN_URL, API_KEY)

    # Example code to integrate with Jellyfin player settings
    # This would add an interface in the player for setting a sleep timer
    def add_to_player_settings():
        """Add sleep timer controls to the video player UI."""
        print("Integrate with Jellyfin video player settings...")
        # Extend Jellyfin plugin system to include this feature.
        # Example UI logic would go here.

    # Start the plugin integration
    add_to_player_settings()
