from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
import os
import streamlit as st
import requests
import pandas as pd
import numpy as np
import googlemaps
import os


from dotenv import load_dotenv
load_dotenv()



os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Retrieve the WEATHER_API_KEY environment variable
weather_api_key = os.getenv("WEATHER_API_KEY")

st.title(" AI Product Travel Agent ")
#model_list = ["gemma2-9b-it", "llama-3.1-8b-instant" ,"llama-3.3-70b-versatile"]


# First input
from_city = st.text_input("Please Enter Destination Travel City:")
# Second input
number_of_days = st.text_input("Please enter number of Days :")

# Display the collected inputs
if from_city and number_of_days:
    st.write(f"You entered for the first input: {from_city}")
    st.write(f"You entered for the second input: {number_of_days}")
else:
    st.write("Please enter both inputs.")




## Processing of Weather



# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key

#API_KEY = weather_api_key

#st.write(f"API Key :  {weather_api_key}")

BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

##Function to get the weather data..

def get_weather_data(city):
    """Fetches weather data for a given city from OpenWeatherMap."""
    # st.write(f"Inside get_weather function :  {city}")
    params = {
        'q': city,
        'appid': weather_api_key,
        'units': 'metric'  # or 'imperial' for Fahrenheit
    }

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={weather_api_key}&units=metric"

    # st.write(f"Complete URL :  {complete_url}")    

    # st.write(f"Inside get_weather function :  {city}")
    response = requests.get(BASE_URL, params=params)
  

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={weather_api_key}&units=metric"

    # st.write(f"Complete URL  :  {complete_url}")
    # st.write(f"Response inside get_weather function :  {response}")
    # st.write(f"Response STATUS CODE :  {response.status_code}")

    
    if response.status_code == 200:
        st.success("Status Code Passed!")
        return response.json()        
    else:
        st.success("Status Code Failed!")
        return None

## 5 days forecast data ..




# st.title("Weather Dashboard ")

#city_name = st.text_input("Enter City Name:")

# Pass the City Name

# city_name = from_city
# if st.button("Get Weather"):
#     if city_name:
#         city_name = from_city
#         st.write(f"Inside get_weather function :  {city_name}")
#         weather_data = get_weather_data(city_name)
#         if weather_data:
#             st.success("Showing Weather Data...!")
#             main_data = weather_data['main']
#             weather_desc = weather_data['weather'][0]['description']
#             wind_speed = weather_data['wind']['speed']
            
#             st.subheader(f"Weather in {city_name.capitalize()}")
#             st.write(f"**Temperature:** {main_data['temp']}°C")
#             st.write(f"**Feels Like:** {main_data['feels_like']}°C")
#             st.write(f"**Humidity:** {main_data['humidity']}%")
#             st.write(f"**Conditions:** {weather_desc.capitalize()}")
#             st.write(f"**Wind Speed:** {wind_speed} m/s")

#             st.write("===============.")                       
#         else:
#             st.error("Could not retrieve weather data. Please check the city name or API key.")
#     else:
#         st.warning("Please enter a city name.")

#===========================================================================


#=================================================================

#Get Tourist Attractions.

# Retrieve the any API Key environment variable

# google_cloud_apikey = os.getenv("google_cloud_api_key")
# api_key = google_cloud_apikey
# print(f"API Key : {api_key}")
# st.write(f"API Key  :  {api_key}")

# Retrieve the any API Key environment variable
google_cloud_apikey = os.getenv("google_cloud_api_key")
api_key = google_cloud_apikey

def get_places(location, radius, keyword):
    """
    Uses the Google Maps Places API to find places near a given location.

    Args:
        location (str): The location to search near, e.g., "Pune, Maharashtra".
        radius (int): The radius in meters to search within.
        keyword (str): Keywords to filter the search results.

    Returns:
        pandas.DataFrame: A DataFrame containing the search results, or None if an error occurred.
    """
    try:
        gmaps = googlemaps.Client(key=google_cloud_apikey)
        places_result = gmaps.places(query=keyword, location=location, radius=radius)

        if places_result and places_result['results']:
            places_data = []
            for place in places_result['results']:
                name = place.get('name')
                address = place.get('formatted_address')             
               
                places_data.append({
                    'Name': name,
                    'Address': address,
                    
                })
            return pd.DataFrame(places_data)
        else:
            st.error("No places found for the given criteria.")
            return None
    except googlemaps.exceptions.ApiError as e:
        st.error(f"Google Maps API error: {e}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


#=================================================================

## Main program to process everything..

# Retrieve the any API Key environment variable
google_cloud_apikey = os.getenv("google_cloud_api_key")
api_key = google_cloud_apikey


# You can add a button to process the inputs
if st.button("Show Iternary  "):
    if from_city and number_of_days:
        #st.success("Inputs processed successfully!")
        # st.write("Processed successfully.")
        # Add your processing logic here, e.g.,
        # result = input_one + " " + input_two
        # st.write(f"Concatenated result: {result}")
        city_name = from_city        
        if city_name:
            city_name = from_city
            # st.write(f"Inside get_weather function :  {city_name}")
            ## Call the Weather data for the city. 
            weather_data = get_weather_data(city_name)
            if weather_data:
                # st.success("Showing Weather Data...!")
                main_data = weather_data['main']
                weather_desc = weather_data['weather'][0]['description']
                wind_speed = weather_data['wind']['speed']
                
                st.subheader(f"Weather in {city_name.capitalize()}")
                st.write(f"**Temperature:** {main_data['temp']}°C")
                st.write(f"**Feels Like:** {main_data['feels_like']}°C")
                st.write(f"**Humidity:** {main_data['humidity']}%")
                st.write(f"**Conditions:** {weather_desc.capitalize()}")
                st.write(f"**Wind Speed:** {wind_speed} m/s")

                st.write("===============.")                       
            else:
                st.error("Could not retrieve weather data. Please check the city name or API key.")

        
                            
        # Show Toursit Attractions

            city_name = from_city

            radius = 5000
            keyword = "tourist attractions"
            location = city_name
            #st.write("Calling Tourist Attractions.")
            df_places = get_places(location, radius, keyword)

            if df_places is not None:
                # st.subheader("Toursit Attractions (Places to VISIT) :")
                st.subheader(f"Toursit Attractions (Places to VISIT) in :  {city_name.capitalize()}")
                st.dataframe(df_places)   
                #st.write("Completed Showing Tourist Attractions.")
            else:
                st.error("Could not retrieve the Places data ......")


    else:
        st.warning("Both inputs must be provided to process.")
        st.write("Input required.")
        




    
