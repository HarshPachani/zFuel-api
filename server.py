from flask import Flask, jsonify
from scrapy import Selector
import json
import requests

app = Flask(__name__)

@app.route('/api/gujarat',methods=['GET'])
def gujarat_petrol_price():
    # url to scrap
    scrap_url = 'https://www.goodreturns.in/petrol-price-in-gujarat-s12.html'

    # petrol prices
    even_price = []
    odd_price = []

    # petrol cities
    even_cities = []
    odd_cities = []

    # Use requests to get the HTML content of the page
    response = requests.get(scrap_url)

    # Use scrapy to parse the HTML content
    selector = Selector(text=response.text)

    # Extract the petrol price from the parsed HTML
    try:

        # petrol prices of even rows
        petrol_price_even = selector.css(
            '.gold_silver_table table .even_row td').getall()

        # petrol prices of odd rows
        petrol_price_odd = selector.css(
            '.gold_silver_table table .odd_row td').getall()

        # access for the today's petrol price even only
        for j in range(1, len(petrol_price_even), 3):
            selector = Selector(text=petrol_price_even[j])
            price = selector.css('td::text').get()
            even_price.append(float(price[2:]))

        # access for the today's petrol price odd only
        for j in range(1, len(petrol_price_odd), 3):
            selector = Selector(text=petrol_price_odd[j])
            price = selector.css('td::text').get()
            odd_price.append(float(price[2:]))

        # even and odd rows merged
        petrol_price = even_price + odd_price

        for i in petrol_price_even:
            selector = Selector(text=i)
            city = selector.css('td a::attr(title)').get()
            if city is None:
                pass
            else:
                even_cities.append(city)

        for i in petrol_price_odd:
            selector = Selector(text=i)
            city = selector.css('td a::attr(title)').get()
            if city is None:
                pass
            else:
                odd_cities.append(city)

        
        petrol_city = even_cities + odd_cities

    except Exception as e:
        return ('Failed')

    city_price = {}
    for key, value in zip(petrol_city, petrol_price):
        city_price[key] = value
    return jsonify(city_price)


if __name__ == '__main__':
    app.run(debug=True, port=5000,host='0.0.0.0')