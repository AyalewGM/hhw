import datetime
import pandas as pd
from flask import Flask, render_template, request,logging
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import logging
import ssl

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'registration'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hamrishealthandwellness@gmail.com'
app.config['MAIL_PASSWORD'] = 'Emuadd@2509'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mysql = MySQL(app)
mail = Mail(app)

logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('/var/www/hhw/nutras/test.log')
logger.addHandler(handler)

@app.route('/')
def entry():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about') #-----changed from /about-us
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/classes')
def classes():
    return render_template('classes.html')

#@app.route('/begenaclasses')
#def begenaclasses():
 #   return render_template('classbegena.html')
#--------HHW----begin--------
@app.route('/holistic')
def holistic():
    return render_template('holistic.html')

@app.route('/rbti')
def rbti():
    return render_template('rbti.html')

@app.route('/herbs')
def herbs():
    return render_template('herbs.html')

@app.route('/dfasting')
def dfasting():
    return render_template('dfasting.html')

@app.route('/restore')
def restore():
    return render_template('restore.html')

@app.route('/body_vagus')
def body_vagus():
    return render_template('body_vagus.html')

@app.route('/school')
def school():
    return render_template('school.html')

@app.route('/blog')
def blog():
    return render_template('blog-details-right-sidebar.html')

#--------HHW-----end-------
@app.route('/masinkoclass')
def masinkoclasses():
    return render_template('classmasinko.html')

#------AM Started 
@app.route('/kirarclass')
def classkirar():
    return render_template('classkirar.html')

@app.route('/abinetclass')
def classabinet():
    return render_template('classabinet.html')
#######End##########

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/shop_category')#Sample 
def shop_category():
    return render_template('shop_category.html')

#------AM Started 
@app.route('/shop_cart')
def shop_cart():
    return render_template('shop_cart.html')

@app.route('/shop_checkout')
def shop_checkout():
    return render_template('shop_checkout.html')

@app.route('/shop_account')
def shop_account():
    return render_template('shop_account.html')

@app.route('/portfolio_gallery')
def portfolio_gallery():
    return render_template('portfolio_gallery.html')

@app.route('/about-me')
def about_me():
    return render_template('about_me.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/coming')
def coming():
    return render_template('coming_soon.html')

@app.route('/error')
def error():
    return render_template('404-error.html')

@app.route('/classes_desc')
def classes_desc():
    return render_template('classes_desc.html')

@app.route('/classes_schedule')
def classes_schedule():
    return render_template('classes_schedule.html')

@app.route('/challenges')
def challenges():
    return render_template('challenges.html')

@app.route('/classes_single')
def classes_single():
    return render_template('classes_single.html')

@app.route('/challenge_single')
def challenge_single():
    return render_template('challenge_single.html')

@app.route('/events_list')
def events_list():
    return render_template('events_list.html')

@app.route('/events_month')
def events_month():
    return render_template('events_month.html')

@app.route('/events_masonry')
def events_masonry():
    return render_template('events_masonry.html')

@app.route('/events_single')
def events_single():
    return render_template('events_single.html')

#----------End-----------

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'GET':
        logging.info(f"Request: {str(request.data)}")
        return render_template("contact.html")
    app.logger.info(request.json)

    if request.method == 'POST':
        logger.info("==================================")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address'] 
        message = request.form["message"]
        df = pd.DataFrame([["Name", name], ['email', email],['address', address], ['subject', phone], ['Message', message]],
                          columns=["Title", "information"])
        message_sender(df)
        return render_template('index.html')

@app.route('/registration', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        logging.info(str(request.data))
        return render_template("online_regesteration.html")

    if request.method == 'POST':
        logger.info(f"==================={str(request.form['bDay'])}")

        last_name = request.form['lastName']
        first_name = request.form['firstName']
        baptism_name = request.form['firstName']
        gender = request.form["gender"]
        phone = request.form["phone"]
        email = request.form["email"]
        country = request.form["country"]
        bday  = request.form["bDay"]
        password = request.form["password"]
        df = pd.DataFrame([["Last Name", last_name], ['First Name',first_name], ['email', email]], columns = ["person", "information"])

        message_sender(df,  registration=True)
        #bday = datetime.datetime.strptime(bday, "%Y-%m-%d").date()
        logger.info(f"Birth day :{bday}")
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO student VALUES(%s, %s,%s,%s,%s, %s,%s, %s,%s,%s)', (0,last_name, first_name, baptism_name, gender, phone, email, bday,country,password))
        mysql.connection.commit()
        cursor.close()

        return render_template('home_5.html')

def message_sender(df, registration=False):#, 'addis_mul@gmail.com'
    if registration:
        last_name = df['information'][0]
        first_name = df['information'][1]
        msg_raw = 'Hi Admin, user {} {} has been registered">'.format(first_name, last_name)
    else:
        name = df['information'][0]
        msg_raw = 'Hi Admin, user {} has sent you message.'.format(name)

    df = styler(df)
    msg = Message(msg_raw, sender = 'hamrishealthandwellness@gmail.com', recipients = ['hamrishealthandwellness@gmail.com'], bcc = ['addis.megun@gmail.com'])
    msg.html = df
    mail.send(msg)
    return "Message sent!"

def styler(df):

    styles =[
        {
            "selector":"th",
            "props":[
        ("background","#BEBEBE"),
        ("color","#458b74"),
        ("font-family","verdana"),
        ("text-align", "left"),

        ],
        }
    ]
    dfhtml = (df.style.set_table_styles(styles).render())
    content = """
    <html>
    <head>
    <body>
    <h3>  The following message received </h3>
    {0}
    </br>
    </body>
    </head>
    </html>
    """.format(dfhtml)
    return content


if __name__ == '__main__':
    app.run(host='0.0.0.0',  port=5000, debug=True)
