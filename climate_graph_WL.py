#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 18:58:21 2020

@author: armin
Copyright (C) 2020  Armin Niessner
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
# =============================================================================
# climate diagram after Walter & Lieth (1960)
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def graphWL(name, altitude, df, T_col, P_col, Tmin = None, Tmax = None, 
          Tdelta = None, absTmax = None, absTmin = None, center = "north", 
          coord = None, bar = False):
    
    year = []
    year.append(df.index[0].year)
    year.append(df.index[-1].year)
    ydelta = year[1] - year[0] + 1
    
    df_mean = df.resample("MS").mean()
    df_min = df.resample("MS").min()
    df_sum = df.resample("MS").sum()
    
    meanT_l = []
    sumP_l = []
    freeze = []
    p_freeze = []
    for month in np.arange(1,13):
        df_month_mean = df_mean[df_mean.index.month == month]
        df_month_min = df_min[df_min.index.month == month]
        df_month_sum = df_sum[df_mean.index.month == month]
        meanT_l.append(df_month_mean[T_col].mean())
        sumP_l.append(df_month_sum[P_col].mean())
        if bar == True:
            if df_month_mean[Tmin].mean() < 0:
                freeze.append(-2.4)
            else:
                freeze.append(0)
            if df_month_min[Tmin].min() < 0:
                p_freeze.append(-2.4)
            else:
                p_freeze.append(0)
                
    if Tdelta == True:
        Tdelta = df[Tmax] - df[Tmin]
        Tdelta = Tdelta.mean()
    elif type(Tdelta) is int or type(Tdelta) is float:
        Tdelta = Tdelta
    elif type(Tdelta) is str:
        Tdelta = df[Tdelta].mean()
    if type(Tmin) is str:
        Tmin = df[Tmin].mean()
    elif type(Tmin) is int or type(Tmin) is float:
        Tmin = Tmin
    if type(Tmax) is str:
        Tmax = df[Tmax].mean()
    elif type(Tmax) is int or type(Tmin) is float:
        Tmax = Tmax
    if type(absTmax) is str:
        absTmax = df[absTmax].max()
    elif type(absTmax) is int or type(absTmax) is float:
        absTmax = absTmax
    if type(absTmin) is str:
        absTmin = df[absTmin].min()
    elif type(absTmin) is int or type(absTmin) is float:
        absTmin = absTmin
    
                
        
    
    #x = np.arange(1,13)
    x = np.arange(0.5, 14.5)
    x_M = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
    for i in np.arange(0,len(x_M)):
        x_M[i] = "        " + x_M[i]
    
    if center == "south":
        x_M = x_M[6:12] + x_M[0:6]
        meanT_l = meanT_l[6:12] + meanT_l[0:6]
        sumP_l = sumP_l[6:12] + sumP_l[0:6]
        freeze = freeze[6:12] + freeze[0:6]
        p_freeze = p_freeze[6:12] + p_freeze[0:6]
    
    meanT_l.insert(0, meanT_l[-1])
    meanT_l.append(meanT_l[1])
    sumP_l.insert(0, sumP_l[-1])
    sumP_l.append(sumP_l[1])
    if freeze:
        freeze.insert(0, freeze[-1])
        freeze.append(freeze[1])
    if p_freeze:
        p_freeze.insert(0, p_freeze[-1])
        p_freeze.append(p_freeze[1])
        
    if freeze and p_freeze:
        for i in np.arange(len(freeze)):
            if freeze[i] != 0:
                p_freeze[i] = 0
        
    fig1 = plt.figure(figsize = (6, 7)) # width, height
    fig1.subplots_adjust(0.15,0.1,0.88,0.87,0,0)
    ax1 = plt.subplot2grid((6,1), (1,0), rowspan=5, colspan=1)
    ax2 = ax1.twinx()
    ax3 = plt.subplot2grid((6,1), (0,0), rowspan=1, colspan=1)
    ax4 = ax3.twinx()
    
    ax1.plot(x, meanT_l, c = "r")
    ax2.plot(x, sumP_l, c = "b")
    ax3.plot(x, meanT_l, c = "r")
    ax4.plot(x, sumP_l, c = "b")
    sumP_2 = [y/2 for y in sumP_l]
    
    x_interp = np.arange(0.5, 14.5, 0.1)
    meanT_interp = np.interp(x_interp, x, meanT_l)
    sumP_interp = np.interp(x_interp, x, sumP_2)
    zero_l = [0 for i in range(140)]
    meanT_fill = np.maximum(meanT_interp, zero_l)
        
    ax1.fill_between(x_interp, meanT_fill, sumP_interp, where = (np.asarray(meanT_fill) < np.asarray(sumP_interp)), 
                     edgecolor='blue', facecolor = "w", interpolate = True, hatch = "||")
    ax1.fill_between(x_interp, meanT_fill, sumP_interp, where = (np.asarray(meanT_fill) >= np.asarray(sumP_interp)), 
                     edgecolor='red', facecolor = "w", interpolate = True, hatch = "..")
    ax4.fill_between(x, sumP_l, 100, facecolor = "blue")
    if freeze:
        ax1.bar(x, freeze, 1, facecolor = "k", ec = "k")
    if p_freeze:
        ax1.bar(x, p_freeze, 1, facecolor = "w", hatch = "//")

    ax1.set_ylim(-30,50)
    ax1.set_xticks(np.arange(1, 13))
    ax1.set_xticklabels(x_M)
    ax1.set_xlim(1,13)
    ax2.set_ylim(-60,100)
    ax3.set_ylim(50,60)
    ax3.set_yticks([])
    ax3.set_xlim(1,13)
    ax4.set_ylim(100,350)
    ax4.set_yticks([300])
    
    ax1.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_position('zero')
    ax1.tick_params(axis='x', which='major', pad=18, direction = "in", length = 10) 
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_position('zero')
    ax2.tick_params(labelbottom=False, bottom=False)
    ax3.tick_params(labelbottom=False, bottom=False)
    ax3.spines['top'].set_visible(False)
    ax4.spines['top'].set_visible(False)
    ax3.spines['bottom'].set_visible(False)
    ax4.spines['bottom'].set_visible(False)
    ax1.tick_params(labelsize = 12)
    ax2.tick_params(labelsize = 12)
    ax3.tick_params(labelsize = 12)
    ax4.tick_params(labelsize = 12)
    
    ax3.set_ylabel("[°C]", fontsize = 12, rotation = "horizontal", labelpad = 20)
    ax4.set_ylabel("[mm]", fontsize = 12, rotation = "horizontal", labelpad = 0.5)
    
    # mean annual temperature
    ax3.text(0.65, 1.15, "{} °C".format(np.round(np.mean(meanT_l),1)), fontsize = 12, ha='left', va='center', transform=ax3.transAxes)
    # annual temperature
    ax3.text(0.85, 1.15, "{} mm".format(int(np.sum(sumP_l))), fontsize = 12, ha='left', va='center', transform=ax3.transAxes)
    # name and altitude
    ax3.text(0.5, 1.6, "{} {} m asl".format(name, altitude), fontsize = 14, ha='center', va='center', transform=ax3.transAxes)
    if coord:
        ax3.text(0.5, 1.4, "{}".format(coord), fontsize = 12, ha='center', va='center', transform=ax3.transAxes)
    # timeframe
    if year:
        ax3.text(0.0, 1.1, "{}-{} [{}]".format(year[0], year[1], ydelta), fontsize = 12, ha='left', va='center', transform=ax3.transAxes)
    # absolut temperature maximum
    if absTmax != None:
        ax1.text(-0.1, 0.7, np.round(absTmax,1), fontsize = 12, ha='right', va='center', transform=ax1.transAxes)
    # mean daily temperature maximum
    if Tmax != None:
        ax1.text(-0.1, 0.6, np.round(Tmax,1), fontsize = 12, ha='right', va='center', transform=ax1.transAxes)
    # mean daily amplitude in  temperature
    if Tdelta != None:
        ax1.text(-0.1, 0.4, np.round(Tdelta,1), fontsize = 12, ha='right', va='center', transform=ax1.transAxes)
    # mean daily temperature minimum
    if Tmin != None:
        ax1.text(-0.1, 0.2, np.round(Tmin,1), fontsize = 12, ha='right', va='center', transform=ax1.transAxes)
    # absolut temperature minimum
    if absTmin != None:
        ax1.text(-0.1, 0.1, np.round(absTmin,1), fontsize = 12, ha='right', va='center', transform=ax1.transAxes)
    
# graphWL("Fairbanks", "132", fairbanks_d.loc["1980":"2010",:], "Tmean", "PP", Tmin = "Tmin", Tmax = "Tmax", Tdelta = True, absTmax = "Tmax", absTmin = "Tmin", 
#       coord = "64.8° N, 148° W", bar = True)
    
