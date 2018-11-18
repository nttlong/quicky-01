import pymqr
import datetime
model = pymqr.create_model(
    "users",
    [
        pymqr.doc.Username,
        pymqr.doc.HasPassword,
        "Email"
    ],
    [
        pymqr.Index(
            pymqr.doc.username,
            pymqr.IndexOption(
                unique=True
            )
        ),
        pymqr.Index(
            pymqr.doc.email,
            pymqr.IndexOption(
                unique=True
            )
        )
    ],
    dict(
        Username=pymqr.FieldInfo(str),
        Email=str,
        PasswordSalt=str,
        HashPassword=str,
        LoginTimes=[datetime.datetime],
        Profile=dict(
            FirstName=str,
            LastName=str,
            BirthDate=datetime.datetime
        ),
        Workings=pymqr.FieldInfo(
            list,
            [
                "Year",
                "CompanyName"
            ],
            dict(
                Year = int,
                CompanyName = str,
                Description = str
            )
        ),
        PasswordChangeList = pymqr.FieldInfo(
            list,
            [
                "OldPassword",
                "Time",
                "UtcTime"
            ],
            dict(
                OldPassword = str,
                Time = datetime.datetime,
                UtcTime = datetime.datetime
            )
        )
    )

)
x = model
