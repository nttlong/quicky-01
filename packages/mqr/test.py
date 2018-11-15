import compilers
import expression_parser
x=compilers.compile_expression("c.a.d=15")
# expr,params=expression_parser.parse("$x==@test1",test1=2,username='admin')
print x
#print params