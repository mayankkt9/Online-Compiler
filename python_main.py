#!/usr/bin/env python3
from nltk.tokenize import sent_tokenize, word_tokenize 
from pyswip import Prolog
import sys

def lexer_job():
	str = open('sourcecode.jvs', 'r').read()
	str1 = word_tokenize(str)
	lex=""
	lex+='['
	for i in range(0,len(str1)):
		if i>1 and str1[i]=='=' and str1[i-1]==':':
			continue;
		if str1[i]==':' and str1[i+1]=='=':
			lex+=str1[i]+str1[i+1]
			i+=2
		elif str1[i]=='(':
			lex+='('
		elif str1[i]==')':
			lex+=')'
		else:
			lex+=str1[i]
		lex+=','
	lex = lex[:-1]
	lex+=']'
	return lex

def create_parse_tree(lex):
	prolog.consult("assignSemantics.pl")
	query1 = "program(P,"+lex+",[])."
	parsetree = prolog.query(query1)
	return parsetree

def give_semantics(parsetree):
	x=""
	for sol in parsetree:
		x=sol["P"]
	xval = sys.argv[1]
	yval = sys.argv[2]
	query2 = "program_eval("+x+", "+xval+","+yval+", Z)"
	ans = prolog.query(query2)
	z=""
	for sol in ans:
		z=sol["Z"]
		print(sol["Z"])

prolog = Prolog()
lex = lexer_job()
parse_tree = create_parse_tree(lex)
give_semantics(parse_tree)

#program(P, [begin, var, z, ; , var, x, ;, z, :=, x, end, .], []), write(P), program_eval(P, 2, 3, Z).

