import pandas

def get_sportsmen(conn):
    return pandas.read_sql(
    '''
        SELECT * FROM sportsmen
    ''', 
    conn
    )

def get_info_t_sportsmen(conn, sportsmen_id):
    return pandas.read_sql('''
        WITH get_trainers(info_t_id, trainers_name)
        AS (
            SELECT info_t_id, trainer_name
            FROM trainer JOIN info_t_trainer USING(trainer_id)
            GROUP BY info_t_id
        )
        SELECT 
            description AS Описание, 
            trainers_name AS Тренер,
            borrow_date AS Дата_тренировки, 
            return_date AS Дата_подтверждения_тренировки,
            info_t_sportsmen_id
        FROM
        sportsmen
        JOIN info_t_sportsmen USING(sportsmen_id)
        JOIN info_t USING(info_t_id)
        JOIN get_trainers USING(info_t_id)
        WHERE sportsmen.sportsmen_id = :id
        ORDER BY 3
    ''', 
    conn, 
    params={"id": sportsmen_id}
    )

def get_new_sportsmen(conn, new_sportsmen):
    cur = conn.cursor()
    cur.execute(
        '''
            INSERT INTO sportsmen (sportsmen_name)
            VALUES (:new_sportsmen)
        ''',
        {"new_sportsmen": new_sportsmen}
    )
    conn.commit()
    return cur.lastrowid

def borrow_info_t(conn, info_t_id, sportsmen_id):
    cur = conn.cursor()
    cur.executescript(
        f'''
            INSERT INTO info_t_sportsmen (info_t_id, sportsmen_id, borrow_date, return_date)
            VALUES ({info_t_id}, {sportsmen_id}, DATE("NOW"), NULL);

            UPDATE info_t
            SET available_numbers = available_numbers - 1
            WHERE info_t_id = {info_t_id}
        ''',
    )
    conn.commit()

def set_return_date(conn, info_t_sportsmen_id):
    cur = conn.cursor()
    cur.execute(
        f'''
            UPDATE info_t_sportsmen
            SET return_date = DATE('NOW')
            WHERE info_t_sportsmen_id = {info_t_sportsmen_id}
        '''
    )
    cur.execute(
        f'''
            UPDATE info_t
            SET available_numbers = available_numbers + 1
            WHERE info_t_id = (SELECT info_t_id FROM info_t_sportsmen WHERE info_t_sportsmen_id = {info_t_sportsmen_id})
        '''
    )
    conn.commit()

def del_info_t_sportsmen(conn, info_t_sportsmen_id):
    cur = conn.cursor()
    cur.execute(
        f'''
            UPDATE info_t
            SET available_numbers = available_numbers + 1
            WHERE info_t_id = (SELECT info_t_id FROM info_t_sportsmen
            WHERE info_t_sportsmen_id = {info_t_sportsmen_id})
        '''
    )
    cur.execute(
        f'''
            DELETE FROM info_t_sportsmen
            WHERE
            info_t_sportsmen_id = {info_t_sportsmen_id}
        '''
    )
    conn.commit()

def add_info_t(conn, description, type_T, week_day, duration, available_numbers):
    cur = conn.cursor()
    cur.execute(
        f'''
            INSERT INTO info_T (description, type_T_id, week_day_id, duration, available_numbers)
            VALUES
                ('{description}', {type_T}, {week_day}, {duration}, {available_numbers})
        '''
    )
    conn.commit()
    return cur.lastrowid

def add_trainer(conn, info_t_id, trainer_id):
    cur = conn.cursor()
    cur.execute(
        f'''
                INSERT INTO info_t_trainer (info_t_id, trainer_id)
                VALUES
                    ({info_t_id}, {trainer_id})
            '''
    )
    conn.commit()
    cur.close()