# -*- coding: utf-8 -*-
# numero de estados, cardinalidade do alfabeto (n,k)
# k-1 nomes seperados por ;
# n linhas de k colunas+1 colunas, contendo:
# nome do estado e as transições, separados por ;

import copy

class eNFA(object):
	def __init__(self, states, alphabet,
				transitions, initial_state,
				terminal_states):

		self.states = set(states)
		self.alphabet = set(alphabet)
		self.transitions = transitions  # map de estados pra um map de alphabeto - set de estados 
		self.initial_state = initial_state
		self.terminal_states = terminal_states

	def e_closure(self, state):
		e_clo = set()
		#e_clo.add(state)

		stack = []
		stack.append(state)
		while(len(stack) > 0):
			curr = stack.pop()

			if 'e' not in self.transitions[curr].keys(): continue

			for e_tr in self.transitions[curr]['e']:
				if (e_tr not in e_clo):
					stack.append(e_tr)
					e_clo.add(e_tr)

		return e_clo

class NFA(object):
	def __init__(self):
		self.states = set()
		self.alphabet = set()
		self.transitions = {} # map de estados pra um map de alphabeto - set de estados 
		self.initial_state = None
		self.terminal_states = set()

	def add_states(self, states):
		self.states = set(states)
		for state in self.states:
			self.transitions[state] = {}
			for symbol in self.alphabet:
				self.transitions[state][symbol] = set()

class DFA(object):
	def __init__(self):
		self.states = set()
		self.alphabet = set()
		self.transitions = {} # map de estados pra um map de alphabeto - estado
		self.initial_state = None
		self.terminal_states = set()

	def output_to_file(self, filename):
		print "Printing states:"
		for state in self.states:
			print state

		for state in self.transitions:
			for symbol in self.alphabet:
				print "State: " + str(state) + " - " + symbol + " - " + str(self.transitions[state][symbol]) 

class AutomatonConverter(object):
	def dfa_from_enfa(self, enfa):
		nfa = self.nfa_from_enfa(enfa)
		dfa = self.dfa_from_nfa(nfa)

		return dfa

	def nfa_from_enfa(self, enfa):
		nfa = NFA()
		nfa.states = enfa.states
		nfa.alphabet = enfa.alphabet
		nfa.initial_state = enfa.initial_state
		nfa.terminal_states = enfa.terminal_states

		nfa.transitions = copy.deepcopy(enfa.transitions)
		
		#Remove eps transitions
		for s, tr in nfa.transitions.iteritems():
			del tr['e']

		for s in enfa.states:
			e_closure = enfa.e_closure(s)

			#Check if s is terminal state
			for ter_s in enfa.terminal_states:
				if ter_s in e_closure:
					nfa.terminal_states.append(s)
					break

			for s_e in e_closure:
				for symbol, s_trs in enfa.transitions[s_e].iteritems():
					if (symbol == 'e'): continue
					for s_tr in s_trs:
						nfa.transitions[s][symbol].append(s_tr)
				
		return nfa

	def dfa_from_nfa(self, nfa):
		dfa = DFA()
		dfa.initial_state = frozenset([nfa.initial_state])
		dfa.states = set([dfa.initial_state])
		dfa.alphabet = nfa.alphabet
		unprocessed_states = dfa.states.copy()	
		while len(unprocessed_states) > 0: 
			current_dfa_state = unprocessed_states.pop()
			dfa.transitions[current_dfa_state] = {}
			
			for symbol in dfa.alphabet: 
				next_states = set()
				for nfa_state in current_dfa_state:
					next_states.update(nfa.transitions[nfa_state][symbol])
				
				dfa.transitions[current_dfa_state][symbol] = next_states

				if not next_states in dfa.states: 
					dfa.states.add(frozenset(next_states))
					unprocessed_states.add(frozenset(next_states))

		for state in dfa.states: 
			if state and len(state & nfa.terminal_states) > 0: 
				dfa.terminal_states.update(state)
		return dfa
