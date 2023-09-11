from typing import Sequence

import pymysql

from app import config


def __create_connection():
    con = pymysql.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        database=config.MYSQL_DB,
        password=config.MYSQL_PASSWORD,
        user=config.MYSQL_USER,
        autocommit=False
    )
    return con


def ping():
    try:
        with __create_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT VERSION()")
            version = cur.fetchone()
            print("Database version: {}".format(version[0]))
    except Exception as error:
        print(error)
        return False
    else:
        return True


def get_emails_list(con: pymysql.Connection, list_id: int, limit: int = 100000, offset: int = 0) -> Sequence[str]:  # todo TESTS
    stmt = """ 
        select concat(mail.email.name, '@', mail.domain.name) as email
            from mail.email_domain_list
                join mail.email on email_domain_list.email_id = email.id
                join mail.domain on email_domain_list.domain_id = domain.id
            where list_id = %(list_id)s
            limit %(limit)s offset %(offset)s
    """

    cur = con.cursor()
    cur.execute(stmt, {
        'list_id': list_id,
        'limit': limit,
        'offset': offset
    })
    results = [i[0] for i in cur.fetchall()]
    return results


def delete_email_domain_list(con: pymysql.Connection):
    stmt = '''
    delete from email_domain_list
    '''
    try:
        cur = con.cursor()
        cur.execute(stmt)
        con.commit()
        return
    except Exception as error:
        print(error)


def insert_into_email_domain_list(con: pymysql.Connection, email_id: int, domain_id: int, list_id: int) -> bool:  # todo TEST
    stmt = '''
    insert into email_domain_list
        (email_id, domain_id, list_id)
        values
        (%(email_id)s, %(domain_id)s, %(list_id)s)
    '''
    try:
        cur = con.cursor()
        cur.execute(stmt, {
            'email_id': email_id, 'domain_id': domain_id, 'list_id': list_id
        })
        con.commit()
        return True
    except Exception as error:
        print(error)
        return False


def insert_into_email(con: pymysql.Connection, name: str) -> int | None:
    stmt = '''
    insert into email (name)
        values (%(name)s) on duplicate key update name=%(name)s
    RETURNING id

    '''
    try:
        cur = con.cursor()
        cur.execute(stmt, {
            'name': name
        })
        name_id: int = cur.fetchone()[0]
        con.commit()
    except Exception as error:
        print(error)
        return None
    else:
        return name_id


def insert_into_list(con: pymysql.Connection, name: str) -> int | None:
    stmt = '''
    insert into list (name)
        values (%(name)s) on duplicate key update name=%(name)s
    RETURNING id
    '''
    try:
        cur = con.cursor()
        cur.execute(stmt, {
            'name': name
        })
        name_id: int = cur.fetchone()[0]
        con.commit()
    except Exception as error:
        print(error)
        return None
    else:
        return name_id


def insert_into_domain(con: pymysql.Connection, name: str) -> int | None:
    stmt = '''
    insert into domain (name)
        values (%(name)s) on duplicate key update name=%(name)s
    RETURNING id
    '''
    try:
        cur = con.cursor()
        cur.execute(stmt, {
            'name': name
        })
        name_id: int = cur.fetchone()[0]
        con.commit()
    except Exception as error:
        print(error)
        return None
    else:
        return name_id


def insert_email_in_one_transaction(con: pymysql.Connection, email: str, source_name: str) -> tuple | None:
    stmt = '''
SET @email = %(email)s;
SET @source_name = %(source_name)s;
SET @username = SUBSTRING_INDEX(@email, '@', 1);
SET @domain = SUBSTRING_INDEX(@email, '@', -1);
insert into email (name) values (@username) on duplicate key update name=@username RETURNING id as email_id;
insert into domain (name) values (@domain) on duplicate key update name=@domain RETURNING id as domain_id;
insert into list (name) values (@source_name) on duplicate key update name=@source_name RETURNING id as list_id;
insert ignore into email_domain_list (email_id, domain_id, list_id) values (email_id, domain_id, list_id) returning @email, list_id;
    '''.replace('\n', '').strip()
    try:

        cur = con.cursor()
        cur.execute(stmt, {
            'email': email,
            'source_name': source_name,
        })
        result: tuple = cur.fetchone()
        con.commit()
    except Exception as error:
        print(error)
        return None
    else:
        return result


def insert_email_in_separate_transactions(con, email: str, source_name: str) -> tuple[int, int, int] | None:
    result = None

    try:
        username, domain = email.split('@')
        domain_id = insert_into_domain(con, domain)
        email_id = insert_into_email(con, username)
        list_id = insert_into_list(con, source_name)
        insertion_result = insert_into_email_domain_list(con, domain_id=domain_id, email_id=email_id, list_id=list_id)
        if insertion_result:
            return domain_id, email_id, list_id
    except Exception as error:
        print(error)
        return None
