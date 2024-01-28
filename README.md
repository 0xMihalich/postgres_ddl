# postgres_ddl
получение DDL для таблицы, представления или функции из РСУБД Postgres/Greenplum

данный скрипт протестирован на OS Windows 10 x64 и Ubuntu 22.04 x64
работа в других системах требует добавления соответствующей сборки pg_dump
в директорию проекта и добавления условия для выбора правильного исполняемого файла

исходники для сборки pg_dump: https://github.com/postgres/postgres

официальная документация по сборке: https://www.postgresql.org/docs/devel

для получения запроса необходимо создать объект UserConn(NamedTuple), содержащий параметры подключения к РСУБД:
- user: str
- password: str
- host: str
- port: int
- database: str

пример использования:
```python
from postgres_ddl import postgres_ddl, UserConn


conn = UserConn('user',      # пользователь
                'password',  # пароль
                'localhost', # адрес сервера
                5432,        # порт
                'public',)   # схема
# название таблицы, представления или функции
table = "public.test"        # тестовая таблица
# отправляем запрос на получение DDL
print(postgres_ddl(table, conn))
```
