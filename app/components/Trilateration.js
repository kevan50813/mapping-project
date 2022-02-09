import React from 'react';
import { ScrollView, View } from 'react-native';
import { styles } from './styles';
import Plotly from 'react-native-plotly';

export const Trilateration = () => {
  var data = [{
    x: [5, 10, 15, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    y: [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
  
    mode: 'markers',
  
    marker: {
  
      size: 40,
  
      color: [0]
  
    }
  
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
