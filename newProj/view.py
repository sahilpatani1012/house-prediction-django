from django.http import HttpResponse
from .Main import create_map  # Assuming Main.py is in the same Django app
from .geocoding import geocode_postcode
from .API_requests import fetch_house_prices, fetch_crime_rate, fetch_population
from .data_preprocessing import preprocess_house_prices_data, preprocess_population_data, preprocess_crime_data


def map_api_endpoint(request):
    api_key = "RBTHF0AXJL"  # Your actual API key
    postcode = request.GET.get('postcode')
    rooms = request.GET.get('rooms')
    print(postcode)
    print(rooms)
    if not postcode:
        return HttpResponse("Postcode is required", status=400)

    # Assume bedroom count is still 3 as hardcoded in the main function
    house_prices_data = fetch_house_prices(api_key, postcode, rooms)
    crime_data = fetch_crime_rate(api_key, postcode)
    population_data = fetch_population(api_key, postcode)

    # Preprocess data
    house_prices = preprocess_house_prices_data(house_prices_data)
    crime = preprocess_crime_data(crime_data)
    population = preprocess_population_data(population_data)

    # Create map
    map_ = create_map(house_prices, population, crime, api_key, postcode)
    map_html = map_._repr_html_()

    return HttpResponse(map_html)