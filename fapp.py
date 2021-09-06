
from os import getenv, environ
#from livereload import Server
from flask import Flask, render_template, session, request, redirect, url_for, g
import string
#from users import get_user, add_user, verify_user
import mysql.connector

app = Flask(__name__)

app.secret_key = 'Bruce Wayne is Batman'

cnx = mysql.connector.connect(user='fctools', password='rootdata',
                              host='fctools.mysql.pythonanywhere-services.com',
                               database='fctools$fcdata')

cursor = cnx.cursor(buffered=True)
#cnx.close()


@app.route('/', methods=['GET','POST'])
def home_page():



    system_list = []

    query = ("SELECT system FROM system_data")
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        system_list.append(row[0])

    if request.method == 'POST':

        action = request.form.get('action')

        if request.form.get('action') == 'Save':
            system = request.form.get('system')
            region = request.form.get('region')
            aliance = request.form.get('aliance')
            dotlan = request.form.get('dotlan')
            zkill = request.form.get('zkill')
            remarks = request.form.get('remarks')
            
            if system in system_list:
                message = "System already listed. Please check system list on the right."
                return render_template('system.html', message=message)



            add_system = ("INSERT INTO system_data "
              "(system, region, aliance, dotlan, zkill, remarks) "
              "VALUES (%(system)s, %(region)s, %(aliance)s, %(dotlan)s, %(zkill)s, %(remarks)s)")

            data = {
            'system': system,
            'region': region,
            'aliance': aliance,
            'dotlan': dotlan,
            'zkill': zkill,
            'remarks' : remarks
            }
            cursor.execute(add_system, data)
            cnx.commit()
     
        
        elif action[:6] == "system":

            system_name = action[8:]
            query = ("SELECT system, region, aliance, dotlan, zkill, remarks FROM system_data")
            cursor.execute(query)
            result = cursor.fetchall()
            s_data=["","","","","",""]
            for row in result:
                if row[0] == system_name:
                    for i in range(6):
                        s_data[i] = row[i]

                    
            return render_template('system.html', system_list=system_list, s_data=s_data)

        elif request.form.get('action') == 'Update':
            system = request.form.get('system')
            region = request.form.get('region')
            aliance = request.form.get('aliance')
            dotlan = request.form.get('dotlan')
            zkill = request.form.get('zkill')
            remarks = request.form.get('remarks')
            
            if system not in system_list:
                message = "You cannot change the system name"
                return render_template('message.html', message=message)



            update_system = ("""UPDATE system_data SET      region=%s, 
                                                            aliance=%s, 
                                                            dotlan=%s, 
                                                            zkill=%s, 
                                                            remarks=%s
                WHERE system=%s
                """)

            data = (region, aliance, dotlan, zkill, remarks, system)
            cursor.execute(update_system, data)
            cnx.commit()
            message = "Information updated"
            return render_template('message.html', message=message)


        else:
            print("*** No such action ***", request.form.get('action'))

        
    
    return render_template('home.html', system_list=system_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = verify_user(password=password, email=email)
        if user:
            session['userid'] = user[0]
            return render_template('home.html', user=user)
        else:
            msg = 'Invalid email or password'
            return render_template('login.html', msg=msg)

        return
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('home_page'))

# Do not alter this if statement below
# This should stay towards the bottom of this file
if __name__ == "__main__":
    flask_env = getenv('FLASK_ENV')
    if flask_env != 'production':
        environ['FLASK_ENV'] = 'development'
        app.debug = True
        app.asset_debug = True
        server = Server(app.wsgi_app)
        server.serve()
    app.run()