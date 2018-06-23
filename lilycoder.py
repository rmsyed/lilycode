import re
import random
import math
import sys



#............. reserved objects .................
reservedObjs = []
handle = open("C:/Users/A/Documents/Michigan/University/Semester3/SI710/webapis.txt","r")
reservedList = handle.read().split("\n")
for i in range(0,len(reservedList)):
	if len(reservedList[i])>1:
		reservedObjs.append(reservedList[i])
handle.close()

#............. reserved keywords....................
reservedWords = [
"break",
"case",
"class",
"catch",
"const",
"continue",
"debugger",
"default",
"delete",
"do",
"else",
"export",
"extends",
"finally",
"for",
"function",
"if",
"import",
"in",
"instanceof",
"let",
"new",
"return",
"super",
"switch",
"this",
"throw",
"try",
"typeof",
"var",
"void",
"while",
"with",
"yield"
]

twoahead = ["in","instanceof"]

reservedStrVars = []

reservedFuncs = [
"decodeURI",
"decodeURIComponent",
"encodeURI",
"encodeURIComponent",
"escape",
"eval",
"isFinite",
"isNaN",
"Number",
"parseFloat",
"parseInt",
"String",
"unescape",

"alert",
"atob",
"blur",
"btoa",
"clearInterval",
"clearTimeout",
"close",
"confirm",
"createPopup",
"focus",
"getComputedStyle",
"getSelection",
"matchMedia",
"moveBy",
"moveTo",
"open",
"print",
"prompt",
"resizeBy",
"resizeTo",
"scroll",
"scrollBy",
"scrollTo",
"setInterval",
"setTimeout",
"stop"
]


reservedClasses= ["Object","Function","Boolean","Error","EvalError","InternalError","RangeError","ReferenceError","SyntaxError","TypeError","URIError","String","RegExp","Number","Math","Date","Window","window","Array"]

#............ library of random set of words (taken from wikipedia article).............
handle = open("junkwords.txt","r")
junkWords = handle.read().split(" ")
handle.close()




#............. BEGIN................

#....... in renaming the variables, we need to make sure that we don't rename any global functions 
#or objects like "document", "navigator" and "String". Now, 
#if we don't know ahead of time what the full list of reserved objects are, we have to simply apply some heuristics. For example, if a 
#new instance of the class is being created but no function for that class has been defined, we know that this is in-built.
#Secondly, if we notice that some property of such and such variable is being accessed,
# we know that is only possible if it has been defined beforehand



#............. Load javascript from a file..................
def loadFile(filename):
	global truestr
	handle = open(filename, "r")
	truestr = handle.read()
	handle.read()

loadFile("C:/Users/A/Documents/Michigan/University/Semester3/SI710/calc.js")




# ok, so one of the problems we see with renaming variables is in terms of evals and document elements written in the form of string expressions. Since the string contents itself are not affected, any linkages they may have with external variables can be disrupted if such variables are renamed. A crude solution would be to not rename any variables if such variables appear in strings as well.
# for now, we will list this as being one of the several limitations. In future versions, we can try to develop a way to circumvent this issue as well.




def computeNum(basenum):
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
#......... generates Lily encrypted variables .............
def generateLily():
	global uninum, createdLilies
	#lilystr = bin(uninum)[2:].zfill(10)
	lilystr = bin(uninum)[2:]
	lilystr = lilystr.replace("0","l").replace("1","I")
	uninum+=1
	createdLilies.append(lilystr)
	return lilystr


#.......... check if a given word is already lilied	
def isLily(checkWord):
	for i in range(0,len(checkWord)):
		if not ((checkWord[i]=="I") or (checkWord[i]=="l")):
			return False
	return True

	
			
strFuncName = generateLily()
	
	
	
	

#.............. remove all tabs ...................
def removeTabs():
	global truestr
	truestr = truestr.replace(chr(9),chr(32))
	
removeTabs()



