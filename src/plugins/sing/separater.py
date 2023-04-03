import os
import platform
from threading import Lock
from pathlib import Path

cuda_devices = ''


def set_separate_cuda_devices(devices: str):
    global cuda_devices
    cuda_devices = devices


def separate(song_path: Path, output_dir: Path, locker: Lock = Lock()):
    MODEL = 'hdemucs_mmi'
    STEM = song_path.stem

    vocals = output_dir / MODEL / STEM / "vocals.mp3"
    no_vocals = output_dir / MODEL / STEM / "no_vocals.mp3"
    vocals_with_stem = vocals.parent / f'{STEM}.mp3'

    if (not vocals_with_stem.exists() and not vocals_with_stem.exists()) or not no_vocals.exists():
        # 这个库没提供 APIs，暂时简单粗暴用命令行了
        cmd = ''
        if cuda_devices:
            if platform.system() == 'Windows':
                cmd = f'set CUDA_VISIBLE_DEVICES={cuda_devices} && '
            else:
                cmd = f'CUDA_VISIBLE_DEVICES={cuda_devices} '
        cmd += f'python -m demucs --two-stems=vocals --mp3 --mp3-bitrate 128 -n {MODEL} {str(song_path)} -o {output_dir}'
        with locker:
            print(cmd)
            os.system(cmd)

        if not vocals.exists() or not no_vocals.exists():
            return None

    if not vocals_with_stem.exists():
        os.rename(vocals, vocals_with_stem)

    return vocals_with_stem, no_vocals
