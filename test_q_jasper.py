import qjasper
qjasper.set_config(
    url="http://172.16.7.67:8080/jasperserver",
    user="jasperadmin",
    password="jasperadmin"
)
_filter =qjasper.filter()
_filter.type=qjasper.resource_types.query
# _filter.limit=200
# _filter.offset=0
# _filter.type=qjasper.resource_types.jdbcDataSource
# lst= qjasper.resources.search(_filter)
lst= qjasper.resources.get_info("datasources/DanhSachNhanVien")
import pprint
# for item in lst:
pprint.pprint(lst.__to_dict__())