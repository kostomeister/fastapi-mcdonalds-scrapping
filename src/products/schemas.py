from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    calories: str
    fats: str
    carbs: str
    proteins: str
    unsaturated_fats: str
    sugar: str
    salt: str
    portion: str
