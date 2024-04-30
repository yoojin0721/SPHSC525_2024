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
event_id1 = {'203': 1}
event_id2 = {'207': 2}  # Replace with your event IDs and codes

# Define epochs parameters
tmin = -0.2  # Start time of the epoch relative to event onset (in seconds)
tmax = 1.0   # End time of the epoch relative to event onset (in seconds)

# Extract epochs for participant 1
epochs_participant1 = mne.Epochs(raw_participant1, events=events_participant1, event_id=event_id1, tmin=tmin, tmax=tmax)
epochs_participant1_2 = mne.Epochs(raw_participant1, events=events_participant1, event_id=event_id2, tmin=tmin, tmax=tmax)

# Extract epochs for participant 2
epochs_participant2 = mne.Epochs(raw_participant2, events=events_participant2, event_id=event_id1, tmin=tmin, tmax=tmax)
epochs_participant2_2 = mne.Epochs(raw_participant2, events=events_participant2, event_id=event_id2, tmin=tmin, tmax=tmax)

epochs_participant3 = mne.Epochs(raw_participant3, events=events_participant3, event_id=event_id1, tmin=tmin, tmax=tmax)
epochs_participant3_2 = mne.Epochs(raw_participant3, events=events_participant3, event_id=event_id2, tmin=tmin, tmax=tmax)

# Compute average ERPs for all participants, event 1 ('203')
avg_erp_participant1_event1 = epochs_participant1.average()
avg_erp_participant2_event1 = epochs_participant2.average()
avg_erp_participant3_event1 = epochs_participant3.average()

# Compute average ERPs for all participants, event 2 ('207')
avg_erp_participant1_event2 = epochs_participant1_2.average()
avg_erp_participant2_event2 = epochs_participant2_2.average()
avg_erp_participant3_event2 = epochs_participant3_2.average()



#set y-axis min max
max_val_203 = 8
max_val_207 = 8
min_val_203 = -6
min_val_207 = -6

grand_avg_erp_event1 = mne.grand_average([avg_erp_participant1_event1, avg_erp_participant2_event1, avg_erp_participant3_event1])
grand_avg_erp_event2 = mne.grand_average([avg_erp_participant1_event2, avg_erp_participant2_event2, avg_erp_participant3_event2])

# Plot the grand average ERP for event type '203'
plt.figure(figsize=(10, 6))
plt.plot(grand_avg_erp_event1.times, grand_avg_erp_event1.data[0], label='Grand Average', color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (uV)')
plt.title('Grand Average ERPs - Event 203')
plt.legend()
plt.grid(True)
plt.show()

# Plot the grand average ERP for event type '207'
plt.figure(figsize=(10, 6))
plt.plot(grand_avg_erp_event2.times, grand_avg_erp_event2.data[0], label='Grand Average', color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (uV)')
plt.title('Grand Average ERPs - Event 207')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(grand_avg_erp_event1.times, grand_avg_erp_event1.data[0], label='Event 203', color='blue')
plt.plot(grand_avg_erp_event2.times, grand_avg_erp_event2.data[0], label='Event 207', color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (uV)')
plt.title('Grand Average ERPs')
plt.legend()
plt.grid(True)
plt.show()
