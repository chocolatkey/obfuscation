#ifndef __OBFUSCATION__UTILS_H__
#define __OBFUSCATION__UTILS_H__

#include <gmp.h>
#include <stdio.h>

double
current_time(void);

FILE *
open_file(const char *dir, const char *file, const char *mode);

int
load_mpz_scalar(const char *fname, mpz_t x);

#endif
