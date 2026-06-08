cmake_minimum_required(VERSION 3.17)
project(Pillow LANGUAGES C)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)

# ── Feature options (injected by Conan via CMakeToolchain, or set manually) ──
option(PILLOW_WITH_JPEG       "Enable JPEG support"             ON)
option(PILLOW_WITH_ZLIB       "Enable zlib (PNG/ZIP) support"   ON)
option(PILLOW_WITH_PNG        "Enable PNG support"              ON)
option(PILLOW_WITH_TIFF       "Enable TIFF support"             ON)
option(PILLOW_WITH_JPEG2000   "Enable JPEG 2000 support"        ON)
option(PILLOW_WITH_FREETYPE   "Enable FreeType2 support"        ON)
option(PILLOW_WITH_RAQM       "Enable Raqm text shaping"        ON)
option(PILLOW_WITH_LCMS       "Enable LittleCMS2 support"       ON)
option(PILLOW_WITH_WEBP       "Enable WebP support"             ON)
option(PILLOW_WITH_AVIF       "Enable AVIF support"             ON)
option(PILLOW_WITH_IMAGEQUANT "Enable libimagequant support"    OFF)
option(PILLOW_WITH_TK         "Enable Tk integration"           OFF)
option(PILLOW_WITH_XCB        "Enable XCB clipboard (Linux)"    OFF)

# ── Find packages provided by Conan ──────────────────────────────────────────
# Target names come from the CMakeDeps generator; verify against your CCI recipe
# versions if find_package fails.
if(PILLOW_WITH_JPEG)
    find_package(JPEG REQUIRED)           # libjpeg -> JPEG::JPEG
endif()
if(PILLOW_WITH_ZLIB)
    find_package(ZLIB REQUIRED)           # zlib -> ZLIB::ZLIB
endif()
if(PILLOW_WITH_PNG)
    find_package(PNG REQUIRED)            # libpng -> PNG::PNG
endif()
if(PILLOW_WITH_TIFF)
    find_package(TIFF REQUIRED)           # libtiff -> TIFF::TIFF
endif()
if(PILLOW_WITH_JPEG2000)
    find_package(OpenJPEG REQUIRED)       # openjpeg -> OpenJPEG::OpenJPEG
endif()
if(PILLOW_WITH_FREETYPE)
    find_package(freetype REQUIRED)       # freetype -> Freetype::Freetype
endif()
if(PILLOW_WITH_RAQM)
    find_package(harfbuzz REQUIRED)       # harfbuzz -> harfbuzz::harfbuzz
    find_package(fribidi REQUIRED)        # fribidi -> fribidi::fribidi
endif()
if(PILLOW_WITH_LCMS)
    find_package(lcms REQUIRED)           # lcms -> lcms::lcms
endif()
if(PILLOW_WITH_WEBP)
    find_package(WebP REQUIRED)           # libwebp -> WebP::webp WebP::webpmux WebP::webpdemux
endif()
if(PILLOW_WITH_AVIF)
    find_package(libavif REQUIRED)        # libavif -> avif (no namespace)
endif()
if(PILLOW_WITH_IMAGEQUANT)
    find_package(libimagequant REQUIRED)  # libimagequant -> libimagequant::libimagequant
endif()
if(PILLOW_WITH_TK)
    find_package(tcl REQUIRED)            # tcl -> tcl::tcl
    find_package(tk REQUIRED)             # tk -> tk::tk
endif()
if(PILLOW_WITH_XCB)
    find_package(libxcb REQUIRED)         # libxcb -> libxcb::libxcb
endif()

# ── Pillow version (propagated as compile definition to _imaging) ─────────────
file(READ "${CMAKE_SOURCE_DIR}/src/PIL/_version.py" _ver_content)
string(REGEX MATCH "\"([^\"]+)\"" _ "${_ver_content}")
set(PILLOW_VERSION "${CMAKE_MATCH_1}")
message(STATUS "Pillow ${PILLOW_VERSION}")

# ── Endianness ────────────────────────────────────────────────────────────────
include(TestBigEndian)
test_big_endian(WORDS_BIGENDIAN)

