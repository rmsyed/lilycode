import re
import random
import math
import sys
import argparse



class Lily():

	#............. reserved objects .................
	reservedObjs = []
	handle = open("webapis.txt","r")
	reservedList = handle.read().split("\n")
	for i in range(0,len(reservedList)):
		if len(reservedList[i])>1:
			reservedObjs.append(reservedList[i])
	handle.close()

	#............. reserved keywords....................
	reservedWords = ["break","case","class","catch","const","continue","debugger","default","delete","do","else","export","extends","finally","for","function","if","import","in","instanceof","let","new","return","super","switch","this","throw","try","typeof","var","void","while","with","yield"]
	twoahead = ["in","instanceof"]
	reservedStrVars = []
	reservedFuncs = ["decodeURI","decodeURIComponent","encodeURI","encodeURIComponent","escape","eval","isFinite","isNaN","Number","parseFloat","parseInt","String","unescape","alert","atob","blur","btoa","clearInterval","clearTimeout","close","confirm","createPopup","focus","getComputedStyle","getSelection","matchMedia","moveBy","moveTo","open","print","prompt","resizeBy","resizeTo,","scroll,","scrollBy,","scrollTo,","setInterval,","setTimeout,","stop"]
	reservedClasses= ["Object","Function","Boolean","Error","EvalError","InternalError","RangeError","ReferenceError","SyntaxError","TypeError","URIError","String","RegExp","Number","Math","Date","Window","window","Array","document"]



	#............ library of random set of words.............
	handle = open("junkwords.txt","r")
	junkWords = handle.read().split("\n")
	handle.close()

	#............. BEGIN................

	#....... in renaming the variables, we need to make sure that we don't rename any global functions 
	# or objects like "document", "navigator" and "String". Now, 
	# if we don't know ahead of time what the full list of reserved objects are, we have to simply apply some heuristics. For example, if a 
	# new instance of the class is being created but no function for that class has been defined, we know that this is in-built.
	# Secondly, if we notice that some property of such and such variable is being accessed,
	# we assume that is only possible if it has been defined beforehand




	#............. Load the source javascript file..................
	def loadFile(self, filename):
		handle = open(filename, "r")
		self.truestr = handle.read()
		handle.read()




	#............... Pseudo-random replacement of numbers in source file with numerical expressions.............

	def computeNum(self,basenum):
		randNum = random.random()
		if basenum==int(basenum):
			basenum = int(basenum)
		if randNum<=0.5 or (not basenum==int(basenum)):
			# leave the number as is
			return str(basenum)
		else:
			# generate a mathematical substitute
			# options:
			# 1. addition
			# 2. logical XOR
			# 3. logical NOT
			if (randNum>0.5 and randNum<=0.7):
				# addition
				lowerNum = basenum - int(random.random()*70)
				upperNum = basenum-lowerNum
				return "("+str(lowerNum)+"+"+str(upperNum)+")"
			if randNum>0.7 and randNum<=0.85:
				# xor
				basenum = int(basenum)
				rander = int(random.random()*basenum)
				basedigits = int(math.log(basenum+2,2)+1)
				randbin = bin(rander)[2:].zfill(basedigits)
				xorval = bin(0)[2:].zfill(basedigits)
				destbin = bin(basenum)[2:].zfill(basedigits)
				for i in range(0,len(randbin)):
					# at each level, if the destination was a 1 but the rander was a 0, the xor should be 1.
					if randbin[i]==destbin[i]:
						xorval = xorval[0:i]+"0"+xorval[i+1:]
					else:
						xorval = xorval[0:i]+"1"+xorval[i+1:]
						
				return "("+str(rander)+"^"+str(int(xorval,2))+")"
			if randNum>0.85 and randNum<=1:
				# not
				basenum = int(basenum)
				notval = str((basenum+1)*-1)	
				return "(~"+notval+")"
				
				
				

	uninum = 18
	createdLilies = []
	createdJunks = []
	#......... generates Lily variables .............
	def generateLily(self):
		lilystr = bin(self.uninum)[2:]
		lilystr = lilystr.replace("0","l").replace("1","I")
		self.uninum+=1
		self.createdLilies.append(lilystr)
		return lilystr



	#.......... check if a given word is already Lilied	
	def isLily(self, checkWord):
		for i in range(0,len(checkWord)):
			if not ((checkWord[i]=="I") or (checkWord[i]=="l")):
				return False
		return True


	def __init__(self, input_loc, output_loc, html_loc):
		self.strFuncName = self.generateLily()
		self.loadFile(input_loc)
		self.removeTabs()
		self.replaceStrings()
		self.removeComments()
		self.removeLines()
		self.removeWhitespace()
		self.replaceProps()

		self.injectDummies()
		self.replaceStrings()
		self.replaceProps()

		self.replaceVars()
		self.replaceNums()
		self.baseInjections()
		self.saveToFile(output_loc, html_loc)
		
		

	#.............. remove all tabs ...................
	def removeTabs(self):
		self.truestr = self.truestr.replace(chr(9),chr(32))
		





	def str_regex(self, match):
		#print (match)
		#print (match.group(0))
		#print (match.group(1))
		#print (match.group(2))
		#print (match.group(3))
		#print ("WWW")
		basematch = match
		prematch = match.group(1)
		match = match.group(3)
		hexarr = ""
		strPart = match
		if strPart:
			for i in range(0,len(strPart)):
				hexarr += str(ord(strPart[i]))+","
			hexarr = hexarr[:-1]
		else:
			hexStr = prematch+basematch.group(2)+basematch.group(2)
			return hexStr

		# inject the hex replacement

		hexStr = prematch+ self.strFuncName+"(["+hexarr+"])"
		return hexStr



	#............. replace all strings...................
	def replaceStrings(self):
		#self.truestr = re.sub(r"(\"|\')(.*?)\1",self.str_regex, self.truestr)
		#self.truestr = re.sub(r"(^|[^\\])(\"|\')\2", self.pre_str_regex, self.truestr)
		#self.truestr = re.sub(r"(^|[^\\])(\"|\')\2\2(.*?[^\\])?\2\2\2",self.str_regex, self.truestr)
		self.truestr = re.sub(r"(^|[^\\])(\"|\')\2\2(.*?)(?<!\\)\2\2\2",self.str_regex, self.truestr)		
		self.truestr = re.sub(r"(^|[^\\])(\"|\')(.*?)(?<!\\)\2",self.str_regex, self.truestr)

	# we have to replace the strings FIRST otherwise the whitespace remover could erroneously remove string character's whitespace









	#................. remove all comments...........................
	#..... To avoid unintentionally modifying strings that use comment symbols, the replaceStrings() function
	#..... MUST be called first


	def removeComments(self):
		#... get rid of the single-line comments
		self.truestr = re.sub(r"\/\/.+([\r\n]+)", "\\1", self.truestr)

		#... get rid of the multi-line comments (assuming single-line format)
		self.truestr = re.sub(r"\/\*[^\r|\n]*?\*\/", "", self.truestr)

		#... get rid of the multi-line comments (assuming multi-line format)
		self.truestr = re.sub(r"\/\*(.|\r|\n)*?([\r|\n]+)(.|\r|\n)*?\*\/", "\n", self.truestr)







	#............... remove all lines...................
	#.............. we make the assumption that all "if" statements are constructed using {}
	def removeLines(self):
		i = 0
		self.truestr = re.sub(r"([;|}|{]{1})[ ]*[\r|\n]+","\\1", self.truestr)






		
	def removeWhitespace(self):
		# we can simply remove ALL double or more whitespace
		self.truestr = re.sub(r"[ ]{2,}"," ", self.truestr)
		





	def props_regex(self, match):
		match = match.group()
		#preglyph = match[0]
		match = match[1:]
		hexarr = ""
		keyword = match
		for k in range(0,len(keyword)):
			hexarr += str(ord(keyword[k]))+","
		hexarr = hexarr[:-1]
		hexStr = "["+self.strFuncName+"(["+hexarr+"])" + "]"
		return hexStr




	#............... replace property names as bracketed strings...............
	def replaceProps(self):
		self.truestr = re.sub(r"\.[A-Za-z_][A-Za-z0-9_]+", self.props_regex, self.truestr)








	#................ Creates a junk variable and assigns it either a number or a string
	def genjunkvar(self):
		dummyvar = self.generateLily()
		randNum = random.random()
		# should the dummy be a string or a number?
		if randNum<0.5:
			dummyval = "'"+self.junkWords[int(random.random()*(len(self.junkWords)-1))]+"'"
			if random.randint(0,5)>0:
				dummyval = self.stringLibrary(dummyval)
		else:
			dummyval = int(random.random()*1600)
			
		return [dummyvar, str(dummyval)]
		
		
		
		

	#... defines all the string functions and the parameters (and restrictions) they accept
	#... this allows us to arbitrarily use any string functions in our junk variables to add authenticity
	def stringLibrary(self, basestr):
		# each function is defined by <func_name><arg_type1>,<restrict1>,<arg_type2>,<restrict2>...
		commonDelims =[":"," ",",",";","*","\\n","\\r","\\t"]
		func1 = ["charAt","num","(tinyint)"]
		func2 = ["indexOf","string",""]
		func3 = ["indexOf","string","","num","(tinyint)"]
		func4 = ["substr","num","(tinyint)"]
		func5 = ["substr","num","(tinyint)","num","(tinyint)"]
		func6 = ["toLowerCase"]
		func7 = ["split","string","(delim)"]
		func8 = ["lastIndexOf","string",""]
		
		allfuncs = [func1,func2,func3,func4,func5,func6,func7,func8]
		selfunc = allfuncs[random.randint(6,len(allfuncs)-1)]
		
		netres = basestr +"."+selfunc[0]+"("
		i=1
		while i<len(selfunc):
			if i%2==1:
				argType = selfunc[i]
				argRestrict = selfunc[i+1]
				if argType=="num":
					if argRestrict=="(tinyint)":
						argval = str(random.randint(0,16))
						netres+=argval+","
				if argType=="string":
					if argRestrict=="":
						netres += "'"+self.junkWords[random.randint(0,len(self.junkWords)-1)]+"',"
					if argRestrict=="(delim)":
						netres += "'"+commonDelims[random.randint(0,len(commonDelims)-1)]+"',"
			i+=1
		
		# close this function
		if len(selfunc)==1:
			# this function has no arguments. seal it
			netres += ")"
		else:
			netres = netres[:-1]+")" # remove trailing comma
			
		# return encapsulated string
		return netres
		
		
		
		
		
	def generateIf(self):
		if len(self.createdJunks)>0:
			dummyvar = self.createdJunks[random.randint(0,len(self.createdJunks)-1)]
		else:
			dummyvar = self.generateLily()
		randNum = random.random()
		allopsNum = ["<","<=",">",">="]
		# should the dummy be a string or a number?
		if randNum<0.5:
			dummyval = "'"+self.junkWords[int(random.random()*(len(self.junkWords)-1))]+"'"
			if random.randint(0,1)==0:
				dummyOp = "=="
			else:
				dummyOp = "!="
			dummyval
		else:
			dummyval = int(random.random()*16000)
			dummyOp = allopsNum[random.randint(0,3)]
			
		return [dummyvar, dummyOp, str(dummyval)]
		
		



	def junk_regex(self,match):
		if random.random()>0.8:
			[dummyvar, dummyOp, dummyval] = self.generateIf()
			[junkvar, junkval] = self.genjunkvar()
			self.createdJunks.append(junkvar)
			randnum = random.randint(0,1)
			junkinject = junkvar + "="+junkval+";"
			if randnum==0:
				junkinject += self.generateLily() + "=("+junkvar + "=="+junkval+"?"+str(random.randint(0,300)) + ":"+str(random.randint(0,10))+");"
			elif randnum==1:
				lilvar = self.generateLily()
				self.createdJunks.append(lilvar)
				junkinject += "for("+lilvar+"=0;"+lilvar+"=="+junkvar+";"+lilvar+"++){"+dummyvar+"="+junkval+";}"
			
			#... decide whether or not to encapsulate this in an if statement
			if random.randint(0,1)==0:
				#print ";"+dummyvar+"='';if("+dummyvar+dummyOp+dummyval+"){"+junkinject+ "}"
				self.createdJunks.append(dummyvar)
				return ";"+dummyvar+"='';if("+dummyvar+dummyOp+dummyval+"){"+junkinject+ "};"
			else:
				#print ";"+junkinject
				return ";"+junkinject+";"

		else:
			return ";"


	def junk_regex_pre(self,match):
		match = match.group()
		match = match.replace(";", "LILY:::TEMP")
		return match


	#.............. inject junk variables.................
	def injectDummies(self):
		self.truestr = re.sub(r"for[ |\t]*?\(.*?;.*?;.*\)", self.junk_regex_pre ,self.truestr)
		self.truestr = re.sub(r";", self.junk_regex, self.truestr)
		self.truestr = self.truestr.replace("LILY:::TEMP", ";")






	#............... replace the variables by enforcing lily............
	#........... for each variable we find, we must replace ALL instances that have that variable name in a consistent way. So we will keep a bank of all the names we have found thus far and the mapping the identifier has been assigned. Then, we come across a new keyword, if it already has a mapping, just apply it.

	replacedClasses = {}
	mappings = {}

	def var_regex(self, match):
		match = match.group()
		space1 = ""
		space2 = ""
		if match in self.reservedClasses:
			if match in self.replacedClasses:
				return space1+self.replacedClasses[match]+space2
			else:
				newname = self.generateLily()
				self.replacedClasses[match] = newname
				return space1+self.replacedClasses[match]+space2


		#... check if this variable is already Lilied
		if self.isLily(match):
			return space1+match+space2


		#... this variable has not been renamed yet. Let's give it a go.
		keyword = match
		if not keyword in self.mappings:
			if (not keyword in self.reservedWords) and (not keyword in self.reservedFuncs) and (not keyword in self.reservedClasses) and (not keyword in self.reservedObjs) and (not keyword in self.reservedStrVars):
				self.mappings[keyword] = self.generateLily()

		#... if this variable was able to be Lilied or if it already was done previously
		if keyword in self.mappings:
			return space1+self.mappings[keyword]+space2


		return space1+match+space2




	def replaceVars(self):
		#... try finding a variable name to replace
		self.truestr = re.sub(r"[A-Za-z_][A-Za-z0-9_]+\b", self.var_regex, self.truestr)





	#.............. replace numbers with expressions...................
	def replaceNums(self):		
		# for each number we locate, we will replace it
		i=0
		numIndex = -1
		while i<len(self.truestr):
			selval = ord(self.truestr[i])
			isNum = False
			if (selval>=48 and selval<=57):
				isNum = True
				
			if numIndex==-1:
				if isNum:
					# this is a valid number. Is this the start of a number or is it preceded by variable terms.
					if not re.search("[A-Za-z_\$]",self.truestr[i-1]):
						# this is the start of the number
						numIndex = i
			else:
				# a number is already being accumulated. can we continue? decimals are allowed
				if not (isNum or self.truestr[i]=="."):
					# the number has ended. capture the number string
					numstr = self.truestr[numIndex:i]
					replaceNum = self.computeNum(float(numstr))
					origlen = len(self.truestr)
					self.truestr = self.truestr[0:numIndex]+replaceNum+self.truestr[i:]
					i+=(len(self.truestr)-origlen)
					numIndex = -1
					
			i+=1






	#................ create the base injections......................
	def baseInjections(self):
		funcName = self.strFuncName
		funcArg = self.generateLily()
		funcIter = self.generateLily()
		funcRes = self.generateLily()
		#....... create string rendering function ........
		basestr = "function "+funcName+"("+funcArg+"){"
		basestr += funcRes+"='';"
		fromCode = "\\x66\\x72\\x6f\\x6d\\x43\\x68\\x61\\x72\\x43\\x6f\\x64\\x65"
		basestr += "for(var "+funcIter+"=0;"+funcIter+"<"+funcArg+".length;"+funcIter+"++){"
		basestr += funcRes+"+=String['"+fromCode+"']("+funcArg+"["+funcIter+"]);"
		basestr += "}return "+funcRes+";}"
		#......... create replaced classes ............
		tempstr = ""
		for key,val in self.replacedClasses.iteritems():
			hexstr = ""
			for i in range(0,len(key)):
				hexstr += str(ord(key[i]))+","
			hexstr = hexstr[:-1]
			tempstr += "var "+val+"=eval("+self.strFuncName+"(["+hexstr+"]));"
		basestr+=tempstr
		
		self.truestr = basestr+self.truestr









	#................... output to file.......................
	def saveToFile(self,filename, filename_html):
		#print "\n\n....................\nWriting file\n...................\n\n"+self.truestr
		if filename_html:
			netres = "<html><head></head><body><script type='text/javascript'>"+self.truestr+"</script></body></html>"
			handle = open(filename_html,"w")
			handle.write(netres)
			handle.close()
		netres = self.truestr
		handle = open(filename,"w")
		handle.write(netres)
		handle.close()



		

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", help="location of input javascript file")
	parser.add_argument("-o", "--output", help="location of output javascript file", nargs="?")
	parser.add_argument("-html", "--output_html", help="location of output html/javascript file", nargs="?")
	args = parser.parse_args()
	inloc = args.input
	if args.output:
		outloc = args.output
	else:
		outloc = inloc+"(2).js"
	html_loc = args.output_html

	lilyinst = Lily(inloc, outloc,html_loc)


