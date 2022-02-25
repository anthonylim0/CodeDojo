import numpy as np
import pandas as pd

from sklearn import cluster
import scipy.cluster

import requests
import json
import random
from math import radians, cos, sin, asin, sqrt

user_filePath = {Your File Path}
csv = {Your CSV File}
data = pd.read_csv(user_filePath + csv)

#This route list is used for demonstration purposes
route_list = [1481067, 1481077, 1481103]

#Under actual usage, we would like to use this
#route_list = data['route_id'].unique()

#For demonstration purposes, we randomize the route ID we use.
zone = random.choice(route_list)

filter_data = data[data["route_id"]==zone]
x, y = "latitude", "longitude"
color = "zone_id"
data = filter_data.copy()
X = filter_data[["latitude","longitude"]]
max_k = 10
distortions = [] 
for i in range(1, max_k+1):
    if len(X) >= i:
       model = cluster.KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
       model.fit(X)
       distortions.append(model.inertia_)

## best k: the lowest derivative
k = [i*100 for i in np.diff(distortions,2)].index(min([i*100 for i in np.diff(distortions,2)]))
model = cluster.KMeans(n_clusters=k, init='k-means++')
X = filter_data[["latitude","longitude"]]

## clustering
dtf_X = X.copy()
dtf_X["cluster"] = model.fit_predict(X)

## find real centroids
closest, distances = scipy.cluster.vq.vq(model.cluster_centers_, 
                     dtf_X.drop("cluster", axis=1).values)
dtf_X["centroids"] = 0
for i in closest:
    dtf_X["centroids"].iloc[i] = 1

## add clustering info to the original dataset
filter_data[["cluster","centroids"]] = dtf_X[["cluster","centroids"]]
th_centroids = model.cluster_centers_
centroids = []
for i in range(k):
    centroids.append((th_centroids[i][0], th_centroids[i][1]))

# LTA API
url = "http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2"

payload={}
headers = {
  'AccountKey': {Your API Key}
}

response = requests.request("GET", url, headers=headers, data=payload)

text = response.text
y = json.loads(text)

carparks = []
for i in range(len(y['value'])):
    x = y['value'][i]["Location"].split()
    carparks.append([float(x[0]), float(x[1])])

def distance(lat1, lat2, lon1, lon2):
	
	# The math module contains a function named
	# radians which converts from degrees to radians.
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	
	# Haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

	c = 2 * asin(sqrt(a))
	
	# Radius of earth in kilometers. Use 3956 for miles
	r = 6371
	
	# calculate the result
	return(c * r)
	
	
ls = []
c2c = {}
# driver code
for i in centroids:
    minim = 10000
    for j in carparks:
        d = distance(i[0], j[0], i[1], j[1])
        if d < minim:
            minim = d
            opt_carpark = j
    if opt_carpark not in ls:
        ls.append(opt_carpark)
    c2c[centroids.index(i)] = ls.index(opt_carpark)

filter_data["carparks"] = filter_data["cluster"].map(c2c)
filter_data = filter_data.drop(filter_data.columns[[0,1,2,3,4,8]], axis=1)
filter_data = filter_data.to_numpy()
filter_data = filter_data.tolist()

def output_stun():
    return ls

def output_seed():
    return filter_data