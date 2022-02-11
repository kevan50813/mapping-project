import React from 'react';
import Plotly from 'react-native-plotly';
import { ScrollView, Text, View } from 'react-native';
import { styles } from './styles';

export const APVisualisation = (props) => {
  /* loads in the data from wifi_Nodes.json */

  let networkData = props.networks;

  networkData.forEach((element, index) => {

    if (element.type === "unscanned")
      element.type = "gray";
    else if (element.type === "scanned")
      element.type = "green";
    else if (element.type === "used")
      element.type = "red";
  });

  /*
   *  stores the data inside an object in an array (plotly needs this format)
   *  with formatting of the markers set inside too so that the data can be
   *  plotted onto the graph
   */
  let data = [
    {
      x: networkData.map(element => element.coordinates[0]),

      y: networkData.map(element => element.coordinates[1]),

      mode: 'markers',

      type: 'scatter',

      text: networkData.map(element => element.BSSID),

      textposition: 'top center',

      textfont: {
        family: 'Raleway, sans-serif',
      },

      marker: { size: 12, color: networkData.map(element => element.type) },
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
      <View style={{flex: 6}}>
      <Plotly data={data} layout={layout} />
      </View>
  );
};
