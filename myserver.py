import time
import os
from flask import Flask, render_template, request, session, escape, redirect, url_for

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


from datetime import date
import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/sanagustin.db"
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(SECRET_KEY='azbys', DATABASE=os.path.join(app.instance_path, 'mysite.sqlite'),)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 16*2**20
app.config["ALLOWED_EXTENSIONS"] = set(["pdf", "png", "jpg", "jpeg", "gif"])
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(app.root_path, "cache")
app.config["SECRET_KEY"] = "azbys"
app.config["SESSION_FILE_THRESHOLD"] = 1000
Base = declarative_base()


engine = create_engine(dbdir)
session_maker = sessionmaker()
session_maker.configure(bind=engine)
Base.metadata.create_all(engine)
sessionx = session_maker()
if app.config is None:
    app.config.from_object(app.config.BaseConfig)
else:
    app.config.from_object(app.config)

db = SQLAlchemy(app)


app.secret_key = 'azbys'


try:

    class UsuariosOficiales(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), unique=True, nullable=False)
        password = db.Column(db.String(80), nullable=False)
        nombreusuario = db.Column(db.String(255))
        codigo = db.Column(db.String(255))
        celular = db.Column(db.String(255))
        direccion = db.Column(db.String(255), nullable=False)

        def serialize(self):
            return {
                "id": self.id, "username": self.username, "password": self.password, "nombreusuario": self.nombreusuario, "codigo ": self.codigo, "celular": self.celular, "direccion": self.direccion
            }

    class OficialesEntrada(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        idoficial = db.Column(db.String(50), unique=True, nullable=False)
        codigo = db.Column(db.String(80), nullable=False)
        horaEntrada = db.Column(db.String(255))
        horaSalida = db.Column(db.String(255))
        puesto = db.Column(db.String(255))

        def serialize(self):
            return {
                "id": self.id, "idoficial": self.idoficial, "codigo": self.codigo, "horaEntrada": self.horaEntrada, "horaSalida ": self.horaSalida, "puesto": self.puesto
            }

    class UsuariosSanAgustin(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), unique=True, nullable=False)
        password = db.Column(db.String(80), nullable=False)
        nombreusuario = db.Column(db.String(255))
        pin = db.Column(db.String(255))
        casa = db.Column(db.String(255))
        permanentes = db.Column(db.String(255), nullable=False)

        def serialize(self):
            return {
                "id": self.id, "username": self.username, "password": self.password, "nombreusuario": self.nombreusuario, "pin": self.pin, "casa": self.casa, "permanentes": self.permanentes
            }

    class VisitasDiariasDB(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        idcondomino = db.Column(db.String(50))
        nombrevisita = db.Column(db.String(80))
        empresa = db.Column(db.String(255))
        hora = db.Column(db.String(255))
        fecha = db.Column(db.String(255))

        def serialize(self):
            return {
                "id": self.id, "idcondomino": self.idcondomino, "nombrevisita": self.nombrevisita, "empresa": self.empresa, "hora": self.hora, "fecha": self.fecha
            }

    class Ranchos(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        idcondomino = db.Column(db.String(50))
        etapa = db.Column(db.String(80))
        hora = db.Column(db.String(255))
        fecha = db.Column(db.String(255))

        def serialize(self):
            return {
                "id": self.id, "idcondomino": self.idcondomino, "etapa": self.etapa, "hora": self.hora, "fecha": self.fecha
            }
    db.create_all()
    db.session.commit()

except Exception as e:
    print(str(e))

def create_app():
    @app.route('/home2')
    def perfil_home():
        return render_template('perfil_home.html')
    
    @app.route('/')
    def uno():
        return render_template('uno.html')

    @app.route('/cv')
    def cv():
        return render_template('cv.html')

    @app.route('/oficiales')
    def oficiales():
        return render_template('oficiales/oficiales.html')

    @app.route("/logoutf")
    def logoutf():
        try:
            session.pop('loggedin', None)
            return redirect(url_for('.oficiales'))
        except:
            return redirect(url_for('.oficiales'))

    @app.route("/loginf", methods=["GET", "POST"])
    def loginf():

        if request.method == "POST":
            mensaje = ''
            usuario_condominio = request.form["username"]
            password_condominio = request.form["password"]
            time.sleep(2)
            user = UsuariosOficiales.query.filter_by(
                username=request.form["username"]).first()
            if user and check_password_hash(user.password, request.form["password"]):
                session["usernamef"] = user.username
                session["idf"] = user.id
                session["loggedin"] = True
                usx = str(session["usernamef"])
                user = UsuariosOficiales.query.filter_by(username=usx).first()
                id_condominio = user.id
                usuario_condominio = user.username
                password_condominio = user.password
                nombreusuario_condominio = user.nombreusuario
                codigo = user.codigo
                celular = user.celular
                direccion = user.direccion
                usuarioCompleto = [[id_condominio, usuario_condominio, password_condominio,
                                    nombreusuario_condominio, codigo, celular, direccion]]
                time.sleep(1)
                mensaje = ''
#codigo conjunto del tuturial video 1 2 y 3
                usx = str(session["usernamef"])
                user = UsuariosOficiales.query.filter_by(username=usx).first()
                id_condominio = user.id
                usuario_condominio = user.username
                password_condominio = user.password
                nombreusuario_condominio = user.nombreusuario
                codigo = user.codigo
                celular = user.celular
                direccion = user.direccion
                usuarioCompleto = [[id_condominio, usuario_condominio, password_condominio,
                                    nombreusuario_condominio, codigo, celular, direccion]]
                time.sleep(1)
                nombre_xxx = nombreusuario_condominio
                msk = ''
                ausencias = '0'
                tardias = '1'
                faltas = '1'
                meritos = '98'
                amonestaciones = '0'
                return redirect(url_for('.homef'))
            else:
                mensaje = "Tu usuario es incorrecto, por seguridad te hemos sacado de nuestra plataforma"
        else:
            mensaje = 'Favor iniciar sesión'

        return render_template("oficiales/login.html", mensaje=mensaje)

    @app.route("/homef", methods=["GET", "POST"])
    def homef():
        if "usernamef" in session:
            session['loggedin'] = True
            mensaje = ''
            usx = str(session["usernamef"])
            user = UsuariosOficiales.query.filter_by(username=usx).first()
            id_condominio = user.id
            usuario_condominio = user.username
            password_condominio = user.password
            nombreusuario_condominio = user.nombreusuario
            codigo = user.codigo
            celular = user.celular
            direccion = user.direccion
            usuarioCompleto = [[id_condominio, usuario_condominio, password_condominio,
                                nombreusuario_condominio, codigo, celular, direccion]]
            time.sleep(1)
            mensaje = ''
            msk = ''
            ausencias = '0'
            tardias = '1'
            faltas = '1'
            meritos = '98'
            amonestaciones = 'gfdg'

            return render_template('oficiales/.html', usuario_xxx=nombreusuario_condominio, tardias=tardias, faltas=faltas, meritos=meritos, amonestaciones=amonestaciones, ausencias=ausencias, direccion=direccion, mensaje=mensaje, celular=celular, codigo=codigo, msk=msk, usuarioCompleto=usuarioCompleto)
        else:
            session.pop('loggedin', None)
            session.pop('idf', None)
            session.pop('usernamef', None)
            mensaje = ''
        return render_template('oficiales/login.html')

    @app.route("/registrarf", methods=["GET", "POST"])
    def registrarf():
        mensaje = ''
        if request.method == "POST":
            if request.form["acceso"] == '':
                hashed_pw = generate_password_hash(
                    request.form["password"], method="sha256")
                username = request.form["username"]
                password = hashed_pw
                nombreusuario = request.form["nombreusuario"]
                codigo = request.form["codigo"]
                celular = request.form["celular"]
                direccion = request.form["direccion"]
                time.sleep(.6)
                try:
                    new_user = UsuariosOficiales(username=request.form["username"], password=hashed_pw, nombreusuario=request.form["nombreusuario"],
                                                 codigo=request.form["codigo"], celular=request.form["celular"], direccion=request.form["direccion"])
                    db.session.add(new_user)
                    db.session.commit()
                    mensaje = 'Te has registrado con exito'
                    return redirect("oficiales/login.html", mensaje=mensaje)
                except:
                    mensaje = 'Usuario incorrecto, por seguridad te hemos sacado del sistema'
                    session.pop('loggedin', None)
                    session.pop('id', None)
                    session.pop('usernamef', None)
            return redirect("oficiales/login.html", mensaje=mensaje)

    @app.route("/formregistrof")
    def formregistrof():
        return render_template("oficiales/registrar.html")

    @app.route("/emtrada")
    def emtrada():
        return render_template("oficiales/entrada.html")

    @app.route('/horaentradaf', methods=['GET', 'POST'])
    def horaentradaf():
        mensaje = ''
        fechass = str(datetime.datetime.now())

        if request.method == 'POST':
            mensaje = 'Entrada registrada'
            try:
                idoficial = session["id"]
                puesto = request.form["puesto"]
                codigo = request.form["codigo"]
                nombre_usuario = session['usernamef']
                horaEntrada = fechass
                horaSalida = ''
                time.sleep(.6)

                try:
                    OficialesEntrada(idoficial=idoficial, codigo=codigo,
                                     horaEntrada=horaEntrada, horaSalida=horaSalida, puesto=puesto)
                    db.session.commit()
                    mensaje = 'se registro con exito tu entrada'
                    return render_template('oficiales/entrada.html', mensaje=mensaje)

                except Exception as e:
                    mensaje = 'ERROR DE REGISTRO' + str(e)
                    return redirect(url_for('.homef', mensaje=mensaje, fechass=fechass))
            except:
                pass
        return render_template(url_for('.emtrada', mensaje=mensaje, fechass=fechass))

    @app.route("/logout")
    def logout():
        try:
            session.pop('id', None)
            session.pop("username", None)
            mensaje = "¡Hasta pronto!"
            return redirect(url_for('.login', mensaje=mensaje))
        except:
            session.pop('id', None)
            session.pop("username", None)
            mensaje = "¡Hasta pronto!"

        return redirect(url_for('.perfil_home'))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            mensaje = ''
            usuario_condominio = request.form["username"]
            password_condominio = request.form["password"]
            time.sleep(2)
            user = UsuariosSanAgustin.query.filter_by(
                username=request.form["username"]).first()
            if user and check_password_hash(user.password, request.form["password"]):
                session["username"] = user.username
                session["id"] = user.id
                usx = str(session["username"])
                user = UsuariosSanAgustin.query.filter_by(username=usx).first()
                id_condominio = user.id
                usuario_condominio = user.username
                password_condominio = user.password
                nombreusuario_condominio = user.nombreusuario
                pin_condominio = user.pin
                casa_condominio = user.casa
                permanentes_condominio = user.permanentes
                usuarioCompleto = [[id_condominio, usuario_condominio, password_condominio,
                                    nombreusuario_condominio, pin_condominio, casa_condominio, permanentes_condominio]]
                time.sleep(1)
                mensaje = '{}'.format(nombreusuario_condominio)

                return redirect(url_for('.home', mensaje=mensaje, usuarioCompleto=usuarioCompleto))
            else:
                mensaje = "Tu usuario es incorrecto, por seguridad te hemos sacado de nuestra plataforma"
        else:
            mensaje = ''
            session["username"] = None
            session["id"] = None
        return render_template("sanagustin/login.html", mensaje=mensaje)

    @app.route("/sanagustin", methods=["GET", "POST"])
    def home():
        mensaje = ''
        try:
            if "username" in session:
                mensaje = ''
                usx = str(session["username"])
                user = UsuariosSanAgustin.query.filter_by(username=usx).first()

                id_condominio = session["id"]

                usuario_condominio = user.username
                password_condominio = user.password
                nombreusuario_condominio = user.nombreusuario
                pin_condominio = user.pin
                casa_condominio = user.casa
                permanentes_condominio = user.permanentes
                usuarioCompleto = [[id_condominio, usuario_condominio, password_condominio,
                                    nombreusuario_condominio, pin_condominio, casa_condominio, permanentes_condominio]]
                time.sleep(1)
                minombre = '{}'.format(nombreusuario_condominio)

                mensaje = ' Bienvenid@ a Hacienda San Agustín, es un gusto tenerte por acá '
                return render_template('sanagustin/home.html', mensaje=mensaje, minombre=minombre, usuarioCompleto=usuarioCompleto)
            else:
                session.pop('id', None)
                session.pop('username', None)
                mensaje = ''
                msk = ''
        except:
            session.pop('id', None)
            session.pop('username', None)
            mensaje = 'error de inicio'
        return redirect(url_for('.login', mensaje=mensaje))

    @app.route("/registrar", methods=["GET", "POST"])
    def registrar():
        mensaje = ''
        msk = ''
        if request.method == "POST":
            if request.form['acceso'] == '':
                hashed_pw = generate_password_hash(
                    request.form["password"], method="sha256")
                username = request.form["username"]
                password = hashed_pw
                nombreusuario = request.form["nombreusuario"]
                pin = request.form["pin"]
                casa = request.form["casa"]
                permanentes = request.form["permanentes"]
                time.sleep(.6)
                try:
                    new_user = UsuariosSanAgustin(username=request.form["username"], password=hashed_pw, nombreusuario=request.form[
                                                  "nombreusuario"],   pin=request.form["pin"], casa=request.form["casa"], permanentes=request.form["permanentes"])
                    db.session.add(new_user)
                    db.session.commit()
                    mensaje = 'Te has registrado con exito'
                except Exception as e:
                    mensaje = 'ERROR DE REGISTRO {} '.format(e)

                    session.pop('id', None)
                    session.pop('username', None)
            else:
                session["username"] = None
                session["id"] = None
                mensaje = 'El codigo de acceso no es correcto'
                return redirect(url_for(".login", mensaje=mensaje))
        else:
            mensaje = 'error de usuario'
            session["username"] = None
            session["id"] = None
        return redirect(url_for(".login", mensaje=mensaje))

    @app.route("/registrar_visita_diaria_san_agustin", methods=["GET", "POST"])
    def registrar_visita_diaria_san_agustin():
        mensaje = ''
        msk = ''
        try:
            if request.method == "POST":
                idactual = str(session["id"])
                nombreusuario = request.form["nombrevisita"]
                empresa = request.form["empresa"]
                hora = request.form["horahora"]

                fecha = datetime.datetime.now()
                time.sleep(.6)
                new_user = VisitasDiariasDB(
                    idcondomino=idactual, nombrevisita=request.form["nombrevisita"],   empresa=request.form["empresa"], hora=request.form["horahora"], fecha=fecha)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('ver_mis_visitas'))

        except:
            session["username"] = None
            session["id"] = None
            return redirect(url_for('sanagustin/login'))

        return redirect(url_for('ver_mis_visitas'))

    @app.route("/ver_mis_visitas", methods=["GET", "POST"])
    def ver_mis_visitas():
        mensaje = ''
        msk = ''
        try:
            if "username" in session:
                idactual = str(session["id"])
                allxxx = VisitasDiariasDB.query.filter_by(idcondomino=idactual)
                allxxx = list(map(lambda x: x.serialize(), allxxx))

                arrayUno = []
                arrayDos = []
                for i in allxxx:
                    for x in i:
                        arrayDos.append(i[x])
                    arrayUno.append(arrayDos)
                    arrayDos = []

                return render_template('sanagustin/misvisitas.html', mensaje=mensaje, datos=arrayUno)
            else:
                mensaje = 'No podimos entrar a mis visitas'
        except Exception as e:
            mensaje = str(e)

        return redirect('.home', mensaje=mensaje)

    @app.route("/actualizar_perfil_condomino", methods=["GET", "POST"])
    def actualizar_perfil_condomino():
        mensaje = ''
        msk = ''
        if request.method == "POST":
            idk = str(session["id"])
            nombrek = request.form["nombrek"]
            usernamek = request.form["usernamek"]
            passwordk = request.form["passwordk"]

            hashed_pw = generate_password_hash(
                request.form["passwordk"], method="sha256")
            passwordk = hashed_pw

            pink = request.form["pink"]
            casak = request.form["casak"]
            permanentesk = request.form["permanentesk"]

            actualizar_perfil_app = (sessionx.query(
                UsuariosSanAgustin).filter_by(id=idk).first())

            actualizar_perfil_app.username = usernamek
            actualizar_perfil_app.password = passwordk

            actualizar_perfil_app.nombreusuario = nombrek
            actualizar_perfil_app.pin = pink
            actualizar_perfil_app.casa = casak
            actualizar_perfil_app.permanentes = permanentesk
            sessionx.commit()
            mensaje = 'Se actualizó tu perfil'
            return redirect(url_for('.home', mensaje=mensaje))

        else:
            session["username"] = None
            session["id"] = None
            return redirect(url_for('.login'))

        return redirect(url_for('.login'))

    @app.route("/registrar_rancho_casa", methods=["GET", "POST"])
    def registrar_rancho_casa():
        arrayUno = []
        arrayDos = []
        mensaje = ''
        try:
            if request.method == "POST":
                idactual = str(session["id"])
                etapa = request.form["etapa"]
                hora = request.form["horahora"]
                fecha = datetime.datetime.now()
                time.sleep(.6)
                new_user = Ranchos(
                    idcondomino=idactual, etapa=request.form["etapa"],   hora=request.form["horahora"], fecha=fecha)
                db.session.add(new_user)
                db.session.commit()
                mensaje = 'PISCINA APARTADA'
        except Exception as e:
            mensaje = str(e)

        try:
            if "username" in session:
                allxxx = Ranchos.query.all()
                allxxx = list(map(lambda x: x.serialize(), allxxx))
                arrayUno = []
                arrayDos = []
                for i in allxxx:
                    for x in i:
                        arrayDos.append(i[x])
                    arrayUno.append(arrayDos)
                    arrayDos = []

                fecha = date.today()
                mensaje = 'Dia actual: {}'.format(fecha)
                return render_template('sanagustin/ranchos.html', mensaje=mensaje, arrayUno=arrayUno)
            else:
                mensaje = 'No podimos entrar a mis visitas'
        except Exception as e:
            mensaje = str(e)
        return render_template('sanagustin/ranchos.html', mensaje=mensaje, arrayUno=arrayUno)

    return app
if __name__=='__main__':
    app = create_app()
    app.run(debug=True,host = '0.0.0.0', port =8989)