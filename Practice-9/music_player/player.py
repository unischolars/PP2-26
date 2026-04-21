import os
import pygame


class MusicPlayer:
    SUPPORTED_EXTENSIONS = (".mp3", ".wav", ".ogg")

    def __init__(self, music_dir: str):
        pygame.mixer.init()
        self.tracks:  list[str] = []
        self.current: int       = 0
        self.playing: bool      = False
        self._load_tracks(music_dir)

    def _load_tracks(self, music_dir: str) -> None:
        if not os.path.isdir(music_dir):
            return
        for filename in sorted(os.listdir(music_dir)):
            if filename.lower().endswith(self.SUPPORTED_EXTENSIONS):
                self.tracks.append(os.path.join(music_dir, filename))

    def play(self) -> None:
        if not self.tracks:
            return
        pygame.mixer.music.load(self.tracks[self.current])
        pygame.mixer.music.play()
        self.playing = True

    def stop(self) -> None:
        pygame.mixer.music.stop()
        self.playing = False

    def next_track(self) -> None:
        if not self.tracks:
            return
        self.current = (self.current + 1) % len(self.tracks)
        self.play()

    def prev_track(self) -> None:
        if not self.tracks:
            return
        self.current = (self.current - 1) % len(self.tracks)
        self.play()

    def update_playing_status(self) -> None:
        if self.playing and not pygame.mixer.music.get_busy():
            self.playing = False

    @property
    def current_track_name(self) -> str:
        if not self.tracks:
            return "No tracks loaded"
        return os.path.basename(self.tracks[self.current])

    @property
    def playlist_info(self) -> str:
        if not self.tracks:
            return "—"
        return f"Track {self.current + 1} / {len(self.tracks)}"

    @property
    def status_label(self) -> str:
        return "Playing" if self.playing else "Stopped"