cmake_minimum_required(VERSION 3.15)
project(LocalPeer)

if(NOT DEFINED QT_VERSION_MAJOR)
    if(DEFINED Launcher_QT_VERSION_MAJOR)
        set(QT_VERSION_MAJOR "${Launcher_QT_VERSION_MAJOR}")
    elseif(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
        set(QT_VERSION_MAJOR 6)
    else()
        message(FATAL_ERROR "LocalPeer requires QT_VERSION_MAJOR or Launcher_QT_VERSION_MAJOR to be set")
    endif()
endif()

if(NOT TARGET Qt${QT_VERSION_MAJOR}::Core OR NOT TARGET Qt${QT_VERSION_MAJOR}::Network)
    find_package(Qt${QT_VERSION_MAJOR} COMPONENTS Core Network REQUIRED)
endif()

set(SINGLE_SOURCES
src/LocalPeer.cpp
src/LockedFile.cpp
src/LockedFile.h
include/LocalPeer.h
)

if(UNIX)
    list(APPEND SINGLE_SOURCES
        src/LockedFile_unix.cpp
    )
endif()

if(WIN32)
    list(APPEND SINGLE_SOURCES
        src/LockedFile_win.cpp
    )
endif()

add_library(LocalPeer STATIC ${SINGLE_SOURCES})
target_include_directories(LocalPeer PUBLIC include)

target_link_libraries(LocalPeer Qt${QT_VERSION_MAJOR}::Core Qt${QT_VERSION_MAJOR}::Network ${LocalPeer_LIBS})
