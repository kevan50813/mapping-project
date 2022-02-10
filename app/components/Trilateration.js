import React, { useState } from 'react';
import { View } from 'react-native';
import { styles } from './styles';
import Plotly from 'react-native-plotly';
import { Button } from './Button';

export const Trilateration = () => {
  /* loads in the data from wifi_Nodes.json */
  const [networkData, setNetworkData] = useState([]);

  const loadData = async () => {
    await setNetworkData(
      require('./Wifi_Nodes.json').features.map(({ geometry, properties }) => ({
        x_data: geometry.coordinates[0],
        y_data: geometry.coordinates[1],
        SSID: properties.AP_Name,
        BSSID: properties.MacAddress,
      })),
    );
  };

  /*
   *  stores the data inside an object in an array (plotly needs this format)
   *  with formatting of the markers set inside too so that the data can be
   *  plotted onto the graph
   */
  let data = [
    {
      x: networkData.map(element => element.x_data),

      y: networkData.map(element => element.y_data),

      mode: 'markers',

      type: 'scatter',

      text: networkData.map(element => element.BSSID),

      textposition: 'top center',

      textfont: {
        family: 'Raleway, sans-serif',
      },

      marker: { size: 12 },
    },
  ];
  /*
   *  sets how the graph will be laid out and also where the circles for
   *  trilateration are set up
   */

  let layout = {
    title: 'Basic scatter plot',
    xaxis: {
      automargin: true,

      tickangle: 90,

      title: {
        text: 'Latitude',

        standoff: 20,
      },
    },

    yaxis: {
      automargin: true,

      tickangle: 90,

      title: {
        text: 'Longitude',

        standoff: 20,
      },
    },

    shapes: [
      {
        type: 'circle',

        xref: 'x',

        yref: 'y',

        x0: -1.5542,

        y0: 53.8087,

        x1: -1.554,

        y1: 53.8088,

        line: {
          color: 'blue',
        },
      },
    ],
  };

  /*
   *  returns a button for getting and storing the json data
   *  as well as the graph that is being plotted
   */
  return (
    <View style={styles.background}>
      <Button style={styles.button} title="Load JSON Data" onPress={loadData} />
      <Plotly data={data} layout={layout} />
    </View>
  );
};
