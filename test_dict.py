x=dict(
    contact=("object",
             False,
             dict(
                 tel="text",
                 fax="text",
                 email="text",
                 address="text"
             )
             ),
    map_location=("object",
                  False,
                  dict(
                      latitude="number",
                      longitude="number"
                  )),
    test=("text", True)
)
