find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_ECE448 gnuradio-ece448)

FIND_PATH(
    GR_ECE448_INCLUDE_DIRS
    NAMES gnuradio/ece448/api.h
    HINTS $ENV{ECE448_DIR}/include
        ${PC_ECE448_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_ECE448_LIBRARIES
    NAMES gnuradio-ece448
    HINTS $ENV{ECE448_DIR}/lib
        ${PC_ECE448_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-ece448Target.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_ECE448 DEFAULT_MSG GR_ECE448_LIBRARIES GR_ECE448_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_ECE448_LIBRARIES GR_ECE448_INCLUDE_DIRS)
