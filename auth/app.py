import fastapi
from starlette.templating import Jinja2Templates
import os


templates = Jinja2Templates("templates")

app = fastapi.FastAPI()
