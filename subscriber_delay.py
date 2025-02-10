#!/usr/bin/env python3

import pandas as pd
import math
import rospy
import datetime
from etsi_its_msgs.msg import CPM
from ublox_msgs.msg import NavPVT
from sensor_msgs.msg import NavSatFix
import os

# Initiallize variables
last_vehicle_latitude = None
last_vehicle_longitude = None
csv_file_name = None

def convert_to_decimal_degrees(value):
    # The format is DDDMMMMMMMM (degrees and millionths of a degree)
    degrees = value / 10000000
    return degrees 

def haversine(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance between two points on the Earth
    R = 6371000  # Earth radius in meters
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def cpm_received_callback(msg):
    global last_vehicle_latitude, last_vehicle_longitude, v2x_delays, e2e_delays, distances
    
    # Extract relevant information from cpm_received topic
    t4 = ((msg.header.stamp.secs * 1000 + msg.header.stamp.nsecs // 1e6) - 1072915200000) % 65536  # Using t4 mod 65536 , Date offset 1072915200000
    t2 = msg.generation_delta_time
    mast_latitude = convert_to_decimal_degrees(msg.reference_position.latitude)
    mast_longitude = convert_to_decimal_degrees(msg.reference_position.longitude)
    
    # Extract time of measurement
    time_of_measurement = msg.listOfPerceivedObjects.perceivedObjectContainer[0].timeOfMeasurement

    # Calculate v2x_delay 
    v2x_delay = t4 - t2
    # Calculate e2e_delay for each object
    e2e_delay = t4 - t2 + time_of_measurement

    # Convert 9-digit latitude and longitude values to decimal degrees
    last_vehicle_latitude_decimal = convert_to_decimal_degrees(last_vehicle_latitude)
    last_vehicle_longitude_decimal = convert_to_decimal_degrees(last_vehicle_longitude)
    
    # Calculate distance between mast and vehicle 
    distance = haversine(mast_latitude, mast_longitude, last_vehicle_latitude_decimal, last_vehicle_longitude_decimal)
    
    # Save the latest data to CSV file
    save_latest_to_csv(v2x_delay, e2e_delay,distance, csv_file_name)

def navpvt_callback(msg):
    global last_vehicle_latitude, last_vehicle_longitude
    # Extract relevant information from gnss/navpvt topic
    last_vehicle_latitude = msg.lat
    last_vehicle_longitude = msg.lon

def save_latest_to_csv(v2x_delay,e2e_delay,distance,csv_file_name):
    # Create a DataFrame with the latest data point
    data = {'v2x_delay': [v2x_delay], 'e2e_delay': [e2e_delay], 'distance': [distance]}
    df = pd.DataFrame(data)

    # If the CSV file doesn't exist, create it with header
    if not os.path.isfile(csv_file_name):
        df.to_csv(csv_file_name, index=False)
    else:
        df.to_csv(csv_file_name, mode='a', header=False, index=False)
    
if __name__ == '__main__':
    rospy.init_node('your_node_name')  # Initialize the ROS node
    last_vehicle_latitude = None
    last_vehicle_longitude = None

    # Get the current date and time to create a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")[2:]
    csv_file_name = f'delay_vs_distance_{timestamp}.csv'

    # Subscribe to ROS topics
    rospy.Subscriber('/cpm_received', CPM, cpm_received_callback)
    rospy.Subscriber('/gnss/navpvt', NavPVT, navpvt_callback)

    rospy.spin()  # Keep the node running
