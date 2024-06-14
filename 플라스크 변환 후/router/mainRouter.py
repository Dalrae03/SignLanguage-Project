from flask import Blueprint, render_template, request, redirect, session
import bcrypt
from model.db import get_db_connection

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    if 'is_logined' in session:
        return render_template('firstLayout2.html', title="CTH 메인페이지", content_template="Main Page/index.html", username=session['nickname'])
    else:
        return render_template('firstLayout.html', title="CTH 메인페이지", content_template="Main Page/index.html")

@main_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if username and email and password:
            try:
                connection = get_db_connection()
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                    result = cursor.fetchone()
                    if result is None:
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (username, email, hashed_password))
                        connection.commit()
                        return redirect('/?signup=success')
                    else:
                        return redirect('/?signup=useing')
            except Exception as e:
                print('Database query error:', e)
                return 'Database query error', 500
            finally:
                connection.close()
        else:
            return 'Required fields are missing', 400
    return render_template('layout.html', title="CTH 회원가입 페이지", content_template="SignUp Page/signup.html")

@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email and password:
            try:
                connection = get_db_connection()
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                    user = cursor.fetchone()
                    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                        session['is_logined'] = True
                        session['nickname'] = user['name']
                        return redirect('/?login=success')
                    else:
                        return redirect('/?login=error')
            except Exception as e:
                print('Database query error:', e)
                return 'Database query error', 500
            finally:
                connection.close()
        else:
            return redirect('/?login=noinput')
    return render_template('layout.html', title="CTH 로그인 페이지", content_template="Login Page/login.html")

@main_blueprint.route('/studying')
def studying():
    if 'is_logined' in session:
        return render_template('firstLayout2.html', title="CTH 수어 학습하기", content_template="Main Page/studying.html", username=session['nickname'])
    else:
        return redirect('/?nologin')

@main_blueprint.route('/logout')
def logout():
    session.pop('is_logined', None)
    session.pop('nickname', None)
    return redirect('/')

@main_blueprint.route('/lecture')
def lecture():
    if 'is_logined' in session:
        return render_template('firstLayout2.html', title="CTH 자화 자음 학습하기", content_template="Main Page/lecture.html", username=session['nickname'])
    else:
        return redirect('/?nologin')

@main_blueprint.route('/flashCard')
def flashCard():
    if 'is_logined' in session:
        return render_template('firstLayout2.html', title="CTH 플래시카드", content_template="Main Page/flashCard.html", username=session['nickname'])
    else:
        return redirect('/?nologin')

@main_blueprint.route('/acidRain')
def acidRain():
    if 'is_logined' in session:
        return render_template('firstLayout2.html', title="CTH 산성비", content_template="Main Page/acidRain.html", username=session['nickname'])
    else:
        return redirect('/?nologin')

@main_blueprint.route('/class')
def class_view():
    if 'is_logined' in session:
        return render_template('firstLayout2.html', title="CTH 자화 자음 1강", content_template="Main Page/class.html", username=session['nickname'])
    else:
        return redirect('/?nologin')


@main_blueprint.route('/myPage')
def myPage():
    if 'is_logined' in session:
        return render_template('firstLayout2.html', title="CTH 마이페이지", content_template="Main Page/myPage.html", username=session['nickname'])
    else:
        return redirect('/?nologin')


@main_blueprint.route('/myCheckPage')
def myCheckPage():
    if 'is_logined' in session:
        return render_template('firstLayout2.html', title="CTH 마이페이지", content_template="Main Page/myCheck.html", username=session['nickname'])
    else:
        return redirect('/?nologin')