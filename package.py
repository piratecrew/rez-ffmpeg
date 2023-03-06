name = "ffmpeg"

version = "5.1"

description = \
    """
    ffmpeg
    """

variants = [
    ["platform-linux"]
]

uuid = "repository.ffmpeg"

build_command = """
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$REZ_BUILD_INSTALL_PATH $REZ_BUILD_SOURCE_PATH;
if [[ $REZ_BUILD_INSTALL -eq 1 ]];
then
    cmake --build $REZ_BUILD_PATH -j11
    cmake --install $REZ_BUILD_PATH -j11
else
    echo we wont even build if you are not running install as we have several external projects that would install during buildstep;
fi
"""

def commands():
    env.CMAKE_MODULE_PATH.append("{root}/cmake")
    env.PATH.prepend("{root}/bin")
    env.LD_LIBRARY_PATH.append("{root}/lib")
