# import required libraries
import os
import ffmpeg
from pathlib import Path
from multiprocessing import Process
from files.video import Video, DEFAULT_SCRAMBLE
from files.exceptions import VException

DEFAULT_MODE = "video"

# VEnc class
class VEnc:
    def __init__(self, input_raw, mode=DEFAULT_MODE) -> None:
        
        self.video = None   

        video_e = None

        input_video = input_raw

        if mode == "video":
            try:
                self.video = Video(input_video)
            except VException as e:
                video_e = e

        if self.video is None:
            if video_e is not None:
                raise video_e

        
        if self.video is None:
            print(f"Will not handle video")

    # Set Password
    def set_password(self, password):
        if self.video:
            self.video.set_password(password)

    # Encrption function by calling a process for multiprocessing
    def _crypt(self, crypt_mode, output, scramble, preview, per_frame, quiet):
        procs = []
        
        if self.video:
            video_crypt_fn = self.video.encrypt if crypt_mode == 0 else self.video.decrypt
            output_video = f"tmp_{output}" 
            video_crypt_fn(output_video, scramble, preview, per_frame, quiet)

        [p.join() for p in procs]

    def encrypt(self, output=None, scramble=DEFAULT_SCRAMBLE, preview=False, per_frame=False, quiet=False):
        self._crypt(0, output, scramble, preview, per_frame, quiet)

    def decrypt(self, output=None, scramble=DEFAULT_SCRAMBLE, preview=False, per_frame=False, quiet=False):
        self._crypt(1, output, scramble, preview, per_frame, quiet)
