from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from typing import TypedDict, List
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
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
import json
import pandas as pd



from dotenv import load_dotenv
load_dotenv()



os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# Retrieve the WEATHER_API_KEY environment variable
weather_api_key = os.getenv("WEATHER_API_KEY")

st.title(" AI Product Travel Agent ")

st.text_area("Travel Agent AI Assistant ", "✅This is a travel Assistant\n ✅The Assistant provides you Weather data\n✅This will provide you TOP 10 Tourist Attractions\n✅Provides you Flight Details "
             
             ,height=100, disabled=True)


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
    st.subheader("Showing Weather Data..")
    # st.write("--")  
    # """Fetches weather data for a given city from OpenWeatherMap."""
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
        st.success("Weather Data Fetched!")
        return response.json()        
    else:
        st.success("Weather Data Failed!")
        return None



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
        st.write(f"Places City : {location}")
        st.write(f"Places Keyword : {keyword}")
        st.write(f"Radius : {radius}")

        places_data = None
        places_result = None
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

def Get_Flights_Data(input_city):    
    try:
        from_city  = "Pune"
        to_city = input_city
        destination_city = to_city
        home_country = "India"

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful Travel assistant designed to output JSON. Identify and return the top 5 **cheapest departing flights** be it non-stop and or connecting flights and show price in INR , no markdown or explanation "),         

                ( "human", 
                
                "Please provide 5 sample flight options from {from_city} to {to_city} be it non-stop and or connecting flights and price in Indian Rupees , in strict JSON format."
                "Each flight should include: 'Airline', 'Flight Number', 'Departure Time', 'Arrival Time', 'Duration', and 'Price'."
                
                ),
                
            ]   

        )   
        # 3. Instantiate the JSONOutputParser
        #parser = JsonOutputParser()
        output_parser = JsonOutputParser()
        selected_model = "gemma2-9b-it"
        model_selected = "gemma2-9b-it"
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.5,max_tokens=500).bind(response_format={"type": "json_object"})
        chain = prompt | llm | output_parser
        response= chain.invoke({"from_city": from_city, "to_city": to_city})
        # Convert the output to a JSON string for display
        json_output = json.dumps(response, indent=2)
        json_string_records = json_output # indent for pretty printing
        flight_data = json.loads(json_string_records)
        df = pd.DataFrame(flight_data)
        response_df = pd.DataFrame(response)
        st.write("--")      
         ##Convert data to HTML
        html_table = response_df.to_html(index=False, border=1)
        st.write("--")
        st.subheader("📋Showing Flight Details...")
        st.markdown(html_table, unsafe_allow_html=True)
        st.write("--")
        st.success("Flights Details Fetched Successful!")     
    except Exception as e:
        st.error(f"An error occurred Executing Function Get_Flights_Data : {e}")
#=================================================================
#         
def Get_Toursit_Places(input_city):    
    try:

        city_name = input_city
        user_input = input_city

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful Travel assistant and provide Top 5 Touist Attractions in the city given as input designed to output in strict JSON format.. "),         

                ( "human", 
                
                "Please provide Top 10 Touist Attractions {user_input} "
                "Provide Data as : 'Name', 'Location', 'Open Time' "
                
                ),
            
            ]
        )

        # 3. Instantiate the JSONOutputParser
        #parser = JsonOutputParser()
        output_parser = JsonOutputParser()
        selected_model = "gemma2-9b-it"
        model_selected = "gemma2-9b-it"
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.5,max_tokens=1000).bind(response_format={"type": "json_object"})
        #chain = prompt | model | parser
        chain = prompt | llm | output_parser
        response = chain.invoke(user_input)
        # print(response)
        # st.write(response)

        # 8. Convert the output to a JSON string for display
        json_output = json.dumps(response, indent=2)
        # 3. Use json.dumps() to serialize the list of dictionaries to a JSON string
        json_string_records = json_output # indent for pretty printing       

        response_df = pd.DataFrame(response)
        st.write("--")
        #Convert to List of Dictionaries
        list_of_dicts = response_df.to_dict(orient="records")
         ##Convert data to HTML
        html_table = response_df.to_html(index=False, border=1)
        st.write("--")
        #st.write("🏨Showing Hotel Details\n...")
        st.subheader("🏨 Showing Top Toursit Attractions\n")
        st.markdown(html_table, unsafe_allow_html=True)
        st.write("--")




    except Exception as e:
        st.error(f"An error occurred Executing Function Get_Hotels_and_AvgCosts : {e}")
