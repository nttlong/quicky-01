from func_rec import rec_process,BinaryExpression,char_codes,expression_types,binary_ops
from func_rec import unary_ops,literals,isDecimalDigit,isIdentifierStart,isIdentifierPart
from func_rec import NumericLiteralExpression,StringLiteralExpression,ArrayExpression
from func_rec import UnaryExpression,MemberExpression,CallExpression,LiteralExpression,ThisExpression
from func_rec import IdentifierExpression,ConditionalExpression
from func_rec import CompoundExpression,BinaryOperatorInfo

def getMaxKeyLen(obj):
    #type: (dict)-> int
    max_len = 0
    for key, value in obj.items():
        len = key.__len__()
        if len > max_len:
            max_len = len
    return max_len
def binaryPrecedence(op_val):
    return binary_ops.get(op_val,0)
def createBinaryExpression(operator, left, right):
    #type(str,dict,dict) -> BinaryExpression
    return BinaryExpression(operator,left,right)


def exprI(rec):
    #type: (rec_process)->str
    """
    :param rec:rec_process
    :return:chr
    """
    if rec.index>=rec.expr.__len__():
        return None
    return rec.expr[rec.index]
def exprICode(rec):
    # type: (rec_process) -> int
    if(not isinstance(rec,rec_process)):
        raise Exception("parameter is incorect type")
    if rec.index>=rec.expr.__len__():
        return None
    return ord(rec.expr[rec.index])

def gobbleSpaces(rec):
    #type: (rec_process) -> rec_process
    """
    Push `index` up to the next non-space character
    :return:
    """
    ch=exprICode(rec)
    while ch in [32,9,10,13]:
        rec.index = rec.index + 1
        ch=exprICode(rec.index)

    return rec

def gobbleNumericLiteral(rec):
    #type:(rec_process)->NumericLiteralExpression
    number = ''
    ch = None
    chCode = None
    while isDecimalDigit(exprICode(rec)):
        number += exprI(rec)
        rec.index += 1
    if exprICode(rec) ==char_codes.PERIOD_CODE:#can start with a decimal marker
        number += exprI(rec)
        rec.index += 1
        while isDecimalDigit(exprICode(rec)):
            number += exprI(rec)
            rec.index += 1
    ch = exprI(rec)
    if ch in ['e','E']:#exponent marker
        number += exprI(rec.index)
        rec.index += 1
        ch = exprI(rec.index)
        if ch in ['+','-']:#exponent sign
            number += exprI(rec.index)
            rec.index += 1
        while isDecimalDigit(exprICode(rec.index)):
            number += exprI(rec.index)
            rec.index += 1

        if not isDecimalDigit(exprICode(rec.index-1)):
            raise Exception('Expected exponent {0} at {1}'.format (number + exprI(rec.index),rec.index))
    chCode = exprICode(rec)
    #Check to make sure this isn't a variable name that start with a number (123abc)
    if isIdentifierStart(chCode):
        raise Exception("Variable names cannot start with a number {0} at {1}".format(number + exprI(rec.index),rec.index))
    elif chCode == char_codes.PERIOD_CODE:
        raise Exception('Unexpected period {0}'.format(rec.index))
    return NumericLiteralExpression(number)

def gobbleStringLiteral(rec):
    #type: (rec_process)->StringLiteralExpression
    str = ''
    quote = exprI(rec)
    rec.index += 1
    closed = False
    ch= None
    while rec.index <rec.length:
        ch = exprI(rec)
        rec.index += 1
        if ch == quote:
            closed = True
            break
        elif ch=="\\":# Check for all of the common escape codes
            if ch == "n":
                str += '\\n'
            elif ch== 'r':
                str += '\\n'
            elif ch=='t':
                str += '\\n'
            elif ch=='b':
                str += '\\n'
            elif ch== 'f':
                str+="\\f"
            elif ch == "v":
                str+="\\0xB"
            else:
                str+=ch
        else:
            str += ch
    if not closed:
        raise Exception('Unclosed quote after {0} at {1}"'.format(str , rec.index));
    return   StringLiteralExpression(str,quote)
