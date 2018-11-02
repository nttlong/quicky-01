.. code-block::

    import datetime
    from bson.objectid import ObjectId

    from qmongo import qcollections
    test=qcollections.queryable(db,"test-16")
    ret,err =test.insert(
        [
            dict(
                boolVal=True,
                dateVal=datetime.datetime.now(),
                textVal="test",
                decVale=0.12,
                intVal=12
            )

        ]
    )

    test.project(
        fromBoolToText="convert(boolVal,'string')",
        fromBoolToInt="convert(boolVal,'int')",
        fromBoolToDate="convert(boolVal,'date')",
        fromDateToText="convert(dateVal,'string')",
        fromDateToInt="convert(dateVal,'int')",
        fromDateToBool="convert(datelVal,'bool')",
    )

    import pprint
    pprint.pprint(test.__pipe_line__)
    pprint.pprint(test.items)

https://docs.mongodb.com/manual/reference/operator/aggregation/convert/#example

    .. code-block::

        from qmongo import qcollections
        orders=qcollections.queryable(db,"orders-17")
        ret,err =orders.insert(
            [
                {"_id": 1, "item": "apple", "qty": 5, "price": 10},
                {"_id": 2, "item": "pie", "qty": 10, "price": 20.0},
                {"_id": 3, "item": "ice cream", "qty": 2, "price": 4.99},
                {"_id": 4, "item": "almonds"},
                {"_id": 5, "item": "bananas", "qty": 5000000000, "price": 1.25}

            ]
        )

        """
        Define stage to add convertedPrice and convertedQty fields with the converted price and qty values
        priceQtyConversionStage = {
           $addFields: {
              convertedPrice: { $convert: { input: "$price", to: "decimal", onError: "Error", onNull: NumberDecimal("0") } },
              convertedQty: { $convert: {
                 input: "$qty", to: "int",
                 onError:{$concat:["Could not convert ", {$toString:"$qty"}, " to type integer."]},
                 onNull: NumberInt("0")
              } },
           }
        };
        """
        priceQtyConversionStage=orders.create().add_fields(
            [orders.compile("concat('Could not convert ',toString(qty),' to type integer.')")],
            convertedPrice="convert(price,'decimal',0,'Error')",
            convertedQty="convert(qty,'int',0,{0})",
        )
        """
        If price or qty values cannot be converted, the conversion returns a string
        totalPriceCalculationStage = {
           $project: { totalPrice: {
             $switch: {
                branches: [
                  { case: { $eq: [ { $type: "$convertedPrice" }, "string" ] }, then: "NaN" },
                  { case: { $eq: [ { $type: "$convertedQty" }, "string" ] }, then: "NaN" },
                ],
                default: { $multiply: [ "$convertedPrice", "$convertedQty" ] }
             }
        } } };

        """
        totalPriceCalculationStage=orders.create().project(
            totalPrice="switch("
                       "case(type(convertedPrice)=='string','NaN'),"
                       "case(type(convertedQty)=='string','NaN'),"
                       "convertedPrice*convertedQty)"
        )
        """
        db.orders.aggregate( [
           priceQtyConversionStage,
           totalPriceCalculationStage
        ])
        """
        orders.add_stages(
            priceQtyConversionStage.pipe_line,
            totalPriceCalculationStage.pipe_line
        )

        import pprint
        pprint.pprint(priceQtyConversionStage.pipe_line)
        pprint.pprint(orders.__pipe_line__)
        pprint.pprint(orders.items)