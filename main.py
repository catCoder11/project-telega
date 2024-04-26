from data import db_session
import datetime
import random
import string
from flask import Flask, render_template, redirect, request, session
from data.users import *
from data.k_tables import *
from data.access import *
from forms.user import *
from forms.redacture import *
from data.rasp import Rasp
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
import os

def get_me_back():
    try:
        x = current_user.telegram_id
    except:
        return redirect("/")
    current_class = session.get("klass", 0)
    db_sess = db_session.create_session()
    access = db_sess.query(Access).filter(Access.klass_id == current_class,
                                          Access.telegram_id == current_user.telegram_id,
                                          Access.access_type_id == 3).first()
    if not access:
        return True


def get_date(weekday, reverse=False):
    x = datetime.date.today()
    while x.weekday() != int(weekday):
        if reverse:
            x -= datetime.timedelta(days=1)
        else:
            x += datetime.timedelta(days=1)
    return x


def main():
    if not os.path.isfile("db/school_rasp.db"):
        db_session.global_init("db/school_rasp.db")
        subjects = ["Русский", "Алгебра", "Литература", "Физкультура",
                    "Музыка", "Физика", "Геометрия", "Математика", "Информатика",
                    "География", "Обществознание", "ОБЖ", "История",
                    "Биология", "ИЗО", "Труды", "Иностранный язык", "Химия", "Разговоры о важном"]
        db_sess = db_session.create_session()
        db_sess.add(K_access_type(name="Пользователь"))
        db_sess.add(K_access_type(name="Куратор"))
        db_sess.add(K_access_type(name="Админ"))
        for sbj in subjects:
            subject = K_subject()
            subject.name = sbj
            subject.creator = "KotyaPool"
            db_sess.add(subject)
        db_sess.commit()
    else:
        db_session.global_init("db/school_rasp.db")
    app.run(port=PORT, host=HOST)


HOST = "localhost"
PORT = "8080"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=100)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if not current_user.is_authenticated:
        return redirect('/register')
    date = get_date("0")
    db_sess = db_session.create_session()
    current_class = session.get("klass", 0)
    check = db_sess.query(Access).filter(Access.telegram_id == current_user.telegram_id).first()
    if not current_class and bool(check):
        return redirect("/choose_class")
    full_rasp = {"понедельник": "", "вторник": "", "среда": "", "пятница": "", "суббота": "", "воскресенье": ""}
    i = 0
    rasp_subj = db_sess.query(Rasp).filter(Rasp.klass_id == current_class).all()
    for key in full_rasp.keys():
        full_rasp[key] = sorted([el for el in rasp_subj if el.start_time.date().weekday() == i],
                                key=lambda x: x.start_time)
        i += 1
    if db_sess.query(Access).filter(Access.klass_id == current_class,
                                    Access.telegram_id == current_user.telegram_id,
                                    Access.access_type_id==3).first():
        check=True
    else:
        check=False
    form = RaspForm()
    if form.validate_on_submit():
        if form.create_class.data:
            return redirect("/create_class")
        elif form.add_class.data:
            return redirect("/add_class")
        elif form.redact_teachers.data:
            return redirect("/teachers")
        elif form.redact_auditories.data:
            return redirect("/auditories")
        elif form.redact_corpuses.data:
            return redirect("/corpuses")
    return render_template('main_page.html', title='Расписание', form=form, full_rasp=full_rasp,
                           check=check, current_user=current_user)

@app.route('/choose_class', methods=['GET', 'POST'])
@login_required
def choose():
    form = ChooseClassForm()
    db_sess = db_session.create_session()
    if form.submit.data:
        x = form.klass.data.split(" ")[1]
        session['klass'] = x
        current_user.current_class_id = x
        return redirect('/')
    filt = db_sess.query(Access).filter(Access.telegram_id == current_user.telegram_id).all()
    form.klass.choices = ["ID " + str(el.klass.id) + " :" + el.klass.name for el in filt]
    return render_template("choose_class.html", form=form)

@app.route('/teachers', methods=['GET', 'POST'])
def teachers():
    if get_me_back():
        return redirect("/")
    db_sess = db_session.create_session()
    current_class = session.get("klass", 0)
    klass = db_sess.query(K_klass).filter(K_klass.id == current_class).first()
    teachers = db_sess.query(K_teacher).filter(K_teacher.klass == klass).all()
    return render_template('teachers.html', form=teachers, host=HOST, port=PORT)


