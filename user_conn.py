from typing import NamedTuple


class UserConn(NamedTuple):
    user: str
    password: str
    host: str
    port: int
    database: str
