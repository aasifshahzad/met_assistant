#!/usr/bin/env python

from typing import Optional, List, Tuple, Dict
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from openai import OpenAI
import requests
import json
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime
import numpy as np
from datetime import datetime, timezone

timeformat = "unixtime"


def get_openmeteo_client():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    return openmeteo_requests.Client(session=retry_session)

openmeteo = get_openmeteo_client()

def get_weather_description(code: int , city_location: Optional[str] = "") -> Optional[str]:
    # Central_Europe_cities
    central_europe_cities = ["Berlin","Vienna","Prague","Budapest","Warsaw","Bratislava","Ljubljana","Zagreb","Munich","Frankfurt","Zurich","Geneva","Milan","Rome","Madrid","Paris","Brussels","Amsterdam" # Add more cities as needed
    ]
    # Weather Codes
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Drizzle with Light intensity",
        53: "Drizzle with Moderate intensity",
        55: "Drizzle with Dense intensity",
        56: "Freezing Drizzle: Light intensity",
        57: "Freezing Drizzle: Dense intensity",
        61: "Rain with Slight intensity",
        63: "Rain with Moderate intensity",
        65: "Rain with Heavy intensity",
        66: "Freezing Rain with Light intensity",
        67: "Freezing Rain with Heavy intensity",
        71: "Snowfall with Slight intensity",
        73: "Snowfall with Moderate intensity",
        75: "Snowfall with Heavy intensity",
        77: "Snow grains",
        80: "Rain showers with Slight intensity",
        81: "Rain showers with Moderate intensity",
        82: "Rain showers with Violent intensity",
        85: "Snow showers with Slight",
        86: "Snow showers with Heavy",
        95: "Thunderstorm with Slight or moderate",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }

    # Check if the code is in the dictionary
    if code in weather_codes:
        if code in [95, 96, 99] and city_location not in central_europe_cities:
            return "Thunderstorm with hail warning is not available outside Central Europe"
        else:
            return weather_codes[code]
    else:
        return "Unknown weather code"

def convert_timestamp_to_date_and_time(timestamp, time_zone=timezone.utc):
    try:
        dt_object = datetime.fromtimestamp(timestamp, time_zone)
        date = dt_object.strftime("%d-%m-%Y")
        time = dt_object.strftime("%H:%M")
        return date, time
    except Exception as e:
        print(f"Error converting timestamp to date and time: {e}")
        return None, None

def get_user_input(user_date_input,user_hour_input):
    date_formats = ["%Y/%m/%d", "%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"]

    # Try parsing the date with different formats
    parsed_date = None
    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(user_date_input, date_format).strftime("%Y-%m-%d")
            break  # Break if parsing is successful
        except ValueError:
            pass  # Continue to the next format if parsing fails

    if parsed_date is None:
        print("Invalid date format. Please use 'YYYY/MM/DD', 'DD-MM-YYYY', 'YYYY-MM-DD', or 'DD/MM/YYYY'.")
        return None

    try:
        # Ensure the hour is a valid integer
        hour = int(user_hour_input)
        # Validate the hour is in the range [0, 23]
        if not (0 <= hour <= 23):
            print("Invalid hour. Please enter a valid hour in the range [0, 23].")
            return None
    except ValueError:
        print("Invalid hour. Please enter a valid integer for the hour.")
        return None

    # Combine date and time, defaulting minutes and seconds to 00:00
    target_datetime = f"{parsed_date} {hour:02d}:00:00"
    return target_datetime



    # Now you can use target_datetime in your air_quality_data function
    # result = air_quality_data(openmeteo, latitude, longitude, target_datetime)

