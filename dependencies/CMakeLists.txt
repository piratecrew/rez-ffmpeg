# Set config wrapper variables
configure_file(configure_wrapper.in configure_wrapper @ONLY)

# Source url's
set(url_nasm https://www.nasm.us/pub/nasm/releasebuilds/${NASM_VERSION}/nasm-${NASM_VERSION}.tar.bz2)
set(url_yasm https://www.tortall.net/projects/yasm/releases/yasm-${YASM_VERSION}.tar.gz)
set(url_x264 https://code.videolan.org/videolan/x264.git)
set(url_x265 https://bitbucket.org/multicoreware/x265_git/downloads/x265_${X265_VERSION}.tar.gz)
set(url_fdk-aac https://github.com/mstorsjo/fdk-aac.git)
set(url_lame https://downloads.sourceforge.net/project/lame/lame/${LAME_VERSION}/lame-${LAME_VERSION}.tar.gz)
set(url_opus https://archive.mozilla.org/pub/opus/opus-${OPUS_VERSION}.tar.gz)
set(url_ogg http://downloads.xiph.org/releases/ogg/libogg-${OGG_VERSION}.tar.gz)
set(url_vorbis http://downloads.xiph.org/releases/vorbis/libvorbis-${VORBIS_VERSION}.tar.gz)
set(url_vpx https://chromium.googlesource.com/webm/libvpx.git)

#
# NASM
#
ExternalProject_add(
    nasm
    URL ${url_nasm}
    UPDATE_COMMAND ./autogen.sh
    CONFIGURE_COMMAND ${conf_wrapper} ./configure --prefix=${DEP_ROOT}
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${conf_wrapper} make
)

#
# YASM
#
ExternalProject_add(
    yasm
    URL ${url_yasm}
    CONFIGURE_COMMAND ${conf_wrapper} ./configure --prefix=${DEP_ROOT}
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${conf_wrapper} make
)

#
# x264
#
ExternalProject_add(
    x264
    DEPENDS nasm yasm
    GIT_REPOSITORY ${url_x264}
    GIT_SHALLOW true
    CONFIGURE_COMMAND ${conf_wrapper} ./configure --prefix=${CMAKE_INSTALL_PREFIX} --enable-pic --enable-static
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${conf_wrapper} make
)

#
# x265
#
ExternalProject_add(
    x265
    DEPENDS nasm yasm
    URL ${url_x265}
    UPDATE_COMMAND echo add_subdirectory(source) > CMakeLists.txt
    CMAKE_ARGS -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX} -DCMAKE_ASM_NASM_FLAGS=-w-macro-params-legacy -DCMAKE_PROJECT_NAME=x265 -DENABLE_SHARED:bool=off -DENABLE_PIC=ON "-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true"
    BUILD_IN_SOURCE 0
    INSTALL_COMMAND make install
)

#
# fdk-aac
#
ExternalProject_add(
    fdk-aac
    GIT_REPOSITORY ${url_fdk-aac}
    GIT_TAG v${FDK_AAC_VERSION}
    UPDATE_COMMAND autoreconf -fiv
    CONFIGURE_COMMAND ${conf_wrapper} ./configure --prefix=${CMAKE_INSTALL_PREFIX} --disable-shared
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${conf_wrapper} make
)

#
# lame
#
ExternalProject_add(
    lame
    DEPENDS nasm
    URL ${url_lame}
    CONFIGURE_COMMAND ${conf_wrapper} ./configure --prefix=${CMAKE_INSTALL_PREFIX} --disable-shared --enable-nasm
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${conf_wrapper} make
)

#
# opus
#
ExternalProject_add(
    opus
    URL ${url_opus}
    UPDATE_COMMAND autoreconf -fiv
    CONFIGURE_COMMAND ${conf_wrapper} ./configure --prefix=${CMAKE_INSTALL_PREFIX} --disable-shared
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${conf_wrapper} make
)

#
# ogg
#
ExternalProject_add(
    ogg
    URL ${url_ogg}
    CONFIGURE_COMMAND ${conf_wrapper} ./configure --prefix=${CMAKE_INSTALL_PREFIX} --disable-shared
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${conf_wrapper} make
)

#
# vorbis
#
ExternalProject_add(
    vorbis
    DEPENDS ogg
    URL ${url_vorbis}
    CONFIGURE_COMMAND ${conf_wrapper} ./configure --prefix=${CMAKE_INSTALL_PREFIX} --with-ogg=${CMAKE_INSTALL_PREFIX} --disable-shared
    INSTALL_COMMAND make install
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${conf_wrapper} make
)

#
# vpx
#
ExternalProject_add(
    vpx
    DEPENDS yasm
    GIT_REPOSITORY ${url_vpx}
    GIT_TAG v${VPX_VERSION}
    CONFIGURE_COMMAND ${conf_wrapper} ./configure --prefix=${CMAKE_INSTALL_PREFIX} --disable-shared --disable-examples --disable-unit-tests --enable-pic --enable-vp9-highbitdepth --as=yasm
    INSTALL_COMMAND make install
    BUILD_IN_SOURCE 1
    BUILD_COMMAND ${conf_wrapper} make
)
