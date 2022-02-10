import React from 'react';
import { ScrollView, View } from 'react-native';
import { styles } from './styles';
import Plotly from 'react-native-plotly';

export const Trilateration = () => {
  
  const loadData = async () => {
    setNetworkData(
      require('./Wifi_Nodes.json').features.map(({ geometry, properties }) => ({
        coordinates: geometry.coordinates,
        SSID: properties.AP_Name,
        BSSID: properties.MacAddress,
      })),
    );
  };

  var data = [{

  
  x: [1, 2, 3, 4, 5],

  y: [1, 6, 3, 6, 1],

  mode: 'markers+text',

  type: 'scatter',

  name: 'Team A',

  text: ['A-1', 'A-2', 'A-3', 'A-4', 'A-5'],

  textposition: 'top center',

  textfont: {

    family:  'Raleway, sans-serif'

  },

  marker: { size: 12 }
  
  }];
   
  
  var layout = {
  
    title: 'Scatter Plot with a Color Dimension',
    xaxis: {

      automargin: true,

      tickangle: 90,

      title: {

        text: "Latitude",

        standoff: 20

      }},
  
    yaxis: {

        automargin: true,
  
        tickangle: 90,
  
        title: {
  
          text: "Longitude",
  
          standoff: 20
  
        }}

  };
  
    return (
      <Plotly
        data={data}
        layout={layout}
      />
    )
  
};
