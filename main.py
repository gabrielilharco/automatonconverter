from automaton import *

def enfa_from_file(fname):
	content = [line.rstrip('\n') for line in open(fname)]

	states_list = [s for s in content[0].split('\t')]
	alph_list = [s for s in content[1].split('\t')]
	initial_state = content[2].split('\t')[0]
	terminal_states = [s for s in content[3].split(';')]

	transitions = {}
	for i in range(len(states_list)):
		t_line = content[i + 4].split('\t')
		ori = states_list[i]

		transitions[ori] = {}

		for idx, t_col in enumerate(t_line):
			trs = t_col.split(';')
			
			transitions[ori][alph_list[idx]] = []
			for j in range(len(trs)):
				if trs[j] == '-': continue
				transitions[ori][alph_list[idx]].append(trs[j])
		# print states_list
		# print alph_list
		# print initial_state
		# print terminal_states
		# print transitions

	return eNFA(states_list, alph_list,
			transitions, initial_state,
			terminal_states)


def main():
	conv = AutomatonConverter()
	from sys import argv
	enfa = enfa_from_file(argv[1])

	# dummy nfa
	# nfa = NFA()
	# nfa.add_states(['q0', 'q1', 'q2'])
	# nfa.alphabet = set(['a', 'b'])
	# nfa.transitions['q0']['a'] = set(['q0','q1'])
	# nfa.transitions['q0']['b'] = set(['q2'])
	# nfa.transitions['q1']['a'] = set(['q0'])
	# nfa.transitions['q1']['b'] = set(['q1','q2'])
	# nfa.transitions['q2']['a'] = set(['q1'])
	# nfa.transitions['q2']['b'] = set(['q0','q2'])
	# nfa.initial_state = 'q0'
	# nfa.terminal_states = set(['q1'])
	# dfa = conv.dfa_from_nfa(nfa)
	# dfa.output_to_file("dfa.txt")

	dfa = conv.dfa_from_enfa(enfa)
	dfa.output_to_file("dfa.txt")

if __name__ == '__main__':
	main()