"""
gobbleStringLiteral = function() {
							 var str = '', quote = exprI(index++), closed = false, ch;

							 while(index < length) {
								 ch = exprI(index++);
								 if(ch === quote) {
									 closed = true;
									 break;
								 } else if(ch === '\\') {
									 // Check for all of the common escape codes
									 ch = exprI(index++);
									 switch(ch) {
										 case 'n': str += '\n'; break;
										 case 'r': str += '\r'; break;
										 case 't': str += '\t'; break;
										 case 'b': str += '\b'; break;
										 case 'f': str += '\f'; break;
										 case 'v': str += '\x0B'; break;
										 default : str += ch;
									 }
								 } else {
									 str += ch;
								 }
							 }

							 if(!closed) {
								 throwError('Unclosed quote after "'+str+'"', index);
							 }

							 return {
								 type: LITERAL,
								 value: str,
								 raw: quote + str + quote
							 };
						 }
"""
def gobbleArguments(rec,termination):

    args = []
    closed = False
    while rec.index < rec.length:
        gobbleSpaces(rec)
        rec.ch_i = exprICode(rec)
        if rec.ch_i == termination:
            closed = True
            rec.index+=1
            break;
        elif rec.ch_i ==char_codes.COMMA_CODE:
            rec.index+=1
        else:
            node = gobbleExpression(rec)
            if not node or node.type==expression_types.COMPOUND:
                raise Exception('Expected comma {)}'.format(rec.index))
            args.append(node)

    if not closed:
        raise Exception('Expected {0} at {1}'.format(chr(termination),rec.index))
    return args

def gobbleArray(rec):
    #type:(rec_process)->ArrayExpression
    rec.index+=1
    return  ArrayExpression(gobbleArguments(rec,expression_types.CBRACK_CODE))

def gobbleGroup(rec):
    rec.index+=1
    node = gobbleExpression(rec)
    gobbleSpaces(rec)
    if exprICode(rec)==char_codes.CPAREN_CODE:
        rec.index+=1
        return node
    else:
        return node
        #raise Exception('Unclosed ('+ rec.index.__str__())

def gobbleIdentifier(rec):
    ch = exprICode(rec)
    start = rec.index
    identifier=None
    if isIdentifierStart(ch):
        rec.index+=1
    else:
        raise Exception('Unexpected '.format(exprI(rec), rec.index))
    while rec.index<rec.length:
        ch = exprICode(rec)
        if isIdentifierPart(ch):
            rec.index+=1
        else:
            break
    identifier = rec.expr[start:rec.index]
    if literals.has_key(identifier):
        return LiteralExpression(identifier)
    elif identifier=="this":
        return ThisExpression()
    else:
        return IdentifierExpression(identifier)



def gobbleVariable(rec):
    # type:(rec_process)->ArrayExpression

    if rec.ch_i == char_codes.OPAREN_CODE:
        node = gobbleGroup(rec)
    else:
        node = gobbleIdentifier(rec)
    gobbleSpaces(rec)
    rec.ch_i = exprICode(rec)
    while rec.ch_i ==char_codes.PERIOD_CODE or rec.ch_i ==char_codes.OBRACK_CODE or rec.ch_i ==  char_codes.OPAREN_CODE:
        rec.index+=1
        if rec.ch_i ==char_codes.PERIOD_CODE:
            gobbleSpaces(rec)
            return MemberExpression(False,node,gobbleIdentifier())

        elif rec.ch_i ==char_codes.OBRACK_CODE:
            node = MemberExpression(True, node, gobbleExpression(rec))
            gobbleSpaces(rec)
            rec.ch_i = exprICode(rec)
            if rec.ch_i !=char_codes.CBRACK_CODE:
                raise Exception('Unclosed ['+ rec.index.__str__())
            rec.index+=1
        elif rec.ch_i == char_codes.OPAREN_CODE:
            node=CallExpression(gobbleArguments(rec,char_codes.CPAREN_CODE),node)

        gobbleSpaces(rec)
        rec.ch_i = exprICode(rec)
    return node

