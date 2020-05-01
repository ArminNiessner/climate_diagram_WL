# climate_diagram_WL
A python script to create a climate diagram after Walter &amp; Lieth (1960)

```python
climate_graph_WL.graphWL(name, altitude, df, T_col, P_col, Tmin = None, Tmax = None, 
          Tdelta = None, absTmax = None, absTmin = None, center = "north", 
          coord = None, bar = False)
```

parameter | explanation
---|---
 `name` | Name of the station or location 
 `altitude`| Altitude above sea level
 `df` | A pandas dataframe. Index should be in pandas datetime format, having a monthly or better a daily frequency. The dataframe should have at least two columns with one for temperature and one for precipitation
`T_col` | Name of the column with temperature observations in °C
`P_col` | Name of the column with precipitation in mm
`Tmin` | Column that contains daily minimum temperature or provide an integer or float to show in figure
`Tmax` | Column that contains daily maximum temperature or provide an integer or float to show in figure
`Tdelta` | Set to `True` if dataframe has a daily resolution and contains columns for daily minimum and maximum temperature provided as `Tmin` and `Tmax`. Or, provide an integer or float to show in figure
`absTmax` | Provide an integer or float to show in figure or the name of the column with daily maximum temperature if `df` is on daily basis
`absTmin` | Provide an integer or float to show in figure or the name of the column with daily minimum temperature if `df` is on daily basis
`center` | Set to "south" if station is located in the southern hemisphere. Default = "north"
`coord` | Coordinates of the location to print in figure
`bar` | Set to `True` if `df` is on a daily basis and a column for daily minimum temperature is provided, to show a bar under the graph that indicates months with temperatures below 0 ° C

![Climate Fairbanks](/FairbanksWL1.png)