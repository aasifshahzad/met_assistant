tools=[
{
    "type": "function",
    "function": {
      "name": "get_openmeteo_client",
      "description": "Retrieves an Open-Meteo API client configured with caching and retry mechanism.",
      "parameters": {
        "type": "object",
        "properties": {
          "cache_path": {
            "type": "string",
            "format": "string",
            "description": "Path to the cache directory. Defaults to '.cache'."
          },
          "expire_after": {
            "type": "string",
            "format": "integer",
            "description": "Cache expiration time in seconds. Defaults to 3600."
          },
          "retries": {
            "type": "string",
            "format": "integer",
            "description": "Number of retries in case of an error. Defaults to 5."
          },
          "backoff_factor": {
            "type": "string",
            "format": "float",
            "description": "Factor by which the delay between retries will increase. Defaults to 0.2."
          }
        },
        "required": []
      },
      "return": {
        "type": "object",
        "properties": {
          "openmeteo_client": {
            "type": "object",
            "description": "Open-Meteo API client instance."
          }
        }
      }
    }
  },
  {
  "type": "function",
  "function": {
      "name": "get_weather_code_description",
      "description": "Retrieves a weather description based on the provided weather code and, optionally, the city location.",
      "parameters": {
          "type": "object",
          "properties": {
              "code": {
                  "type": "string",
                  "format": "integer",
                  "description": "Weather code."
              },
              "city_location": {
                  "type": "string",
                  "format": "string",
                  "description": "City location for specific thunderstorm warnings. Optional."
              }
          },
          "required": ["code"]
      },
      "return": {
          "type": "string",
          "description": "Weather description or a message indicating unknown weather code. If thunderstorm warning is not applicable outside Central Europe, an additional message is returned."
      },
      "note": {
          "type": "string",
          "content": "Central Europe cities are considered for thunderstorm warnings (codes 95, 96, 99). Additional cities can be added to the `central_europe_cities` list. Weather codes are mapped to descriptive strings in the `weather_codes` dictionary."
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "convert_timestamp_to_date_and_time",
      "description": "Converts a Unix timestamp to a date and time string.",
      "parameters": {
          "type": "object",
          "properties": {
              "timestamp": {
                  "type": "string",
                  "format": "float",
                  "description": "Unix timestamp."
              },
              "time_zone": {
                  "type": "string",
                  "description": "Time zone for the unixtime."
              }
          },
          "required": ["timestamp"]
      },
      "return": {
          "type": "tuple",
          "items": [
              {"type": "string", "description": "Date string formatted as \"%d-%m-%Y\"."},
              {"type": "string", "description": "Time string formatted as \"%H:%M\"."}
          ],
          "description": "Returns a tuple containing date and time strings. Returns (None, None) in case of an error."
      },
      "note": {
          "type": "string",
          "content": "The date is formatted as \"%d-%m-%Y\". The time is formatted as \"%H:%M\"."
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "get_user_input",
      "description": "Validates user input for date and hour, and returns a formatted datetime string.",
      "parameters": {
          "type": "object",
          "properties": {
              "user_date_input": {
                  "type": "string",
                  "format": "string",
                  "description": "User-provided date input."
              },
              "user_hour_input": {
                  "type": "string",
                  "format": "string",
                  "description": "User-provided hour input."
              }
          },
          "required": ["user_date_input","user_hour_input"]
      },
      "return": {
          "type": "string",
          "description": "Formatted datetime string or None if input is invalid."
      },
      "note": {
          "type": "string",
          "content": "Supports date formats: \"%Y/%m/%d\", \"%d-%m-%Y\", \"%Y-%m-%d\", \"%d/%m/%Y\". Validates the hour is a valid integer in the range [0, 23]."
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "get_lat_long_from_city",
      "description": "Retrieves the latitude and longitude coordinates for a given city name.",
      "parameters": {
          "type": "object",
          "properties": {
              "city_name": {
                  "type": "string",
                  "format": "string",
                  "description": "Name of the city."
              },
              "count": {
                  "type": "string",
                  "format": "integer",
                  "description": "Number of results to return (default is 1)."
              },
              "language": {
                  "type": "string",
                  "format": "string",
                  "description": "Language for the response (default is 'en')."
              },
              "format": {
                  "type": "string",
                  "format": "string",
                  "description": "Response format (default is 'json')."
              }
          },
          "required": ["city_name"]
      },
      "return": {
          "type": "tuple",
          "items": [
              {"type": "float", "description": "Longitude coordinate."},
              {"type": "float", "description": "Latitude coordinate."}
          ],
          "description": "Returns a tuple containing latitude and longitude coordinates. Returns None in case of an error."
      },
      "note": {
          "type": "string",
          "content": "Uses the Open-Meteo geocoding API: https://geocoding-api.open-meteo.com/v1/search. The count parameter determines the number of results to return."
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "extract_city_info",
      "description": "Extracts information about a city using the Open-Meteo geocoding API.",
      "parameters": {
          "type": "object",
          "properties": {
              "city_name": {
                  "type": "string",
                  "format": "string",
                  "description": "Name of the city."
              },
              "count": {
                  "type": "string",
                  "format": "integer",
                  "description": "Number of results to return (default is 1)."
              },
              "language": {
                  "type": "string",
                  "format": "string",
                  "description": "Language for the response (default is 'en')."
              },
              "format": {
                  "type": "string",
                  "format": "string",
                  "description": "Response format (default is 'json')."
              }
          },
          "required": ["city_name"]
      },
      "return": {
          "type": "object",
          "description": "Dictionary containing city information. Returns None in case of an error.",
          "properties": {
              "City Name": {"type": "string", "description": "Name of the city."},
              "Latitude": {"type": "float", "description": "Latitude coordinate."},
              "Longitude": {"type": "float", "description": "Longitude coordinate."},
              "Population": {"type": "integer", "description": "Population of the city."},
              "Country": {"type": "string", "description": "Country where the city is located."},
              "Country Code": {"type": "string", "description": "Country code of the city."},
              "Elevation": {"type": "float", "description": "Elevation of the city."},
              "Timezone": {"type": "string", "description": "Timezone of the city."}
          }
      },
      "note": {
          "type": "string",
          "content": "Uses the Open-Meteo geocoding API: https://geocoding-api.open-meteo.com/v1/search."
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "daily_river_discharge",
      "description": "Retrieves daily river discharge data for a specific location and target date.",
      "parameters": {
          "type": "object",
          "properties": {
              "latitude": {"type": "string",
                           "format": "float",
                           "description": "Latitude of the location."},
              "longitude": {"type": "string",
                            "format": "float",
                            "description": "Longitude of the location."},
              "target_date": {"type": "string",
                              "format": "string",
                              "description": "Target date in the format \"%Y-%m-%d\"."}
          },
"required": [ "latitude", "longitude", "target_date"]
      },
      "return": {
          "type": "object",
          "description": "Dictionary containing the date and river discharge. Returns None if data is not available or an error occurs.",
          "properties": {
              "Date": {"type": "string", "description": "Formatted date of the river discharge."},
              "River discharge": {"type": "number", "description": "River discharge value in m³/s."}
          }
      },
      "note": {
          "type": "string",
          "content": "Uses the Open-Meteo flood API: https://flood-api.open-meteo.com/v1/flood."
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "air_quality_data",
      "description": "Retrieves air quality data for a specific location and target datetime.",
      "parameters": {
          "type": "object",
          "properties": {
 
              "latitude": {"type": "string",
                           "format": "float",
                           "description": "Latitude of the location."},
              "longitude": {"type": "string",
                            "format": "float",
                            "description": "Longitude of the location."},
              "target_datetime": {"type": "string",
                              "format": "string",
                              "description": "Target date in the format \"%Y-%m-%d\"."}
          },
"required": [ "latitude", "longitude", "target_datetime"]
      },
      "return": {
          "type": "object",
          "description": "Dictionary containing air quality data. Returns None if data is not available or an error occurs.",
          "properties": {
              "Date and Time": {"type": "string", "description": "Formatted date and time of the air quality data."},
              "PM 10": {"type": "string", "description": "PM 10 value in µg/m³."},
              "PM 2.5": {"type": "string", "description": "PM 2.5 value in µg/m³."},
              "Aerosol Optical Depth": {"type": "string", "description": "Aerosol Optical Depth value."},
              "Dust": {"type": "string", "description": "Dust value."}
          }
      },
      "note": {
          "type": "string",
          "content": "Uses the Open-Meteo air quality API: https://air-quality-api.open-meteo.com/v1/air-quality."
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "describe_european_aqi",
      "description": "Describes the European Air Quality Index based on the given AQI value.",
      "parameters": {
          "type": "object",
          "properties": {
              "aqi_value": {
                          "type": "string",
                          "format": "float",
                          "description": "Air Quality."
                          }
          },
          "required": ["aqi_value"]
      },
      "return": {
          "type": "string",
          "description": "Description of the air quality."
      },
      "note": {
          "type": "string",
          "content": "AQI ranges and descriptions are based on European standards."
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "describe_us_aqi",
      "description": "Describes the US Air Quality Index based on the given AQI value.",
      "parameters": {
          "type": "object",
          "properties": {
              "aqi_value": {"type": "string",
                            "format": "float",
                            "description": "Air Quality Index value."}
          },
          "required": ["aqi_value"]
      },
      "return": {
          "type": "string",
          "description": "Description of the air quality."
      },
      "note": {
          "type": "string",
          "content": "AQI ranges and descriptions are based on US standards."
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "describe_current_air_quality_index",
      "description": "Describes the current air quality index for a specific location and target datetime.",
      "parameters": {
          "type": "object",
          "properties": {
 
              "latitude": {"type": "string",
                           "format": "float",
                           "description": "Latitude of the location."},
              "longitude": {"type": "string",
                            "format": "float",
                            "description": "Longitude of the location."},
              "target_datetime": {"type": "string",
                              "format": "string",
                              "description": "Target date in the format \"%Y-%m-%d\"."}
          },
"required": [ "latitude", "longitude", "target_datetime"]
      },
      "return": {
          "type": "object",
          "description": "Dictionary containing descriptions of European and US AQI. Returns None if data is not available or an error occurs.",
          "properties": {
              "Date and Time": {"type": "string", "description": "Formatted date and time of the air quality data."},
              "European AQI": {"type": "string", "description": "Description and rating of the European AQI."},
              "US AQI": {"type": "string", "description": "Description and rating of the US AQI."}
          }
      },
      "note": {
          "type": "string",
          "content": "Uses the Open-Meteo air quality API: https://air-quality-api.open-meteo.com/v1/air-quality."
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "daily_marine_data",
      "description": "Retrieves daily marine data for a specific location and target datetime.",
      "parameters": {
          "type": "object",
          "properties": {
 
              "latitude": {"type": "string",
                           "format": "float",
                           "description": "Latitude of the location."},
              "longitude": {"type": "string",
                            "format": "float",
                            "description": "Longitude of the location."},
              "target_datetime": {"type": "string",
                              "format": "string",
                              "description": "Target date in the format \"%Y-%m-%d\"."}
          },
"required": [ "latitude", "longitude", "target_datetime"]
      },
      "return": {
          "type": "object",
          "description": "Dictionary containing daily marine data. Returns None if data is not available or an error occurs.",
          "properties": {
              "Date and Time": {"type": "string", "description": "Formatted date and time of the marine data."},
              "Max Wave Height": {"type": "number", "description": "Maximum wave height for the specified date."}
          }
      },
      "note": {
          "type": "string",
          "content": "Uses the Open-Meteo marine API: https://marine-api.open-meteo.com/v1/marine."
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "hourly_marine_data",
      "description": "Retrieves hourly marine data for a specific location and target datetime.",
      "parameters": {
          "type": "object",
          "properties": {
 
              "latitude": {"type": "string",
                           "format": "float",
                           "description": "Latitude of the location."},
              "longitude": {"type": "string",
                            "format": "float",
                            "description": "Longitude of the location."},
              "target_datetime": {"type": "string",
                              "format": "string",
                              "description": "Target date in the format \"%Y-%m-%d\"."}
          },
"required": [ "latitude", "longitude", "target_datetime"]
      },
      "return": {
          "type": "object",
          "description": "Dictionary containing hourly marine data. Returns None if data is not available or an error occurs.",
          "properties": {
              "Date and Time": {"type": "string", "description": "Formatted date and time of the marine data."},
              "Wave Height": {"type": "number", "description": "Hourly wave height in meters."},
              "Wave Direction": {"type": "number", "description": "Hourly wave direction in degrees."},
              "Wave Period": {"type": "number", "description": "Hourly wave period in seconds."}
          }
      },
      "note": {
          "type": "string",
          "content": "Uses the Open-Meteo marine API: https://marine-api.open-meteo.com/v1/marine."
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "climate_change_data",
      "description": "Retrieves climate change data for a specific location and target year.",
      "parameters": {
          "type": "object",
                      "properties": {
 
              "latitude": {"type": "string",
                           "format": "float",
                           "description": "Latitude of the location."},
              "longitude": {"type": "string",
                            "format": "float",
                            "description": "Longitude of the location."},
              "target_year": {"type": ["integer", "null"], "description": "Target year for data retrieval. If null, data for all years is considered."}

          },
"required": [ "latitude", "longitude"]
      },
      "return": {
          "type": "object",
          "description": "Dictionary containing climate change data for the target year. Returns None if data is not available or an error occurs.",
          "properties": {
              "Year": {"type": "integer", "description": "The target year for which the data is retrieved."},
              "Temperature Max": {"type": "string", "description": "Mean daily maximum temperature in degrees Celsius."},
              "Temperature Min": {"type": "string", "description": "Mean daily minimum temperature in degrees Celsius."},
              "Precipitation Sum": {"type": "string", "description": "Sum of daily precipitation in millimeters."}
          }
      },
      "note": {
          "type": "string",
          "content": "Uses the Open-Meteo climate API: https://climate-api.open-meteo.com/v1/climate."
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "describe_current_weather",
      "description": "Retrieves the current weather data for a specific location.",
      "parameters": {
          "type": "object",
          "properties": {
 
              "latitude": {"type": "string",
                           "format": "float",
                           "description": "Latitude of the location."},
              "longitude": {"type": "string",
                            "format": "float",
                            "description": "Longitude of the location."},
          },
"required": [ "latitude", "longitude"]
      },
      "return": {
          "type": "object",
          "description": "Dictionary containing current weather data. Returns None if data is not available or an error occurs.",
          "properties": {
              "date": {"type": "string", "description": "Current date in the format 'YYYY-MM-DD'."},
              "time": {"type": "string", "description": "Current time in the format 'HH:MM:SS'."},
              "day_or_night": {"type": "string", "description": "Indicates whether it is day or night."},
              "coordinates": {
                  "type": "object",
                  "properties": {
                      "latitude": {"type": "number", "description": "Latitude of the location (rounded to 4 decimal places)."},
                      "longitude": {"type": "number", "description": "Longitude of the location (rounded to 4 decimal places)."}
                  },
                  "description": "Geographical coordinates of the location."
              },
              "elevation": {
                  "type": "object",
                  "properties": {
                      "value": {"type": "number", "description": "Elevation value (rounded to 4 decimal places)."},
                      "unit": {"type": "string", "description": "Unit of elevation (e.g., 'meters')."}
                  },
                  "description": "Elevation data."
              },
              "temperature_2m": {
                  "type": "object",
                  "properties": {
                      "value": {"type": "string", "description": "Current temperature at 2 meters above ground."},
                      "unit": {"type": "string", "description": "Temperature unit (e.g., '°C')."}
                  },
                  "description": "Temperature data."
              },
              "relative_humidity_2m": {
                  "type": "object",
                  "properties": {
                      "value": {"type": "string", "description": "Current relative humidity at 2 meters above ground."},
                      "unit": {"type": "string", "description": "Relative humidity unit (e.g., '%')."}
                  },
                  "description": "Relative humidity data."
              },
              "precipitation": {
                  "type": "object",
                  "properties": {
                      "value": {"type": "string", "description": "Current precipitation."},
                      "unit": {"type": "string", "description": "Precipitation unit (e.g., 'mm')."}
                  },
                  "description": "Precipitation data."
              },
              "rain": {
                  "type": "object",
                  "properties": {
                      "value": {"type": "string", "description": "Current rain."},
                      "unit": {"type": "string", "description": "Rain unit (e.g., 'mm')."}
                  },
                  "description": "Rain data."
              },
              "showers": {
                  "type": "object",
                  "properties": {
                      "value": {"type": "string", "description": "Current showers."},
                      "unit": {"type": "string", "description": "Showers unit (e.g., 'mm')."}
                  },
                  "description": "Showers data."
              },
              "snowfall": {
                  "type": "object",
                  "properties": {
                      "value": {"type": "string", "description": "Current snowfall."},
                      "unit": {"type": "string", "description": "Snowfall unit (e.g., 'mm')."}
                  },
                  "description": "Snowfall data."
              },
              "weather_code": {"type": "string", "description": "Current weather code."},
              "weather_description": {"type": "string", "description": "Description of the current weather."},
              "cloud_cover": {
                  "type": "object",
                  "properties": {
                      "value": {"type": "string", "description": "Current cloud cover."},
                      "unit": {"type": "string", "description": "Cloud cover unit (e.g., '%')."}
                  },
                  "description": "Cloud cover data."
              },
              "surface_pressure": {
                  "type": "object",
                  "properties": {
                      "value": {"type": "string", "description": "Current surface pressure."},
                      "unit": {"type": "string", "description": "Surface pressure unit (e.g., 'hPa')."}
                  },
                  "description": "Surface pressure data."
              },
              "wind_speed_10m": {
                  "type": "object",
                  "properties": {
                      "value": {"type": "string", "description": "Current wind speed at 10 meters above ground."},
                      "unit": {"type": "string", "description": "Wind speed unit (e.g., 'm/s')."}
                  },
                  "description": "Wind speed data."
              },
              "wind_direction_10m": {
                  "type": "object",
                  "properties": {
                      "value": {"type": "string", "description": "Current wind direction at 10 meters above ground."},
                      "unit": {"type": "string", "description": "Wind direction unit (e.g., 'degrees')."}
                  },
                  "description": "Wind direction data."
              },
              "wind_gusts_10m": {
                  "type": "object",
                  "properties": {
                      "value": {"type": "string", "description": "Current wind gusts at 10 meters above ground."},
                      "unit": {"type": "string", "description": "Wind gusts unit (e.g., 'm/s')."}
                  },
                  "description": "Wind gusts data."
              }
          }
      },
      "note": {
          "type": "string",
      }
  }
},
{
  "type": "function",
  "function": {
      "name": "get_today_weather_data",
      "description": "Retrieves daily weather data for a specific location and target date.",
      "parameters": {
          "type": "object",
          "properties": {
 
              "latitude": {"type": "string",
                           "format": "float",
                           "description": "Latitude of the location."},
              "longitude": {"type": "string",
                            "format": "float",
                            "description": "Longitude of the location."},
              "target_date": {
                  "type": "string",
                  "description": "Target date in the format 'YYYY-MM-DD'."
              }
          },
"required": [ "latitude", "longitude", "target_date"]
      },
      "return": {
          "type": "object",
          "description": "JSON-formatted dictionary containing daily weather data for the target date. Returns None if data is not available or an error occurs.",
          "properties": {
              "Weather data for the target date": {
                  "type": "string",
                  "description": "Formatted date of the weather data."
              },
              "Weather Code": {
                  "type": "string",
                  "description": "Description of the weather code."
              },
              "Max Temperature": {
                  "type": "string",
                  "description": "Mean daily maximum temperature in degrees Celsius."
              },
              "Min Temperature": {
                  "type": "string",
                  "description": "Mean daily minimum temperature in degrees Celsius."
              },
              "Daylight Duration": {
                  "type": "string",
                  "description": "Duration of daylight in hours."
              },
              "Sunshine Duration": {
                  "type": "string",
                  "description": "Duration of sunshine in hours."
              },
              "UV Index Max": {
                  "type": "string",
                  "description": "Maximum UV index."
              },
              "UV Index Clear Sky Max": {
                  "type": "string",
                  "description": "Maximum UV index under clear sky."
              },
              "Precipitation Sum": {
                  "type": "string",
                  "description": "Sum of daily precipitation in millimeters."
              },
              "Rain Sum": {
                  "type": "string",
                  "description": "Sum of daily rain in millimeters."
              },
              "Showers Sum": {
                  "type": "string",
                  "description": "Sum of daily showers in millimeters."
              },
              "Snowfall Sum": {
                  "type": "string",
                  "description": "Sum of daily snowfall in millimeters."
              },
              "Precipitation Hours": {
                  "type": "string",
                  "description": "Duration of precipitation in hours."
              },
              "Precipitation Probability Max": {
                  "type": "string",
                  "description": "Maximum precipitation probability."
              },
              "Wind Speed 10m Max": {
                  "type": "string",
                  "description": "Maximum wind speed at 10 meters above ground."
              },
              "Wind Gusts 10m Max": {
                  "type": "string",
                  "description": "Maximum wind gusts at 10 meters above ground."
              },
              "Wind Direction 10m Dominant": {
                  "type": "string",
                  "description": "Dominant wind direction at 10 meters above ground."
              },
              "Shortwave Radiation Sum": {
                  "type": "string",
                  "description": "Sum of shortwave radiation in J/m^2."
              },
              "ET0 FAO Evapotranspiration": {
                  "type": "string",
                  "description": "Evapotranspiration according to FAO in millimeters."
              }
          }
      },
      "note": {
          "type": "string",
          "content": "Uses the Open-Meteo weather API: https://api.open-meteo.com/v1/forecast."
      }
  }
}
]















