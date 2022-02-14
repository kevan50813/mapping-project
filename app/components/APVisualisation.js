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
      .map(getNetworkKey)
      .slice(0, 3),
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

  const shapes = [];
  if (usedBSSIDs.size > 0) {
    const points = knownNetworks.filter(n => usedBSSIDs.has(getNetworkKey(n)));
    const avgLat =
      points.reduce((average, n) => average + n.coordinates[0], 0) /
      usedBSSIDs.size;
    const avgLon =
      points.reduce((average, n) => average + n.coordinates[1], 0) /
      usedBSSIDs.size;

    const radius = 0.000025;

    shapes.push({
      type: 'circle',
      xref: 'x',
      yref: 'y',
      x0: avgLat - radius,
      y0: avgLon - radius,
      x1: avgLat + radius,
      y1: avgLon + radius,
      line: {
        color: 'green',
      },
      fillcolor: 'lightgreen',
      opacity: 0.5,
    });
  }

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
    shapes,
  };

  return <Plotly data={data} layout={layout} />;
};
