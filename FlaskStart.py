from flask import Flask, request, Response
import requests
import json


app = Flask(__name__)
api_key = "Eva5ydwsdS6Py141TMa5UwT0c74q9UuIhSDF31AQNi8"


@app.route('/v1/apiservice', methods = ['GET'])
def get_results():
    query_dict = request.args.to_dict(flat=False)
    print(query_dict)
    latitude = f"{query_dict['latitude'][0]}"
    longitude = f"{query_dict['longitude'][0]}"
    query = f"{query_dict['query'][0]}"
    limit = f"{query_dict['limit'][0]}"
    dis_url = f"https://discover.search.hereapi.com/v1/discover?at={latitude},{longitude}&limit={limit}&q={query}&apikey={api_key}"

    response_dis = requests.get(dis_url)
    data_disco = response_dis.json()

    # Check for successful response
    if response_dis.status_code == 200:
        # Query Api Result
        query = data_disco["items"][0]["position"]
        q_address = data_disco["items"][0]["address"]
        q_street = q_address["label"]
        q_city = q_address["city"]
        q_postalCode = q_address["postalCode"]
        q_lat = query["lat"]
        q_lng = query["lng"]

        response_list=[]
        for item in data_disco['items']:
            title = item['title']
            address = item['address']['label']
            latitude = item['position']['lat']
            longitude = item['position']['lng']

            opening_hours = item.get('openingHours', [])
            if opening_hours:
                opening_hours_text = opening_hours[0].get('text', [])
                if opening_hours_text:
                    opening_hours_text = ', '.join(opening_hours_text)
                else:
                    opening_hours_text = "Not available"
            else:
                opening_hours_text = "Not available"

            contacts = item.get('contacts', [])
            contact_numbers = []
            for contact in contacts:
                phones = contact.get('phone', [])
                for phone in phones:
                    contact_numbers.append(phone['value'])

            websites = []
            www_values = item.get('www', [])
            for www_value in www_values:
                websites.append(www_value['value'])

            response = {"Title": f"{title}", "Address": f"{address}", "Latitude": f"{latitude}", "Longitude": f"{longitude}", "Opening Hours": f"{opening_hours_text}", "Contact Numbers": f"{', '.join(contact_numbers)}", "Websites" : f"{', '.join(websites)}"}
            response_list.append(response)

            print(f"Title: {title}")
            print(f"Address: {address}")
            print(f"Latitude: {latitude}, Longitude: {longitude}")
            print(f"Opening Hours: {opening_hours_text}")
            print(f"Contact Numbers: {', '.join(contact_numbers)}")
            print(f"Websites: {', '.join(websites)}")
            print("-" * 50)
        response = json.dumps(response_list, indent=4)
        data = json.loads(response)
        json_data = json.dumps(data)
        return Response(json_data, status=200, mimetype='application/json')
    else:
        print(f"Error: {response_dis.status_code}")
        response = {"Error": f"{response_dis.status_code}"}
        response = json.dumps(response, indent=4)
        data = json.loads(response)
        json_data = json.dumps(data)
        return Response(json_data, status=400, mimetype='application/json')

if __name__ == '__main__':
    app.run()