import jwt
import datetime
from utils.utils import load_environment_variables

env_variables = load_environment_variables()
email = 'abc@xd.com'
token = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, env_variables['SECRET_KEY'])
out = jwt.decode(token, env_variables['SECRET_KEY'], algorithms=["HS256"])
print(out)