#=================================================================
def Get_Hotels_and_AvgCosts(input_city,number_of_days):    
    try:
        import json

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful Travel assistant and provide Top 5  best Hotels in the city given as input designed to output in strict JSON format.. "),         

                ( "human", 
                
                "Please provide Top 5 best Hotels in the city {user_input} "
                "Each Hotel should include: 'Name', 'Location', 'price_per_night in INR as number only'  "
                
                ),
                
            ]
        )

        # 3. Instantiate the JSONOutputParser
        #parser = JsonOutputParser()
        output_parser = JsonOutputParser()

        selected_model = "gemma2-9b-it"
        model_selected = "gemma2-9b-it"


        #Invoke the LLM Model and bind the Json object 
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.5,max_tokens=1000).bind(response_format={"type": "json_object"})

        #chain = prompt | model | parser
        chain = prompt | llm | output_parser

        user_input = input_city

        # Invoke the chain with the user input
        #response = chain.invoke({"Query": user_input, "format_instructions": output_parser.get_format_instructions()})
        response = chain.invoke(user_input)
        # print(response)
        # st.write(response)

        # 8. Convert the output to a JSON string for display
        json_output = json.dumps(response, indent=2)
        # 3. Use json.dumps() to serialize the list of dictionaries to a JSON string
        json_string_records = json_output # indent for pretty printing
 
        response_df = pd.DataFrame(response)
        st.write("--")
         ##Convert data to HTML
        html_table = response_df.to_html(index=False, border=1)
        st.write("--")
        #st.write("🏨Showing Hotel Details\n...")
        st.subheader(" 🏨 Hotel List (Top 5 Standard Hotels ) \n")
        st.markdown(html_table, unsafe_allow_html=True)
        st.write("--")

        ## Showing Average cost of the Hotels.

        st.write("--")
        st.header("Showing Average cost of the hotel")

        #num_days = 5
        num_days = number_of_days

        hotel_type = "Standard"  
        # Create prompt using ChatPromptTemplate
        template = ChatPromptTemplate.from_template(
            "Estimate the average per-day cost of a {hotel_type} hotel in INR for the city {user_input} for {num_days} days."
        )
        prompt1 = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful Travel assistant .. "),         

                ( "human", 
                
                "Estimate the average per-day cost of a {hotel_type} hotel in INR for the city {user_input} for {num_days} days and provide answer in one single line."
                
                
                ),
                
            ]
        )

         # LLM
        llm1 = ChatOpenAI(temperature=0.2)
        # Create the output parser
        output_parser1 = StrOutputParser()

        #chain = prompt | model | parser
        chain = prompt1 | llm1 | output_parser1      
        response= chain.invoke( {"hotel_type": hotel_type, "user_input": user_input,"num_days": num_days } )

        st.write(f"💰 Average Cost of Hotel : {response}")
        st.write("--")      

        st.success("Hotels Data Fetched Successful!")


    except Exception as e:
        st.error(f"An error occurred Executing Function Get_Hotels_and_AvgCosts : {e}")


#=================================================================
## Show the Hotel Details.
def Search_Hotels(input_city):
    try:
        # Get all the Hotel Details in a particular Area...
        radius = 1500
        input_city_name = input_city
        google_cloud_apikey = os.getenv("google_cloud_api_key")
        api_key = google_cloud_apikey        
        gmaps = googlemaps.Client(key=api_key)
        st.info("Executing Hotel Search....")
        places_result = gmaps.places(query=f"TOP five hotels in {input_city_name} with rate per night", radius=radius, type='lodging')
        if places_result['results']:
            st.subheader("Found Hotels:")
            for place in places_result['results']:
                st.write(f"**{place.get('name')}**")
                st.write(f"Address: {place.get('formatted_address')}")
                st.write(f"Rating: {place.get('rating', 'N/A')}")
                st.write(f"Price  : {place.get('price_level', 'N/A')}")
                st.write(f"Serves Breakfast : {place.get('serves_breakfast', 'N/A')}")
                st.write(f"Serves Brunch : {place.get('serves_brunch', 'N/A')}")
                st.write(f"User Ratings : {place.get('user_ratings_total', 'N/A')}")
                st.write(f"Opening Hours : {place.get('opening_hours', 'N/A')}")
                st.write(f"Booking URL : {place.get('url', 'N/A')}")
                st.markdown("---")
        else:
            st.info("No hotels found for this location and radius.")
    except Exception as e:
            st.error(f"An error occurred Executing Hotel Search : {e}")

#=================================================================

## Main program to process everything..

# Retrieve the any API Key environment variable
google_cloud_apikey = os.getenv("google_cloud_api_key")
api_key = google_cloud_apikey



# You can add a button to process the inputs
if st.button("Show Travel Iternary  "):
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
            st.header("Showing Full Travel Iternary")
            st.write("--")  

            #==========================================================================
            ##Show the Weather data and call the function..                  
            weather_data = get_weather_data(city_name)
            if weather_data:
                # st.success("Showing Weather Data...!")
                main_data = weather_data['main']
                weather_desc = weather_data['weather'][0]['description']
                wind_speed = weather_data['wind']['speed']
                
                st.markdown("---")  
                st.subheader(f"Weather in {city_name.capitalize()}")
                st.write(f"**Temperature:** {main_data['temp']}°C")
                st.write(f"**Feels Like:** {main_data['feels_like']}°C")
                st.write(f"**Humidity:** {main_data['humidity']}%")
                st.write(f"**Conditions:** {weather_desc.capitalize()}")
                st.write(f"**Wind Speed:** {wind_speed} m/s")                   
                st.markdown("---")                 
            else:
                st.error("Could not retrieve weather data. Please check the city name or API key.")
      
                            
            #==========================================================================

            ## call the function for Toursit Attractions..
            # Show Toursit Attractions  
            location = city_name
            Get_Toursit_Places(location)

            #==========================================================================

            #Show the Hotels in the Area..
            city_name = from_city
            ## Calling for Hotel and Hotels Costs
            #Search_Hotels(city_name)
            Get_Hotels_and_AvgCosts(city_name,number_of_days)

            #==========================================================================

             #Show the Fligts for a particular Destination.
            destination_city = from_city
            Get_Flights_Data(destination_city)

            #==========================================================================
    else:
        st.warning("Main Function : Both inputs must be provided to process.")
        st.write("Main Function Input required.")
        




    
