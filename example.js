function calc(num1, num2, op) {
	/* check if the operator is valid for any of the following:
	+	addition
	-	subtraction
	*	multiplication
	/	division */

	if(op=="+") {
		return num1+num2;
	}
	else if(op=="-") {
		return num1-num2;
	}
	else if(op=="*") {
		return num1*num2;
	}
	else if(op=="/") {
		return num1/num2;
	}
	else {
		return ("invalid operator"); // alerts for invalid operator.
	}
}
alert(calc(2,9,"+"));
alert(calc(2,9,"-"));
alert(calc(2,9,"*"));
alert(calc(2,9,"/"));
alert(calc(2,9,""));

