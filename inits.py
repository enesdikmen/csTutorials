from flask import Flask
import view
from flask_login import LoginManager
from user_forms import User
from db import db


app = Flask(__name__)
app.config.from_object("settings")

#Url rules
app.add_url_rule("/", view_func=view.main)
app.add_url_rule("/home", view_func=view.main)
app.add_url_rule("/sign_up", view_func=view.sign_up, methods=['GET', 'POST'])
app.add_url_rule("/login", view_func=view.login, methods=['GET', 'POST'])
app.add_url_rule("/logout", view_func=view.logout)

app.add_url_rule("/admin_tutorial", view_func=view.admin_tutorial, methods=['GET'])


app.add_url_rule("/add_tutorial", view_func=view.add_tutorial, methods=['GET', 'POST'])
app.add_url_rule("/tutorial", view_func=view.tutorial)
app.add_url_rule("/tutorials", view_func=view.tutorials, methods=['GET', 'POST'])
app.add_url_rule("/edit_tutorial", view_func=view.edit_tutorial, methods=['GET', 'POST'])
app.add_url_rule("/delete_tutorial", view_func=view.delete_tutorial, methods=['GET'])


app.add_url_rule("/add_topic", view_func=view.add_topic, methods=['GET', 'POST'])
app.add_url_rule("/edit_topic", view_func=view.edit_topic, methods=['POST'])
app.add_url_rule("/delete_topic", view_func=view.delete_topic, methods=['POST'])

app.add_url_rule("/educator", view_func=view.educator, methods=['GET', 'POST'])
app.add_url_rule("/add_educator", view_func=view.add_educator, methods=['GET', 'POST'])
app.add_url_rule("/delete_educator", view_func=view.delete_educator)
app.add_url_rule("/edit_educator", view_func=view.edit_educator, methods=['POST'])

app.add_url_rule("/enroll", view_func=view.enroll)
app.add_url_rule("/remove_enrollment", view_func=view.remove_enrollment)

app.add_url_rule("/add_comment", view_func=view.add_comment, methods=['POST'])
app.add_url_rule("/edit_comment", view_func=view.edit_comment, methods=['POST'])
app.add_url_rule("/delete_comment", view_func=view.delete_comment)





app.add_url_rule("/account", view_func=view.account)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'is-warning'

@login_manager.user_loader
def load_user(user_id):
    user_row = db.get_user(user_id)
    return User(user_id, user_row[0], user_row[1]) if user_row else None