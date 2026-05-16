import os

# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
# DATABASE_URL = "mysql+mysqlconnector://<root>:<root>@<127.0.0.1>:<3306>/<users>"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+aiomysql://root:root@localhost:3306/testdb"
)
