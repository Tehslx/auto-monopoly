from backend.config.config import *
from backend.database.forms import LoginForm, RegistrationForm, MonopolyAccountForm
from backend.database.extensions import db
from backend.database.models import User
import backend.libs.monopolyone.monopolyone


app = Flask(__name__)
app.config['SECRET_KEY'] = '992h9bd422ab8es4d12e23dg2h53ds5dafcb9a3v3ec15f71bbf5dc987dsh27823bcbf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth'

failed_login_attempts = {}
bot_processes = {}
bot_queues = {}  # Очереди для вывода бота по user_id

socketio = SocketIO(app) # сокеты

@login_manager.user_loader
def load_user(user_id):
    with db.session() as session:
        return session.get(User, int(user_id))

def create_database():
    if not os.path.exists('instance/site.db'):
        with app.app_context():
            db.create_all()

def get_health_data(proxy=None):
    MonopolyOne = backend.libs.monopolyone.monopolyone.Client()
    print(MonopolyOne.status_health(proxy=proxy))
    url = "https://monopoly-one.com/api/status.health"
    try:
        if proxy:
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
            response = requests.get(url, proxies=proxies, timeout=5)
        else:
            response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def get_cache_key():
    if not current_user.is_authenticated:
        return "no_user"
    user_id = current_user.id
    proxy = current_user.proxy if current_user.proxy else "no_proxy"
    return f"health_data_{user_id}_{proxy}"

def get_cached_health_data():
    cache_key = get_cache_key()
    
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    proxy = None
    if current_user.is_authenticated:
        proxy = current_user.proxy if not current_user.is_admin or (current_user.is_admin and current_user.proxy) else None

    health_data = get_health_data(proxy)
    if health_data and health_data.get("code") == 0:
        total = health_data.get("data", {}).get("total", {})
        sections = health_data.get("data", {}).get("sections", {})
    else:
        total = {}
        sections = {}

    cache.set(cache_key, (total, sections), timeout=30)
    return total, sections

def should_show_api_status():
    if not current_user.is_authenticated:
        return False
    if current_user.is_admin:
        return True
    return bool(current_user.proxy)

def read_output(process, user_id):
    """Чтение вывода процесса и отправка через WebSocket"""
    while True:
        try:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                bot_queues[user_id].put(line.strip())
                socketio.emit('bot_output', {'user_id': user_id, 'message': line.strip()}, namespace='/console')
        except Exception as e:
            socketio.emit('bot_output', {'user_id': user_id, 'message': f"Ошибка чтения вывода: {str(e)}"}, namespace='/console')
            break
    socketio.emit('bot_output', {'user_id': user_id, 'message': 'Бот завершил работу'}, namespace='/console')

def read_error(process, user_id):
    """Чтение ошибок процесса и отправка через WebSocket"""
    while True:
        try:
            line = process.stderr.readline()
            if not line and process.poll() is not None:
                break
            if line:
                bot_queues[user_id].put(line.strip())
                socketio.emit('bot_output', {'user_id': user_id, 'message': f"Ошибка: {line.strip()}"}, namespace='/console')
        except Exception as e:
            socketio.emit('bot_output', {'user_id': user_id, 'message': f"Ошибка чтения ошибок: {str(e)}"}, namespace='/console')
            break

