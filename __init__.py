from os.path    import dirname
from re         import search, findall
from subprocess import Popen, PIPE
from sys        import platform
from typing     import Optional

from .user_conn  import UserConn


# данный скрипт протестирован на OS Windows 10 x64 и Ubuntu 22.04 x64
# работа в других системах требует добавления соответствующей сборки pg_dump
# в директорию проекта и добавления условия для выбора правильного исполняемого файла
if platform == "win32":
    pg_dump = "pg_dump.exe"
elif platform == "linux":
    pg_dump = "pg_dump"
else:
    raise Exception("Unsupported platform")


def postgres_ddl(table: str, connection: UserConn,) -> Optional[str]:
    "получение DDL для TABLE, VIEW или FUNCTION из РСУБД Postgres/Greenplum"
    "с использованием pg_dump (PostgreSQL) 17devel"
    "на вход передается два параметра:"
    "table      - название таблицы, представления или функции с указанием схемы"
    "connection - объект NamedTuple с описанием параметров подключения"
    "при отсутствии в РСУБД таблицы функция вернет None, иначе строку с DDL-запросом"

    hooks_words = findall(r'\"(.*?)\"', table)

    for word in hooks_words:
        table = table.replace(f'"{word}"', f'"\\"{word}\\""')
    
    command = ('{}/bin/{} --dbname=postgresql://{}:{}@{}:{}/{} -s -t {}'
               .format(dirname(__file__),
                       pg_dump,
                       connection.user,
                       connection.password,
                       connection.host,
                       connection.port,
                       connection.database,
                       table,))
    
    proc = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
    out, _ = proc.communicate()
    table = out.decode()
    find = search('CREATE (TABLE|VIEW|MATERIALIZED|FUNCTION|OR REPLACE FUNCTION)', table)
    
    if not find:
        return
    
    start = find.span()[0]

    return table[start: start + table[start: ].find(";") + 1]


if __name__ == '__main__':
    # создаем объект соединения
    conn = UserConn('user',      # пользователь
                    'password',  # пароль
                    'localhost', # адрес сервера
                    5432,        # порт
                    'public',)   # схема
    # название таблицы, представления или функции
    table = "public.test"        # тестовая таблица
    # отправляем запрос на получение DDL
    print(postgres_ddl(table, conn))
