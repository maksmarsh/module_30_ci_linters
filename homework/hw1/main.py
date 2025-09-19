from typing import List
from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select
import models
import schemas
from database import engine, session
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(application: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        yield
        await session.close()
        await engine.dispose()


app = FastAPI()


@app.post('/descriptions_recipe/', response_model=schemas.DescriptionsOut)
async def descriptions(description: schemas.DescriptionsIn) -> models.Descriptions:
    new_description = models.Descriptions(**description.model_dump())
    async with session.begin():
        session.add(new_description)
    new_recipe = models.Recipes(
        id=new_description.id,
        dish_name=new_description.dish_name,
        cooking_time=new_description.cooking_time,
    )
    async with session.begin():
        session.add(new_recipe)

    return new_description


@app.get('/recipes/', response_model=List[schemas.RecipesOut])
async def recipes() -> List[models.Recipes]:
    res = await session.execute(
        select(models.Recipes).order_by(
            models.Recipes.number_of_views.desc(), models.Recipes.cooking_time
        )
    )
    return list(res.scalars().all())


@app.get('/descriptions_recipe/{recipe_id}', response_model=schemas.DescriptionsOut)
async def recipes_id(recipe_id) -> models.Descriptions:
    # res = await session.execute(select(models.Descriptions).filter_by(id=recipe_id))
    recipe = (await session.execute(select(models.Descriptions).filter_by(id=recipe_id))).scalars().first()
    await session.close()
    if recipe:
        await session.commit()
        return recipe
    else:
        raise HTTPException(status_code=404, detail="Recipe not found")


"""
запуск: fastapi dev main.py
или:  uvicorn main:app --reload
"""