def start_bot_process(user):
    if not user.monopoly_email or not user.monopoly_password:
        user.bot_enabled = False
        db.session.commit()
        return False
    try:
        env = os.environ.copy()
        env['MONOPOLY_EMAIL'] = user.monopoly_email
        env['MONOPOLY_PASSWORD'] = user.monopoly_password
        if user.proxy:
            env['MONOPOLY_PROXY'] = user.proxy
        process = subprocess.Popen(
            ['python', 'backend/monopoly.py'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        bot_processes[user.id] = process
        bot_queues[user.id] = queue.Queue()
        threading.Thread(target=read_output, args=(process, user.id), daemon=True).start()
        threading.Thread(target=read_error, args=(process, user.id), daemon=True).start()
        return True
    except Exception:
        user.bot_enabled = False
        db.session.commit()
        return False

def stop_bot_process(user_id):
    if user_id in bot_processes and bot_processes[user_id].poll() is None:
        try:
            bot_processes[user_id].terminate()
            bot_processes[user_id].wait(timeout=5)
        except subprocess.TimeoutExpired:
            bot_processes[user_id].kill()
        except Exception:
            pass
        finally:
            del bot_processes[user_id]
            if user_id in bot_queues:
                del bot_queues[user_id]

def initialize_bot_processes():
    """Возобновляет процессы ботов для пользователей с bot_enabled=True при старте приложения"""
    with app.app_context():
        users = User.query.filter_by(bot_enabled=True).all()
        for user in users:
            start_bot_process(user)

@app.route('/')
def index():
    total, sections = get_cached_health_data() if should_show_api_status() else ({}, {})
    pending_total = User.query.filter_by(is_confirmed=False).count()
    show_api_status = should_show_api_status()
    return render_template('index.html', 
                           total=total, 
                           sections=sections, 
                           pending_total=pending_total, 
                           show_api_status=show_api_status)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    total, sections = get_cached_health_data() if should_show_api_status() else ({}, {})
    if current_user.is_authenticated and current_user.is_confirmed:
        return redirect(url_for('index'))

    login_form = LoginForm()
    registration_form = RegistrationForm()
    error_message = None
    success_message = None

    if 'login_submit' in request.form and login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        if username in failed_login_attempts:
            attempts, block_time = failed_login_attempts[username]
            if block_time > datetime.now():
                error_message = f'Аккаунт заблокирован на 15 минут. Осталось попыток: {5 - attempts}.'
                return render_template('auth.html', 
                                       login_form=login_form, 
                                       registration_form=registration_form, 
                                       error_message=error_message, 
                                       success_message=success_message, 
                                       total=total, 
                                       sections=sections, 
                                       show_api_status=should_show_api_status())

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            if user.is_confirmed:
                login_user(user, remember=True)
                if username in failed_login_attempts:
                    del failed_login_attempts[username]
                return redirect(url_for('profile', id=user.id))
            else:
                error_message = 'Аккаунт еще не подтвержден администратором.'
        else:
            if username not in failed_login_attempts:
                failed_login_attempts[username] = (1, datetime.now())
            else:
                attempts, _ = failed_login_attempts[username]
                attempts += 1
                if attempts >= 5:
                    failed_login_attempts[username] = (attempts, datetime.now() + timedelta(minutes=15))
                    error_message = 'Превышено количество попыток. Аккаунт заблокирован на 15 минут.'
                else:
                    failed_login_attempts[username] = (attempts, datetime.now())
                    error_message = f'Неверный никнейм или пароль. Осталось попыток: {5 - attempts}.'
        return render_template('auth.html', 
                               login_form=login_form, 
                               registration_form=registration_form, 
                               error_message=error_message, 
                               success_message=success_message, 
                               total=total, 
                               sections=sections, 
                               show_api_status=should_show_api_status())

    if request.method == 'POST' and 'register_submit' in request.form:
        @limiter.limit("5 per hour")
        def limited_registration():
            nonlocal error_message, success_message
            if registration_form.validate_on_submit():
                hashed_password = generate_password_hash(registration_form.password.data, method='pbkdf2:sha256')
                is_first_user = User.query.count() == 0
                new_user = User(
                    username=registration_form.username.data,
                    password=hashed_password,
                    is_confirmed=is_first_user,
                    is_admin=is_first_user
                )
                db.session.add(new_user)
                db.session.commit()
                success_message = 'Аккаунт успешно зарегистрирован' + (' и подтвержден как администратор.' if is_first_user else ' и ожидает подтверждения администратора.')
            else:
                if registration_form.username.errors:
                    error_message = registration_form.username.errors[0]
                else:
                    error_message = 'Ошибка при регистрации. Проверьте введенные данные.'
            return render_template('auth.html', 
                                   login_form=login_form, 
                                   registration_form=registration_form, 
                                   error_message=error_message, 
                                   success_message=success_message, 
                                   total=total, 
                                   sections=sections, 
                                   show_api_status=should_show_api_status())
        return limited_registration()

    show_api_status = should_show_api_status()
    return render_template('auth.html', 
                           login_form=login_form, 
                           registration_form=registration_form, 
                           error_message=error_message, 
                           success_message=success_message, 
                           total=total, 
                           sections=sections, 
                           show_api_status=show_api_status)

@app.route('/toggle_bot', methods=['POST'])
@login_required
def toggle_bot():
    data = request.get_json()
    if not data or 'enabled' not in data:
        return jsonify({'success': False, 'error': 'Неверный запрос'}), 400

    enabled = data['enabled']
    user_id = current_user.id
    user = db.session.get(User, user_id)

    if enabled:
        if not current_user.monopoly_email or not current_user.monopoly_password:
            return jsonify({'success': False, 'error': 'Добавьте данные аккаунта Monopoly'}), 400
        if user_id not in bot_processes or bot_processes[user_id].poll() is not None:
            if start_bot_process(user):
                user.bot_enabled = True
                db.session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': 'Не удалось запустить бота'}), 500
        else:
            user.bot_enabled = True
            db.session.commit()
            return jsonify({'success': True})
    else:
        stop_bot_process(user_id)
        user.bot_enabled = False
        db.session.commit()
        return jsonify({'success': True})

@app.route('/send_hello', methods=['POST'])
@login_required
def send_hello():
    GAME_M1TV_URL_TEMPLATE = "https://monopoly-one.com/m1tv/#/{}/{}"
    user_id = current_user.id
    try:
        MonopolyOne = backend.libs.monopolyone.monopolyone.Client()
        sign1 = MonopolyOne.sign_in(email="tomas_shelby63@mail.ru", password="1234567890")
        access_token1 = sign1.access_token
        current_game = MonopolyOne.users_get(user_ids=sign1.user_id, access_token=access_token1).user_1.current_game
        access_token2 = MonopolyOne.sign_in(email="rob679bd@gmail.com", password="Korobkaradio14!", proxy="shegzfs:gukwiHj66dtnrsdb@188.130.142.203:5500").access_token
        access_token3 = MonopolyOne.sign_in(email="sairusz59@gmail.com", password="X3YuhdgFw!iX.kY", proxy="shegzfs:gukwiHj66dtnrsdb@188.130.142.239:5500").access_token

        room1 = MonopolyOne.room_create(maxplayers=4, access_token=access_token1).room_id
        MonopolyOne.room_join(room1, access_token=access_token2)
        MonopolyOne.room_join(room1, access_token=access_token3)

        current_game = MonopolyOne.users_get(user_ids=sign1.user_id, access_token=access_token1).user_1.current_game
        gs_id = current_game.gs_id
        gs_game_id = current_game.gs_game_id
        url = GAME_M1TV_URL_TEMPLATE.format(gs_id, gs_game_id) if gs_id and gs_game_id else None
        socketio.emit('bot_output', {'user_id': user_id, 'message': f'Игра запущена, смотреть: {url}'}, namespace='/console')
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    total, sections = get_cached_health_data()
    pending_total = User.query.filter_by(is_confirmed=False).count()
    if current_user.id != id:
        return redirect(url_for('profile', id=current_user.id))
    
    user = User.query.get_or_404(id)
    form = MonopolyAccountForm()
    error_message = None
    success_message = None

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            proxy = form.proxy.data

            if not current_user.is_admin and not proxy:
                error_message = "Прокси обязателен для заполнения."
            else:
                api_url = "https://monopoly-one.com/api/auth.signin"
                payload = {"email": email, "password": password}
                try:
                    response = requests.post(api_url, json=payload)
                    response_data = response.json()

                    if response_data.get("code") == 0:
                        user.monopoly_email = email
                        user.monopoly_password = password
                        user.proxy = proxy
                        db.session.commit()
                        cache.delete(get_cache_key())
                        if user.bot_enabled:
                            stop_bot_process(user.id)
                            start_bot_process(user)
                    else:
                        error_code = response_data.get("code")
                        error_msg = response_data.get("message", "Ошибка авторизации в Monopoly")
                        error_message = f"{error_msg} (код: {error_code})"
                except requests.exceptions.RequestException as e:
                    error_message = f"Ошибка при запросе к API Monopoly: {str(e)}"
                except ValueError:
                    error_message = "Ошибка при обработке ответа от API Monopoly."
        else:
            errors = []
            for field, field_errors in form.errors.items():
                errors.extend(field_errors)
            error_message = 'Ошибка при сохранении данных: ' + '; '.join(errors)

    show_api_status = should_show_api_status()
    return render_template('profile.html',
                           user=user,
                           form=form,
                           total=total,
                           sections=sections,
                           pending_total=pending_total,
                           error_message=error_message,
                           show_api_status=show_api_status,
                           bot_enabled=user.bot_enabled)

@socketio.on('connect', namespace='/console')
def handle_connect():
    if current_user.is_authenticated:
        user_id = current_user.id
        emit('bot_output', {'user_id': user_id, 'message': 'Подключение к консоли установлено'}, namespace='/console')
        if user_id in bot_queues:
            while not bot_queues[user_id].empty():
                emit('bot_output', {'user_id': user_id, 'message': bot_queues[user_id].get()}, namespace='/console')

@app.route('/profile/delete_monopoly/<int:user_id>', methods=['POST'])
@login_required
def delete_monopoly(user_id):
    user = User.query.get_or_404(user_id)
    if user.id != current_user.id:
        total, sections = get_cached_health_data()
        return render_template('404.html', total=total, sections=sections)
    user.monopoly_email = None
    user.monopoly_password = None
    user.proxy = None
    stop_bot_process(user.id)
    user.bot_enabled = False
    db.session.commit()
    cache.delete(get_cache_key())
    return redirect(url_for('profile', id=user.id))

@app.route('/admin')
@login_required
def admin():
    total, sections = get_cached_health_data()
    if not current_user.is_admin:
        return render_template('404.html', total=total, sections=sections)
    confirmed_users = User.query.filter_by(is_confirmed=True).limit(4).all()
    pending_users = User.query.filter_by(is_confirmed=False).limit(4).all()
    confirmed_total = User.query.filter_by(is_confirmed=True).count()
    pending_total = User.query.filter_by(is_confirmed=False).count()
    show_api_status = should_show_api_status()
    return render_template('admin.html',
                           total=total,
                           sections=sections,
                           confirmed_users=confirmed_users,
                           pending_users=pending_users,
                           confirmed_total=confirmed_total,
                           pending_total=pending_total,
                           show_api_status=show_api_status)

@app.route('/admin/load_more', methods=['GET'])
@login_required
def load_more():
    if not current_user.is_admin:
        total, sections = get_cached_health_data()
        return render_template('404.html', total=total, sections=sections)
    offset = int(request.args.get('offset', 0))
    limit = 4
    section = request.args.get('section')
    
    if section == 'confirmed':
        users = User.query.filter_by(is_confirmed=True).offset(offset).limit(limit).all()
        total = User.query.filter_by(is_confirmed=True).count()
    elif section == 'pending':
        users = User.query.filter_by(is_confirmed=False).offset(offset).limit(limit).all()
        total = User.query.filter_by(is_confirmed=False).count()
    else:
        return jsonify({'error': 'Invalid section'}), 400

    users_data = [{
        'id': user.id,
        'username': user.username,
        'monopoly_email': user.monopoly_email or 'N/A',
        'monopoly_password': user.monopoly_password or 'N/A',
        'proxy': user.proxy or 'N/A'
    } for user in users]

    return jsonify({
        'users': users_data,
        'has_more': offset + len(users) < total
    })

@app.route('/admin/confirm/<int:user_id>', methods=['POST'])
@login_required
def confirm_user(user_id):
    if not current_user.is_admin:
        total, sections = get_cached_health_data()
        return render_template('404.html', total=total, sections=sections)
    user = User.query.get_or_404(user_id)
    user.is_confirmed = True
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        total, sections = get_cached_health_data()
        return render_template('404.html', total=total, sections=sections)
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/logout')
@login_required
def logout():
    total, sections = get_cached_health_data() if should_show_api_status() else ({}, {})
    logout_user()
    return redirect(url_for('index'))

@app.route('/health')
@limiter.limit("100 per hour")
def health():
    if not current_user.is_admin and not current_user.proxy:
        return redirect(url_for('index'))
    
    total, sections = get_cached_health_data()
    pending_total = User.query.filter_by(is_confirmed=False).count()
    show_api_status = should_show_api_status()
    return render_template('health.html',
                           total=total,
                           sections=sections,
                           pending_total=pending_total,
                           show_api_status=show_api_status)

@app.route('/why-proxy')
def whyproxy():
    total, sections = get_cached_health_data() if should_show_api_status() else ({}, {})
    pending_total = User.query.filter_by(is_confirmed=False).count()
    show_api_status = should_show_api_status()
    return render_template('why-proxy.html',
                           total=total,
                           sections=sections,
                           pending_total=pending_total,
                           show_api_status=show_api_status)

@app.errorhandler(404)
def page_not_found(error):
    total, sections = get_cached_health_data() if should_show_api_status() else ({}, {})
    pending_total = User.query.filter_by(is_confirmed=False).count()
    show_api_status = should_show_api_status()
    return render_template('404.html',
                           total=total,
                           sections=sections,
                           pending_total=pending_total,
                           show_api_status=show_api_status), 404

@app.errorhandler(429)
def ratelimit_handler(e):
    total, sections = get_cached_health_data() if should_show_api_status() else ({}, {})
    pending_total = User.query.filter_by(is_confirmed=False).count()
    if request.path == '/auth':
        error_message = "Слишком много регистраций с вашего IP. Пожалуйста, подождите час перед следующей попыткой."
        return render_template('auth.html',
                               login_form=LoginForm(),
                               registration_form=RegistrationForm(),
                               error_message=error_message,
                               total=total,
                               sections=sections,
                               show_api_status=should_show_api_status()), 429
    else:
        error_message = "Слишком много запросов. Пожалуйста, подождите перед следующей попыткой."
        return render_template('429.html',
                               error_message=error_message,
                               total=total,
                               sections=sections,
                               pending_total=pending_total,
                               show_api_status=should_show_api_status()), 429

if __name__ == '__main__':
    with app.app_context():
        create_database()
        initialize_bot_processes()
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)