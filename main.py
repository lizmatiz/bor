import time  # to simulate a real time data, time loop
import pandas as pd  # read csv, df manipulation
import streamlit as st  # 🎈 data web app development
import serial

st.set_page_config(
    page_title="Chub Dashboard!",
    page_icon=":rocket:",
    layout="wide",
)

sensor_serial = serial.Serial('/dev/tty.usbserial-1140', 9600)

df = None
    

# dashboard title
st.title("Chub Dashboard! :rocket: :stars:")

# creating a single-element container
placeholder = st.empty()

# near real-time / live feed simulation
while True:
    if sensor_serial.in_waiting != 0:
        sensor_data = sensor_serial.readline().decode().strip()
        #st.text(sensor_data)

        if len(sensor_data) >= 2 and sensor_data[0] == '@':
            sensor_data = sensor_data[1:]
            split_sensor_data = sensor_data.split(',')

            try:
                accel_x = float(split_sensor_data[0])
                accel_y = float(split_sensor_data[1])
                accel_z = float(split_sensor_data[2])
                air_temp = float(split_sensor_data[3])
                altitude = float(split_sensor_data[4])
            except:
                pass
            

            data = {
                'timestamp': pd.Timestamp.now(),
                'accel_x': accel_x,
                'accel_y': accel_y,
                'accel_z': accel_z,
                'air_temp': air_temp,
                'altitude': altitude
            }
            
            if df is None:
                df = pd.DataFrame([data], index = [0])
            else:
                df.loc[len(df)] = data

            with placeholder.container():

                # create three columns
                kpi1, kpi2, kpi3 = st.columns(3)

                # fill in those three columns with respective metrics or KPIs
                kpi1.metric(
                    label="X Acceleration",
                    value= data['accel_x'],
                    #delta=round(avg_age) - 10,
                )
                
                kpi2.metric(
                    label="Y Acceleration",
                    value= data['accel_y'],
                    #delta=-10 + count_married,
                )
                
                kpi3.metric(
                    label="Z Acceleration",
                    value=data['accel_z'],
                    #delta=-round(balance / count_married) * 100,
                )
                
                
                # create three columns for charts
                fig_col1, fig_col2, fig_col3 = st.columns(3)
                with fig_col1:
                    st.markdown("Acceleration")
                    st.line_chart(
                        df, x="timestamp", y=["accel_x", "accel_y", "accel_z"], color=["#FF0000", "#0000FF", "#2596BE"]
                    )
                with fig_col2:
                    st.markdown("Air Temperature (C)")
                    st.line_chart(
                        df, x="timestamp", y=["air_temp"], color=["#FF0000"]
                    )
                with fig_col3:
                    st.markdown("Altitude ")
                    st.line_chart(
                        df, x="timestamp", y=["altitude"], color=["#2596BE"]
                    )

                st.dataframe(df)
                
                time.sleep(1)
