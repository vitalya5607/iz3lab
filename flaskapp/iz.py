from flask import Flask
app = Flask(__name__)
#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
 return " <html><head></head> <body> Hello World! </body></html>"

from flask import render_template
#наша новая функция сайта

# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
# модули валидации полей формы
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
# используем csrf токен, можете генерировать его сами
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта google
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lezdz8bAAAAAAxzFfaJYmk-g7X1_nuN_U-_TS3i'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lezdz8bAAAAALNfgbR5rW_dd0lhrS7FokJziFhY'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
# создаем форму для загрузки файла
class NetForm(FlaskForm):
 # поле для введения строки, валидируется наличием данных
 # валидатор проверяет введение данных после нажатия кнопки submit
 # и указывает пользователю ввести данные если они не введены
 # или неверны
 cho = StringField('Повернуть на', validators = [DataRequired()])
 gor = StringField('горизонталь', validators = [DataRequired()])
 ver = StringField('вертикаль', validators = [DataRequired()])
 # поле загрузки файла
 # здесь валидатор укажет ввести правильные файлы
 upload = FileField('Load image', validators=[
 FileRequired(),
 FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
 # поле формы с capture
 recaptcha = RecaptchaField()
 #кнопка submit, для пользователя отображена как send
 submit = SubmitField('send')

# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

## функция для оброботки изображения
def draw(filename,cho,gor,ver):
 ##открываем изображение
 print(filename)
 img= Image.open(filename)

##делаем график
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(img, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(b, ax=ax)
 gr_path = "./static/newgr.png"
 sns.displot(data)
 plt.savefig(gr_path)
 plt.close()

##переворот
 img=img.rotate(cho,expand=True)
 output_filename = filename
 img.save(output_filename)

##изменение размера по осям
 size=(gor,ver)
 img = img.resize(size)
 img.save(output_filename)

 return output_filename,gr_path,gr_path

# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
 # создаем объект формы
 form = NetForm()
 # обнуляем переменные передаваемые в форму
 filename=None
 newfilename=None
 grname=None
 grname2=None
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  # файлы с изображениями читаются из каталога static
  filename = os.path.join('./static', secure_filename(form.upload.data.filename))
  ch=form.cho.data
  ch=int(ch)
  osii=form.gor.data
  osii=int(osii)
  ra=form.ver.data
  ra=int(ra)
  form.upload.data.save(filename)
  newfilename,grname,grname2 = draw(filename,ch,osii,ra)

 return render_template('net.html',form=form,image_name=newfilename,gr_name=grname,gr_name2=grname2)

 if __name__ == "__main__":
  app.run(host='127.0.0.1',port=5000)
