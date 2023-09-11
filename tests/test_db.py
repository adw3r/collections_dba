from app import database, config


def prune_db(func):
    def wrapper(*args, **kwargs):
        if config.MYSQL_HOST != '127.0.0.1' or 'prod' in config.ENV_FILENAME:
            raise Exception('Can`t do this in production environment!')

        with database.create_connection() as con:
            cursor = con.cursor()
            cursor.execute('delete from list')
            cursor.execute('delete from domain')
            cursor.execute('delete from email')
            cursor.execute('delete from email_domain_list')
            cursor.execute('ALTER TABLE domain AUTO_INCREMENT = 1')
            cursor.execute('ALTER TABLE email AUTO_INCREMENT = 1')
            cursor.execute('ALTER TABLE list AUTO_INCREMENT = 1')
            cursor.execute('ALTER TABLE email_domain_list AUTO_INCREMENT = 1')
            con.commit()

    return wrapper


def test_db_connection():
    assert database.ping() is True


@prune_db
def test_delete_from_table():
    with database.create_connection() as con:
        database.delete_email_domain_list(con)
        emails_list = database.get_emails_list(con, 1)
        assert emails_list == []


@prune_db
def test_insert_into_email():
    name = 'wezxasqw'
    with database.create_connection() as con:
        name_id = database.insert_returning_id_into_email(con, name)
        assert name_id is not None


@prune_db
def test_insert_into_list():
    list_name = 'alotof'
    with database.create_connection() as con:
        list_id = database.insert_returning_id_into_list(con, list_name)
        assert list_id is not None


@prune_db
def test_insert_into_domain():
    name = '1secmail.com'
    with database.create_connection() as con:
        domain_id = database.insert_returning_id_into_domain(con, name)
        assert domain_id is not None


@prune_db
def test_insert_into_email_domain_list():
    with database.create_connection() as con:
        domain_id = database.insert_returning_id_into_domain(con, '1secmail.com')
        email_id = database.insert_returning_id_into_email(con, 'wezxasqw')
        list_id = database.insert_returning_id_into_list(con, 'alotof')
        database.insert_into_email_domain_list(con, email_id, domain_id, list_id)

        emails_list = database.get_emails_list(con, list_id)
        assert emails_list == ['wezxasqw@1secmail.com']


@prune_db
def test_insert_email_in_separate_transactions():
    email: str = 'wezxasqw@gmail.com'
    source_name: str = 'alotof'
    with database.create_connection() as con:
        result = database.insert_email_in_separate_transactions(con, email, source_name)
        print(result)
        assert result is not None


@prune_db
def test_get_emails_list():
    email: str = 'wezxasqw@gmail.com'
    source_name: str = 'alotof'

    with database.create_connection() as con:
        domain_id, email_id, list_id = database.insert_email_in_separate_transactions(con, email, source_name)
        emails_list = database.get_emails_list(con, domain_id)
        assert emails_list == ['wezxasqw@1secmail.com']
