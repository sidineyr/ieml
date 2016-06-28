import connexion
import handlers
from flask_cors import CORS


app = connexion.App(__name__, specification_dir='api-doc/')
app.add_api('rest_api.yaml')
app.after_request = lambda *args: None # a dirty hack so flask_cors doesn't screw up
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.app.secret_key = 'ZLX9PUQULLAKKLWDI1B9CDZ34H1LIGCW7CA3OVJYWLWF23UW80ONS0REZQAKJKKSFVPIF037VGIXIVE6AYN5AJJRONF2TFKMLLZM'
app.app.config['SESSION_TYPE'] = 'filesystem'

if __name__ == '__main__':
    app.run(debug=True) # served on the local network