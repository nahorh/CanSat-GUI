from time import sleep
from tkinter import *
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import serial
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from PIL import ImageTk
from scipy.ndimage import gaussian_filter1d

from window_utilities import window_utils


class PLOT_SCREEN:
    def __init__(self, SCREEN,serial_device):
        self.ser = serial_device
        self.start_plotting = False
        self.temperature_c = self.temperature_f = self.humidity = self.heat_index_c = self.heat_index_f = self.uv_index = self.uv_sensor_voltage = np.array([
        ])

        def update_plot():
            try:
                data = self.ser.readline()
                data = data.decode()
                data = data.strip('\r\n')
                data = data.split(',')
                for i in range(len(data)):
                    data[i] = float(data[i])
                self.humidity = np.append(self.humidity, data[0])
                self.temperature_c = np.append(
                    self.temperature_c, data[1])
                self.temperature_f = np.append(
                    self.temperature_f, data[2])
                self.heat_index_c = np.append(
                    self.heat_index_c, data[3])
                self.heat_index_f = np.append(
                    self.heat_index_f, data[4])
                self.uv_index = np.append(self.uv_index, data[5])
                self.uv_sensor_voltage = np.append(
                    self.uv_sensor_voltage, data[6])


                lines1.set_xdata(np.linspace(
                    0, len(self.humidity), len(self.humidity)))
                lines1.set_ydata(gaussian_filter1d(self.humidity, sigma=2))

                lines2.set_xdata(np.linspace(
                    0, len(self.temperature_c), len(self.temperature_c)))
                lines2.set_ydata(gaussian_filter1d(
                    self.temperature_c, sigma=2))

                lines3.set_xdata(np.linspace(
                    0, len(self.temperature_f), len(self.temperature_f)))
                lines3.set_ydata(gaussian_filter1d(
                    self.temperature_f, sigma=2))

                lines4.set_xdata(np.linspace(
                    0, len(self.heat_index_c), len(self.heat_index_c)))
                lines4.set_ydata(gaussian_filter1d(self.heat_index_c, sigma=2))

                lines5.set_xdata(np.linspace(
                    0, len(self.heat_index_f), len(self.heat_index_f)))
                lines5.set_ydata(gaussian_filter1d(self.heat_index_f, sigma=2))

                lines6.set_xdata(np.linspace(
                    0, len(self.uv_index), len(self.uv_index)))
                lines6.set_ydata(gaussian_filter1d(self.uv_index, sigma=2))

                lines7.set_xdata(np.linspace(
                    0, len(self.uv_sensor_voltage), len(self.uv_sensor_voltage)))
                lines7.set_ydata(gaussian_filter1d(
                    self.uv_sensor_voltage, sigma=2))

                update_plots_axes()
                canvas1.draw()
                pass
            except Exception as e:
                #print('error updating plot')
                #print(e)
                pass
            self.real_time_plot_monitor=SCREEN.after(1000, update_plot)

        
        def start_plotting():
            self.real_time_plot_monitor= SCREEN.after(1000, update_plot)
            start_plotting_btn['state'] = 'disabled'
            stop_plotting_btn['state'] = 'normal'
            pass
        
        def stop_plotting():
            SCREEN.after_cancel(self.real_time_plot_monitor)
            start_plotting_btn['state'] = 'normal'
            stop_plotting_btn['state'] = 'disabled'
            pass
        START_STOP_BTN_FRAME = window_utils.create_frame(SCREEN)
        start_plotting_btn = Button(
            START_STOP_BTN_FRAME, text='START PLOTTING', borderwidth=1, command=start_plotting,bg='orange',fg='white')
        start_plotting_btn.pack(side=LEFT, anchor=CENTER, padx=10)
        stop_plotting_btn = Button(START_STOP_BTN_FRAME, text='PAUSE PLOTTING',command=stop_plotting,bg='orange',fg='white',borderwidth=1)
        stop_plotting_btn.pack(side=RIGHT, anchor=CENTER, padx=10)

        def update_plots_axes():
            xlim_start = 0
            if len(self.humidity) > 60:
                xlim_start = len(self.humidity)-60
            xlim_end = len(self.humidity)
            fig1.set_xlim(xlim_start, xlim_end)
            fig1.set_ylim(self.humidity.min()-5, self.humidity.max()+5)

            xlim_start = 0
            if len(self.temperature_c) > 60:
                xlim_start = len(self.temperature_c)-60
            xlim_end = len(self.temperature_c)
            fig2.set_xlim(xlim_start, xlim_end)
            fig2.set_ylim(self.temperature_c.min()-5,
                          self.temperature_c.max()+5)

            xlim_start = 0
            if len(self.temperature_f) > 60:
                xlim_start = len(self.temperature_f)-60
            xlim_end = len(self.temperature_f)
            fig3.set_xlim(xlim_start, xlim_end)
            fig3.set_ylim(self.temperature_f.min()-5,
                          self.temperature_f.max()+5)

            xlim_start = 0
            if len(self.heat_index_c) > 60:
                xlim_start = len(self.heat_index_c)-60
            xlim_end = len(self.heat_index_c)
            fig4.set_xlim(xlim_start, xlim_end)
            fig4.set_ylim(self.heat_index_c.min()-5, self.heat_index_c.max()+5)

            xlim_start = 0
            if len(self.heat_index_f) > 60:
                xlim_start = len(self.heat_index_f)-60
            xlim_end = len(self.heat_index_f)
            fig5.set_xlim(xlim_start, xlim_end)
            fig5.set_ylim(self.heat_index_f.min()-5, self.heat_index_f.max()+5)

            xlim_start = 0
            if len(self.uv_index) > 60:
                xlim_start = len(self.uv_index)-60
            xlim_end = len(self.uv_index)
            fig6.set_xlim(xlim_start, xlim_end)
            fig6.set_ylim(self.uv_index.min()-5, self.uv_index.max()+5)

            xlim_start = 0
            if len(self.uv_sensor_voltage) > 60:
                xlim_start = len(self.uv_sensor_voltage)-60
            xlim_end = len(self.uv_sensor_voltage)
            fig7.set_xlim(xlim_start, xlim_end)
            fig7.set_ylim(self.uv_sensor_voltage.min()-5,
                          self.uv_sensor_voltage.max()+5)
            pass
        figure = plt.figure(figsize=(20,8))
        # humidity
        fig1 = figure.add_subplot(335)
        fig1.set_xlabel('Time (s)', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        fig1.set_ylabel('Humidity (%)', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        lines1 = fig1.plot([], [])[0]

        # temperature_c
        fig2 = figure.add_subplot(331)
        fig2.set_xlabel('Time (s)', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        fig2.set_ylabel('Temperature (°C)', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        lines2 = fig2.plot([], [])[0]

        # temperature_f
        fig3 = figure.add_subplot(334)
        fig3.set_xlabel('Time (s)', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        fig3.set_ylabel('Temperature (°F)', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        lines3 = fig3.plot([], [])[0]

        # heat_index_c
        fig4 = figure.add_subplot(333)
        fig4.set_xlabel('Time (s)', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        fig4.set_ylabel('Heat Index (°C)', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        lines4 = fig4.plot([], [])[0]

        # heat_index_f
        fig5 = figure.add_subplot(336)
        fig5.set_xlabel('Time (s)', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        fig5.set_ylabel('Heat Index (°F)', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        lines5 = fig5.plot([], [])[0]

        # uv index
        fig6 = figure.add_subplot(337)
        fig6.set_xlabel('Time (s)', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        fig6.set_ylabel('UV Index', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        lines6 = fig6.plot([], [])[0]

        fig7 = figure.add_subplot(339)
        fig7.set_xlabel('Time (s)', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        fig7.set_ylabel('UV Sensor Voltage', fontsize=int(
            SCREEN.winfo_screenheight()/80))
        lines7 = fig7.plot([], [])[0]

        figure.tight_layout()

        canvas1 = FigureCanvasTkAgg(figure, master=SCREEN)
        canvas1.get_tk_widget().pack(anchor=CENTER, side=TOP)
        canvas1.draw()
        toolbar = NavigationToolbar2Tk(canvas1, SCREEN)
        toolbar.config(bg='')
        toolbar.update()

'''
BY DEFAULT THE WINDOW SHOULD ALL THE GRAPHS IN PLACE AS EMPTY

AFTER SUCCESSFUL CONNECTION WITH MCU IT SHOULD GET THE DATA AND UPDATE ACCORDINGLY

DECLARE THE PLOT OBJS SEPERATELY FOR EACH PLOT AND USE THEIR LINE PROPERTY FOR EFFICIENCY

KEEPING THE GRAPHS AND WINDOW STATIC AND CHANGING ONLY THE PLOT LINE AND THE GRAPH LIMITS IS THE WORK TO BE DONE.

THE GRAPH SHOULD BE SCROLLABLE WHENEVER PAUSED

'''
