
from pydantic import BaseModel


class BaseRecipes(BaseModel):
    __tablename__ = 'recipes'
    dish_name: str
    number_of_views: int
    cooking_time: int

class RecipesIn(BaseModel):
    ...

class RecipesOut(BaseRecipes):
    id: int

    class Config:
        orm_mode = True


class BaseDescriptions(BaseModel):
    __tablename__ = 'descriptions'
    dish_name: str
    cooking_time: int
    ingredients: str
    text_description: str

class DescriptionsIn(BaseDescriptions):
    dish_name: str
    cooking_time: int
    ingredients: str
    text_description: str

class DescriptionsOut(BaseDescriptions):
    id: int

    class Config:
        orm_mode = True