#................. remove all comments...........................
def removeComments():
	global truestr
	
	# first remove the multiline comments
	commIndex = truestr.find("/*")
	while commIndex>=0:
		commEnd = truestr.find("*/", commIndex)
		if commEnd==-1:
			# this is the end of the file
			truestr = truestr[0:commIndex]
			commIndex = -1
		else:
			# there is an end to this comment. find it and remove
			origlen = len(truestr)
			truestr = truestr[0:commIndex]+truestr[commEnd+2:]
			commIndex = truestr.find("/*",commEnd+len(truestr)-origlen+1)
			
			
	
	commIndex = truestr.find("//")
	while commIndex>=0:
		commEnd = truestr.find("\r",commIndex)
		if commEnd==-1:
			commEnd = truestr.find("\n",commIndex)
			if commEnd==-1:
				# this comment exists at the last line of the file
				truestr = truestr[0:commIndex]
				commIndex = -1
			else:
				origlen = len(truestr)
				truestr = truestr[0:commIndex]+truestr[commEnd:]
				commIndex = truestr.find("//",commEnd+1+len(truestr)-origlen)
				continue
		else:
			origlen = len(truestr)
			truestr = truestr[0:commIndex]+truestr[commEnd:]
			commIndex = truestr.find("//",commEnd+1+len(truestr)-origlen)
			continue
		
removeComments()






#............... remove all lines...................
#.............. we take the assumption that all "if" statements are constructed using {}$
def removeLines():
	global truestr
	i = 0
	truestr = truestr.replace(";\r\n",";").replace(";\r",";").replace(";\n",";")
	truestr = truestr.replace("}\r\n","}").replace("}\r","}").replace("}\n","}")
	truestr = truestr.replace("{\r\n","{").replace("{\r","{").replace("{\n","{")
removeLines()






#............. replace all strings...................
def replaceStrings():
	global truestr,strFuncName, reservedStrVars
	startIndex = truestr.find(chr(34))
	while startIndex>=0:
		# check if this is an escaped quote
		if truestr[startIndex-1]=="\\":
			startIndex = truestr.find(chr(34),startIndex+1)
			continue
		
		endIndex = truestr.find(chr(34),startIndex+1)
		strPart = truestr[startIndex+1:endIndex]
		hexarr = ""
		for i in range(0,len(strPart)):
			hexarr += str(ord(strPart[i]))+","
		hexarr = hexarr[:-1]
		# inject the hex replacement
		
		#........... find out the unique keywords in this string that MIGHT have been used as a variable reference.........
		tempstr = re.sub("[^A-Za-z0-9_\$]"," ",strPart)
		prevlen = len(tempstr)+1
		while len(tempstr)>prevlen:
			prevlen = len(tempstr)
			tempstr = tempstr.replace("  "," ")
		allkeys = tempstr.split(" ")
		for i in range(0,len(allkeys)):
			if not allkeys[i] in reservedStrVars:
				reservedStrVars.append(allkeys[i])
		
		#............. end checker..........................
		
		hexStr = strFuncName+"(["+hexarr+"])"
		origlen = len(truestr)
		truestr = truestr[0:startIndex]+hexStr+truestr[endIndex+1:]
		newlen = len(truestr)
		startIndex = truestr.find(chr(34),endIndex+(newlen-origlen))
		
		
	startIndex = truestr.find(chr(39))
	while startIndex>=0:
		# check if this is an escaped quote
		if truestr[startIndex-1]=="\\":
			startIndex = truestr.find(chr(39),startIndex+1)
			continue
			
		endIndex = truestr.find(chr(39),startIndex+1)
		strPart = truestr[startIndex+1:endIndex]
		hexarr = ""
		for i in range(0,len(strPart)):
			hexarr += str(ord(strPart[i]))+","
		hexarr = hexarr[:-1]
		# inject the hex replacement
		hexStr = strFuncName+"(["+hexarr+"])"
		origlen = len(truestr)
		truestr = truestr[0:startIndex]+hexStr+truestr[endIndex+1:]
		newlen = len(truestr)
		startIndex = truestr.find(chr(39),endIndex+(newlen-origlen))
		
replaceStrings()

# we have to replace the strings FIRST otherwise the whitespace remover could erroneously remove string character's whitespace







