cmake_minimum_required(VERSION 3.5)

###############
# Conan support
###############
find_file(CONANBUILDINFO "conanbuildinfo.cmake" PATHS ${CMAKE_BINARY_DIR})
if (CONANBUILDINFO)
    message(STATUS "CONANBUILDINFO: ${CONANBUILDINFO}")
    include(${CONANBUILDINFO})
    message(STATUS "conan_basic_setup()")
    conan_basic_setup(TARGETS)
endif()

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
    #set(CMAKE_BUILD_TYPE Debug)
endif()

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")

add_executable(example example.cpp)
target_link_libraries(example CONAN_PKG::argon2)

enable_testing()
add_test(NAME example
         WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
         COMMAND example)
