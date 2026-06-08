from __future__ import annotations

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout


class PillowConan(ConanFile):
    name = "pillow"
    version = "12.3.0"
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "with_jpeg": [True, False],
        "with_zlib": [True, False],
        "with_png": [True, False],
        "with_tiff": [True, False],
        "with_jpeg2000": [True, False],
        "with_freetype": [True, False],
        # Raqm is always vendored (src/thirdparty/raqm); only harfbuzz+fribidi from Conan.
        "with_raqm": [True, False],
        "with_lcms": [True, False],
        "with_webp": [True, False],
        "with_avif": [True, False],
        "with_imagequant": [True, False],
        "with_tk": [True, False],
        "with_xcb": [True, False],
    }
    default_options = {
        "with_jpeg": True,
        "with_zlib": True,
        "with_png": True,
        "with_tiff": True,
        "with_jpeg2000": True,
        "with_freetype": True,
        "with_raqm": True,
        "with_lcms": True,
        "with_webp": True,
        "with_avif": True,
        "with_imagequant": False,
        "with_tk": False,
        "with_xcb": False,
    }

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        if self.options.with_jpeg:
            self.requires("libjpeg/9e")
        if self.options.with_zlib:
            self.requires("zlib/1.3.1")
        if self.options.with_png:
            self.requires("libpng/1.6.43")
        if self.options.with_tiff:
            self.requires("libtiff/4.6.0")
        if self.options.with_jpeg2000:
            self.requires("openjpeg/2.5.2")
        if self.options.with_freetype:
            self.requires("freetype/2.13.2")
        if self.options.with_raqm:
            self.requires("harfbuzz/10.4.0")
            self.requires("fribidi/1.0.13")
        if self.options.with_lcms:
            self.requires("lcms/2.16")
        if self.options.with_webp:
            self.requires("libwebp/1.4.0")
        if self.options.with_avif:
            self.requires("libavif/1.1.1")
        if self.options.with_imagequant:
            self.requires("libimagequant/4.3.0")
        if self.options.with_tk:
            self.requires("tcl/8.6.13")
            self.requires("tk/8.6.13")
        if self.options.with_xcb:
            self.requires("libxcb/1.16.0")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["PILLOW_WITH_JPEG"] = bool(self.options.with_jpeg)
        tc.variables["PILLOW_WITH_ZLIB"] = bool(self.options.with_zlib)
        tc.variables["PILLOW_WITH_PNG"] = bool(self.options.with_png)
        tc.variables["PILLOW_WITH_TIFF"] = bool(self.options.with_tiff)
        tc.variables["PILLOW_WITH_JPEG2000"] = bool(self.options.with_jpeg2000)
        tc.variables["PILLOW_WITH_FREETYPE"] = bool(self.options.with_freetype)
        tc.variables["PILLOW_WITH_RAQM"] = bool(self.options.with_raqm)
        tc.variables["PILLOW_WITH_LCMS"] = bool(self.options.with_lcms)
        tc.variables["PILLOW_WITH_WEBP"] = bool(self.options.with_webp)
        tc.variables["PILLOW_WITH_AVIF"] = bool(self.options.with_avif)
        tc.variables["PILLOW_WITH_IMAGEQUANT"] = bool(self.options.with_imagequant)
        tc.variables["PILLOW_WITH_TK"] = bool(self.options.with_tk)
        tc.variables["PILLOW_WITH_XCB"] = bool(self.options.with_xcb)
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