#................. replace all regex expressions with equivalents..............
def replaceRegex():
	global truestr,strFuncName
	startIndex = truestr.find("/")
	while startIndex>0:
		# check if this is preceded by a valid variable.
		firstNonWhite = truestr[startIndex-1]
		selindex = startIndex-1
		while firstNonWhite==" ":
			selindex-=1
			firstNonWhite = truestr[selindex]
			if selindex<0:
				break
		if selindex<0:
			startIndex = truestr.find("/",startIndex+1)
			continue
		
		if re.search("[A-Za-z0-9_\$\)\}\]]",truestr[selindex]):
			# this is NOT a regex construct. ignore it
			dummy=1
		else:
			if truestr[startIndex+1]=="/":
				# this is a comment. ignore it
				dummy=1
			else:
				# this is a regex construct. replace it
				isEnder = False
				nextSlash = truestr.find("/",startIndex+1)
				while not isEnder:
					if truestr[nextSlash-1]=="\\":
						# not the end of the expression. get the next
						nextSlash = truestr.find("/",nextSlash+1)
					else:
						isEnder=True
					# possible infinite
				# what was the recovered regex?
				#print "REGEX:",truestr[startIndex:nextSlash]
				print "REGEX:",truestr[startIndex:nextSlash]
				flags = ""
				flagger=nextSlash+1
				tempstr = truestr[flagger]
				while re.search("[A-Za-z]",tempstr):
					flags+=tempstr
					flagger+=1
					tempstr = truestr[flagger]
				hexstr = ""
				basestr = truestr[startIndex+1:nextSlash]
				for i in range(0,len(basestr)):
					hexstr += str(ord(basestr[i]))+","
				hexstr = hexstr[:-1]
				
				flaghex = ""
				for i in range(0,len(flags)):
					flaghex += str(ord(flags[i]))+","
				flaghex=flaghex[:-1]
				
				regstr = "new RegExp("+strFuncName+"(["+hexstr+"])"+","+strFuncName+"(["+flaghex+"]))"
				
				# inject the replacement
				origlen = len(truestr)
				truestr = truestr[0:startIndex]+regstr+truestr[flagger:]
				nextSlash = nextSlash+(len(truestr)-origlen)
				
				startIndex = truestr.find("/",nextSlash+1)
				continue
		
		startIndex = truestr.find("/",startIndex+1)
		
replaceRegex()





	
	
	
	
	
#.............. remove all whitespace...................
def removeWhitespace():
	global truestr, reservedWords
	
	# we can simply remove ALL double or more whitespace
	maxlen = len(truestr)+1
	while len(truestr)<maxlen:
		maxlen = len(truestr)
		truestr = truestr.replace("  "," ")
	
	# loop through the string, isolate any keywords and check ahead to see if the next non-whitespace term is the start of a valid identifier or not. If its not, then we can kill all in-between whitespace.
	varStart = -1
	counter=0
	#for i in range(0,len(truestr)):
	i=0
	while i<len(truestr):
		#i = i-counter
		myord = ord(truestr[i])
		isLetter = False
		isNum = False
		if (myord>=65 and myord<=90) or (myord>=97 and myord<=122):
			isLetter = True
		if (myord>=48 and myord<=57):
			isNum = True
			
		if isLetter:
			# this is a valid identifier. do we need to initiate a new word?
			if varStart==-1:
				varStart = i
		else:
			# this is an invalid character. Shall we terminate?
			if not isNum:
				# was there even a valid string going on in the first place?
				if varStart>=0:
					#print "Found String: ", truestr[varStart:i]
					# now let's check to see if the next non-whitespace term is the valid start of a variable.
					if truestr[i]==" " and (not re.search("[A-Za-z_\$]", truestr[i+1])):
						# we can strip this whitespace
						truestr = truestr[0:i]+truestr[i+1:]
						i-=1
					# now let's check if the preceding whitespace can be stripped.
					elif truestr[varStart-1]==" " and (not re.search("[A-Za-z0-9_\$]",truestr[varStart-2])):
						# we can strip this whitespace
						truestr = truestr[0:varStart-1]+truestr[varStart:]
						i-=1
						
				varStart =  -1
		
		i+=1
	
	
	#........... remove all whitespace characters where the left and right are non-identifiers.....
	i=0
	prevWhite = 0
	origlen = len(truestr)
	while i<origlen:
		i+=1
		nextWhite = truestr.find(" ",prevWhite)
		if(nextWhite==0):
			truestr = truestr[1:]
			continue
		if not nextWhite>prevWhite:
			break
			
		prevWhite = nextWhite+1
		# we found a whitespace
		leftPart = re.search("[A-Za-z0-9_\$]",truestr[nextWhite-1])
		rightPart = re.search("[A-Za-z0-9_\$]",truestr[nextWhite+1])
		if (not leftPart) and (not rightPart):
			# we can erase this space
			truestr = truestr[0:nextWhite]+truestr[nextWhite+1:]
			prevWhite-=1
		
	# loop through the string and look if we found any whitespace. We can remove any and all whitespace that is not semantically important. The only cases where this is important is when the whitespace MUST follow some keyword like "new".
	#for i in range(0,len(reservedWords)):
	#	tempword = reservedWords[i]
	#	myindex = truestr.find(tempword, 0)
	#	while myindex>=0:
			# this word exists in the string. Does it exists as an independent term or is it part of an extended identifier?
	#		if re.search("[A-Za-z_\$]",truestr[myindex-1]):
	#			# this is
	#		myindex = truestr.find(tempword, myindex+1)
	