def gobbleToken(rec):
    #type:(rec_process)->rec_process

    # ch= None
    # to_check = None
    # tc_len = None
    gobbleSpaces(rec)
    ch = exprICode(rec)
    if isDecimalDigit(ch) or ch ==char_codes.PERIOD_CODE: #Char code 46 is a dot `.` which can start off a numeric literal
        return gobbleNumericLiteral(rec)
    elif ch ==char_codes.SQUOTE_CODE or ch ==char_codes.DQUOTE_CODE: #Single or double quotes
        return gobbleStringLiteral(rec)
    elif ch == char_codes.OBRACK_CODE:
        return gobbleArray(rec)
    else:
        to_check = rec.expr[rec.index: rec.index+rec.max_unop_len]
        tc_len = to_check.__len__()
        while tc_len>0:
            """
            Don't accept an unary op when it is an identifier
            Unary ops that start with a identifier-valid character must be followed
            by a non identifier-part valid character
            """
            if unary_ops.has_key(to_check) and\
                    (
                       (not(isIdentifierStart(exprICode(rec))))or
                       (
                               (rec.index+to_check.__len__() < rec.expr.__len__()) and\
                               (not(isIdentifierPart(exprICode(rec.index+to_check.__len__()))))

                       )
                    ):
                rec.index += tc_len
                return UnaryExpression(to_check,gobbleToken(rec),True)

            to_check = to_check[0:tc_len]
            tc_len-=1
        if isIdentifierStart(ch) or ch==char_codes.OPAREN_CODE:
            return gobbleVariable(rec)
    return False

def gobbleBinaryOp(rec):
    """
     Search for the operation portion of the string (e.g. `+`, `===`)
    Start by taking the longest possible binary operations (3 characters: `===`, `!==`, `>>>`)
    and move down from 3 to 2 to 1 character until a matching binary operation is found
    then, return that binary operation
    :return:
    """
    gobbleSpaces(rec)
    biop = None
    to_check = rec.expr[rec.index: rec.index+rec.max_binop_len]
    tc_len = to_check.__len__()
    while tc_len > 0:
        """
        Don't accept a binary op when it is an identifier.
        Binary ops that start with a identifier-valid character must be followed
        by a non identifier-part valid character
        """
        if binary_ops.has_key(to_check) and\
            (
                not (isIdentifierStart(exprICode(rec))) or
                (
                        (rec.index+to_check.__len__()<rec.expr.__len__()) and\
                        not(isIdentifierPart(exprICode(rec.index+to_check.__len__())))

                )
            ):
            rec.index += tc_len
            return to_check
        tc_len-=1
        to_check = to_check[0:tc_len]

    return False

def gobbleBinaryExpression(rec):
    #type:(rec_process)->rec_process
    left = gobbleToken(rec)
    biop = gobbleBinaryOp(rec)
    if not biop: #If there wasn't a binary operator, just return the leftmost node
        return left
    #Otherwise, we need to start a stack to properly place the binary operations in their
    #precedence structure
    biop_info = BinaryOperatorInfo(biop,binaryPrecedence(biop))
    right = gobbleToken(rec)
    if not right:
        raise Exception("Expected expression after {0} , {1}".format(biop, rec.index))
    stack = [left, biop_info, right]
    #Properly deal with precedence using [recursive descent](http://www.engr.mun.ca/~theo/Misc/exp_parsing.htm)
    biop = gobbleBinaryOp(rec)
    while biop:
        prec = binaryPrecedence(biop)
        if prec==0:
            break
        biop_info = BinaryOperatorInfo(biop,prec)
        #// Reduce: make a binary expression from the three topmost entries.
        while stack.__len__() > 2 and prec <= stack[stack.__len__() - 2].prec:
            right = stack.pop()
            biop = stack.pop().value
            left = stack.pop()
            node = createBinaryExpression(biop, left, right)
            stack.append(node)

        node =gobbleToken(rec)
        if not node:
            raise Exception("Expected expression after ".format(biop, rec.index))
        stack.extend([biop_info, node])
        biop = gobbleBinaryOp(rec)
    i = stack.__len__() - 1
    node = stack[i]
    while i>1:
        node = createBinaryExpression(stack[i - 1].value, stack[i - 2], node)
        i -= 2
    return node

