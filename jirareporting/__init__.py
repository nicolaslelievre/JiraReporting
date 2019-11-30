from config import Config
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('jirareporting', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