removeWhitespace()








#............... replace property names as bracketed strings...............
def replaceProps():
	global truestr,strFuncName
	varStart = -1
	counter=0
	#for i in range(0,len(truestr)):
	i=0
	mappings = {}
	while i<len(truestr):
		myord = ord(truestr[i])
		isLetter = False
		isNum = False
		if (myord>=65 and myord<=90) or (myord>=97 and myord<=122):
			isLetter = True
		if (myord>=48 and myord<=57):
			isNum = True
			
		if isLetter:
			# this is a valid identifier. do we need to initiate a new word?
			if varStart==-1:
				varStart = i
		else:
			# this is an invalid character. Shall we terminate?
			if not isNum:
				# was there even a valid string going on in the first place?
				if varStart>=0:
					keyword = truestr[varStart:i]

					# check if keyword is preceded by "."
					if truestr[varStart-1]==".":
						origlen = len(truestr)
						hexarr = ""
						for k in range(0,len(keyword)):
							hexarr += str(ord(keyword[k]))+","
						hexarr = hexarr[:-1]
						hexStr = strFuncName+"(["+hexarr+"])"
						truestr = truestr[0:varStart-1]+"["+hexStr+"]"+truestr[i:]
						i+= (len(truestr)-origlen)
				varStart =  -1
		i = i+1

replaceProps()











#................ Creates a junk variable and assigns it either a number or a string
def genjunkvar():
	global junkWords
	dummyvar = generateLily()
	randNum = random.random()
	# should the dummy be a string or a number?
	if randNum<0.5:
		dummyval = "'"+junkWords[int(random.random()*(len(junkWords)-1))]+"'"
		if random.randint(0,5)>0:
			dummyval = stringLibrary(dummyval)
	else:
		dummyval = int(random.random()*1600)
		
	return [dummyvar, str(dummyval)]
	
	
	
	

# defines all the string functions and the parameters (and restrictions) they accept
#..... this allows us to arbitrarily use any string functions in our junk variables to add authenticity
def stringLibrary(basestr):
	global junkWords
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
					netres += "'"+junkWords[random.randint(0,len(junkWords)-1)]+"',"
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
	
	
	
	
	
def generateIf():
	global createdLilies
	dummyvar = createdLilies[random.randint(0,len(createdLilies)-1)]
	randNum = random.random()
	allopsNum = ["<","<=",">",">="]
	# should the dummy be a string or a number?
	if randNum<0.5:
		dummyval = "'"+junkWords[int(random.random()*(len(junkWords)-1))]+"'"
		if random.randint(0,1)==0:
			dummyOp = "=="
		else:
			dummyOp = "!="
		dummyval
	else:
		dummyval = int(random.random()*16000)
		dummyOp = allopsNum[random.randint(0,3)]
		
	return [dummyvar, dummyOp, str(dummyval)]
	
	
	


