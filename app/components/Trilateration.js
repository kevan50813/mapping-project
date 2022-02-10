import React, { useState } from 'react';
import { ScrollView, View } from 'react-native';
import { styles } from './styles';
import Plotly from 'react-native-plotly';
import { Button } from './Button';

export const Trilateration = () => {
  let [setNetworkData] = useState(null);

  const loadData = async () => {
    try {
      setNetworkData(
        require('./Wifi_Nodes.json').features.map(
          ({ geometry, properties }) => ({
            x_data: geometry.coordinates,
            SSID: properties.AP_Name,
            BSSID: properties.MacAddress,
          }),
        ),
      );
      console.log(x_data);
    } catch (error) {
      console.error(error);
    }
  };

  let data = [
    {
      x: [0, 1, 2, 3],

      y: [0, 1, 2, 3],

      mode: 'markers+text',

      type: 'scatter',

      text: [0, 1, 2, 3],

      textposition: 'top center',

      textfont: {
        family: 'Raleway, sans-serif',
      },

      marker: { size: 12 },
    },
  ];

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
  };

  return (
    <View style={styles.background}>
      <Button style={styles.button} title="Load JSON Data" onPress={loadData} />
      <Plotly data={data} layout={layout} />
    </View>
  );
};
