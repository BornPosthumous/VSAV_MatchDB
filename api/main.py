from urllib.parse import quote
import os

app = Flask(__name__, template_folder="templates", static_folder="templates", static_url_path="")

credentials = {
    'username'  : os.environ['DB_USERNAME'],
    'password'  : os.environ['DB_PASSWORD'],
    'host'      : os.environ['DB_HOST'],
    'database'  : os.environ['DB_DATABASE'],
    'port'      : os.environ['DB_PORT'],
}
con_string = f"postgresql://{credentials['username']}:%s@{credentials['host']}:5432/{credentials['database']}" % quote('dem0nscr@d00')

