name = "ffmpeg"

version = "2.8.4"

description = \
    """
    ffmpeg
    """

variants = [
    ["platform-linux"]
]

uuid = "repository.ffmpeg"

def commands():
    env.CMAKE_MODULE_PATH.append("{root}/cmake")
    env.LD_LIBRARY_PATH.append("{root}/lib")
