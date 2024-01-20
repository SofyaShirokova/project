from app import app
from flask import render_template
from utils import get_db_connection
from models.new_info_t_model import get_type_T, get_week_day, get_trainer

@app.route('/info_t', methods=['GET'])
def new_info_t():
    conn = get_db_connection()

    df_type_T = get_type_T(conn)
    df_week_day = get_week_day(conn)
    df_trainer = get_trainer(conn)

    html = render_template(
        'new_info_t.html',
        df_type_T=df_type_T,
        df_week_day=df_week_day,
        df_trainer=df_trainer,
        len=len,
    )
    return html