def get_lat_long_from_city(city_name: str, count: int = 1, language: str = 'en', format: str = 'json') -> Optional[Tuple[float, float]]:
    api_url: str = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        'name': city_name,
        'count': count,
        'language': language,
        'format': format
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)
        result = response.json()
        # print(result)
        if result:
            longitude = result['results'][0]['longitude']
            latitude = result['results'][0]['latitude']
            return float(longitude), float(latitude)
        else:
            print(f"Error: Unable to retrieve coordinates. API response: {result}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def extract_city_info(city_name: str, count: int = 1, language: str = 'en', format: str = 'json') -> Optional[Tuple[str, float, float, int, str, str, float, str]]:
    api_url: str = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        'name': city_name,
        'count': count,
        'language': language,
        'format': format
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)
        results = response.json()
        
        if results:
            city_name = results['results'][0]['name']
            latitude = results['results'][0]['latitude']
            longitude = results['results'][0]['longitude']
            population = results['results'][0]['population']
            country = results['results'][0]['country']
            country_code = results['results'][0]['country_code']
            elevation = results['results'][0]['elevation']
            timezone = results['results'][0]['timezone']
            
            print(f"City Name: {city_name}")
            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
            print(f"Population: {population}")
            print(f"Country: {country}")
            print(f"Country Code: {country_code}")
            print(f"Elevation: {elevation}")
            print(f"Timezone: {timezone}")
            
            json_output = {
                                    "City Name": city_name,
                                    "Latitude": latitude,
                                    "Longitude": longitude,
                                    "Population": population,
                                    "Country": country,
                                    "Country Code": country_code,
                                    "Elevation": elevation,
                                    "Timezone": timezone
                                }
            
            return json_output
        else:
            print(f"Error: Unable to extract the city info. API response: {results}")
            return None

    except KeyError as e:
        print(f"Error: Key not found in the response - {e}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def daily_river_discharge(openmeteo, latitude, longitude, target_date):
    url = "https://flood-api.open-meteo.com/v1/flood"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "river_discharge",
        "timeformat": "unixtime",
        "past_days": 92,
        "forecast_days": 92,
    }

    try:
        # Assuming openmeteo.weather_api returns a list of responses
        responses = openmeteo.weather_api(url, params=params)

        # Assuming response.Daily() returns the daily data
        response = responses[0].Daily()

        # Assuming response.Variables(0).ValuesAsNumpy() returns river discharge values
        daily_river_discharge = response.Variables(0).ValuesAsNumpy()

        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(response.Time(), unit="s"),
                end=pd.to_datetime(response.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=response.Interval()),
                inclusive="left"
            )
        }

        daily_data["river_discharge"] = daily_river_discharge
        daily_dataframe = pd.DataFrame(data=daily_data)

        # Filter the DataFrame for the target date
        target_date = pd.to_datetime(target_date)
        discharge_value = daily_dataframe[daily_dataframe['date'] == target_date]['river_discharge'].values

        if len(discharge_value) > 0:
            formatted_date = target_date.strftime("%d-%m-%Y")
            rounded_discharge = round(float(discharge_value[0]), 4)
            print(f"River discharge on {formatted_date}: {rounded_discharge} m³/s")
            json_output = {
                            "Date": formatted_date,
                            "River discharge":rounded_discharge
                            }
            return json_output
        else:
            formatted_date = target_date.strftime("%d-%m-%Y")
            print(f"No data available for {formatted_date}")
            return None

    except KeyError as e:
        print(f"Error: Key not found in the response - {e}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def air_quality_data(openmeteo, latitude, longitude, target_datetime):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["pm10", "pm2_5", "aerosol_optical_depth", "dust"],
        "timeformat": "unixtime",
        "past_days": 92,
    }

    try:
        # Assuming openmeteo.weather_api returns a list of responses
        responses = openmeteo.weather_api(url, params=params)

        # Assuming response.Hourly() returns the hourly data
        response = responses[0].Hourly()

        # Assuming response.Variables(index) returns the hourly data for the specified index
        hourly_pm10 = response.Variables(0).ValuesAsNumpy()
        hourly_pm2_5 = response.Variables(1).ValuesAsNumpy()
        hourly_aerosol_optical_depth = response.Variables(2).ValuesAsNumpy()
        hourly_dust = response.Variables(3).ValuesAsNumpy()

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(response.Time(), unit="s"),
                end=pd.to_datetime(response.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=response.Interval()),
                inclusive="left"
            )
        }
        hourly_data["pm10"] = hourly_pm10
        hourly_data["pm2_5"] = hourly_pm2_5
        hourly_data["aerosol_optical_depth"] = hourly_aerosol_optical_depth
        hourly_data["dust"] = hourly_dust

        hourly_dataframe = pd.DataFrame(data=hourly_data)

        # Filter the DataFrame for the target datetime
        target_datetime = pd.to_datetime(target_datetime)
        target_data = hourly_dataframe[hourly_dataframe['date'] == target_datetime]

        if not target_data.empty:
            formatted_datetime = target_datetime.strftime("%Y-%m-%d at %H:%M")
            print(f"AQI data on {formatted_datetime}:")
            print(f"PM10: {round(float(target_data['pm10'].values[0]), 4)} µg/m³")
            print(f"PM2.5: {round(float(target_data['pm2_5'].values[0]), 4)} µg/m³")
            print(f"Aerosol Optical Depth: {round(float(target_data['aerosol_optical_depth'].values[0]), 4)}")
            print(f"Dust: {round(float(target_data['dust'].values[0]), 4)}")
            json_output = {
                            "Date and Time": formatted_datetime,
                            "PM 10": f"{round(float(target_data['pm10'].values[0]), 4)} µg/m³",
                            "PM 2.5":f"{round(float(target_data['pm2_5'].values[0]), 4)} µg/m³",
                            "Aerosol Optical Depth": f"{round(float(target_data['aerosol_optical_depth'].values[0]), 4)}",
                            "dust": f"{round(float(target_data['dust'].values[0]), 4)}"
                        }
            return json_output
        else:
            formatted_datetime = target_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print(f"No data available for {formatted_datetime}")
            return None

    except KeyError as e:
        print(f"Error: Key not found in the response - {e}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def describe_european_aqi(aqi_value):
    if 0 <= aqi_value < 20:
        return "Good"
    elif 20 <= aqi_value < 40:
        return "Fair"
    elif 40 <= aqi_value < 60:
        return "Moderate"
    elif 60 <= aqi_value < 80:
        return "Poor"
    elif 80 <= aqi_value < 100:
        return "Very Poor"
    elif aqi_value >= 100:
        return "Extremely Poor"
    else:
        return "Invalid AQI value"

def describe_us_aqi(aqi_value):
    if 0 <= aqi_value <= 50:
        return "Good"
    elif 51 <= aqi_value <= 100:
        return "Moderate"
    elif 101 <= aqi_value <= 150:
        return "Unhealthy for Sensitive Groups"
    elif 151 <= aqi_value <= 200:
        return "Unhealthy"
    elif 201 <= aqi_value <= 300:
        return "Very Unhealthy"
    elif 301 <= aqi_value <= 500:
        return "Hazardous"
    else:
        return "Invalid AQI value"

def describe_current_air_quality_index(openmeteo, latitude, longitude, target_datetime):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["european_aqi", "us_aqi"],
        "timeformat": "unixtime",
        "past_days": 92,
    }

    try:
        # Assuming openmeteo.weather_api returns a list of responses
        responses = openmeteo.weather_api(url, params=params)

        for response in responses:
            # Current values. The order of variables needs to be the same as requested.
            current = response.get("current", {})

            current_european_aqi = current.get("european_aqi")
            current_us_aqi = current.get("us_aqi")

            if current_european_aqi is not None and current_us_aqi is not None:
                current_aqi_data = {
                    "date": pd.date_range(
                        start=pd.to_datetime(response.get("time"), unit="s"),
                        end=pd.to_datetime(response.get("timeEnd"), unit="s"),
                        freq=pd.Timedelta(seconds=response.get("interval")),
                        inclusive="left"
                    )
                }
                current_aqi_data["current_european_aqi"] = current_european_aqi
                current_aqi_data["current_us_aqi"] = current_us_aqi

                current_aqi_dataframe = pd.DataFrame(data=current_aqi_data)

                # Filter the DataFrame for the target datetime
                target_datetime = pd.to_datetime(target_datetime)
                target_data = current_aqi_dataframe[current_aqi_dataframe['date'] == target_datetime]

                if not target_data.empty:
                    formatted_datetime = target_datetime.strftime("%Y-%m-%d at %H:%M")

                    print(f"Formatted Time {formatted_datetime}")
                    current_european_aqi = target_data['current_european_aqi'].values[0]
                    european_rated = describe_european_aqi(current_european_aqi)
                    print(f"Current european_aqi is {current_european_aqi} and it is rated as {european_rated}")

                    current_us_aqi = target_data['current_us_aqi'].values[0]
                    us_rated = describe_us_aqi(current_us_aqi)
                    print(f"Current us_aqi is {current_us_aqi} and it is rated as {us_rated}")

                    json_output = {
                        "Date and Time": formatted_datetime,
                        "European AQI": f"{round(float(current_european_aqi), 4)} and it is rated as {european_rated}",
                        "US AQI": f"{round(float(current_us_aqi), 4)} and it is rated as {us_rated}",
                    }
                    return json_output
                else:
                    formatted_datetime = target_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"No data available for {formatted_datetime}")
                    return None

        print("No valid data found in the response.")
        return None

    except KeyError as e:
        print(f"Error: Key not found in the response - {e}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def daily_marine_data(openmeteo, latitude, longitude, target_datetime):
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "wave_height_max",
        "timeformat": "unixtime",
        "timezone": "auto",
        "past_days": 92,

    }

    try:
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        # Process daily data
        daily = response.Daily()
        daily_wave_height_max = daily.Variables(0).ValuesAsNumpy()

        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s"),
                end=pd.to_datetime(daily.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            ),
            "daily_wave_height_max": [value for value in daily_wave_height_max]
        }
        
        daily_dataframe = pd.DataFrame(data=daily_data)
        #print(daily_dataframe)
        
        target_datetime = pd.to_datetime(target_datetime)
        target_data = daily_dataframe[daily_dataframe['date'].dt.date == target_datetime.date()]
        
        if not target_data.empty:
            formatted_datetime = target_datetime.strftime("%Y-%m-%d at %H:%M")
            #print(f"Max Wave Height: {round(float(target_data['daily_wave_height_max'].values[0]), 4)}")
            json_output = {
                            "Date and Time": formatted_datetime,
                            "Max Wave Height": {round(float(target_data['daily_wave_height_max'].values[0]), 4)}
                        }
            return json_output
        else:
            formatted_datetime = target_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print(f"No data available for {formatted_datetime}")
            return None

    except KeyError as e:
        print(f"Error: Key not found in the response - {e}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def hourly_marine_data(openmeteo, latitude, longitude, target_datetime):
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["wave_height", "wave_direction","wave_period"],
        "timeformat": "unixtime",
        "timezone": "auto",
        "past_days": 92,
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        # Process hourly data
        hourly = response.Hourly()
        hourly_wave_height = hourly.Variables(0).ValuesAsNumpy()
        hourly_wave_direction = hourly.Variables(1).ValuesAsNumpy()
        current_wave_period = hourly.Variables(2).ValuesAsNumpy()

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s"),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "hourly_wave_height": [value for value in hourly_wave_height],
            "hourly_wave_direction": [value for value in hourly_wave_direction],
            "hourly_wave_period": [value for value in current_wave_period]
            }

        #print("Hourly Data:", hourly_data)
        
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        #print(hourly_dataframe)
        
        target_datetime = pd.to_datetime(target_datetime)
        target_data = hourly_dataframe[hourly_dataframe['date'].dt.date == target_datetime.date()]
        
        if not target_data.empty:
            formatted_datetime = target_datetime.strftime("%Y-%m-%d at %H:%M")
            # print(formatted_datetime)
            # print(f"hourly_wave_height: {round(float(target_data['hourly_wave_height'].values[0]), 4)} meters")
            # print(f"hourly_wave_direction: {round(float(target_data['hourly_wave_direction'].values[0]), 4)} degree"),
            # print(f"hourly_wave_period: {round(float(target_data['hourly_wave_period'].values[0]), 4)} seconds"),
            
            json_output = {
                            "Date and Time": formatted_datetime,
                            "Wave Height": f"{round(float(target_data['hourly_wave_height'].values[0]), 4)} meters",
                            "Wave Direction": f"{round(float(target_data['hourly_wave_direction'].values[0]), 4)} degree",
                            "Wave Period": f"{round(float(target_data['hourly_wave_period'].values[0]), 4)} seconds"
                        }
            return json_output
        else:
            formatted_datetime = target_datetime.strftime("%Y-%m-%d %H:%M:%S")
            print(f"No data available for {formatted_datetime}")
            return None

    except KeyError as e:
        print(f"Error: Key not found in the response - {e}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def climate_change_data(openmeteo, latitude, longitude, target_year):
    url = "https://climate-api.open-meteo.com/v1/climate"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": "1950-01-01",
        "end_date":  "2050-12-31",
        "models":  "MRI_AGCM3_2_S",
        "timeformat": "unixtime",
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        # Process daily data
        daily = response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()

        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s"),
                end=pd.to_datetime(daily.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            ),
            "temperature_2m_max": [value for value in daily_temperature_2m_max],
            "temperature_2m_min": [value for value in daily_temperature_2m_min],
            "precipitation_sum": [value for value in daily_precipitation_sum]
        }

        daily_dataframe = pd.DataFrame(data=daily_data)
        # print(daily_dataframe)

        daily_dataframe['year'] = daily_dataframe['date'].dt.year
        filtered_data = daily_dataframe[daily_dataframe['year'] == target_year]
        # Drop the 'year' column if it's no longer needed
        filtered_data = filtered_data.drop(columns=['year'])
        # Filter for the target year if provided
        if target_year:
            filtered_data = daily_dataframe[daily_dataframe['date'].dt.year == target_year]
            if not filtered_data.empty:
                json_output = {
                    "Year": target_year,
                    "Temperature Max": f"{round(float(filtered_data['temperature_2m_max'].mean()), 4)} °C",
                    "Temperature Min": f"{round(float(filtered_data['temperature_2m_min'].mean()), 4)} °C",
                    "Precipitation Sum": f"{round(float(filtered_data['precipitation_sum'].sum()), 4)} mm",
                }
                return json_output
            else:
                print(f"No data available for the year {target_year}")
                return None
        

    except KeyError as e:
        print(f"Error: Key not found in the response - {e}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def describe_current_weather(openmeteo, latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "surface_pressure", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
        "timeformat": "unixtime"
    }

    try:
        responses = openmeteo.weather_api(url, params=params)

        for response in responses:
            current = response.Current()
            current_weather_code = current.Variables(7).Value()
            weather_description = get_weather_description(current_weather_code, city_location="Berlin")

            current_date = datetime.now().date()
            current_time = datetime.now().time()
            formatted_date = current_date.strftime("%d-%m-%Y")
            formatted_time = current_time.strftime("%H:%M:%S")

            weather_data = {
                "date": formatted_date,
                "time": formatted_time,
                "day_or_night": "Day" if current.Variables(2).Value() else "Night",
                "coordinates": {
                    "latitude": round(response.Latitude(), 4),
                    "longitude": round(response.Longitude(), 4),
                },
                "elevation": {
                    "value": round(response.Elevation(), 4),
                    "unit": "meters"
                },
                "temperature_2m": {
                    "value": round(current.Variables(0).Value(), 4),
                    "unit": "°C"
                },
                "relative_humidity_2m": {
                    "value": round(current.Variables(1).Value(), 4),
                    "unit": "%"
                },
                "precipitation": {
                    "value": round(current.Variables(3).Value(), 4),
                    "unit": "mm"
                },
                "rain": {
                    "value": round(current.Variables(4).Value(), 4),
                    "unit": "mm"
                },
                "showers": {
                    "value": round(current.Variables(5).Value(), 4),
                    "unit": "mm"
                },
                "snowfall": {
                    "value": round(current.Variables(6).Value(), 4),
                    "unit": "mm"
                },
                "weather_code": current_weather_code,
                "weather_description": weather_description,
                "cloud_cover": {
                    "value": round(current.Variables(8).Value(), 4),
                    "unit": "%"
                },
                "surface_pressure": {
                    "value": round(current.Variables(9).Value(), 4),
                    "unit": "hPa"
                },
                "wind_speed_10m": {
                    "value": round(current.Variables(10).Value(), 4),
                    "unit": "m/s"
                },
                "wind_direction_10m": {
                    "value": round(current.Variables(11).Value(), 4),
                    "unit": "degrees"
                },
                "wind_gusts_10m": {
                    "value": round(current.Variables(12).Value(), 4),
                    "unit": "m/s"
                },
            }

            print(json.dumps(weather_data, indent=2))
            return weather_data

        print("No data available")
        return None

    except KeyError as e:
        print(f"Error: Key not found in the response - {e}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def get_today_weather_data(latitude, longitude, target_date):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "daylight_duration",
                  "sunshine_duration", "uv_index_max", "uv_index_clear_sky_max", "precipitation_sum", "rain_sum",
                  "showers_sum", "snowfall_sum", "precipitation_hours", "precipitation_probability_max",
                  "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant",
                  "shortwave_radiation_sum", "et0_fao_evapotranspiration"],
        "timeformat": "unixtime",
        "timezone": "auto",
	    "past_days": 92
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    # Process daily data. The order of variables needs to be the same as requested.
    
    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
    daily_sunrise = daily.Variables(3).ValuesAsNumpy()
    daily_sunset = daily.Variables(2).ValuesAsNumpy()
    daily_daylight_duration = daily.Variables(5).ValuesAsNumpy()
    daily_sunshine_duration = daily.Variables(6).ValuesAsNumpy()
    daily_uv_index_max = daily.Variables(7).ValuesAsNumpy()
    daily_uv_index_clear_sky_max = daily.Variables(8).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(9).ValuesAsNumpy()
    daily_rain_sum = daily.Variables(10).ValuesAsNumpy()
    daily_showers_sum = daily.Variables(11).ValuesAsNumpy()
    daily_snowfall_sum = daily.Variables(12).ValuesAsNumpy()
    daily_precipitation_hours = daily.Variables(13).ValuesAsNumpy()
    daily_precipitation_probability_max = daily.Variables(12).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(15).ValuesAsNumpy()
    daily_wind_gusts_10m_max = daily.Variables(16).ValuesAsNumpy()
    daily_wind_direction_10m_dominant = daily.Variables(17).ValuesAsNumpy()
    daily_shortwave_radiation_sum = daily.Variables(18).ValuesAsNumpy()
    daily_et0_fao_evapotranspiration = daily.Variables(19).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s"),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["weather_code"] = np.round(daily_weather_code[0], 2)
    daily_data["temperature_2m_max"] = np.round(daily_temperature_2m_max, 2)
    daily_data["temperature_2m_min"] = np.round(daily_temperature_2m_min, 2)
    daily_data["sunrise"] = np.round(daily_sunrise, 2)
    daily_data["sunset"] = np.round(daily_sunset, 2)
    daily_data["daylight_duration"] = np.round(daily_daylight_duration, 2)
    daily_data["sunshine_duration"] = np.round(daily_sunshine_duration, 2)
    daily_data["uv_index_max"] = np.round(daily_uv_index_max, 2)
    daily_data["uv_index_clear_sky_max"] = np.round(daily_uv_index_clear_sky_max, 2)
    daily_data["precipitation_sum"] = np.round(daily_precipitation_sum, 2)
    daily_data["rain_sum"] = np.round(daily_rain_sum, 2)
    daily_data["showers_sum"] = np.round(daily_showers_sum, 2)
    daily_data["snowfall_sum"] = np.round(daily_snowfall_sum, 2)
    daily_data["precipitation_hours"] = np.round(daily_precipitation_hours, 2)
    daily_data["precipitation_probability_max"] = np.round(daily_precipitation_probability_max, 2)
    daily_data["wind_speed_10m_max"] = np.round(daily_wind_speed_10m_max, 2)
    daily_data["wind_gusts_10m_max"] = np.round(daily_wind_gusts_10m_max, 2)
    daily_data["wind_direction_10m_dominant"] = np.round(daily_wind_direction_10m_dominant, 2)
    daily_data["shortwave_radiation_sum"] = np.round(daily_shortwave_radiation_sum, 2)
    daily_data["et0_fao_evapotranspiration"] = np.round(daily_et0_fao_evapotranspiration, 2)

    daily_dataframe = pd.DataFrame(data = daily_data)
    #print(daily_dataframe)
    target_date_data = daily_dataframe[daily_dataframe['date'] == target_date]
    target_date_data = target_date_data.apply(lambda x: x.astype(float) if x.name != 'date' else x)

    # Weather data for the target date
    # print(target_date_data)
    # Convert seconds to hours for Daylight Duration and Sunshine Duration
    # Convert seconds to hours for Daylight Duration and Sunshine Duration
    daylight_duration_hours = float(target_date_data["daylight_duration"].values[0]) / 3600
    sunshine_duration_hours = float(target_date_data["sunshine_duration"].values[0]) / 3600
    target_date = pd.to_datetime(target_date)

    # Print statements for each variable with unit names
    # print("\nWeather data for the target date:", target_date.date())
    # print("Weather Code:", get_weather_description(target_date_data["weather_code"].values[0]))
    # print("Max Temperature:", target_date_data["temperature_2m_max"].values[0], "°C")
    # print("Min Temperature:", target_date_data["temperature_2m_min"].values[0], "°C")
    # print("Daylight Duration:", round(daylight_duration_hours, 2), "hours")
    # print("Sunshine Duration:", round(sunshine_duration_hours, 2), "hours")
    # print("UV Index Max:", target_date_data["uv_index_max"].values[0], " (UV Index)")
    # print("UV Index Clear Sky Max:", target_date_data["uv_index_clear_sky_max"].values[0], " (UV Index)")
    # print("Precipitation Sum:", target_date_data["precipitation_sum"].values[0], "mm")
    # print("Rain Sum:", target_date_data["rain_sum"].values[0], "mm")
    # print("Showers Sum:", target_date_data["showers_sum"].values[0], "mm")
    # print("Snowfall Sum:", target_date_data["snowfall_sum"].values[0], "mm")
    # print("Precipitation Hours:", target_date_data["precipitation_hours"].values[0], "hours")
    # print("Precipitation Probability Max:", target_date_data["precipitation_probability_max"].values[0], "%")
    # print("Wind Speed 10m Max:", target_date_data["wind_speed_10m_max"].values[0], "m/s")
    # print("Wind Gusts 10m Max:", target_date_data["wind_gusts_10m_max"].values[0], "m/s")
    # print("Wind Direction 10m Dominant:", target_date_data["wind_direction_10m_dominant"].values[0], "degrees")
    # print("Shortwave Radiation Sum:", target_date_data["shortwave_radiation_sum"].values[0], "J/m^2")
    # print("ET0 FAO Evapotranspiration:", target_date_data["et0_fao_evapotranspiration"].values[0], "mm")

    json_output = {
        "Weather data for the target date": str(target_date.date()),
        "Weather Code": get_weather_description(target_date_data["weather_code"].values[0]),
        "Max Temperature": f"{float(target_date_data['temperature_2m_max'].values[0]):.2f} °C",
        "Min Temperature": f"{float(target_date_data['temperature_2m_min'].values[0]):.2f} °C",
        "Daylight Duration": f"{daylight_duration_hours:.2f} hours",
        "Sunshine Duration": f"{sunshine_duration_hours:.2f} hours",
        "UV Index Max": f"{float(target_date_data['uv_index_max'].values[0]):.2f}  (UV Index)",
        "UV Index Clear Sky Max": f"{float(target_date_data['uv_index_clear_sky_max'].values[0]):.2f}  (UV Index)",
        "Precipitation Sum": f"{float(target_date_data['precipitation_sum'].values[0]):.2f} mm",
        "Rain Sum": f"{float(target_date_data['rain_sum'].values[0]):.2f} mm",
        "Showers Sum": f"{float(target_date_data['showers_sum'].values[0]):.2f} mm",
        "Snowfall Sum": f"{float(target_date_data['snowfall_sum'].values[0]):.2f} mm",
        "Precipitation Hours": f"{float(target_date_data['precipitation_hours'].values[0]):.2f} hours",
        "Precipitation Probability Max": f"{float(target_date_data['precipitation_probability_max'].values[0]):.2f} %",
        "Wind Speed 10m Max": f"{float(target_date_data['wind_speed_10m_max'].values[0]):.2f} m/s",
        "Wind Gusts 10m Max": f"{float(target_date_data['wind_gusts_10m_max'].values[0]):.2f} m/s",
        "Wind Direction 10m Dominant": f"{float(target_date_data['wind_direction_10m_dominant'].values[0]):.2f} degrees",
        "Shortwave Radiation Sum": f"{float(target_date_data['shortwave_radiation_sum'].values[0]):.2f} J/m^2",
        "ET0 FAO Evapotranspiration": f"{float(target_date_data['et0_fao_evapotranspiration'].values[0]):.2f} mm"
    }


    # Convert the dictionary to a JSON-formatted string
    json_output_str = json.dumps(json_output, indent=2)

    # Print the JSON-formatted string
    #print(json_output_str)

    # Return the JSON-formatted string if needed
    return json_output_str
