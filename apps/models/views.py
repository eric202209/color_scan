from flask import Blueprint

user_blueprint = Blueprint('user', __name__, url_prefix="/user")

# 使用藍圖進行映射
@user_blueprint.route("/", endpoint="index")
def index():
    return "index"

class Blueprint:
    def __init__(self, name, import_name, static_folder=None,
        static_url_path=None, template_folder=None, url_prefix=None):

        user_blueprint = Blueprint(
            'user',
            __name__,
            url_prefix="/user",
            template_folder='templates',
            static_folder='static')


    def before_request(self, f):
        """Like :meth:`Flask.before_request` but for a blueprint.  This function
        is only executed before each request that is handled by a function of
        that blueprint.
        """
        self.record_once(
            lambda s: s.app.before_request_funcs.setdefault(self.name, []).append(f)
        )
        return f



