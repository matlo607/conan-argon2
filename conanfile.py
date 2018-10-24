#!/usr/bin/env python3

from conans import ConanFile, CMake, Meson


class Argon2Conan(ConanFile):
    name = "argon2"
    version = "master"
    description = """Reference C implementation of Argon2, the password-hashing
                     function that won the Password Hashing Competition (PHC)"""
    url = "https://github.com/matlo607/phc-winner-argon2.git"
    license = "Apache Public License 2.0"
    settings = "os", "compiler", "build_type", "arch"
    sources = "https://github.com/matlo607/phc-winner-argon2.git"#"https://github.com/P-H-C/phc-winner-argon2"
    source_dir = "{name}-{version}".format(name=name, version=version)
    options = {
        "fPIC": [True, False],
        "shared": [True, False],
        "tests": [True, False]
    }
    default_options = {
        "fPIC": True,
        "shared": True,
        "tests": True
    }
    scm = {
        "type": "git",
        "subfolder": source_dir,
        "url": sources,
        "revision": "feature-be-cmake-friendly"#version
    }
    generators = "cmake", "pkg_config"

    def source(self):
        pass

    def build(self):
        cmake = CMake(self)
        #cmake.verbose = True
        cmake.configure(source_dir=self.source_dir)
        cmake.build()
        if self.options.tests:
            cmake.test()
        cmake.install()
        #meson = Meson(self)
        #meson.options['libdir'] = 'lib'
        #meson.configure(source_folder=self.source_dir)
        #meson.build()
        #if self.options.tests:
        #    meson.test()
        #meson.install()

    def package(self):
        # already done by CMake's install step
        pass

    def package_info(self):
        self.cpp_info.libs = ['argon2']
        if self.settings.os == "Linux":
             self.cpp_info.libs.append("dl")
             self.cpp_info.libs.append("rt")

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')
