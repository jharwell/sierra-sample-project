# ##############################################################################
# Project Configuration
# ##############################################################################
project(argos_project)

# CMake version requirements (for this sample project it doesn't
# matter--anything recent will work)
cmake_minimum_required(VERSION 3.10)

set(CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 17)

# We avoid using the FindARGoS() CMake functionality because that assumes that
# ARGoS is install system wide, or otherwise requires mucking about with CMake
# paths to get it to work. For the purposes of this simple example, just passing
# the path to wherever you have installed ARGoS to is sufficient (installed, not
# built!).
if(NOT ARGOS_INSTALL_DIR)
  message(FATAL_ERROR "ARGOS_INSTALL_DIR must be defined!")
endif()

# ##############################################################################
# ARGoS Dependencies
# ##############################################################################
# Suppresses a spurious warning (at least I think its spurious)
set(OpenGL_GL_PREFERENCE LEGACY)
find_package(OpenGL REQUIRED)

set(SAMPLE_OPENGL_INCLUDE_DIRS ${OPENGL_INCLUDE_DIR})
set(SAMPLE_OPENGL_LIBRARIES ${OPENGL_LIBRARIES})

if(APPLE)
  set(SAMPLE_OPENGL_INCLUDE_DIRS ${SAMPLE_OPENGL_INCLUDE_DIRS}
                                 ${OPENGL_INCLUDE_DIR}/Headers)
endif()

# ARGoS supports both Qt5 and Qt6, so we test for both. Qt5 only supports
# version-less importing since 5.15, so to support earlier version we explicitly
# have to use the version variable, which is always defined by Qt5 and Qt6.
find_package(Qt6 QUIET COMPONENTS Core Widgets Gui OpenGLWidgets)
if(Qt6_FOUND)
  message(STATUS "Found Qt6: version ${Qt6Core_VERSION}")
  message(STATUS "Found Qt6Widgets: version ${Qt6Widgets_VERSION}")
  message(STATUS "Found Qt6Gui: version ${Qt6Gui_VERSION}")
  message(STATUS "Found Qt6OpenGLWidgets: version ${Qt6OpenGLWidgets_VERSION}")
  list(APPEND SAMPLE_QT_INCLUDE_DIRS ${Qt6Widgets_INCLUDE_DIRS}
       ${Qt6Gui_INCLUDE_DIRS} ${Qt6OpenGLWidgets_INCLUDE_DIRS})
  list(APPEND SAMPLE_QT_LIBRARIES Qt6::Widgets Qt6::Gui Qt6::OpenGLWidgets)
else(Qt6_FOUND)
  find_package(
    Qt5 QUIET
    COMPONENTS Widgets Gui
    OPTIONAL_COMPONENTS OpenGLWidgets)
  if(Qt5_FOUND)
    message(STATUS "Found Qt5: version ${Qt5Core_VERSION_}")
    message(STATUS "Found Qt5Widgets: version ${Qt5Widgets_VERSION}")
    message(STATUS "Found Qt5Gui: version ${Qt5Gui_VERSION}")
    list(APPEND SAMPLE_QT_INCLUDE_DIRS ${Qt5Widgets_INCLUDE_DIRS}
         ${Qt5Gui_INCLUDE_DIRS})
    list(APPEND SAMPLE_QT_LIBRARIES Qt5::Widgets Qt5::Gui)
    if(Qt5OpenGLWidgets_FOUND)
      message(
        STATUS "Found Qt5OpenGLWidgets: version ${Qt5OpenGLWidgets_VERSION}")
      list(APPEND SAMPLE_QT_INCLUDE_DIRS ${Qt5OpenGLWidgets_INCLUDE_DIRS})
      list(APPEND SAMPLE_QT_LIBRARIES Qt5::OpenGLWidgets)
    endif(Qt5OpenGLWidgets_FOUND)
  else(Qt5_FOUND)
    message(STATUS "Qt not found.")
  endif(Qt5_FOUND)
endif(Qt6_FOUND)

# The stock version of ARGoS requires Lua, even if you don't use it.
find_package(Lua)
if(NOT LUA_FOUND)
  message(FATAL_ERROR "Lua not found")
endif()

# ##############################################################################
# Libraries
# ##############################################################################
add_library(
  argos_project SHARED ${CMAKE_SOURCE_DIR}/src/footbot_foraging.cpp
                       ${CMAKE_SOURCE_DIR}/src/foraging_loop_functions.cpp)

if(Qt6_FOUND OR Qt5_FOUND)
  target_sources(argos_project
                 PUBLIC ${CMAKE_SOURCE_DIR}/src/foraging_qt_user_functions.cpp)
endif()

# Setup C++ library compilation and linking
target_include_directories(
  argos_project
  PUBLIC ${CMAKE_SOURCE_DIR}/include ${ARGOS_INSTALL_DIR}/include
         ${LUA_INCLUDE_DIR} ${SAMPLE_QT_INCLUDE_DIRS}
         ${SAMPLE_OPENGL_INCLUDE_DIRS})

target_link_libraries(
  argos_project
  argos3core_simulator
  argos3plugin_simulator_dynamics2d
  argos3plugin_simulator_entities
  argos3plugin_simulator_footbot
  argos3plugin_simulator_genericrobot
  argos3plugin_simulator_media
  ${SAMPLE_OPENGL_LIBRARIES})

if(Qt6_FOUND OR Qt5_FOUND)
  target_link_libraries(argos_project argos3plugin_simulator_qtopengl
                        ${SAMPLE_QT_LIBRARIES})
endif()

target_link_directories(argos_project PUBLIC ${CMAKE_BINARY_DIR}
                        ${ARGOS_INSTALL_DIR}/lib/argos3)
