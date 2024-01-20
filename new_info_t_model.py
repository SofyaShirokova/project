import pandas as pd
def get_type_T(conn):
    return pd.read_sql(
    '''
            SELECT
                type_T_id,
                type_T_name
            FROM
                type_T
        ''',
        conn
    )
def get_week_day(conn):
    return pd.read_sql(
    '''
            SELECT
                week_day_id,
                week_day_name
            FROM
                week_day
        ''',
        conn
    )
def get_trainer(conn):
    return pd.read_sql(
        '''
                SELECT
                    trainer_id,
                    trainer_name
                FROM
                    trainer
            ''',
        conn
    )