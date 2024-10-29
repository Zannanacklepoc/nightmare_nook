from flask_app import app
from flask_app.controller import login_reg_controller
from flask_app.models import user
if __name__=="__main__":
    app.run(debug=True) 