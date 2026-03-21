cmake_minimum_required(VERSION 3.15)
project(systeminfo)

set(CMAKE_AUTOMOC ON)
include(CTest)

set(_systeminfo_qt_components Core Gui Network)
if(NOT DEFINED QT_VERSION_MAJOR)
    if(DEFINED Launcher_QT_VERSION_MAJOR)
        set(QT_VERSION_MAJOR "${Launcher_QT_VERSION_MAJOR}")
    elseif(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
        set(QT_VERSION_MAJOR 6)
    else()
        message(FATAL_ERROR "systeminfo requires QT_VERSION_MAJOR or Launcher_QT_VERSION_MAJOR to be set")
    endif()
endif()

if(BUILD_TESTING)
    list(APPEND _systeminfo_qt_components Test)
endif()

set(_systeminfo_missing_qt_components)
foreach(_systeminfo_qt_component IN LISTS _systeminfo_qt_components)
    if(NOT TARGET Qt${QT_VERSION_MAJOR}::${_systeminfo_qt_component})
        list(APPEND _systeminfo_missing_qt_components "${_systeminfo_qt_component}")
    endif()
endforeach()

if(_systeminfo_missing_qt_components)
    find_package(Qt${QT_VERSION_MAJOR} COMPONENTS ${_systeminfo_qt_components} REQUIRED)
endif()

if(BUILD_TESTING)
    if(NOT COMMAND ecm_add_test)
        if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/../extra-cmake-modules/modules/ECMAddTests.cmake")
            list(PREPEND CMAKE_MODULE_PATH
                "${CMAKE_CURRENT_SOURCE_DIR}/../extra-cmake-modules/modules"
                "${CMAKE_CURRENT_SOURCE_DIR}/../extra-cmake-modules/kde-modules"
            )
        else()
            find_package(ECM REQUIRED NO_MODULE)
            list(PREPEND CMAKE_MODULE_PATH "${ECM_MODULE_PATH}")
        endif()
        include(ECMAddTests)
    endif()
endif()

set(systeminfo_SOURCES
include/sys.h
include/distroutils.h
src/distroutils.cpp
)

if (WIN32)
    list(APPEND systeminfo_SOURCES src/sys_win32.cpp)
elseif (UNIX)
    if(APPLE)
        list(APPEND systeminfo_SOURCES src/sys_apple.cpp)
    else()
        list(APPEND systeminfo_SOURCES src/sys_unix.cpp)
    endif()
endif()

add_library(systeminfo STATIC ${systeminfo_SOURCES})
target_link_libraries(systeminfo Qt${QT_VERSION_MAJOR}::Core Qt${QT_VERSION_MAJOR}::Gui Qt${QT_VERSION_MAJOR}::Network ${systeminfo_LIBS})
target_include_directories(systeminfo PUBLIC include)

ecm_add_test(src/sys_test.cpp LINK_LIBRARIES systeminfo Qt${QT_VERSION_MAJOR}::Test TEST_NAME sys)
