# Name of project
project(argos_project)

# CMake version requirements (for this sample project it doesn't
# matter--anything recent will work)
cmake_minimum_required(VERSION 3.10)

set(CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 17)

# Define ARGoS C++ library sources
add_library(argos_project SHARED
  ${CMAKE_SOURCE_DIR}/src/footbot_foraging.cpp
  ${CMAKE_SOURCE_DIR}/src/foraging_loop_functions.cpp
  ${CMAKE_SOURCE_DIR}/src/foraging_qt_user_functions.cpp
  )

# We avoid using the FindARGoS() CMake functionality because that
# assumes that ARGoS is install system wide, or otherwise requirements
# mucking about with CMake paths to get it to work. For the purposes
# of this simple example, just passing the path to wherever you have
# installed ARGoS to is sufficient (installed, not built!).
if(NOT ARGOS_INSTALL_DIR)
  message(FATAL_ERROR "ARGOS_INSTALL_DIR must be defined!")
endif()

# We want visualizations, so we can demo SIERRA features
set(CMAKE_AUTOMOC ON)
find_package(Qt5 REQUIRED COMPONENTS Core Widgets Gui)
set(CMAKE_AUTOMOC OFF)

# Setup C++ library compilation and linking
target_include_directories(argos_project PUBLIC
  ${CMAKE_SOURCE_DIR}/include
  ${ARGOS_INSTALL_DIR}/include
  /usr/include/lua5.3
  /usr/include/lua5.2
  )

target_link_libraries(argos_project
  argos3core_simulator
  argos3plugin_simulator_dynamics2d
  argos3plugin_simulator_entities
  argos3plugin_simulator_footbot
  argos3plugin_simulator_genericrobot
  argos3plugin_simulator_qtopengl
  argos3plugin_simulator_media
  Qt5::Widgets
  Qt5::Core
  Qt5::Gui
  GL
  )

target_link_directories(argos_project PUBLIC
  ${CMAKE_BINARY_DIR}
  ${ARGOS_INSTALL_DIR}/lib/argos3
  )
