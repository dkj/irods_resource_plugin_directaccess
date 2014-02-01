/*** Copyright (c), The Regents of the University of California            ***
 *** For more information please refer to files in the COPYRIGHT directory ***/

/* libdirectaccess.hpp - header file for libdirectaccess.cpp
 */

#ifndef LIBDIRECTACCESS_HPP
#define LIBDIRECTACCESS_HPP

#include <stdio.h>
#ifndef _WIN32
#include <sys/file.h>
#include <sys/param.h>
#endif
#include <errno.h>
#include <sys/stat.h>
#include <string.h>
#ifndef _WIN32
#include <unistd.h>
#endif
#include <sys/types.h>
#if defined(osx_platform)
#include <sys/malloc.h>
#else
#include <malloc.h>
#endif
#include <fcntl.h>
#ifndef _WIN32
#include <sys/file.h>
#include <unistd.h>  
#endif
#include <dirent.h>
   
#if defined(solaris_platform)
#include <sys/statvfs.h>
#endif
#if defined(linux_platform)
#include <sys/vfs.h>
#endif
#if defined(aix_platform) || defined(sgi_platform)
#include <sys/statfs.h>
#endif
#if defined(osx_platform)
#include <sys/param.h>
#include <sys/mount.h>
#endif
#include <sys/stat.h>

#include "rods.hpp"
#include "rcConnect.hpp"
#include "msParam.hpp"
//#include "miscServerFunct.hpp"
#include "fileDriver.hpp"

/* when we resize the state array, do in increments of this */
#define DIRECT_ACCESS_FILE_STATE_ARRAY_SIZE 256

typedef struct directAccessFileState {
    int fd;
    int fileMode;
} directAccessFileState_t;

#endif	/* LIBDIRECTACCESS_HPP */
