#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 13:12:38 2024

@author: yoojinoh
"""

#Avergaing ERP from Cz for participant 004

import mne
import os

os.chdir("/Users/yoojinoh/Desktop/SPHSC525/SS04")


file_path = "/Users/yoojinoh/Desktop/SPHSC525/SS04/SS04-KT-04082016-cnt.cnt"


# Step 1: Load the .cnt file
raw = mne.io.read_raw_cnt(file_path, preload=True)


# Step 3: Convert annotations to events
events, event_dict = mne.events_from_annotations(raw)

# Step 4: Epoching for each event type
event_id = {'Event1': 1, 'Event2': 2}  # Define your event IDs
tmin, tmax = -0.2, 0.8  # Define time window around each event
for event_label, event_code in event_id.items():
    epochs = mne.Epochs(raw, events, event_code, tmin, tmax, baseline=None, preload=True)
    
    # Step 5: Select channel Cz
    cz_epochs = epochs.copy().pick_channels(['Cz'])

    # Step 6: Average epochs
    erp_cz = cz_epochs.average()

    # Plot the ERP for each event type
    fig = erp_cz.plot()
    fig.suptitle(f'ERP for {event_label}')

    # Add event ID label to the plot
    fig.text(0.5, 0.95, f'Event ID: {event_code}', ha='center', fontsize=12, fontweight='bold')


del(raw)


import mne
import matplotlib.pyplot as plt

# Load data
file_path = '/Users/yoojinoh/Desktop/SPHSC525/SS04/SS04-KT-04082016-cnt.cnt'
file_path2 = '/Users/yoojinoh/Desktop/SPHSC525/SS01/SS01-SR-02082016-cnt.cnt'
file_path3 = '/Users/yoojinoh/Desktop/SPHSC525/SS02/SS02-LV-03082016-cnt.cnt'


raw_participant1 = mne.io.read_raw_cnt(file_path, preload=True)
raw_participant2 = mne.io.read_raw_cnt(file_path2, preload=True)
raw_participant3 = mne.io.read_raw_cnt(file_path3, preload=True)
# Convert annotations to events
events_participant1, _ = mne.events_from_annotations(raw_participant1)
events_participant2, _ = mne.events_from_annotations(raw_participant2)
events_participant3, _ = mne.events_from_annotations(raw_participant3)

# Define event IDs and event codes for the events of interest
event_id1 = {'203': 1, '207': 2}  # Replace with your event IDs and codes
event_id2 = {'203': 1, '207': 2}  # Replace with your event IDs and codes
event_id3 = {'203': 1, '207': 2}  # Replace with your event IDs and codes

# Define epochs parameters
tmin = -0.2  # Start time of the epoch relative to event onset (in seconds)
tmax = 0.5   # End time of the epoch relative to event onset (in seconds)

# Extract epochs for participant 1
epochs_participant1 = mne.Epochs(raw_participant1, events=events_participant1, event_id=event_id1, tmin=tmin, tmax=tmax)

# Extract epochs for participant 2
epochs_participant2 = mne.Epochs(raw_participant2, events=events_participant2, event_id=event_id2, tmin=tmin, tmax=tmax)

epochs_participant3 = mne.Epochs(raw_participant3, events=events_participant3, event_id=event_id2, tmin=tmin, tmax=tmax)

# Compute average ERPs for both participants
avg_erp_participant1 = epochs_participant1.average()
avg_erp_participant2 = epochs_participant2.average()
avg_erp_participant3 = epochs_participant3.average()

# Plot the ERPs for Event 207
plt.figure(figsize=(10, 6))
plt.plot(avg_erp_participant1.times, avg_erp_participant1.data[event_id1['207']], label='Participant 1', color='blue')
plt.plot(avg_erp_participant2.times, avg_erp_participant2.data[event_id1['207']], label='Participant 2', color='orange')
plt.plot(avg_erp_participant3.times, avg_erp_participant3.data[event_id1['207']], label='Participant 3', color='pink')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (uV)')
plt.title('Average ERPs - Event 207')
plt.legend()
plt.grid(True)
plt.show()

# Plot the ERPs for Event 203
plt.figure(figsize=(10, 6))
plt.plot(avg_erp_participant1.times, avg_erp_participant1.data[event_id2['203']], label='Participant 1', color='green')
plt.plot(avg_erp_participant2.times, avg_erp_participant2.data[event_id2['203']], label='Participant 2', color='red')
plt.plot(avg_erp_participant3.times, avg_erp_participant3.data[event_id2['203']], label='Participant 2', color='yellow')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (uV)')
plt.title('Average ERPs - Event 203')
plt.legend()
plt.grid(True)
plt.show()
