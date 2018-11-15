import compilers
import pyquery
qr=pyquery.query().lookup(
    From="ddd",
    locaField="vvv",
    foriegbField="ggg",
    alias="ggg"

).lookup(
    From="bbb",
    pipeline="bbbb",
    let="bbbb",
    alias="bbbbb",

)


# import expression_parser
# x=expression_parser.to_mongobd("x=={0}",'aaa')
# # expr,params=expression_parser.parse("$x==@test1",test1=2,username='admin')
print qr.pipeline
#print params