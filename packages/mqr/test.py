import compilers
import expression_parser
x=expression_parser.to_mongobd("x=={0}",'aaa')
# expr,params=expression_parser.parse("$x==@test1",test1=2,username='admin')
print x
#print params