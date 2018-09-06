How to use?
___________

1) Create connection:
    .. code-block::

        from qmongo import qcollections
        import pprint
        connection_name = "lms"
        db = qcollections.connect(connection_name,hots=...,port=...,user=...,password =...,name=...)
        qr = qcollections.queryable(db,"lv.SYS_ValueList") #make queryable collection
        pprint.pprint(qr.items) # get data of "lv.Sys_ValueLis" in lms database into list of dict and print
        items = list(qr.objects) # get data of "lv.Sys_ValueLis" in lms database into list of object
        print items[0].values[0].caption
2) Aggregate:
    .. code-block::

        import datetime
        from qmongo import qcollections
        connection_name = "lms"
        db = qcollections.connect(connection_name,hots=...,port=...,user=...,password =...,name=...)
        qr= qcollections.queryable(connection_name,"lv.SYS_ValueList")
        for item in list(qr.project(list_name=1,_id=0)):
            print item.list_name
        for item in list(qr.project(list_name=1,_id=0)):
            print item.list_name
        qremps = qcollections.queryable(connection_name,"test.emps")
        qremps.insert(first_name="Jonny",last_name="deep",birth_date=datetime.datetime(1973,12,23))
        qremps.insert(first_name="Dezen",last_name="Washington",birth_date=datetime.datetime(1971,1,12))
        qremps = qremps.match("expr(year(birth_date)>@year)",year=1972)
        for x in list(qremps.project(full_name="concat(first_name,' ',last_name)",birth_date=1)):
            print x.full_name
3) Insert data:
    .. code-block::

        from qmongo import qcollections
        connection_name = "lms"
        db = qcollections.connect(connection_name,host=...,port=...,user=...,password =...,name=...)
        qremps = qcollections.queryable(connection_name,"test.emps")
        qremps.insert(first_name="Jonny",last_name="deep",birth_date=datetime.datetime(1973,12,23))
        qremps.insert(first_name="Dezen",last_name="Washington",birth_date=datetime.datetime(1971,1,12))
4) Update data:
        from qmongo import qcollections
        connection_name = "lms"
        db = qcollections.connect(connection_name,host=...,port=...,user=...,password =...,name=...)
        qremps = qcollections.queryable(connection_name,"test.emps")
        empobj = qremps.where("expr(year(birth_date)==1971)").object
        empobj.first_name = "test"
        qremps.where("_id=={0}",empobj._id).set(empobj).commit()
5) Push data:


















