from automaton import AutomatonConverter


def enfa_from_file(file_name):
	pass

def main():
	conv = AutomatonConverter()

	enfa = enfa_from_file("enfa.txt")
	dfa = conv.dfa_from_enfa(enfa)
	dfa.print_to_file("dfa.txt")

if __name__ == '__main__':
	main()