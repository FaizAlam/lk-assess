# lk-assess
## run
`flask --app loop init-db`
to initialize database with tables-schema in loop/schema.sql
<br><br>

`flask --app loop run --debug`
to run app in debug mode

<br>
## layout
<pre>
lk-assess
│ 
├── loop/
│   ├── __init__.py      : main app 
|   ├── apis.py          : apis         
│   ├── config.py        : app config values
│   ├── schema.sql       : db schema
│   ├── db.py            : db connection
│   ├── models.py        : db models
│   ├── repos.py         : db-queries
│   ├── services.py      : business-logic
│   ├── apis.py          : report-api-router
│   ├── task_executors.py : async-pool-executor
│   ├── utils.py         : utilities
│   ├── classes.py       : enums & data-classes
│   ├── config_keeper.py  : config-value-accessor
|   ├── test.py           : pushing data 
│   └── templates/
│       └── index.html    : for web-page view
│
├── data/             : store given csv
├── reports/          : find reports-csv here
└── instance/
    └── loop.sqlite     : created when init-db

</pre>
