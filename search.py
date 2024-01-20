from app import app
from flask import render_template, request
from utils import get_db_connection
from models.search_model import get_trainer_count, get_type_T_count, get_week_day_count, get_filtered_info_ts, get_all_trainers, get_all_type_Ts, get_all_week_days

@app.route('/search', methods=['GET', 'POST'])
def search():
    conn = get_db_connection()

    selected_trainers = []
    selected_type_Ts = []
    selected_week_days = []

    df_trainers = get_trainer_count(conn)
    df_type_Ts = get_type_T_count(conn)
    df_week_days = get_week_day_count(conn)
    df_info_ts = get_filtered_info_ts(
            conn,
            get_all_trainers(conn),
            get_all_type_Ts(conn),
            get_all_week_days(conn)
        )
    
    if request.method == 'POST':
        if 'confirm' in request.form:
            selected_trainers = request.form.getlist("trainers")
            selected_type_Ts = request.form.getlist("type_Ts")
            selected_week_days = request.form.getlist("week_days")

        if 'reset' in request.form:
            selected_trainers = []
            selected_type_Ts = []
            selected_week_days = []
        
        df_info_ts = get_filtered_info_ts(
            conn,
            get_all_trainers(conn) if not selected_trainers else selected_trainers,
            get_all_type_Ts(conn) if not selected_type_Ts else selected_type_Ts,
            get_all_week_days(conn) if not selected_week_days else selected_week_days
        )

    html = render_template(
        'search.html',
        selected_trainers=selected_trainers,
        df_trainers=df_trainers,
        selected_type_Ts=selected_type_Ts,
        df_type_Ts=df_type_Ts,
        selected_week_days=selected_week_days,
        df_week_days=df_week_days,
        df_info_ts=df_info_ts
    )
    return html