@app.route('/redact_teachers/<id>', methods=['GET', 'POST'])
def redact_teachers(id):
    if get_me_back():
        return redirect("/")
    db_sess = db_session.create_session()
    current_class = session.get("klass", 0)
    klass = db_sess.query(K_klass).filter(K_klass.id == current_class).first()
    form = RedactForm()
    form.id = id
    teacher = K_teacher()
    if id != "0":
        teacher = db_sess.query(K_teacher).filter(K_teacher.id == form.id).first()
    if form.validate_on_submit():
        teacher.fio = form.name.data
        teacher.creator = current_user.telegram_id
        if id == "0":
            klass.teachers.append(teacher)
        db_sess.commit()
        return redirect("/teachers")
    w_name = ""
    if id != "0":
        w_name = teacher.fio
    return render_template('redact.html', form=form, w_name=w_name)


@app.route('/auditories', methods=['GET', 'POST'])
def auditories():
    if get_me_back():
        return redirect("/")
    db_sess = db_session.create_session()
    current_class = session.get("klass", 0)
    klass = db_sess.query(K_klass).filter(K_klass.id == current_class).first()
    corpuses = [el.id for el in db_sess.query(K_corpus).filter(K_corpus.klass == klass).all()]
    auditories = db_sess.query(K_auditory).filter(K_auditory.corpus_id.in_(corpuses)).all()
    return render_template('auditories.html', form=auditories, host=HOST, port=PORT, option=["Oleg", "Dimon"])


@app.route('/redact_auditories/<id>', methods=['GET', 'POST'])
def redact_auditories(id):
    if get_me_back():
        return redirect("/")
    db_sess = db_session.create_session()
    current_class = session.get("klass", 0)
    klass = db_sess.query(K_klass).filter(K_klass.id == current_class).first()
    form = RedactAudForm()
    form.id = id
    auditory = K_auditory()
    form.sost.choices = [(el.id, el.name)
                         for el in db_sess.query(K_corpus).filter(K_corpus.klass == klass).all()]
    if id != "0":
        auditory = db_sess.query(K_auditory).filter(K_auditory.id == form.id).first()
    if form.validate_on_submit():
        auditory.name = form.name.data
        auditory.creator = current_user.telegram_id
        corp = db_sess.query(K_corpus).filter(K_corpus.id == form.sost.data[0]).first()
        corp.auditory.append(auditory)
        if id == "0":
            db_sess.add(auditory)
        db_sess.commit()
        return redirect("/auditories")
    w_name = ""
    if id != "0":
        w_name = auditory.name

    return render_template('redact_auditories.html', form=form, w_name=w_name, corpuses=corpuses)


@app.route('/corpuses', methods=['GET', 'POST'])
def corpuses():
    if get_me_back():
        return redirect("/")
    db_sess = db_session.create_session()
    current_class = session.get("klass", 0)
    klass = db_sess.query(K_klass).filter(K_klass.id == current_class).first()
    corpuses = db_sess.query(K_corpus).filter(K_corpus.klass == klass).all()
    return render_template('corpuses.html', form=corpuses, host=HOST, port=PORT)


