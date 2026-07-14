from eralchemy2 import render_er
from database import Base
import models

render_er(Base.metadata, "erd.png")

