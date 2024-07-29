import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load and process the data
original_df = pd.read_csv('./sensor.csv')
df = original_df.copy()

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Convert machine_status column to category
df['machine_status'] = df['machine_status'].astype('category')

# Set timestamp as the index
df.set_index('timestamp', inplace=True)

# Select specific columns
df_1 = df[['sensor_06', 'sensor_10', 'machine_status']]

# Resample data
df_1_resampled = df_1.resample('D').mean()

# Filter data where machine_status is 'BROKEN'
broken_df = df_1[df_1['machine_status'] == 'BROKEN']

# Create the plot
fig = go.Figure()

# Add resampled line plot
fig.add_trace(go.Scatter(x=df_1_resampled.index, y=df_1_resampled['sensor_06'], mode='lines+markers', name='Daily Mean of Sensor 06'))

# Add original data line plot
fig.add_trace(go.Scatter(x=df_1.index, y=df_1['sensor_06'], mode='lines', line=dict(width=0.2), name='Sensor 06'))

# Add 'BROKEN' status points with annotations
fig.add_trace(go.Scatter(
    x=broken_df.index, 
    y=broken_df['sensor_06'], 
    mode='markers+text', 
    marker=dict(color='red', size=20, symbol='cross'),
    text=[f'{i+1}' for i in range(len(broken_df))],  # Number the points
    textposition='top center',
    name='BROKEN Status'
))

# Customize layout
fig.update_layout(
    title='Sensor 06 Data Visualization',
    xaxis_title='Timestamp',
    yaxis_title='Sensor 06 Values',
    plot_bgcolor='white',  # Set plot background color to white
    paper_bgcolor='white', # Set paper background color to white
    font=dict(color='black'), # Set font color to black
    xaxis=dict(showgrid=True, gridcolor='lightgray'), # Show grid lines in light gray
    yaxis=dict(showgrid=True, gridcolor='lightgray'), # Show grid lines in light gray
    template='plotly'
)

# Show the plot
fig.show()