def gobbleExpression(rec):
    #type: (rec_process) -> dict
    """
    The main parsing function. Much of this code is dedicated to ternary expressions
    :return:
    """
    """
    var test = gobbleBinaryExpression(),
                             consequent, alternate;
    """
    test = gobbleBinaryExpression(rec)
    consequent = None
    alternate = None
    gobbleSpaces(rec)
    if exprICode(rec)==char_codes.QUMARK_CODE:#Ternary expression: test ? consequent : alternate
        rec.index += 1
        consequent = gobbleExpression()
        if not consequent:
            raise Exception('Expected expression {0}'.format(rec.index))
        gobbleSpaces()
        if exprICode(rec) ==char_codes.COLON_CODE:
            rec.index += 1
            alternate = gobbleExpression()
            if not alternate:
                raise Exception('Expected expression {0}'.format(rec.index))
            return ConditionalExpression(test,consequent,alternate)

        else:
            raise Exception("Expected :{0}".format(rec.index))
    else:
        return test
"""
gobbleExpression = function() {
							 var test = gobbleBinaryExpression(),
								 consequent, alternate;
							 gobbleSpaces();
							 if(exprICode(index) === QUMARK_CODE) {
								 // Ternary expression: test ? consequent : alternate
								 index++;
								 consequent = gobbleExpression();
								 if(!consequent) {
									 throwError('Expected expression', index);
								 }
								 gobbleSpaces();
								 if(exprICode(index) === COLON_CODE) {
									 index++;
									 alternate = gobbleExpression();
									 if(!alternate) {
										 throwError('Expected expression', index);
									 }
									 return {
										 type: CONDITIONAL_EXP,
										 test: test,
										 consequent: consequent,
										 alternate: alternate
									 };
								 } else {
									 throwError('Expected :', index);
								 }
							 } else {
								 return test;
							 }
						 }
"""
def parse(expr):
    # expr="("+expr+")"
    rec= rec_process()
    rec.max_unop_len = getMaxKeyLen(unary_ops)
    rec.max_binop_len = getMaxKeyLen(binary_ops)
    rec.index = 0
    rec.length = expr.__len__()
    rec.nodes=[]
    node=None
    rec.ch_i=None
    rec.expr=expr
    while rec.index < rec.length:
        rec.ch_i = exprICode(rec)
        if rec.ch_i ==  char_codes.SEMCOL_CODE or rec.ch_i == char_codes.COMMA_CODE:
            rec.index+=1
        else:
            node = gobbleExpression(rec)
            if node:
                rec.nodes.append(node)
            elif rec.index < rec.length:
                raise Exception('Unexpected "{0}" at {1}'.format(exprI(rec), rec.index))

    if rec.nodes.__len__() == 1:
        return rec.nodes[0]
    else:
        return CompoundExpression(rec.nodes)

"""
                    while(index < length) {
						 ch_i = exprICode(index);

						 // Expressions can be separated by semicolons, commas, or just inferred without any
						 // separators
						 if(ch_i === SEMCOL_CODE || ch_i === COMMA_CODE) {
							 index++; // ignore separators
						 } else {
							 // Try to gobble each expression individually
							 if((node = gobbleExpression())) {
								 nodes.push(node);
							 // If we weren't able to find a binary expression and are out of room, then
							 // the expression passed in probably has too much
							 } else if(index < length) {
								 throwError('Unexpected "' + exprI(index) + '"', index);
							 }
						 }
					 }

					 // If there's only one expression just try returning the expression
					 if(nodes.length === 1) {
						 return nodes[0];
					 } else {
						 return {
							 type: COMPOUND,
							 body: nodes
						 };
					 }
"""