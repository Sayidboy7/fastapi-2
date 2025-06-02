from fastapi import FastAPI, Query, HTTPException
import uvicorn
from pydantic import BaseModel
from models import Item, engine
from typing import List, Union, Optional

from sqlmodel import Session, select

api = FastAPI()

class Items(BaseModel):
	name: str
	color: Optional[str]
	price: int



@api.get('/api/items', response_model=List[Item])
def get_items():
	session = Session(engine)

	# Select * from Item
	item = select(Item)
	items = session.exec(item).all()
	print(items)
	return items


@api.get('/api/item/{id}', response_model=Item)
def get_item(id: int) -> Item:
	session = Session(engine)

	item = select(Item).filter(Item.id==id)
	# item = session.get(Item, id)
	item = session.exec(item).first()

	if not item:
		raise HTTPException(status_code=404, detail='Item not Found!')

	return item

@api.post('/api/items')
def create_item(item: Items) -> Item:
	session = Session(engine)

	item = Item(
		name = item.name,
		color = item.color,
		price = item.price
	)

	session.add(item)
	session.commit()
	session.refresh(item)

	raise HTTPException(status_code=201, detail='created!')

@api.put('/api/item/{id}', response_model=Item)
def update_item(id: int, update_item: Items) -> Item:
	session = Session(engine)

	item = session.get(Item, id)
	if not item:
		raise HTTPException(status_code=404, detail='Item not Found!')
			
	if update_item.name:
		item.name = update_item.name
	if update_item.color:
		item.color = update_item.color
	if update_item.price:
		item.price = update_item.price

	session.commit()
	session.refresh(item)

	return item

@api.delete('/api/item/{id}', response_model=Item)
def delete_item(id: int) -> Item:
	session = Session(engine)
	
	item = session.get(Item, id)
	if not item:
		raise HTTPException(status_code=404, detail='Item not Found!')

	session.delete(item)
	session.commit()

	return item


if __name__ == '__main__':
	uvicorn.run(api)
