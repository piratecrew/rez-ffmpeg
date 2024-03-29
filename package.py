name = "ffmpeg"

version = "5.1"

description = \
    """
    ffmpeg
    """

build_requires = [
    "cmake-3.15+,<4",
]

variants = [
    ["platform-linux"]
]

uuid = "repository.ffmpeg"

build_command = """
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$REZ_BUILD_INSTALL_PATH $REZ_BUILD_SOURCE_PATH;
if [[ $REZ_BUILD_INSTALL -eq 1 ]];
then
    cmake --build $REZ_BUILD_PATH
    cmake --install $REZ_BUILD_PATH
    
    cp -r $REZ_BUILD_SOURCE_PATH/cmake $REZ_BUILD_INSTALL_PATH/    
else
    echo we wont even build if you are not running install as we have several external projects that would install during buildstep;
fi
"""

def commands():
    env.PATH.prepend("{root}/bin")
    env.LD_LIBRARY_PATH.append("{root}/lib")
    if building:
        env.PKG_CONFIG_PATH.append("{root}/lib/pkgconfig")
        env.CMAKE_MODULE_PATH.append("{root}/cmake")
        env.FFMPEG_ROOT="{root}" # CMake Hint
