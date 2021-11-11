from z3 import *
import sys
import argparse

BITVEC_WIDTH = 64

class BitVecHelper:

	uniq_id = 0

	@staticmethod
	def new_uniq_bitvec():
		BitVecHelper.uniq_id += 1	
		bitvec_name = "bitvec" + "_" + str(BitVecHelper.uniq_id)
		return BitVec(bitvec_name, BITVEC_WIDTH)

	@staticmethod
	def new_uniq_bitvecs(num):
		l = []
		for i in range(num):
			l.append(BitVecHelper.new_uniq_bitvec())
		return l

class Tnum:

	uniq_id = 0

	def __init__(self, v, m):
		self.value = v
		self.mask = m

	@classmethod
	def new_tnum_from_bitvec(cls, v, m):
		return cls(v, m)
	
	@classmethod
	def new_tnum_from_bits(cls, v, m):
		val = BitVecVal(v, BITVEC_WIDTH)
		mask = BitVecVal(m, BITVEC_WIDTH)
		return cls(val, mask)

	@staticmethod
	def new_tnum_from_name(nm):
		"""
		globally non-unique tnum
		"""
		v = BitVec(nm + '_v', BITVEC_WIDTH)
		m = BitVec(nm + '_m', BITVEC_WIDTH)
		return Tnum(v, m)

	@staticmethod
	def new_uniq_tnum():
		Tnum.uniq_id += 1
		uniq_id_str = "tnum" + "_" + str(Tnum.uniq_id)
		value_bitvec = BitVec(uniq_id_str + "_v", BITVEC_WIDTH)
		mask_bitvec = BitVec(uniq_id_str + "_m", BITVEC_WIDTH)
		return Tnum(value_bitvec, mask_bitvec)

	@staticmethod
	def new_uniq_tnum_from_name(name):
		Tnum.uniq_id += 1
		uniq_id_str = str(Tnum.uniq_id)
		value_bitvec = BitVec(name + "_" + uniq_id_str + "_" + "v", 
			BITVEC_WIDTH)
		mask_bitvec = BitVec(name + "_" + uniq_id_str + "_" + "m", 
			BITVEC_WIDTH)
		return Tnum(value_bitvec, mask_bitvec)

	@staticmethod
	def new_uniq_tnums(num):
		l = []
		for i in range(num):
			l.append(Tnum.new_uniq_tnum())
		return l
		
	@staticmethod
	def new_uniq_tnums_from_names(names):
		l = []
		for n in names:
			l.append(Tnum.new_uniq_tnum_from_name(n))
		return l

	@staticmethod
	def is_in_tnum(x, t):
		"""
		if concrete bits of x match tnum, x is in tnum. 
		~mask contains 1 for all concrete bits, and 0 for all unknown bits.
		<value_expression> & ~mask will propagate all concrete bits, 
		and zero out all unknown bits.
		"""
		return t.value == x & ~t.mask

	@staticmethod
	def contains_tnum(self, other):
		"""
		does this tnum contain the other tnum?
		"""
		return self.mask | other.mask == self.mask

	@staticmethod
	def is_wellformed(t):
		"""
		for a wellformed tnum, 
		a. concrete bits are 0 in mask, value bit can by anything.
		b. unknown bits are 0 in value, 1 in mask.
		so value & mask should propagate 0 for concrete bits (by a), 
		and 0 for unknown bits (by b) => fully 0.
		note: value = value & ~mask makes a tnum well-formed. 
		"""
		return (t.value & t.mask) == 0

	@staticmethod
	def is_known_tnum(t):
		return t.mask == BitVecVal(0, BITVEC_WIDTH)

	@staticmethod
	def tnum_equals(a, b):
		return And((a.value == b.value), (a.mask == b.mask))

	def to_string(self):
		assert type(self.value) == z3.z3.BitVecNumRef
		assert type(self.mask) == z3.z3.BitVecNumRef
		s =  []
		for i in range(BITVEC_WIDTH):
			l = BitVecVal(1, BITVEC_WIDTH) << i
			v = self.value & l
			m = self.mask & l
			if (simplify(v == BitVecVal(0, BITVEC_WIDTH)) and 
					simplify(m != BitVecVal(0, BITVEC_WIDTH))):
				s.insert(0, "x")
			elif (simplify(v == BitVecVal(0, BITVEC_WIDTH)) and 
					simplify(m == BitVecVal(0, BITVEC_WIDTH))):
				s.insert(0, "0")
			elif (simplify(v != BitVecVal(0, BITVEC_WIDTH)) and 
					simplify(m == BitVecVal(0, BITVEC_WIDTH))):
				s.insert(0, "1")
			else:
				raise AssertionError("not wellformed")
		return "".join(s)


	# return a tnum representing a left shift of 'shift' on the tnum 'a'
	@staticmethod
	def tnum_lshift(a, shift, res):
		f = []
		f.append(res.value == a.value << shift)
		f.append(res.mask == a.mask << shift)
		return And(f)

	# return a tnum representing a right shift of 'shift' on the tnum 'a'
	@staticmethod
	def tnum_rshift(a, shift, res):
		f = []
		f.append(res.value == LShR(a.value, shift))
		f.append(res.mask == LShR(a.mask, shift))
		return And(f)

	# return a tnum representing a right shift of 'shift' on the tnum 'a'
	@staticmethod
	def tnum_arshift(a, shift, res):
		f = []
		f.append(res.value == a.value >> shift)
		f.append(res.mask == a.mask >> shift)
		return And(f)

	# return a formula representing the addition of two tnums 'a' and 'b'
	@staticmethod
	def tnum_add(a, b, res):
		f = []
		sm, sv, sigma, chi, mu = BitVecHelper.new_uniq_bitvecs(5)
		f.append(sm == a.mask + b.mask)
		f.append(sv == a.value + b.value)
		f.append(sigma == sm + sv)
		f.append(chi == sigma ^ sv)
		f.append(mu == chi | a.mask | b.mask)
		f.append(res.value == sv & ~mu)
		f.append(res.mask == mu)
		return And(f)

	# return a tnum representing the subtraction of two tnums 'a' and 'b'
	@staticmethod
	def tnum_sub(a, b, res):
		f = []
		dv, alpha, beta, chi, mu = BitVecHelper.new_uniq_bitvecs(5)
		f.append(dv == a.value - b.value)
		f.append(alpha == dv + a.mask)
		f.append(beta == dv - b.mask)
		f.append(chi == alpha ^ beta)
		f.append(mu == chi | a.mask | b.mask)
		f.append(res.value == dv & ~mu)
		f.append(res.mask == mu)
		return And(f)

	# return a tnum representing the bitwise and of two tnums 'a' and 'b'
	@staticmethod
	def tnum_and(a, b, res):
		f = []
		alpha, beta, v = BitVecHelper.new_uniq_bitvecs(3)
		f.append(alpha == a.value | a.mask)
		f.append(beta == b.value | b.mask)
		f.append(v == a.value & b.value)
		f.append(res.value == v)
		f.append(res.mask == alpha & beta & ~v)
		return And(f)

	# return a tnum representing the bitwise or of two tnums 'a' and 'b'
	@staticmethod
	def tnum_or(a, b, res):
		f = []
		v, mu =  BitVecHelper.new_uniq_bitvecs(2)
		f.append(v == a.value | b.value)
		f.append(mu == a.mask | b.mask)
		f.append(res.value == v)
		f.append(res.mask == mu & ~v)
		return And(f)

	# return a tnum representing the bitwise xor of two tnums 'a' and 'b'
	@staticmethod
	def tnum_xor(a, b, res):
		f = []
		v, mu =  BitVecHelper.new_uniq_bitvecs(2)
		f.append(v == a.value ^ b.value)
		f.append(mu == a.mask | b.mask)
		f.append(res.value == v & ~mu)
		f.append(res.mask == mu)
		return And(f)

	@staticmethod
	def hma(acc, value, mask, res):

		accs = []
		masks = []
		values = []

		accs.append(acc)
		masks.append(mask)
		values.append(value)

		f = []

		# loop goes from 1...64 (total 64),
		# so, accs = [acc_1, ... acc_64] (total 64)
		for i in range(1, BITVEC_WIDTH + 1):
			acc_i = Tnum.new_uniq_tnum()
			mask_i = BitVecHelper.new_uniq_bitvec()			
			value_i = BitVecHelper.new_uniq_bitvec()
			accs.append(acc_i)
			masks.append(mask_i)
			values.append(value_i)
			f.append(
				If((masks[i-1] & BitVecVal(1, BITVEC_WIDTH) != BitVecVal(0, BITVEC_WIDTH)),
				(Tnum.tnum_add(accs[i-1], Tnum.new_tnum_from_bitvec(BitVecVal(0, BITVEC_WIDTH), values[i-1]), acc_i)),
				(Tnum.tnum_equals(acc_i, accs[i-1])))	
			)
			f.append(mask_i == LShR(masks[i-1], BitVecVal(1, BITVEC_WIDTH)))
			f.append(value_i == values[i-1] << BitVecVal(1, BITVEC_WIDTH))

		f.append(Tnum.tnum_equals(res, accs[BITVEC_WIDTH]))

		return And(f)


	@staticmethod
	def tnum_kern_mul(a, b, res):
		f = []
		res_acc_1 = Tnum.new_uniq_tnum()
		res_1 = Tnum.hma(Tnum.new_tnum_from_bitvec(a.value * b.value, 
			BitVecVal(0, BITVEC_WIDTH)), a.mask, b.mask | b.value, res_acc_1)
		res_acc_2 = Tnum.new_uniq_tnum()
		res_2 = Tnum.hma(res_acc_1, b.mask, a.value, res_acc_2)
		f.append(res_1)
		f.append(res_2)
		f.append(res.value == res_acc_2.value)
		f.append(res.mask == res_acc_2.mask)
		return And(f)


	@staticmethod
	def tnum_our_mul(tnum_a, tnum_b, tnum_c):
		num_iterations = BITVEC_WIDTH + 1
		acc_m		= [Tnum.new_uniq_tnum() for i in range(0, num_iterations)]
		acc_v		= [Tnum.new_uniq_tnum() for i in range(0, num_iterations)]
		part_prod_v  = [Tnum.new_uniq_tnum() for i in range(0, num_iterations)]
		part_prod_m  = [Tnum.new_uniq_tnum() for i in range(0, num_iterations)]
		curr_a	   = [Tnum.new_uniq_tnum() for i in range(0, num_iterations)]
		curr_b	   = [Tnum.new_uniq_tnum() for i in range(0, num_iterations)]
		formulas = []
		formulas += [
			acc_v[0].value == BitVecVal(0, BITVEC_WIDTH),
			acc_v[0].mask  == BitVecVal(0, BITVEC_WIDTH),
			acc_m[0].value == BitVecVal(0, BITVEC_WIDTH),
			acc_m[0].mask  == BitVecVal(0, BITVEC_WIDTH),
			curr_a[0].value == tnum_a.value,
			curr_a[0].mask  == tnum_a.mask,
			curr_b[0].value == tnum_b.value,
			curr_b[0].mask  == tnum_b.mask
		]
		# unrolled loop of the following:
		# if bit k of b is a certain 0, add nothing to acc
		# if bit k of b is a certain 1, add a directly to acc
		# if bit k of b is uncertain,   add tnum(0, a.v | a.m) to acc
		for i in range(1, num_iterations):
			certain_b_lsb = (curr_b[i-1].mask & BitVecVal(1, BITVEC_WIDTH) == 
				BitVecVal(0, BITVEC_WIDTH))
			uncertain_b_lsb = (curr_b[i-1].mask & BitVecVal(1, BITVEC_WIDTH) == 
				BitVecVal(1, BITVEC_WIDTH))
			b_lsb   = curr_b[i-1].value & BitVecVal(1, BITVEC_WIDTH)
			certain_b_1 = And([certain_b_lsb, b_lsb == BitVecVal(1, BITVEC_WIDTH)])
			certain_b_0 = And([certain_b_lsb, b_lsb == BitVecVal(0, BITVEC_WIDTH)])
			assign_part_prod = And([
				Implies(certain_b_1,
						And([part_prod_v[i].value == curr_a[i-1].value,
							 part_prod_v[i].mask  == BitVecVal(0, BITVEC_WIDTH),
							 part_prod_m[i].value == BitVecVal(0, BITVEC_WIDTH),
							 part_prod_m[i].mask  == curr_a[i-1].mask])),
				Implies(certain_b_0,
						And([part_prod_v[i].value == BitVecVal(0, BITVEC_WIDTH),
							 part_prod_v[i].mask  == BitVecVal(0, BITVEC_WIDTH),
							 part_prod_m[i].value == BitVecVal(0, BITVEC_WIDTH),
							 part_prod_m[i].mask  == BitVecVal(0, BITVEC_WIDTH)])),
				Implies(uncertain_b_lsb,
						And([part_prod_m[i].value == BitVecVal(0, BITVEC_WIDTH),
							 part_prod_m[i].mask  == 
							 	(curr_a[i-1].value | curr_a[i-1].mask),
							 part_prod_v[i].value == BitVecVal(0, BITVEC_WIDTH),
							 part_prod_v[i].mask  == BitVecVal(0, BITVEC_WIDTH)]))
				])
			assign_acc_v = Tnum.tnum_add(acc_v[i-1], part_prod_v[i], acc_v[i])
			assign_acc_m = Tnum.tnum_add(acc_m[i-1], part_prod_m[i], acc_m[i])
			assign_curr_a = Tnum.tnum_lshift(curr_a[i-1], 
				BitVecVal(1, BITVEC_WIDTH), curr_a[i])
			assign_curr_b = Tnum.tnum_rshift(curr_b[i-1], 
				BitVecVal(1, BITVEC_WIDTH), curr_b[i])
			formulas.append(assign_part_prod)
			formulas.append(assign_acc_v)
			formulas.append(assign_acc_m)
			formulas.append(assign_curr_a)
			formulas.append(assign_curr_b)

		formulas.append(Tnum.tnum_add(acc_v[num_iterations - 1], 
			acc_m[num_iterations -1], tnum_c))

		return And(formulas)

