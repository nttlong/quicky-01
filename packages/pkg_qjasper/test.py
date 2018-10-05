import qjasper
qjasper.set_config(
    url="http://172.16.7.67:8080/jasperserver",
    user="jasperadmin",
    password="jasperadmin"
)
lst=qjasper.reports.get_all_report("danh")
ret=qjasper.reports.render_report_to_html("reports/Danh_sach_nhan_vien",1)
print ret