#.............. inject junk variables.................
def injectJunkVars():
	global truestr, junkWords, createdLilies
	
	# first locate all the different lines in this file. each line is computed in terms of the semicolons
	allLines = []
	forIndex = -1
	semis = 0
	semiStart = -1
	i=0
	forBlocks = [] # array of start-end points of for blocks
	semiPoints = [] # array of each index where a semicolon appeared
	
	while i<len(truestr):
		if truestr[i:i+3]=="for" and (not re.search("[A-Za-z0-9_\$]",truestr[i-1])) and (not re.search("[A-Za-z0-9_\$]",truestr[i+3])):
			# means that we have found a for keyword that is neither preceded or followed by a valid identifier keyword. This is a control statement
			semis = 0
			forIndex = i
			# lookahead for the two semicolons in this construct
			semiOne = truestr.find(";",forIndex)
			semiTwo = truestr.find(";",semiOne+1)
			forBlocks.append([i,semiTwo])
			i = semiTwo+1
		if truestr[i]==";":
			if random.random()>0.5:
				i+=1
				continue
				
			# should we inject a dummy conditional here? if(<math conditional>){//dummy vars}	
				
			# should we consider making the dummy variable reference a lily var?
			# (this has to be defined BEFORE the generator otherwise, we will have a false lily)
			lilyval = createdLilies[int(random.random()*(len(createdLilies)-1))]

			# we shall inject a dummy variable here
			[dummyvar, dummyval] = genjunkvar()	
			
			
			# (this won't work because the stringLibrary() function may result in an undefined variable)
			# blind concatenation doesn't capture this possible error
			#if random.random()>0.6:
			#	dummyval = lilyval+"+"+str(dummyval)
			
			
			# should we consider wrapping this statement in an if conditional
			# an if conditional returns the expression body, the conditional expression
			#[condLeft, condOp, condRight] = generateIf()
			
			
			injectstr = dummyvar + "="+str(dummyval)+";"
			origlen = len(truestr)
			truestr = truestr[0:i+1]+injectstr+truestr[i+1:]
			i+=(len(truestr)-origlen)
		i+=1
	

	
#injectJunkVars()










#............... replace the variables by enforcing lily............
#........... for each variable we find, we must replace ALL instances that have that variable name in a consistent way. So we will keep a bank of all the names we have found thus far and the mapping the identifier has been assigned. Then, we come across a new keyword, if it already has a mapping, just apply it.

replacedClasses = {}

def replaceVars():
	global truestr, reservedWords, reservedFuncs, reservedClasses, reservedObjs, reservedStrVars
	global replacedClasses
	varStart = -1
	counter=0
	#for i in range(0,len(truestr)):
	i=0
	mappings = {}
	while i<len(truestr):
		myord = ord(truestr[i])
		isLetter = False
		isNum = False
		if (myord>=65 and myord<=90) or (myord>=97 and myord<=122):
			isLetter = True
		if (myord>=48 and myord<=57):
			isNum = True
			
		if isLetter:
			# this is a valid identifier. do we need to initiate a new word?
			if varStart==-1:
				varStart = i
		else:
			# this is an invalid character. Shall we terminate?
			if not isNum:
				# was there even a valid string going on in the first place?
				if varStart>=0:
					keyword = truestr[varStart:i]
					
					# if this keyword is an instantiation of a global object, let's replace it and then inject it as an eval at the start
					isReplaced = False
					if keyword in reservedClasses:
						if keyword in replacedClasses:
							newWord = replacedClasses[keyword]
						else:
							# this is the first occurrence. Generate a Lily
							newWord = generateLily()
							replacedClasses[keyword] = newWord
						
						origlen = len(truestr)
						truestr = truestr[0:varStart]+newWord+truestr[i:]
						i+= (len(truestr)-origlen)
						isReplaced=True
					
					
					if not isReplaced and (not keyword in reservedWords) and (not keyword in reservedFuncs) and (not keyword in reservedClasses) and (not keyword in reservedObjs) and (not keyword in reservedStrVars):
						# we've found a custom keyword. Replace it.
						if isLily(keyword):
							# this is already encoded. leave it.
							varStart = -1
							i=i+1
							continue
						#print "Found String: ", truestr[varStart:i]
												
						# if this keyword already has been Lily'd, use the term it has previously been assigned
						if keyword in mappings:
							newWord = mappings[keyword]
						else:
							# this is the first occurrence. Generate a Lily
							newWord = generateLily()
							mappings[keyword] = newWord
						
						origlen = len(truestr)
						truestr = truestr[0:varStart]+newWord+truestr[i:]
						i+= (len(truestr)-origlen)
				varStart =  -1
		i = i+1
