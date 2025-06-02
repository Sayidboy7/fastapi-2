from flask import Flask, render_template, request, redirect, url_for, abort
import requests
import json

app = Flask(__name__)
API_URL = 'http://127.0.0.1:8000/'


@app.route('/')
def home():
	items = requests.get(API_URL + f'/api/items')
	
	return render_template('index.html', items=items.json())


@app.route('/item/info/<int:id>')
def item_info(id):
	item = requests.get(API_URL + f'api/item/{id}')
	print(item)

	return render_template('item_detail.html', item=item.json())


@app.route('/item/create', methods=['POST','GET'])
def create_item():
	if request.method == 'POST':
		name = request.form.get('name')
		color = request.form.get('color')
		price = request.form.get('price')

		json = {
			'name' : name,
			'color' : color,
			'price' : price
		}

		response = requests.post(API_URL + f'api/items', json=json)
		if not response:
			print(response)
			return abort(400)

		return redirect(url_for('home'))

	return render_template('edit_item.html')


@app.route('/item/update/<int:id>', methods=['POST', 'GET'])
def update_item(id):
	item = requests.get(API_URL + f'api/item/{id}')
	print(item.json())

	if request.method == 'POST':
		name = request.form.get('name')
		color = request.form.get('color')
		price = request.form.get('price')

		json = {
			'name' : name,
			'color' : color,
			'price' : price
		}

		response = requests.put(API_URL + f'api/item/{id}', json=json)
		print(response)

		return redirect(url_for('home'))

	return render_template('edit_item.html', item=item.json())

@app.route('/item/delete/<int:id>')
def delete_item(id):
	response = requests.delete(API_URL + f'api/item/{id}')
	print(response)

	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True)