@app.route('/redact_corpuses/<id>', methods=['GET', 'POST'])
def redact_corpuses(id):
    if get_me_back():
        return redirect("/")
    db_sess = db_session.create_session()
    form = RedactForm()
    form.id = id
    corpus = K_corpus()
    current_class = session.get("klass", 0)
    klass = db_sess.query(K_klass).filter(K_klass.id == current_class).first()
    if id != "0":
        corpus = db_sess.query(K_corpus).filter(K_corpus.id == form.id).first()
    if form.validate_on_submit():
        corpus.name = form.name.data
        corpus.creator = current_user.telegram_id
        if id == "0":
            klass.corpus.append(corpus)
        db_sess.commit()
        return redirect("/corpuses")
    w_name = ""
    if id != "0":
        w_name = corpus.name
    return render_template('redact.html', form=form, w_name=w_name)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", current_user=current_user)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.telegram_id == form.telegram_id.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", current_user=current_user)
        user = User(
            name=form.name.data,
            telegram_id = form.telegram_id.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.telegram_id == form.telegram_id.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=form, current_user=current_user)
    return render_template('login.html', title='Авторизация', form=form, current_user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('klass', None)
    return redirect("/")


@app.route('/create_class', methods=['GET', 'POST'])
def create_class():
    if get_me_back():
        return redirect("/")
    db_sess = db_session.create_session()
    form = RedactForm()
    form.id = "0"
    if form.validate_on_submit():
        klass = K_klass()
        klass.name = form.name.data
        klass.creator = current_user.telegram_id
        klass.class_key = "".join(random.choices(string.printable, k=15))
        access = Access()
        access.creator = current_user.telegram_id
        access.telegram_id = current_user.telegram_id
        access.access_type_id = 3
        db_sess.add(klass)
        klass.access.append(access)
        current_user.current_class_id = klass.id
        db_sess.commit()
        return redirect("/")
    return render_template('redact.html', title='Создать класс', form=form, current_user=current_user,
                           w_name="")


@app.route('/add_class', methods=['GET', 'POST'])
def add_class():
    if get_me_back():
        return redirect("/")
    form = RedactForm()
    code_error = ""
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        check = db_sess.query(K_klass).filter(K_klass.class_key == form.name.data).first()
        if check:
            if not db_sess.query(Access).filter(Access.telegram_id == current_user.telegram_id).all():
                access = Access()
                current_user.current_class_id = check.id
                access_type = db_sess.query(K_access_type).filter(K_access_type.id == 1).first()
                access_type.access.append(access)
                check.access.append(access)
                user = db_sess.query(User).filter(User.id == current_user.id).first()
                user.access.append(access)
                db_sess.add(access)
                db_sess.commit()
        else:
            code_error = "Неверный ключ"
    else:
        code_error = "Вы уже состоите в этом классе"
    return render_template('add_class.html', title='Войти в класс', form=form, current_user=current_user,
                           code_error=code_error)

@app.route('/days', methods=['GET', 'POST'])
def days():
    week = ["понедельник", "вторник", "среда", "пятница", "суббота", "воскресенье"]
    form = [(i, week[i]) for i in range(len(week))]
    return render_template('/days.html', form=form, host=HOST, port=PORT)

@app.route('/redact_day/<week_day>', methods=['GET', 'POST'])
def redact_day(week_day):
    if get_me_back():
        return redirect("/")
    db_sess = db_session.create_session()
    current_class = session.get("klass", 0)
    date = get_date(week_day, reverse=True)
    rasps = db_sess.query(Rasp).filter(Rasp.klass_id == current_class).all()
    rasps = sorted([el for el in rasps if el.start_time.date() == date], key=lambda x: x.start_time)
    return render_template('rasp.html', form=rasps, week_day=week_day, host=HOST, port=PORT)


@app.route('/redact_rasp/<week_day>/<id>', methods=['GET', 'POST'])
def redact_rasp(id, week_day):
    if get_me_back():
        return redirect("/")
    db_sess = db_session.create_session()
    form = RedactRaspForm()
    if id == "0":
        rasp = Rasp()
    else:
        rasp = db_sess.query(Rasp).filter(Rasp.id == id).first()
    current_class = session.get("klass", 0)
    klass = db_sess.query(K_klass).filter(K_klass.id == current_class).first()
    corpuses = [el.id for el in db_sess.query(K_corpus).filter(K_corpus.klass == klass).all()]
    auditories = db_sess.query(K_auditory).filter(K_auditory.corpus_id.in_(corpuses)).all()
    form.auditory.choices = [(el.id, el.name) for el in auditories]

    form.teacher.choices = [(el.id, el.fio) for el in db_sess.query(K_teacher).filter(K_teacher.klass == klass).all()]

    form.subject.choices = [(el.id, el.name) for el in db_sess.query(K_subject).all()]
    error = ""
    if form.submit and not (form.auditory.data and form.teacher.data and form.subject.data):
        error = "Нет нужных данных. Добавьте их и вернитесь\n"
        return render_template("redact_rasp.html", form=form, err=error)
    if form.validate_on_submit():
        rasp.auditory = db_sess.query(K_auditory).filter(K_auditory.id == form.auditory.data).first()
        rasp.teacher = db_sess.query(K_teacher).filter(K_teacher.id == form.teacher.data).first()
        rasp.subject = db_sess.query(K_subject).filter(K_subject.id == form.subject.data).first()
        rasp.klass = klass
        time = form.time.data
        date = get_date(week_day, reverse=True)
        rasp.start_time = datetime.datetime.combine(date, time)
        if id == "0":
            db_sess.add(rasp)
        db_sess.commit()
        return redirect("/redact_day/" + week_day)
    return render_template("redact_rasp.html", form=form, error=error)


if __name__ == '__main__':
    main()