replaceVars()
#print truestr

print "KEYS:::"
print reservedStrVars

print replacedClasses


#.............. replace numbers with expressions...................
def replaceNums():
	global truestr, reservedWords
	
	# for each number we locate, we will replace it
	i=0
	numIndex = -1
	while i<len(truestr):
		selval = ord(truestr[i])
		isNum = False
		if (selval>=48 and selval<=57):
			isNum = True
			
		if numIndex==-1:
			if isNum:
				# this is a valid number. Is this the start of a number or is it preceded by variable terms.
				if not re.search("[A-Za-z_\$]",truestr[i-1]):
					# this is the start of the number
					numIndex = i
		else:
			# a number is already being accumulated. can we continue? decimals are allowed
			if not (isNum or truestr[i]=="."):
				# the number has ended. capture the number string
				numstr = truestr[numIndex:i]
				replaceNum = computeNum(float(numstr))
				origlen = len(truestr)
				truestr = truestr[0:numIndex]+replaceNum+truestr[i:]
				i+=(len(truestr)-origlen)
				numIndex = -1
				
		i+=1
				
replaceNums()




#.............. inject junk variables.................
def injectJunkVars2():
	global truestr
	
	# first locate all the different lines in this file. each line is computed in terms of the semicolons
	allLines = []
	forIndex = -1
	semis = 0
	semiStart = -1
	i=0
	forBlocks = [] # array of start-end points of for blocks
	semiPoints = [] # array of each index where a semicolon appeared
	
	while i<len(truestr):
		if truestr[i:i+3]=="for" and (not re.search("[A-Za-z_\$]",truestr[i-1])) and (not re.search("[A-Za-z0-9_\$]",truestr[i+3])):
			# means that we have found a for keyword that is neither preceded or followed by a valid identifier keyword. This is a control statement
			semis = 0
			forIndex = i
			# lookahead for the two semicolons in this construct
			semiOne = truestr.find(";",forIndex)
			semiTwo = truestr.find(";",semiOne+1)
			forBlocks.append([i,semiTwo])
			i = semiTwo+1
		i+=1	
	
	# now let's capture ALL semicolons
	prevSemi = -1
	curSemi = truestr.find(";")
	semiPoints.append(0)
	while curSemi>prevSemi:
		semiPoints.append(curSemi)
		prevSemi = curSemi
		curSemi = truestr.find(";",prevSemi+1)
		
		
	print semiPoints
	print forBlocks
	
		
	# chunk the entire string by semicolon seperator
	truearr = truestr.split(";")
	print "LEN:",len(truearr),":",len(semiPoints)
	netarr = []
	temparr = []
	for i in range(0,len(truearr)):
		# check if this element is a fraction of a for split
		isFrag = False
		for k in range(0,len(forBlocks)):
			if (semiPoints[i]>=forBlocks[k][0] and semiPoints[i]<=forBlocks[k][1]):
				# this semicolon is a fragment. append it
				temparr.append(truearr[i])
				isFrag = True
				break
		if isFrag:
			continue
			
		if not isFrag:
			if len(temparr)>0:
				netarr.append(";".join(temparr))
			else:
				netarr.append(truearr[i])
			temparr = []
	
	print "PRINTING........"
	print "\n...\n".join(netarr)
	
injectJunkVars()


