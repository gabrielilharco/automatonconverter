# -*- coding: utf-8 -*-
# numero de estados, cardinalidade do alfabeto (n,k)
# k-1 nomes seperados por ;
# n linhas de k colunas+1 colunas, contendo:
# nome do estado e as transições, separados por ;

from __future__ import print_function
import copy

def setToString(varset):
	return '{{{}}}'.format(', '.join(map(repr, varset)))

class eNFA(object):
	def __init__(self, states, alphabet,
				transitions, initial_state,
				terminal_states):

		self.states = set(states)
		self.alphabet = set(alphabet)
		# map de (estados -> map de (alphabeto -> set de estados))
		self.transitions = transitions
		self.initial_state = initial_state
		self.terminal_states = terminal_states

	def e_closure(self, state):
		e_clo = set()
		#e_clo.add(state)

		stack = []
		stack.append(state)
		while len(stack) > 0:
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
		# map de (estados -> map de (alphabeto -> set de estados))
		self.transitions = {}
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
		# map de (estados -> map de (alphabeto -> estado))
		self.transitions = {}
		self.initial_state = None
		self.terminal_states = set()

	def isTerminal(self, state):
		for single in state:
			if single in self.terminal_states:
				return True
		return False

	def output_to_file(self, filename):
		# print "Printing states:"
		# for state in self.states:
		# 	print state

		# for state in self.transitions:
		# 	for symbol in self.alphabet:
		# 		print "State: " +str(state) + \
		# 		" - " + symbol + " - " + \
		# 		str(self.transitions[state][symbol])
		
		basesize = 15
		columnwidth = basesize + 1
		width = columnwidth * (len(self.alphabet) + 1)
		print ("Output DFA")
		print (width * "-")
		print ((width-columnwidth) / 2 * "-" + \
			"Transition Table" + (width-columnwidth) / 2 * "-")
		print (width * "-")
		print ("     State     |", end="", sep = "")
		for alpha in self.alphabet:
			print("{:>{basesize}}|".format(
				alpha, basesize=basesize), end="", sep="")
		print ("\n"+ width * "-")
		for state in sorted(self.states):
			outputState = setToString(state)
			if state in self.terminal_states:
				outputState = "*" + outputState
			elif state == self.initial_state:
				outputState = "->" + outputState
			print ("{:>{basesize}}|".format(
				outputState, basesize=basesize),end="", sep = "")
			for alpha in self.alphabet:
				print("{:>{basesize}}|".format(
					setToString(self.transitions[state][alpha]),
					basesize=basesize), end="", sep="")
			print()
		print (width * "-")

class AutomatonConverter(object):
	def dfa_from_enfa(self, enfa):
		nfa = self.nfa_from_enfa(enfa)

		# print nfa.states
		# print nfa.alphabet
		# print nfa.initial_state
		# print nfa.terminal_states
		# print nfa.transitions

		dfa = self.dfa_from_nfa(nfa)

		return dfa

	def nfa_from_enfa(self, enfa):
		nfa = NFA()
		nfa.add_states(enfa.states)
		nfa.alphabet = enfa.alphabet
		nfa.alphabet.remove('e')
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
					if symbol == 'e': continue
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
			if state and len(state & set(nfa.terminal_states)) > 0:
				dfa.terminal_states.add(state)
		return dfa
