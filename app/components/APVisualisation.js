import React from 'react';
import Plotly from 'react-native-plotly';
import { Network } from './Scan';

const networkColourMapping = {
  [Network.UNSCANNED]: 'gray',
  [Network.SCANNED]: 'lightblue',
  [Network.USED]: 'blue',
};

export const APVisualisation = ({ networks }) => {
  const networkData = {
    xs: networks.map(n => n.coordinates[0]),
    ys: networks.map(n => n.coordinates[1]),
    names: networks.map(n => n.BSSID),
    colours: networks.map(n => networkColourMapping[n.type]),
  };

  /*
   *  stores the data inside an object in an array (plotly needs this format)
   *  with formatting of the markers set inside too so that the data can be
   *  plotted onto the graph
   */
  let data = [
    {
      x: networkData.xs,
      y: networkData.ys,
      text: networkData.names,
      marker: {
        size: 12,
        color: networkData.colours,
      },
      mode: 'markers',
      type: 'scatter',
    },
  ];
  /*
   *  sets how the graph will be laid out and also where the circles for
   *  trilateration are set up
   */

  let layout = {
    title: 'Access Points',
    xaxis: {
      title: {
        text: 'Latitude',
      },
    },
    yaxis: {
      title: {
        text: 'Longitude',
      },
      tickangle: 60,
    },
    margin: {
      b: 80,
      t: 60,
      l: 60,
      r: 20,
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

  return <Plotly data={data} layout={layout} />;
};
