#!/usr/bin/env python3

from conans import ConanFile, AutoToolsBuildEnvironment, tools

class Argon2Conan(ConanFile):
    name = "argon2"
    version = "master"
    description = """Reference C implementation of Argon2, the password-hashing
                     function that won the Password Hashing Competition (PHC)"""
    url = "https://github.com/P-H-C/phc-winner-argon2"
    license = "Apache Public License 2.0"
    settings = "os", "compiler", "build_type", "arch"
    sources = "https://github.com/P-H-C/phc-winner-argon2"
    source_dir = "{name}-{version}".format(name=name, version=version)
    scm = {
        "type": "git",
        "subfolder": source_dir,
        "url": sources,
        "revision": version
    }
    generators = "cmake"

    def source(self):
        pass

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            with tools.chdir(self.source_dir):
                self.run("make")
                self.run("make test")
                self.run("make install PREFIX={}".format(self.package_folder))

    def package(self):
        # already done by 'make install'
        pass

    def package_info(self):
        self.cpp_info.libs = ['argon2']