#................. convert all ifs to single-time fors ..................
def convertIfs():
	global truestr
	#prevIndex = truestr.find("if(")
	prevIndex = 0
	startIndex = truestr.find("if(")
	while (startIndex>=prevIndex):
		bracketStart = truestr.find("(",startIndex)
		thresholder = 200
		bracketCount = 1
		prevBracket = bracketStart
		counter=0
		while bracketCount>0:
			counter+=1
			if counter>thresholder:
				print "breakdown break"
				break
			nextOpen = truestr.find("(",prevBracket+1)
			nextClose = truestr.find(")",prevBracket+1)
			if nextClose<nextOpen:
				nextBracket = nextClose
				bracketCount-=1
			else:
				nextBracket = nextOpen
				bracketCount+=1
				
			# now we know where the next bracket of some form is
			if bracketCount==0:
				bracketEnd = nextBracket
				break
			
			prevBracket = nextBracket
		#..... now we've found our brackets.....
		print "FOUNDIF: ",truestr[bracketStart:bracketEnd]
		
		#..... make sure this is a bracketed if, not single-line....
		if truestr[bracketEnd+1]=="{":
			newVar = generateLily()
			conditional = truestr[bracketStart+1:bracketEnd]
			repstr = "for("+newVar+"=0;("+conditional+") && ("+newVar+"<1);"+newVar+"++)"
			origlen = len(truestr)
			truestr = truestr[0:startIndex]+repstr+truestr[bracketEnd+1:]
			startIndex+=(len(truestr)-origlen)
			
			# investigate if there is a corresponding "else".
			condend = startIndex+len(repstr)
			nextElse = truestr.find("else",condend)
			if nextElse>0:
				# another else does exist somewhere. is it corresponding to this if?
				sCount = 0
				eCount = 0
				nextS = truestr.find("{",condend)
				prevS = nextS
				if nextS>0:
					sCount=1
				nextE = truestr.find("}",condend)
				prevE = nextE
				if nextE>0:
					eCount=1
				while(nextS>=prevS and nextS<nextElse):
					prevS = nextS
					nextS = truestr.find("{",prevS+1)
					if nextS>prevS:
						sCount+=1
						
				while(nextE>=prevE and nextE<nextElse):
					prevE = nextE
					nextE = truestr.find("}",prevE+1)
					if nextE>prevE:
						eCount+=1
				
				if sCount==eCount:
					print "YAY:",sCount
					# this is a valid else
					newVar = generateLily()
					repstr = "for("+newVar+"=0;(!("+conditional+")) && ("+newVar+"<1);"+newVar+"++)"
					origlen = len(truestr)
					truestr = truestr[0:nextElse]+repstr+truestr[nextElse+4:]
					startIndex+=(len(truestr)-origlen)
			
			
		prevIndex = startIndex
		startIndex = truestr.find("if(",startIndex+1)	
			
#convertIfs()





#.................. for all the new junk strings that used properties, obfuscate those........
replaceProps()






#.............. do a final rundown. replace any remaining strings ..................	
replaceStrings()




#................ create the base injections......................
def baseInjections():
	global truestr,strFuncName, replacedClasses
	funcName = strFuncName
	funcArg = generateLily()
	funcIter = generateLily()
	funcRes = generateLily()
	#....... create string rendering function ........
	basestr = "function "+funcName+"("+funcArg+"){"
	basestr += funcRes+"='';"
	fromCode = "\\x66\\x72\\x6f\\x6d\\x43\\x68\\x61\\x72\\x43\\x6f\\x64\\x65"
	basestr += "for(var "+funcIter+"=0;"+funcIter+"<"+funcArg+".length;"+funcIter+"++){"
	basestr += funcRes+"+=String['"+fromCode+"']("+funcArg+"["+funcIter+"]);"
	basestr += "}return "+funcRes+";}"
	#......... create replaced classes ............
	tempstr = ""
	for key,val in replacedClasses.iteritems():
		hexstr = ""
		for i in range(0,len(key)):
			hexstr += str(ord(key[i]))+","
		hexstr = hexstr[:-1]
		tempstr += "var "+val+"=eval("+strFuncName+"(["+hexstr+"]));"
	basestr+=tempstr
	
	truestr = basestr+truestr


baseInjections()







#................... output to file.......................
def saveToFile(filename):
	global truestr
	print "\n\n....................\nWriting file\n...................\n\n"+truestr
	netres = "<html><head></head><body><script type='text/javascript'>"+truestr+"</script></body></html>"
	handle = open(filename,"w")
	handle.write(netres)
	handle.close()
	
	
saveToFile("C:/Users/A/Documents/Michigan/University/Semester3/SI710/testjs.html")