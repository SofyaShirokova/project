from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_sportsmen, get_info_t_sportsmen, get_new_sportsmen, borrow_info_t, set_return_date,del_info_t_sportsmen, add_info_t, add_trainer

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()

    if request.values.get('sportsmen'):
        sportsmen_id = int(request.values.get('sportsmen'))
        session['sportsmen_id'] = sportsmen_id
    elif request.values.get('new_sportsmen'):
        new_sportsmen = request.values.get('new_sportsmen')
        session['sportsmen_id'] = get_new_sportsmen(conn, new_sportsmen)
        print("get_new_sportsmen(conn, new_sportsmen) = ", get_new_sportsmen(conn, new_sportsmen))
    elif request.values.get('info_t'):
        info_t_id = int(request.values.get('info_t'))
        borrow_info_t(conn, info_t_id, session['sportsmen_id'])
    elif request.values.get('return_val'):
        info_t_sportsmen_id = request.values.get("return_val")
        set_return_date(conn, info_t_sportsmen_id)
    elif request.values.get('delete'):
        info_t_sportsmen_id = request.values.get('info_t_sportsmen_id')
        del_info_t_sportsmen(conn, info_t_sportsmen_id)

    elif request.values.get('add_new_info_t'):
        description = request.values.get('description')
        type_T = int(request.values.get('type_T'))
        week_day = int(request.values.get('week_day'))
        duration = int(request.values.get('duration'))
        available_numbers = int(request.values.get('available_numbers'))

        info_t_id = add_info_t(conn, description, type_T, week_day, duration, available_numbers)
        trainer_id = request.values.get('trainer')
        add_trainer(conn, info_t_id, trainer_id)

    else:
        if "sportsmen_id" in session.keys():
            session['sportsmen_id'] = session['sportsmen_id']
        else:
            session['sportsmen_id'] = 1

    df_sportsmen = get_sportsmen(conn)
    df_info_t_sportsmen = get_info_t_sportsmen(conn, session['sportsmen_id'])

    html = render_template(
        'index.html',
        sportsmen_id=session['sportsmen_id'],
        combo_box=df_sportsmen,
        info_t_sportsmen=df_info_t_sportsmen,
        len=len,
    )
    return html


