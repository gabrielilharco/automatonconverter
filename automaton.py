# -*- coding: utf-8 -*-
# numero de estados, cardinalidade do alfabeto (n,k)
# k-1 nomes seperados por ;
# n linhas de k colunas+1 colunas, contendo:
# nome do estado e as transições, separados por ;

class eNFA(object):
	def __init__(self):
		self.states = set()
		self.alphabet = set()
		self.transitions = {} # map de estados pra um map de alphabeto - lista de estados 
		self.initial_state = None
		self.terminal_states = set()

class NFA(object):
	def __init__(self):
		self.states = set()
		self.alphabet = set()
		self.transitions = {} # map de estados pra um map de alphabeto - lista de estados 
		self.initial_state = None
		self.terminal_states = set()

class DFA(object):
	def __init__(self):
		self.states = set()
		self.alphabet = set()
		self.transitions = {} # map de estados pra um map de alphabeto - estado
		self.initial_state = None
		self.terminal_states = set()


class AutomatonConverter(object):
	def dfa_from_enfa(self, enfa):
		nfa = nfa_from_enfa(enfa)
		dfa = dfa_from_nfa(nfa)

		return dfa

	def nfa_from_enfa(self, enfa):
		pass

	def dfa_from_nfa(self, nfa):
		pass
