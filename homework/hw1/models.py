from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
# from traitlets.utils import descriptions

from database import Base

class Descriptions(Base):
    __tablename__ = 'descriptions'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    dish_name = Column(String, index=True)
    cooking_time = Column(Integer, nullable=False)
    ingredients = Column(String, index=True)
    text_description = Column(String, index=True)


class Recipes(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, ForeignKey("descriptions.id"), primary_key=True)
    dish_name = Column(String, nullable=False)
    number_of_views = Column(Integer, default=0)
    cooking_time = Column(Integer, nullable=False)
    descriptions = relationship("Descriptions", cascade="all, delete-orphan", single_parent=True)
