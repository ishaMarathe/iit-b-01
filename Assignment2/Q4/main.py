import requests
api_key =  "af9b93c6222e0dc3658ba32186c1c93c"
city = input("Enter city: ")
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(url)
print("status:", response.status_code)
weather = response.json()
print("Temperature: ", weather["main"]["temp"])
print("Humidity: ", weather["main"]["humidity"])
print("Sunrise: ",weather["sys"]["sunrise"])
print("Sunset: ",weather["sys"]["sunset"])
