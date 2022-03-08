import React from 'react';
import Plotly from 'react-native-plotly';
import { NetworkType } from './NetworkProvider';

const networkColours = {
  [NetworkType.UNSCANNED]: 'lightgray',
  [NetworkType.SCANNED]: 'blue',
  [NetworkType.USED]: 'red',
};

const getNetworkKey = n => n.BSSID.slice(0, -1);

export const APVisualisation = ({
  knownNetworks,
  visibleNetworks,
  usedNetworks,
  predictedLocation,
}) => {
  const scannedBSSIDs = new Set(visibleNetworks.map(getNetworkKey));
  const usedBSSIDs = new Set(usedNetworks.map(getNetworkKey));

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

  // only plot predicted location if we get one!
  try {
    if (predictedLocation.point[0] !== -1) {
      data[0].x.push(predictedLocation.point[0]);
      data[0].y.push(predictedLocation.point[1]);
      data[0].text.push('point');
      data[0].marker.color.push('purple');
    }
  } catch (e) {
    console.log(e);
  }

  /*
   *  sets how the graph will be laid out and also where the circles for
   *  trilateration are set up
   */

  const shapes = [];
  usedNetworks.forEach(network => {
    // TODO - actual conversion for metres -> lat/lon distance
    const radius = network.distance / 20000;
    shapes.push({
      type: 'circle',
      xref: 'x',
      yref: 'y',
      x0: network.coordinates[0] - radius,
      y0: network.coordinates[1] - radius,
      x1: network.coordinates[0] + radius,
      y1: network.coordinates[1] + radius,
      line: {
        color: 'red',
      },
      fillcolor: 'red',
      opacity: 0.2,
      layer: 'below',
    });
  });

  let layout = {
    title: 'Access Points',
    xaxis: {
      title: {
        text: 'Latitude',
      },
      automargin: true,
    },
    yaxis: {
      title: {
        text: 'Longitude',
      },
      tickangle: 60,
      automargin: true,
    },
    shapes,
  };

  return <Plotly data={data} layout={layout} />;
};
