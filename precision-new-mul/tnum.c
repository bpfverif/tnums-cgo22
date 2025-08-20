#include "tnum.h"

#define TNUM(_v, _m)                                                           \
  (struct tnum) { .value = _v, .mask = _m }

const struct tnum tnum_unknown = {.value = 0, .mask = 0xffffffffffffffffULL};

struct tnum tnum_const(u64 value) {
  return TNUM(value, 0);
}

int tnum_sbin(char *str, size_t size, struct tnum a) {
  size_t n;

  for (n = 64; n; n--) {
    if (n < size) {
      if (a.mask & 1)
        str[n - 1] = 'x';
      else if (a.value & 1)
        str[n - 1] = '1';
      else
        str[n - 1] = '0';
    }
    a.mask >>= 1;
    a.value >>= 1;
  }
  size_t min = size - 1 < (size_t)64 ? size - 1 : (size_t)64;
  str[min] = 0;
  return 64;
}

// -----------------------------------------------------------------------------
// tnum shift operations
// -----------------------------------------------------------------------------

struct tnum tnum_lshift(struct tnum a, u8 shift) {
  return TNUM(a.value << shift, a.mask << shift);
}

struct tnum tnum_rshift(struct tnum a, u8 shift) {
  return TNUM(a.value >> shift, a.mask >> shift);
}

struct tnum tnum_arshift(struct tnum a, u8 min_shift) {
  /* if a.value is negative, arithmetic shifting by minimum shift
   * will have larger negative offset compared to more shifting.
   * If a.value is nonnegative, arithmetic shifting by minimum shift
   * will have larger positive offset compare to more shifting.
   */
  return TNUM((s64)a.value >> min_shift, (s64)a.mask >> min_shift);
}

// -----------------------------------------------------------------------------
// tnum arithmetic operations
// -----------------------------------------------------------------------------

struct tnum tnum_add(struct tnum a, struct tnum b) {
  u64 sm, sv, sigma, chi, mu;

  sm = a.mask + b.mask;
  sv = a.value + b.value;
  sigma = sm + sv;
  chi = sigma ^ sv;
  mu = chi | a.mask | b.mask;
  return TNUM(sv & ~mu, mu);
}

struct tnum tnum_sub(struct tnum a, struct tnum b) {
  u64 dv, alpha, beta, chi, mu;

  dv = a.value - b.value;
  alpha = dv + a.mask;
  beta = dv - b.mask;
  chi = alpha ^ beta;
  mu = chi | a.mask | b.mask;
  return TNUM(dv & ~mu, mu);
}

// -----------------------------------------------------------------------------
// tnum bitwise operations
// -----------------------------------------------------------------------------

struct tnum tnum_and(struct tnum a, struct tnum b) {
  u64 alpha, beta, v;

  alpha = a.value | a.mask;
  beta = b.value | b.mask;
  v = a.value & b.value;
  return TNUM(v, alpha & beta & ~v);
}

struct tnum tnum_or(struct tnum a, struct tnum b) {
  u64 v, mu;

  v = a.value | b.value;
  mu = a.mask | b.mask;
  return TNUM(v, mu & ~v);
}

struct tnum tnum_xor(struct tnum a, struct tnum b) {
  u64 v, mu;

  v = a.value ^ b.value;
  mu = a.mask | b.mask;
  return TNUM(v & ~mu, mu);
}

bool tnum_in(struct tnum a, struct tnum b)
{
	if (b.mask & ~a.mask)
		return false;
	b.value &= ~a.mask;
	return a.value == b.value;
}

// -----------------------------------------------------------------------------
// tnum multiplication operations
// -----------------------------------------------------------------------------

/* our_mul (from the paper) */
struct tnum long_mul(struct tnum a, struct tnum b) {
  struct tnum acc = TNUM(0, 0);

  while (a.value || a.mask) {
    /* LSB of tnum a is a certain 1 */
    if (a.value & 1)
      acc = tnum_add(acc, b);
    /* LSB of tnum a is uncertain */
    else if (a.mask & 1) {
      acc = tnum_add(acc, TNUM(0, b.value | b.mask));
    }
    /* Note: no case for LSB is certain 0 */
    a = tnum_rshift(a, 1);
    b = tnum_lshift(b, 1);
  }
  return acc;
}

/* our_mul (from the paper) */
struct tnum our_mul(struct tnum a, struct tnum b) {
  u64 acc_v = a.value * b.value;
  struct tnum acc_m = TNUM(0, 0);

  while (a.value || a.mask) {
    /* LSB of tnum a is a certain 1 */
    if (a.value & 1)
      acc_m = tnum_add(acc_m, TNUM(0, b.mask));
    /* LSB of tnum a is uncertain */
    else if (a.mask & 1)
      acc_m = tnum_add(acc_m, TNUM(0, b.value | b.mask));
    /* Note: no case for LSB is certain 0 */
    a = tnum_rshift(a, 1);
    b = tnum_lshift(b, 1);
  }
  return tnum_add(TNUM(acc_v, 0), acc_m);
}

struct tnum tnum_union(struct tnum a, struct tnum b) {
  u64 v = a.value & b.value;
  u64 mu = (a.value ^ b.value) | a.mask | b.mask;

  return TNUM(v & ~mu, mu);
}

struct tnum new_mul(struct tnum a, struct tnum b)
{
	struct tnum acc = TNUM(0, 0);

	while (a.value || a.mask) {
		/* LSB of tnum a is a certain 1 */
		if (a.value & 1)
			acc = tnum_add(acc, b);
		/* LSB of tnum a is uncertain */
		else if (a.mask & 1) {
			/* x1, where acc_0 and
			 * acc_1 are partial accumulators for cases
			 * LSB(a) = certain 0 and LSB(a) = certain 1.
			 * acc_0 = acc + 0 * b = acc.
			 * acc_1 = acc + 1 * b = tnum_add(acc, b).
			 */
			// acc = tnum_union(tnum_add(acc, TNUM(0, 0)), tnum_add(acc, b));
			acc = tnum_union(acc, tnum_add(acc, b));
		}
		/* Note: no case for LSB is certain 0 */
		a = tnum_rshift(a, 1);
		b = tnum_lshift(b, 1);
	}
	return acc;
}

struct tnum new_mul_2(struct tnum a, struct tnum b)
{
	struct tnum acc = TNUM(0, 0);

	while (a.value || a.mask) {
		/* LSB of tnum a is a certain 1 */
		if (a.value & 1)
			acc = tnum_add(acc, b);
		/* LSB of tnum a is uncertain */
		else if (a.mask & 1) {
			/* x1, where acc_0 and
			 * acc_1 are partial accumulators for cases
			 * LSB(a) = certain 0 and LSB(a) = certain 1.
			 * acc_0 = acc + 0 * b = acc.
			 * acc_1 = acc + 1 * b = tnum_add(acc, b).
			 */
			acc = tnum_add(acc, tnum_union(TNUM(0, 0), b));
		}
		/* Note: no case for LSB is certain 0 */
		a = tnum_rshift(a, 1);
		b = tnum_lshift(b, 1);
	}
	return acc;
}