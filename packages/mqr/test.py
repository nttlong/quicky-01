import compilers
import pyquery
qr=pyquery.query().project(dict(
   basicSalary="3000*benefit"
)).match(
    "x==3"
)


# import expression_parser
# x=expression_parser.to_mongobd("x=={0}",'aaa')
# # expr,params=expression_parser.parse("$x==@test1",test1=2,username='admin')
print qr.pipeline
#print params