CMAKE_MINIMUM_REQUIRED(VERSION 3.6)
PROJECT(ffmpeg)
#include(RezBuild)
include(ExternalProject)
set(NASM_VERSION 2.15.05 CACHE STRING "nasm version")
set(YASM_VERSION 1.3.0 CACHE STRING "yasm version")
set(X264_VERSION stable CACHE STRING "x264 version")
set(X265_VERSION 3.5 CACHE STRING "x265 version")
set(FDK_AAC_VERSION 2.0.2 CACHE STRING "fdk aac version")
set(LAME_VERSION 3.100 CACHE STRING "lame version")
set(OPUS_VERSION 1.3.1 CACHE STRING "opus version")
set(OGG_VERSION 1.3.2 CACHE STRING "ogg version")
set(VORBIS_VERSION 1.3.4 CACHE STRING "vorbis version")
set(VPX_VERSION 1.12.0 CACHE STRING "vpx version")
set(FFMPEG_VERSION 5.1 CACHE STRING "ffmpeg version")

set(url_ffmpeg https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2)

#set(make_args -j$ENV{REZ_BUILD_THREAD_COUNT})

if(${REZ_BUILD_INSTALL})
    set(install_cmd make install ${make_args})
else()
    set(install_cmd "")
endif()

# Create a wrapper script for configure commands
set(DEP_ROOT ${PROJECT_BINARY_DIR}/DEPENDENCIES_PREFIX)
set(PKG_CONFIG_PATH "$ENV{PACKAGE_CONFIG_PATH}:${DEP_ROOT}/lib/pkgconfig:${CMAKE_INSTALL_PREFIX}/lib/pkgconfig")
set(PATH "${DEP_ROOT}/bin:${CMAKE_INSTALL_PREFIX}/bin:$ENV{PATH}")
configure_file(dependencies/configure_wrapper.in configure_wrapper @ONLY)
set(conf_wrapper ${PROJECT_BINARY_DIR}/configure_wrapper)

add_subdirectory(dependencies)

ExternalProject_add(
    ffmpeg
    DEPENDS nasm yasm x264 x265 fdk-aac lame opus ogg vorbis vpx
    URL ${url_ffmpeg}
    PREFIX ffmpeg
    UPDATE_COMMAND ""
    CONFIGURE_COMMAND ${conf_wrapper} ./configure --prefix=${CMAKE_INSTALL_PREFIX} --pkg-config-flags=--static --enable-shared --disable-static --enable-pic --extra-libs=-lpthread --extra-libs=-lm --enable-gpl --enable-libfdk_aac --enable-libfreetype --enable-libx264 --enable-libx265 --enable-shared --enable-nonfree --enable-libmp3lame --enable-libopus --enable-libvpx
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${conf_wrapper} make
)

# rez_install_files(
#     cmake/ffmpeg.cmake
#     DESTINATION .
# )

if(${REZ_BUILD_INSTALL})
  install (SCRIPT "${CMAKE_SOURCE_DIR}/dependencies/PostInstall.cmake")
endif()