class TnumOpsVerifier:

	@staticmethod
	def check_tnum_add():
		"""
		F: (x is_in_tnum a) AND (y is_in_tnum b) 
		-> (x + y) is_in_tnum (tnum_add(a, b))
		"""
		
		print("\nVerifying correctness of [tnum_add] for tnums of width [{}] ... ".format(BITVEC_WIDTH), 
			end="", flush=True)
		
		s = SolverFor("QF_BV")
		a = Tnum.new_tnum_from_name('a')
		b = Tnum.new_tnum_from_name('b')
		res = Tnum.new_tnum_from_name('res')
		x = BitVec('x', BITVEC_WIDTH)
		y = BitVec('y', BITVEC_WIDTH)

		f = Implies(
				And(Tnum.is_wellformed(a), 
					Tnum.is_wellformed(b), 
					Tnum.is_in_tnum(x, a), 
					Tnum.is_in_tnum(y, b),
					Tnum.tnum_add(a, b, res)
				), 
				And(Tnum.is_wellformed(res), 
					Tnum.is_in_tnum(x + y, res)
			)
		)

		f = ForAll(
				[a.value, b.value, a.mask, b.mask],  
				ForAll([x, y], f)
			)
		s.add(Not(f))

		if(s.check() == unsat):
			print(" SUCCESS.")
		else:
			print("FAILED.")
			print(s.model())

	@staticmethod
	def check_tnum_sub():
		"""
		F: (x is_in_tnum a) AND (y is_in_tnum b) 
		-> (x - y) is_in_tnum (tnum_sub(a, b))
		"""
		print("\nVerifying correctness of [tnum_sub] for tnums of width [{}] ... ".format(BITVEC_WIDTH), 
			end="", flush=True)
		
		s = SolverFor("QF_BV")
		a = Tnum.new_tnum_from_name('a')
		b = Tnum.new_tnum_from_name('b')
		res = Tnum.new_tnum_from_name('res')
		x = BitVec('x', BITVEC_WIDTH)
		y = BitVec('y', BITVEC_WIDTH)

		f = Implies(
				And(Tnum.is_wellformed(a), 
					Tnum.is_wellformed(b), 
					Tnum.is_in_tnum(x, a), 
					Tnum.is_in_tnum(y, b),
					Tnum.tnum_sub(a, b, res)
				), 
				And(Tnum.is_wellformed(res), 
					Tnum.is_in_tnum(x - y, res)
			)
		)

		f = ForAll(
				[a.value, b.value, a.mask, b.mask],  
				ForAll([x, y], f)
			)
		s.add(Not(f))
		
		if(s.check() == unsat):
			print(" SUCCESS.")
		else:
			print("FAILED.")
			print(s.model())

	@staticmethod
	def check_tnum_and():
		"""
		F: (x is_in_tnum a) AND (y is_in_tnum b) 
		-> (x & y) is_in_tnum (tnum_and(a, b))
		"""
		print("\nVerifying correctness of [tnum_and] for tnums of width [{}] ... ".format(BITVEC_WIDTH), 
			end="", flush=True)
		
		s = SolverFor("QF_BV")
		a = Tnum.new_tnum_from_name('a')
		b = Tnum.new_tnum_from_name('b')
		res = Tnum.new_tnum_from_name('res')
		x = BitVec('x', BITVEC_WIDTH)
		y = BitVec('y', BITVEC_WIDTH)

		f = Implies(
				And(Tnum.is_wellformed(a), 
					Tnum.is_wellformed(b), 
					Tnum.is_in_tnum(x, a), 
					Tnum.is_in_tnum(y, b),
					Tnum.tnum_and(a, b, res)
				), 
				And(Tnum.is_wellformed(res), 
					Tnum.is_in_tnum(x & y, res)
			)
		)

		f = ForAll(
				[a.value, b.value, a.mask, b.mask],  
				ForAll([x, y], f)
			)
		s.add(Not(f))
		
		if(s.check() == unsat):
			print(" SUCCESS.")
		else:
			print("FAILED.")
			print(s.model())

	@staticmethod
	def check_tnum_or():
		"""
		F: (x is_in_tnum a) AND (y is_in_tnum b) 
		-> (x | y) is_in_tnum (tnum_or(a, b))
		"""
		print("\nVerifying correctness of [tnum_or] for tnums of width [{}] ... ".format(BITVEC_WIDTH), 
			end="", flush=True)
		
		s = SolverFor("QF_BV")
		a = Tnum.new_tnum_from_name('a')
		b = Tnum.new_tnum_from_name('b')
		res = Tnum.new_tnum_from_name('res')
		x = BitVec('x', BITVEC_WIDTH)
		y = BitVec('y', BITVEC_WIDTH)

		f = Implies(
				And(Tnum.is_wellformed(a), 
					Tnum.is_wellformed(b), 
					Tnum.is_in_tnum(x, a), 
					Tnum.is_in_tnum(y, b),
					Tnum.tnum_or(a, b, res)
				), 
				And(Tnum.is_wellformed(res), 
					Tnum.is_in_tnum(x | y, res)
			)
		)

		f = ForAll(
				[a.value, b.value, a.mask, b.mask],  
				ForAll([x, y], f)
			)
		s.add(Not(f))
		
		if(s.check() == unsat):
			print(" SUCCESS.")
		else:
			print("FAILED.")
			print(s.model())

	@staticmethod
	def check_tnum_xor():
		"""
		F: (x is_in_tnum a) AND (y is_in_tnum b) 
		-> (x ^ y) is_in_tnum (tnum_xor(a, b))
		"""
		print("\nVerifying correctness of [tnum_xor] for tnums of width [{}] ... ".format(BITVEC_WIDTH), 
			end="", flush=True)
		
		s = SolverFor("QF_BV")
		a = Tnum.new_tnum_from_name('a')
		b = Tnum.new_tnum_from_name('b')
		res = Tnum.new_tnum_from_name('res')
		x = BitVec('x', BITVEC_WIDTH)
		y = BitVec('y', BITVEC_WIDTH)

		f = Implies(
				And(Tnum.is_wellformed(a), 
					Tnum.is_wellformed(b), 
					Tnum.is_in_tnum(x, a), 
					Tnum.is_in_tnum(y, b),
					Tnum.tnum_xor(a, b, res)
				), 
				And(Tnum.is_wellformed(res), 
					Tnum.is_in_tnum(x ^ y, res)
			)
		)

		f = ForAll(
				[a.value, b.value, a.mask, b.mask],  
				ForAll([x, y], f)
			)
		s.add(Not(f))
		
		if(s.check() == unsat):
			print(" SUCCESS.")
		else:
			print("FAILED.")
			print(s.model())

	@staticmethod
	def check_tnum_lshift():
		"""
		F: (x is_in_tnum a) -> (x << sh) is_in_tnum (tnum_lshift(a, sh))
		"""
		print("\nVerifying correctness of [tnum_lshift] for tnums of width [{}] ... ".format(BITVEC_WIDTH), 
			end="", flush=True)
		
		s = SolverFor("QF_BV")
		a = Tnum.new_tnum_from_name('a')
		res = Tnum.new_tnum_from_name('res')
		sh = BitVec('sh', BITVEC_WIDTH)
		x = BitVec('x', BITVEC_WIDTH)
		y = BitVec('y', BITVEC_WIDTH)

		f = Implies(
				And(Tnum.is_wellformed(a),  
					Tnum.is_in_tnum(x, a), 
					Tnum.tnum_lshift(a, sh, res)
				), 
				And(Tnum.is_wellformed(res), 
					Tnum.is_in_tnum(x << sh, res)
			)
		)

		f = ForAll(
				[a.value, a.mask],  
				ForAll([x, y], f)
			)
		s.add(Not(f))
		
		if(s.check() == unsat):
			print(" SUCCESS.")
		else:
			print("FAILED.")
			print(s.model())

	@staticmethod
	def check_tnum_rshift():
		"""
		F: (x is_in_tnum a) -> (x >> sh) is_in_tnum (tnum_rshift(a, sh))
		"""
		print("\nVerifying correctness of [tnum_rshift] for tnums of width [{}] ... ".format(BITVEC_WIDTH), 
			end="", flush=True)
	
		s = SolverFor("QF_BV")
		a = Tnum.new_tnum_from_name('a')
		res = Tnum.new_tnum_from_name('res')
		sh = BitVec('sh', BITVEC_WIDTH)
		x = BitVec('x', BITVEC_WIDTH)
		y = BitVec('y', BITVEC_WIDTH)

		f = Implies(
				And(Tnum.is_wellformed(a),  
					Tnum.is_in_tnum(x, a), 
					Tnum.tnum_rshift(a, sh, res)
				), 
				And(Tnum.is_wellformed(res), 
					Tnum.is_in_tnum(LShR(x, sh), res)
			)
		)

		f = ForAll(
				[a.value, a.mask],  
				ForAll([x, y], f)
			)
		s.add(Not(f))
		
		if(s.check() == unsat):
			print(" SUCCESS.")
		else:
			print("FAILED.")
			print(s.model())

	def check_tnum_arshift():
		"""
		F: (x is_in_tnum a) -> (x >> sh) is_in_tnum (tnum_arshift(a, sh))
		"""
		print("\nVerifying correctness of [tnum_arshift] for tnums of width [{}] ... ".format(BITVEC_WIDTH), 
			end="", flush=True)
		
		s = SolverFor("QF_BV")
		a = Tnum.new_tnum_from_name('a')
		res = Tnum.new_tnum_from_name('res')
		sh = BitVec('sh', BITVEC_WIDTH)
		x = BitVec('x', BITVEC_WIDTH)
		y = BitVec('y', BITVEC_WIDTH)

		f = Implies(
				And(Tnum.is_wellformed(a),  
					Tnum.is_in_tnum(x, a), 
					Tnum.tnum_arshift(a, sh, res)
				), 
				And(Tnum.is_wellformed(res), 
					Tnum.is_in_tnum(x >> sh, res)
			)
		)

		f = ForAll(
				[a.value, a.mask],  
				ForAll([x, y], f)
			)
		s.add(Not(f))
		
		if(s.check() == unsat):
			print(" SUCCESS.")
		else:
			print("FAILED.")
			print(s.model())

	@staticmethod
	def check_tnum_kern_mul():
		"""
		F: (x is_in_tnum a) AND (y is_in_tnum b) 
		-> (x * y) is_in_tnum (tnum_mul(a, b))
		"""
		print("\nVerifying correctness of [tnum_kern_mul] for tnums of width [{}] ... ".format(BITVEC_WIDTH), 
			end="", flush=True)
		
		s = SolverFor("QF_BV")
		a = Tnum.new_tnum_from_name('a')
		b = Tnum.new_tnum_from_name('b')
		res = Tnum.new_tnum_from_name('res')
		x = BitVec('x', BITVEC_WIDTH)
		y = BitVec('y', BITVEC_WIDTH)

		f = Implies(
				And(Tnum.is_wellformed(a), 
					Tnum.is_wellformed(b), 
					Tnum.is_in_tnum(x, a), 
					Tnum.is_in_tnum(y, b),
					Tnum.tnum_kern_mul(a, b, res)
				), 
				And(Tnum.is_wellformed(res), 
					Tnum.is_in_tnum(x * y, res)
			)
		)

		f = ForAll(
				[a.value, b.value, a.mask, b.mask],  
				ForAll([x, y], f)
			)
		s.add(Not(f))
		
		if(s.check() == unsat):
			print(" SUCCESS.")
		else:
			print("FAILED.")
			print(s.model())

	@staticmethod
	def check_tnum_our_mul():
		"""
		F: (x is_in_tnum a) AND (y is_in_tnum b) 
		-> (x * y) is_in_tnum (tnum_our_mul(a, b))
		"""
		print("\nVerifying correctness of [tnum_our_mul] for tnums of width [{}] ... ".format(BITVEC_WIDTH), 
			end="", flush=True)
		
		s = SolverFor("QF_BV")
		a = Tnum.new_tnum_from_name('a')
		b = Tnum.new_tnum_from_name('b')
		res = Tnum.new_tnum_from_name('res')
		x = BitVec('x', BITVEC_WIDTH)
		y = BitVec('y', BITVEC_WIDTH)

		f = Implies(
				And(Tnum.is_wellformed(a), 
					Tnum.is_wellformed(b), 
					Tnum.is_in_tnum(x, a), 
					Tnum.is_in_tnum(y, b),
					Tnum.tnum_our_mul(a, b, res)
				), 
				And(Tnum.is_wellformed(res), 
					Tnum.is_in_tnum(x * y, res)
			)
		)

		f = ForAll(
				[a.value, b.value, a.mask, b.mask],  
				ForAll([x, y], f)
			)
		s.add(Not(f))
		
		if(s.check() == unsat):
			print(" SUCCESS.")
		else:
			print("FAILED.")
			print(s.model())

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--bitwidth", help="bitvector width", type=int, 
		required=True)
	parser.add_argument("--op", 
		help="tnum operation: lshift|rshift|arshift|and|or|xor|add|sub|mul|our_mul", 
		type=str, 
		required=True)

	args=parser.parse_args()
	BITVEC_WIDTH = args.bitwidth

	# shift
	if (args.op == 'lshift'):
		TnumOpsVerifier.check_tnum_lshift()
	elif (args.op == 'rshift'):
		TnumOpsVerifier.check_tnum_rshift()
	elif (args.op == 'arshift'):
		TnumOpsVerifier.check_tnum_arshift()
	# bitwise
	elif (args.op == 'and'):
		TnumOpsVerifier.check_tnum_and()
	elif (args.op == 'or'):
		TnumOpsVerifier.check_tnum_or()
	elif (args.op == 'xor'):
		TnumOpsVerifier.check_tnum_xor()
	# arithmetic
	elif (args.op == 'add'):
		TnumOpsVerifier.check_tnum_add()
	elif (args.op == 'sub'):
		TnumOpsVerifier.check_tnum_sub()
	elif (args.op == 'mul'):
		TnumOpsVerifier.check_tnum_kern_mul()
	elif (args.op == 'our_mul'):
		TnumOpsVerifier.check_tnum_our_mul()
	else:
		parser.print_help()
