
import pandas as pd
import requests
import urllib.parse as urlparse
import datetime


# In[5]:


start = "7.6856578,81.7231435"               # kky
end = "7.6564174,81.7235608"                # armpy
key = "Your tom tom API key"             # API Key
 
# Base URL
base_url = "https://api.tomtom.com/routing/1/calculateRoute/"


# In[6]:


today = datetime.date.today()
departure_time_start = datetime.datetime(today.year, today.month, today.day-1, 0, 0, 0)
 
hour_range = range(0,24)
 
for i in hour_range:
    # Update an hour
    departure_time = departure_time_start.replace(hour=departure_time_start.hour + i)
    
    # Format datetime string
    departure_time = departure_time.strftime('%Y-%m-%dT%H:%M:%S')   
 
    # Create request URL
    request_params = (
        urlparse.quote(start) + ":" + urlparse.quote(end) 
        + "/json?departAt=" + urlparse.quote(departure_time))
 
    request_url = base_url + request_params + "&key=" + key
 
    # Get data
    response = requests.get(request_url)
 
    # Convert to JSON
    json_result = response.json()
    
    # Get summary
    route_summary = json_result['routes'][0]['summary']
    
    # Convert to data frame and append
    if(i == 0):
        df = pd.json_normalize(route_summary)
    else:
        df = df.append(pd.json_normalize(route_summary), ignore_index=True)    
        
    print(f"Retrieving data: {i+1} / {len(hour_range)}")


# In[15]:


import matplotlib.pyplot as plt
 
plt.plot(df['travelTimeInSeconds']/3600)
plt.title('Travel time against departure hour')
plt.xlabel('Departure hour')
plt.ylabel('Travel time [h]')


# In[21]:


plt.plot(df['lengthInMeters']/1000)
plt.title('Travel distance [km] against departure hour')
plt.xlabel('Departure hour')
plt.ylabel('Travel distance [km]')


# In[17]:


plt.scatter(df['lengthInMeters']/1000, df['travelTimeInSeconds']/3600)
plt.title('Travel time [h] against travel distance [km]')
plt.xlabel('Travel time [h]')
plt.ylabel('Distance [km]')


# In[22]:


import seaborn as sns
sns.set_theme(style="ticks")
sns.pairplot(df)


# In[ ]:




