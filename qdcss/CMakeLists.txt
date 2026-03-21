cmake_minimum_required(VERSION 3.15)
project(qdcss)

if(NOT DEFINED QT_VERSION_MAJOR)
    if(DEFINED Launcher_QT_VERSION_MAJOR)
        set(QT_VERSION_MAJOR "${Launcher_QT_VERSION_MAJOR}")
    elseif(CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
        set(QT_VERSION_MAJOR 6)
    else()
        message(FATAL_ERROR "qdcss requires QT_VERSION_MAJOR or Launcher_QT_VERSION_MAJOR to be set")
    endif()
endif()

if(NOT TARGET Qt${QT_VERSION_MAJOR}::Core)
    find_package(Qt${QT_VERSION_MAJOR} COMPONENTS Core REQUIRED)
endif()

set(QDCSS_SOURCES
    include/qdcss.h
    src/qdcss.cpp
)

add_library(qdcss STATIC ${QDCSS_SOURCES})
target_include_directories(qdcss PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(qdcss Qt${QT_VERSION_MAJOR}::Core ${qdcss_LIBS})
