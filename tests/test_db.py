from app import database, config

if config.MYSQL_HOST != '127.0.0.1':
    raise Exception('Can`t do this on production!')


def test_db_connection():
    assert database.ping() is True


def test_delete_from_table():
    with database.__create_connection() as con:
        database.delete_email_domain_list(con)
        emails_list = database.get_emails_list(con, 1)
        assert emails_list == []


def test_insert_into_email_domain_list():
    with database.__create_connection() as con:
        database.insert_into_email_domain_list(con, 1, 1, 1)
        emails_list = database.get_emails_list(con, 1)
        assert emails_list == ['test@gmail.com']


def test_get_emails_list():
    with database.__create_connection() as con:
        emails_list = database.get_emails_list(con, 1)
        assert emails_list == ['test@gmail.com']


def test_insert_into_email():
    name = 'wezxasqw'
    with database.__create_connection() as con:
        con.cursor().execute('delete from email where name = %s', (name,))
        con.commit()
        name_id = database.insert_into_email(con, name)
        assert name_id is not None


def test_insert_into_list():
    name = 'alotof'
    with database.__create_connection() as con:
        con.cursor().execute('delete from list where name = %s', (name,))
        con.commit()
        name_id = database.insert_into_list(con, name)
        assert name_id is not None


def test_insert_into_domain():
    name = '1secmail.com'
    with database.__create_connection() as con:
        con.cursor().execute('delete from domain where name = %s', (name,))
        con.commit()
        name_id = database.insert_into_domain(con, name)
        assert name_id is not None
