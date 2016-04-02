from automaton import AutomatonConverter, NFA


def enfa_from_file(file_name):
	pass

def main():
	conv = AutomatonConverter()

	# dummy nfa
	nfa = NFA()
	nfa.add_states(['q0', 'q1', 'q2'])
	nfa.alphabet = set(['a', 'b'])
	nfa.transitions['q0']['a'] = set(['q0','q1'])
	nfa.transitions['q0']['b'] = set(['q2'])
	nfa.transitions['q1']['a'] = set(['q0'])
	nfa.transitions['q1']['b'] = set(['q1','q2'])
	nfa.transitions['q2']['a'] = set(['q1'])
	nfa.transitions['q2']['b'] = set(['q0','q2'])
	nfa.initial_state = 'q0'
	nfa.terminal_states = set(['q1'])
	dfa = conv.dfa_from_nfa(nfa)
	dfa.print_to_file("dfa.txt")

if __name__ == '__main__':
	main()