# ── Core libImaging object library ───────────────────────────────────────────
# Built as OBJECT so it can be linked directly into _imaging without a
# separate shared library install step.
add_library(libImaging OBJECT
    src/libImaging/Access.c
    src/libImaging/AlphaComposite.c
    src/libImaging/Arrow.c
    src/libImaging/Bands.c
    src/libImaging/BcnDecode.c
    src/libImaging/BcnEncode.c
    src/libImaging/BitDecode.c
    src/libImaging/Blend.c
    src/libImaging/BoxBlur.c
    src/libImaging/Chops.c
    src/libImaging/codec_fd.c
    src/libImaging/ColorLUT.c
    src/libImaging/Convert.c
    src/libImaging/ConvertYCbCr.c
    src/libImaging/Copy.c
    src/libImaging/Crop.c
    src/libImaging/Dib.c
    src/libImaging/Draw.c
    src/libImaging/Effects.c
    src/libImaging/EpsEncode.c
    src/libImaging/Fill.c
    src/libImaging/Filter.c
    src/libImaging/FliDecode.c
    src/libImaging/Geometry.c
    src/libImaging/GetBBox.c
    src/libImaging/GifDecode.c
    src/libImaging/GifEncode.c
    src/libImaging/HexDecode.c
    src/libImaging/Histo.c
    src/libImaging/Jpeg2KDecode.c
    src/libImaging/Jpeg2KEncode.c
    src/libImaging/JpegDecode.c
    src/libImaging/JpegEncode.c
    src/libImaging/Matrix.c
    src/libImaging/Mode.c
    src/libImaging/ModeFilter.c
    src/libImaging/Negative.c
    src/libImaging/Offset.c
    src/libImaging/Pack.c
    src/libImaging/PackDecode.c
    src/libImaging/Palette.c
    src/libImaging/Paste.c
    src/libImaging/PcdDecode.c
    src/libImaging/PcxDecode.c
    src/libImaging/PcxEncode.c
    src/libImaging/Point.c
    src/libImaging/Quant.c
    src/libImaging/QuantHash.c
    src/libImaging/QuantHeap.c
    src/libImaging/QuantOctree.c
    src/libImaging/QuantPngQuant.c
    src/libImaging/RankFilter.c
    src/libImaging/RawDecode.c
    src/libImaging/RawEncode.c
    src/libImaging/Reduce.c
    src/libImaging/Resample.c
    src/libImaging/SgiRleDecode.c
    src/libImaging/Storage.c
    src/libImaging/SunRleDecode.c
    src/libImaging/TgaRleDecode.c
    src/libImaging/TgaRleEncode.c
    src/libImaging/TiffDecode.c
    src/libImaging/Unpack.c
    src/libImaging/UnpackYCC.c
    src/libImaging/UnsharpMask.c
    src/libImaging/XbmDecode.c
    src/libImaging/XbmEncode.c
    src/libImaging/ZipDecode.c
    src/libImaging/ZipEncode.c
)
target_include_directories(libImaging PUBLIC src src/libImaging)
target_link_libraries(libImaging PRIVATE Python3::Module)
set_property(TARGET libImaging PROPERTY POSITION_INDEPENDENT_CODE ON)

# libImaging sources are feature-guarded with HAVE_* and need the same include dirs
# as _imaging. Link each dep PRIVATE so CMake propagates headers without re-linking.
target_compile_definitions(libImaging PRIVATE PILLOW_VERSION="${PILLOW_VERSION}")
if(WORDS_BIGENDIAN)
    target_compile_definitions(libImaging PRIVATE WORDS_BIGENDIAN)
endif()
if(PILLOW_WITH_JPEG)
    target_compile_definitions(libImaging PRIVATE HAVE_LIBJPEG)
    target_link_libraries(libImaging PRIVATE JPEG::JPEG)
endif()
if(PILLOW_WITH_ZLIB)
    target_compile_definitions(libImaging PRIVATE HAVE_LIBZ)
    target_link_libraries(libImaging PRIVATE ZLIB::ZLIB)
