from conans import ConanFile, CMake, tools, RunEnvironment


class CppUTestTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    _cmake_helper = None

    @property
    def _cmake(self):
        if self._cmake_helper is None:
            self._cmake_helper = CMake(self)
        return self._cmake_helper

    def build(self):
        cmake = self._cmake
        cmake.configure()
        cmake.build()

    def test(self):
        cmake = self._cmake
        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
            cmake.test()
