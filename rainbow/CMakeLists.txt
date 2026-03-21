cmake_minimum_required(VERSION 3.15)
project(rainbow)

if(NOT DEFINED QT_VERSION_MAJOR)
    if(DEFINED Launcher_QT_VERSION_MAJOR)
        set(QT_VERSION_MAJOR "${Launcher_QT_VERSION_MAJOR}")
    elseif(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
        set(QT_VERSION_MAJOR 6)
    else()
        message(FATAL_ERROR "rainbow requires QT_VERSION_MAJOR or Launcher_QT_VERSION_MAJOR to be set")
    endif()
endif()

set(_rainbow_qt_components Core Gui)
set(_rainbow_missing_qt_components)
foreach(_rainbow_qt_component IN LISTS _rainbow_qt_components)
    if(NOT TARGET Qt${QT_VERSION_MAJOR}::${_rainbow_qt_component})
        list(APPEND _rainbow_missing_qt_components "${_rainbow_qt_component}")
    endif()
endforeach()

if(_rainbow_missing_qt_components)
    find_package(Qt${QT_VERSION_MAJOR} COMPONENTS ${_rainbow_qt_components} REQUIRED)
endif()

set(RAINBOW_SOURCES
src/rainbow.cpp
)

add_library(Launcher_rainbow STATIC ${RAINBOW_SOURCES})
target_include_directories(Launcher_rainbow PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")

target_link_libraries(Launcher_rainbow Qt${QT_VERSION_MAJOR}::Core Qt${QT_VERSION_MAJOR}::Gui)
