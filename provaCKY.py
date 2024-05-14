"""
Context Free Grammar: 
We are given a Context Free Grammar G = (V, X, R, S) and a string w, where:

V is a finite set of variables or non-terminal symbols,
X is a finite set of terminal symbols,
R is a finite set of rules,
S is the start symbol, a distinct element of V, and
V and X are assumed to be disjoint sets.
"""

# Python implementation for the
# CYK Algorithm

# Non-terminal symbols
non_terminals = ["S", "A", "B"]
terminals = ["a", "b"]

# Rules of the grammar
R = {
	"S": [["A", "B"]],
    "C": [["S", "B"]],
	"A": [["a"]],
	"B": [["b"]],
	}

# Function to perform the CYK Algorithm
def cykParse(w):
	n = len(w)
	print(n)
	
	# Initialize the table
	T = [[set([]) for j in range(n)] for i in range(n)]

	# Filling in the table
	for j in range(0, n):

		# Iterate over the rules
		for lhs, rule in R.items():
			for rhs in rule:
				
				# If a terminal is found
				if len(rhs) == 1 and \
				rhs[0] == w[j]:
					T[j][j].add(lhs)

		for i in range(j, -1, -1): 
			
			# Iterate over the range i to j + 1 
			for k in range(i, j + 1):	 

				# Iterate over the rules
				for lhs, rule in R.items():
					for rhs in rule:
						
						# If a terminal is found
						if len(rhs) == 2 and \
						rhs[0] in T[i][k] and \
						rhs[1] in T[k + 1][j]:
							T[i][j].add(lhs)

	# If word can be formed by rules 
	# of given grammar
	if len(T[0][n-1]) != 0:
		print("True")
	else:
		print("False")

    
        
	
# Driver Code

# Given string
w = "abba"

# Function Call
cykParse(w)
