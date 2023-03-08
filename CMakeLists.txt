CMAKE_MINIMUM_REQUIRED(VERSION 3.6)
PROJECT(ffmpeg)

include(ExternalProject)

set(nasm_version 2.15.05 CACHE STRING "nasm version")
set(nasm_url https://www.nasm.us/pub/nasm/releasebuilds/${nasm_version}/nasm-${nasm_version}.tar.bz2)

set(yasm_version 1.3.0 CACHE STRING "yasm version")
set(yasm_url https://www.tortall.net/projects/yasm/releases/yasm-${yasm_version}.tar.gz)

set(x264_version stable CACHE STRING "x264 version")
set(x264_url https://code.videolan.org/videolan/x264.git)

set(x265_version 3.5 CACHE STRING "x265 version")
set(x265_url https://bitbucket.org/multicoreware/x265_git/downloads/x265_${x265_version}.tar.gz)

set(fdk_aac_version 2.0.2 CACHE STRING "fdk aac version")
set(fdk_aac_url https://github.com/mstorsjo/fdk-aac.git)

set(lame_version 3.100 CACHE STRING "lame version")
set(lame_url https://downloads.sourceforge.net/project/lame/lame/${lame_version}/lame-${lame_version}.tar.gz)

set(opus_version 1.3.1 CACHE STRING "opus version")
set(opus_url https://archive.mozilla.org/pub/opus/opus-${opus_version}.tar.gz)

set(vpx_version 1.12.0 CACHE STRING "vpx version")
set(vpx_url https://chromium.googlesource.com/webm/libvpx.git)

set(ogg_version 1.3.2 CACHE STRING "ogg version")
set(ogg_url http://downloads.xiph.org/releases/ogg/libogg-${ogg_version}.tar.gz)

set(vorbis_version 1.3.4 CACHE STRING "vorbis version")
set(vorbis_url http://downloads.xiph.org/releases/vorbis/libvorbis-${vorbis_version}.tar.gz)

set(FFMPEG_VERSION 5.1 CACHE STRING "ffmpeg version")
set(url_ffmpeg https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2)

# Create a wrapper script for configure commands.
# - Need to update PATH since we are building executables into non-standard locations, 
#   i.e. the build folder. The same is true for the PKG_CONFIG_PATH.
# - Need to enable fPIC since we are linking static libs. Not all dependencies allow
#   this to be configured. Thus, we must setup these flags as part of the environment
#   we build in.
#
# NOTE(tohi): There is an over-use of our custom environment in the configure/build
#             steps below. The reason for this is that the environment is only required
#             in some cases, but it is hard to know exactly which ones these are. 
#             Additionally, not all parts of the environment are needed in all cases. 
#             As such, a simple way to cover all bases is to always use everything and
#             hope that this doesn't break anything. 
set(deps_prefix ${CMAKE_CURRENT_BINARY_DIR}/ffmpeg_build)
set(deps_bindir ${CMAKE_CURRENT_BINARY_DIR}/bin)

set(NEW_PKG_CONFIG_PATH "$ENV{PKG_CONFIG_PATH}:${deps_prefix}/lib/pkgconfig")
set(NEW_PATH "${deps_bindir}:$ENV{PATH}")
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/set_env.in 
    ${CMAKE_CURRENT_BINARY_DIR}/tmp/set_env 
    @ONLY
)
# Copy the configured shell script to the build folder while explicitly setting file
# permissions.
file(
    COPY ${CMAKE_CURRENT_BINARY_DIR}/tmp/set_env
    DESTINATION ${CMAKE_CURRENT_BINARY_DIR}
    FILE_PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
)
set(set_env ${CMAKE_CURRENT_BINARY_DIR}/set_env)

#
# Build dependencies.
# These steps are taken mostly from:
#
# https://trac.ffmpeg.org/wiki/CompilationGuide/Centos
#
# with a few modifications in some places. 

#
# NASM
#
ExternalProject_add(nasm
    URL ${nasm_url}
    UPDATE_COMMAND ./autogen.sh
    CONFIGURE_COMMAND ./configure --prefix=${deps_prefix} --bindir=${deps_bindir}
    BUILD_IN_SOURCE 1
    BUILD_COMMAND make
    INSTALL_COMMAND make install
    #LOG_BUILD 1
)

#
# YASM
#
ExternalProject_add(yasm
    URL ${yasm_url}
    CONFIGURE_COMMAND ./configure --prefix=${deps_prefix} --bindir=${deps_bindir}
    BUILD_IN_SOURCE 1
    BUILD_COMMAND make
    INSTALL_COMMAND make install
    #LOG_BUILD 1
)

#
# x264
#
ExternalProject_add(x264
    DEPENDS nasm yasm
    GIT_REPOSITORY ${x264_url}
    GIT_TAG ${x264_version}
    GIT_SHALLOW 1
    CONFIGURE_COMMAND 
        ${set_env} 
        ./configure 
        "--prefix=${deps_prefix}" 
        "--bindir=${deps_bindir}" 
        "--enable-static" 
        "--enable-pic"
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${set_env} make
    INSTALL_COMMAND make install
    #LOG_CONFIGURE 1
    #LOG_BUILD 1
)

#
# x265
#
set(x265_cmake_args 
    "-G" "Unix Makefiles"
    "-DCMAKE_PROJECT_NAME:string=x265"
    "-DCMAKE_INSTALL_PREFIX=${deps_prefix}"
    "-DCMAKE_RUNTIME_OUTPUT_DIRECTORY=${deps_bindir}"
    "-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON"
    "-DCMAKE_ASM_NASM_FLAGS=-w-macro-params-legacy"
    "-DNASM_ROOT:string=${deps_bindir}"
    "-DENABLE_SHARED:bool=OFF"
    "-DENABLE_PIC:bool=ON"
    "../../src/x265/source"
)
ExternalProject_add(x265
    DEPENDS nasm yasm
    URL ${x265_url}
    CMAKE_ARGS ${x265_cmake_args}
    BUILD_IN_SOURCE 0
    BUILD_COMMAND ${set_env} make
    INSTALL_COMMAND make install
    #LOG_CONFIGURE 1
    #LOG_BUILD 1
)
unset(x265_cmake_args)

#
# fdk-aac
#
ExternalProject_add(fdk-aac
    GIT_REPOSITORY ${fdk_aac_url}
    GIT_TAG v${fdk_aac_version}
    GIT_SHALLOW 1
    UPDATE_COMMAND autoreconf -fiv
    CONFIGURE_COMMAND 
        ${set_env}  
        ./configure 
        "--prefix=${deps_prefix}"
        "--disable-shared"
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${set_env} make 
    INSTALL_COMMAND make install
)

#
# lame
#
ExternalProject_add(lame
    DEPENDS nasm
    URL ${lame_url}
    CONFIGURE_COMMAND 
        ${set_env} 
        ./configure 
        "--prefix=${deps_prefix}"
        "--bindir=${deps_bindir}" 
        "--disable-shared" 
        "--enable-nasm"
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${set_env} make 
    INSTALL_COMMAND make install
)

#
# opus
#
ExternalProject_add(opus
    URL ${opus_url}
    #UPDATE_COMMAND autoreconf -fiv
    CONFIGURE_COMMAND 
        ${set_env}  
        ./configure 
        "--prefix=${deps_prefix}"
        "--disable-shared"
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${set_env} make
    INSTALL_COMMAND make install
)

#
# vpx
#
ExternalProject_add(vpx
    DEPENDS yasm
    GIT_REPOSITORY ${vpx_url}
    GIT_TAG v${vpx_version}
    GIT_SHALLOW 1
    CONFIGURE_COMMAND 
        ${set_env}  
        ./configure 
        "--prefix=${deps_prefix}" 
        "--disable-examples" 
        "--disable-unit-tests" 
        "--disable-shared"
        "--enable-vp9-highbitdepth"
        "--as=yasm"
        "--enable-pic" 
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${set_env} make
    INSTALL_COMMAND make install
)

#
# ogg
#
ExternalProject_add(ogg
    URL ${ogg_url}
    CONFIGURE_COMMAND 
        ${set_env}  
        ./configure 
        "--prefix=${deps_prefix}"
        "--disable-shared"
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${set_env} make
    INSTALL_COMMAND make install
)

#
# vorbis
#
set(url_vorbis http://downloads.xiph.org/releases/vorbis/libvorbis-${VORBIS_VERSION}.tar.gz)
ExternalProject_add(vorbis
    DEPENDS ogg
    URL ${vorbis_url}
    CONFIGURE_COMMAND 
        ${set_env}  
        ./configure 
        "--prefix=${deps_prefix}" 
        "--with-ogg=${deps_prefix}" 
        "--disable-shared"
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${set_env} make
    INSTALL_COMMAND make install
)

# NOTE(tohi): The freetype development libraries can be installed on Rocky Linux with:
#   sudo dnf install freetype-devel

ExternalProject_add(ffmpeg
    DEPENDS nasm yasm x264 x265 fdk-aac lame opus vpx ogg vorbis
    URL ${url_ffmpeg}
    PREFIX ffmpeg
    UPDATE_COMMAND ""
    CONFIGURE_COMMAND                             
        ${set_env} 
        ./configure                               
        "--prefix=${CMAKE_INSTALL_PREFIX}"
        "--pkg-config-flags=--static"
        "--extra-cflags=-I${deps_prefix}/include" 
        "--extra-ldflags=-L${deps_prefix}/lib"        
        "--extra-libs=-lpthread"
        "--extra-libs=-lm"
        "--bindir=${CMAKE_INSTALL_PREFIX}/bin"
        "--enable-gpl"                              
        "--enable-libfdk_aac"                       
        "--enable-libfreetype"                      
        "--enable-libmp3lame"                       
        "--enable-libopus"                          
        "--enable-libvpx"                           
        "--enable-libx264"                             
        "--enable-libx265"                          
        "--enable-nonfree"
        "--enable-shared"                           
        "--disable-static"                          
        "--enable-pic"                              
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${set_env} make
    INSTALL_COMMAND make install
)