endif()
if(PILLOW_WITH_PNG)
    target_link_libraries(libImaging PRIVATE PNG::PNG)
endif()
if(PILLOW_WITH_TIFF)
    target_compile_definitions(libImaging PRIVATE HAVE_LIBTIFF)
    target_link_libraries(libImaging PRIVATE TIFF::TIFF)
    if(WIN32)
        target_compile_definitions(libImaging PRIVATE USE_WIN32_FILEIO)
    endif()
endif()
if(PILLOW_WITH_JPEG2000)
    target_compile_definitions(libImaging PRIVATE HAVE_OPENJPEG)
    target_link_libraries(libImaging PRIVATE openjp2)
    if(WIN32 AND NOT MINGW)
        target_compile_definitions(libImaging PRIVATE OPJ_STATIC)
    endif()
endif()
if(PILLOW_WITH_IMAGEQUANT)
    target_compile_definitions(libImaging PRIVATE HAVE_LIBIMAGEQUANT)
    target_link_libraries(libImaging PRIVATE libimagequant::libimagequant)
endif()
if(PILLOW_WITH_XCB)
    target_compile_definitions(libImaging PRIVATE HAVE_XCB)
    target_link_libraries(libImaging PRIVATE libxcb::libxcb)
endif()

# ── PIL._imaging (core extension) ────────────────────────────────────────────
Python3_add_library(_imaging MODULE
    src/_imaging.c
    src/decode.c
    src/display.c
    src/encode.c
    src/map.c
    src/outline.c
    src/path.c
    $<TARGET_OBJECTS:libImaging>
)
target_include_directories(_imaging PRIVATE src src/libImaging)
target_compile_definitions(_imaging PRIVATE PILLOW_VERSION="${PILLOW_VERSION}")

if(WORDS_BIGENDIAN)
    target_compile_definitions(_imaging PRIVATE WORDS_BIGENDIAN)
endif()

if(PILLOW_WITH_JPEG)
    target_compile_definitions(_imaging PRIVATE HAVE_LIBJPEG)
    target_link_libraries(_imaging PRIVATE JPEG::JPEG)
endif()
if(PILLOW_WITH_ZLIB)
    target_compile_definitions(_imaging PRIVATE HAVE_LIBZ)
    target_link_libraries(_imaging PRIVATE ZLIB::ZLIB)
endif()
if(PILLOW_WITH_TIFF)
    target_compile_definitions(_imaging PRIVATE HAVE_LIBTIFF)
    target_link_libraries(_imaging PRIVATE TIFF::TIFF)
    if(WIN32)
        target_compile_definitions(_imaging PRIVATE USE_WIN32_FILEIO)
    endif()
endif()
if(PILLOW_WITH_JPEG2000)
    target_compile_definitions(_imaging PRIVATE HAVE_OPENJPEG)
    target_link_libraries(_imaging PRIVATE openjp2)
    if(WIN32 AND NOT MINGW)
        target_compile_definitions(_imaging PRIVATE OPJ_STATIC)
    endif()
endif()
if(PILLOW_WITH_IMAGEQUANT)
    target_compile_definitions(_imaging PRIVATE HAVE_LIBIMAGEQUANT)
    target_link_libraries(_imaging PRIVATE libimagequant::libimagequant)
endif()
if(PILLOW_WITH_XCB)
    target_compile_definitions(_imaging PRIVATE HAVE_XCB)
    target_link_libraries(_imaging PRIVATE libxcb::libxcb)
endif()
if(WIN32)
    target_link_libraries(_imaging PRIVATE kernel32 user32 gdi32)
endif()
if(APPLE)
    target_compile_options(_imaging PRIVATE -Wno-nullability-completeness)
endif()

install(TARGETS _imaging DESTINATION PIL)

