cmake_minimum_required(VERSION 3.10)
project(cSUAS_Imagery VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find OpenCV
find_package(OpenCV REQUIRED)

# Include directories
include_directories(
    ${OpenCV_INCLUDE_DIRS}
    ${CMAKE_SOURCE_DIR}/src/cpp
)

# Source files
set(SOURCES
    src/cpp/drone_detector.cpp
    src/cpp/main.cpp
)

# Create executable
add_executable(drone_detection ${SOURCES})

# Link libraries
target_link_libraries(drone_detection
    ${OpenCV_LIBS}
)

# Installation
install(TARGETS drone_detection
    RUNTIME DESTINATION bin
)

# Print configuration
message(STATUS "OpenCV version: ${OpenCV_VERSION}")
message(STATUS "OpenCV include dirs: ${OpenCV_INCLUDE_DIRS}")
message(STATUS "OpenCV libs: ${OpenCV_LIBS}")
