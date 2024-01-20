import pandas

def get_trainer_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (trainer_name, trainer_count) AS (
                SELECT
                    trainer_name,
                    COUNT(info_t_id)
                FROM
                    trainer 
                    JOIN info_t_trainer USING (trainer_id)
                    JOIN info_t USING (info_t_id)
                GROUP BY
                    trainer_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_type_T_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (type_T_name, type_T_count) AS (
                SELECT
                    type_T_name,
                    COUNT(info_t_id)
                FROM
                    type_T
                    JOIN info_t USING (type_T_id)
                GROUP BY
                    type_T_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_week_day_count(conn):
    return pandas.read_sql(
        '''
            WITH cte (week_day_name, week_day_count) AS (
                SELECT
                    week_day_name,
                    COUNT(info_t_id)
                FROM
                    week_day
                    JOIN info_t USING (week_day_id)
                GROUP BY
                    week_day_name
            )
            SELECT * FROM cte
        ''',
        conn
    )

def get_all_trainers(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT trainer_name FROM trainer")
    trainers = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return trainers

def get_all_type_Ts(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT type_T_name FROM type_T")
    type_Ts = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return type_Ts

def get_all_week_days(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT week_day_name FROM week_day")
    week_days = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return week_days


def get_filtered_info_ts(conn, selected_trainers, selected_type_Ts, selected_week_days):
    return pandas.read_sql(
        '''
            WITH get_trainers (info_t_id, trainers) AS (
                SELECT
                    info_t_id,
                    trainer_name
                FROM
                    info_t
                    JOIN info_t_trainer USING (info_t_id)
                    JOIN trainer USING (trainer_id)
                WHERE
                    trainer_name IN {}
                GROUP BY
                    info_t_id
            ),
            get_info_ts AS (
                SELECT
                    description,
                    trainers,
                    type_T_name,
                    week_day_name,
                    duration,
                    available_numbers,
                    info_t_id
                FROM
                    get_trainers
                    JOIN info_t USING (info_t_id)
                    JOIN week_day USING (week_day_id)
                    JOIN type_T USING (type_T_id)
                WHERE
                    week_day_name IN {}
                    AND type_T_name IN {}
            )
            SELECT
                *
            FROM get_info_ts
        '''.format(
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_trainers])),
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_week_days])),
                '({})'.format(', '.join([f'"{elem}"' for elem in selected_type_Ts]))
            ),
        conn
    )
