import React from 'react';
import Plotly from 'react-native-plotly';
import { NetworkType } from './NetworkProvider';

const networkColours = {
  [NetworkType.UNSCANNED]: 'lightgray',
  [NetworkType.SCANNED]: 'lightblue',
  [NetworkType.USED]: 'blue',
};

const getNetworkKey = n => n.BSSID.slice(0, -1);

export const APVisualisation = ({ knownNetworks, visibleNetworks }) => {
  const scannedBSSIDs = new Set(visibleNetworks.map(getNetworkKey));
  // Currently using no networks for trilateration
  const usedBSSIDs = new Set(
    visibleNetworks
      .filter(n => n.SSID === 'eduroam')
      .sort((a, b) => a.level - b.level)
      .slice(0, 3)
      .map(getNetworkKey),
  );

  const getColour = network => {
    const key = getNetworkKey(network);
    if (usedBSSIDs.has(key)) {
      return networkColours[NetworkType.USED];
    }
    if (scannedBSSIDs.has(key)) {
      return networkColours[NetworkType.SCANNED];
    }
    return networkColours[NetworkType.UNSCANNED];
  };

  const networkData = {
    xs: knownNetworks.map(n => n.coordinates[0]),
    ys: knownNetworks.map(n => n.coordinates[1]),
    names: knownNetworks.map(n => n.BSSID),
    colours: knownNetworks.map(getColour),
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
