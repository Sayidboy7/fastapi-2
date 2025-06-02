from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Relationship
from datetime import datetime

db_name = 'database.db'
engine = create_engine(f'sqlite:///{db_name}')

class Item(SQLModel, table=True):
	id: Optional[int] = Field(primary_key=True)
	name: str = None
	color: Optional[str] = None
	price: int
	created_at: Optional[str] = datetime.now()
	category_id: Optional[int] = Field(default=None, foreign_key='category.id')
	category: Optional['Category'] = Relationship(back_populates='items')

	def get_name():
		return 'Item'

class Category(SQLModel, table=True):
	id: Optional[int] = Field(primary_key=True)
	title: str
	items: List[Item] = Relationship(back_populates='category')

	def get_name():
		return 'Category'

def create_tables():
	SQLModel.metadata.create_all(engine)

if __name__ == '__main__':
	create_tables()
