from automaton import *

def main():
	conv = AutomatonConverter()
	from sys import argv
	enfa = eNFA.get_from_file(argv[1])

	dfa = conv.dfa_from_enfa(enfa)
	dfa.output_to_file("dfa.txt")

if __name__ == '__main__':
	main()