# ── PIL._imagingft (FreeType2 + Raqm) ────────────────────────────────────────
if(PILLOW_WITH_FREETYPE)
    set(_imagingft_sources src/_imagingft.c)
    set(_imagingft_defs "")
    set(_imagingft_libs Freetype::Freetype)
    set(_imagingft_includes src src/thirdparty/raqm src/thirdparty/fribidi-shim)

    if(PILLOW_WITH_RAQM)
        # Raqm vendored from src/thirdparty; fribidi from Conan CCI.
        list(APPEND _imagingft_sources src/thirdparty/raqm/raqm.c)
        list(APPEND _imagingft_defs HAVE_RAQM HAVE_FRIBIDI_SYSTEM)
        list(APPEND _imagingft_libs harfbuzz::harfbuzz fribidi::fribidi)
    endif()

    Python3_add_library(_imagingft MODULE ${_imagingft_sources})
    target_include_directories(_imagingft PRIVATE ${_imagingft_includes})
    target_compile_definitions(_imagingft PRIVATE ${_imagingft_defs})
    target_link_libraries(_imagingft PRIVATE ${_imagingft_libs})
    if(APPLE)
        target_compile_options(_imagingft PRIVATE -Wno-nullability-completeness)
    endif()

    install(TARGETS _imagingft DESTINATION PIL)
endif()

# ── PIL._imagingcms (LittleCMS2) ─────────────────────────────────────────────
if(PILLOW_WITH_LCMS)
    Python3_add_library(_imagingcms MODULE src/_imagingcms.c)
    target_include_directories(_imagingcms PRIVATE src)
    target_link_libraries(_imagingcms PRIVATE lcms::lcms)
    if(WIN32)
        target_link_libraries(_imagingcms PRIVATE user32 gdi32)
    endif()
    if(APPLE)
        target_compile_options(_imagingcms PRIVATE -Wno-nullability-completeness)
    endif()

    install(TARGETS _imagingcms DESTINATION PIL)
endif()

# ── PIL._webp ────────────────────────────────────────────────────────────────
if(PILLOW_WITH_WEBP)
    Python3_add_library(_webp MODULE src/_webp.c)
    target_include_directories(_webp PRIVATE src)
    target_link_libraries(_webp PRIVATE WebP::webp WebP::libwebpmux WebP::webpdemux)
    if(APPLE)
        target_compile_options(_webp PRIVATE -Wno-nullability-completeness)
    endif()

    install(TARGETS _webp DESTINATION PIL)
endif()

# ── PIL._avif ────────────────────────────────────────────────────────────────
if(PILLOW_WITH_AVIF)
    Python3_add_library(_avif MODULE src/_avif.c)
    target_include_directories(_avif PRIVATE src)
    target_link_libraries(_avif PRIVATE avif)
    if(WIN32)
        target_link_libraries(_avif PRIVATE ntdll userenv ws2_32 bcrypt)
    endif()
    if(APPLE)
        target_compile_options(_avif PRIVATE -Wno-nullability-completeness)
    endif()

    install(TARGETS _avif DESTINATION PIL)
endif()

# ── PIL._imagingmath ──────────────────────────────────────────────────────────
Python3_add_library(_imagingmath MODULE src/_imagingmath.c)
target_include_directories(_imagingmath PRIVATE src)
if(NOT WIN32)
    target_link_libraries(_imagingmath PRIVATE m)
endif()
install(TARGETS _imagingmath DESTINATION PIL)

# ── PIL._imagingmorph ─────────────────────────────────────────────────────────
Python3_add_library(_imagingmorph MODULE src/_imagingmorph.c)
target_include_directories(_imagingmorph PRIVATE src)
install(TARGETS _imagingmorph DESTINATION PIL)

# ── PIL._imagingtk (Tcl/Tk) ──────────────────────────────────────────────────
if(PILLOW_WITH_TK)
    Python3_add_library(_imagingtk MODULE src/_imagingtk.c src/Tk/tkImaging.c)
    target_include_directories(_imagingtk PRIVATE src src/Tk)
    target_link_libraries(_imagingtk PRIVATE tcl::tcl tk::tk)
    if(WIN32 OR CYGWIN)
        target_link_libraries(_imagingtk PRIVATE psapi)
    endif()
    if(APPLE)
        target_compile_options(_imagingtk PRIVATE -Wno-nullability-completeness)
    endif()

    install(TARGETS _imagingtk DESTINATION PIL)
endif()
