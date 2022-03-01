import React from 'react';
import { Text } from 'react-native';
import * as d3 from 'd3';
import { Path } from 'react-native-svg';
import SvgPanZoom from 'react-native-svg-pan-zoom';
import { styles } from './styles';
import { server } from './App';
import { Circle } from 'react-native-svg';

const DrawMapLocation = (location, proj) => {
  console.log('PROJECTION');
  console.log(proj);
  console.log('---');

  if (Object.keys(location).length === 0) {
    return <></>;
  }

  const point = proj(location.point);
  // TODO
  // const radius = projection(location.error);
  const radius = 10;

  // Hopefully, a stacked set of 3 circles that represent the location and the error.
  return (
    <>
      <Circle cx={point[0]} cy={point[1]} r={radius} stroke="lightblue" />,
      <Circle
        cx={point[0]}
        cy={point[1]}
        r={radius}
        fill="lightblue"
        opacity={0.5}
      />
      ,
      <Circle cx={point[0]} cy={point[1]} r="5" fill="blue" />,
    </>
  );
};

function DrawMapElement(feature, index, path, projection) {
  // TODO make this work with level ranges
  const featurePath = path(feature);

  if (feature.geometry.type === 'Polygon') {
    return (
      <Path
        d={featurePath}
        key={index}
        fill={feature.properties.indoor === 'room' ? 'lightblue' : 'lightgrey'}
        stroke={feature.properties.indoor === 'room' ? 'blue' : 'black'}
      />
    );
  } else if (feature.geometry.type === 'Point') {
    const point = projection(feature.geometry.coordinates[0]);
    return (
      <Circle
        cx={point[0]}
        cy={point[1]}
        r="5"
        key={index}
        fill="red"
        stroke="black"
        strokeWidth="1"
      />
    );
  } else if (feature.geometry.type === 'LineString') {
    return (
      <Path
        d={featurePath}
        key={index}
        stroke="black"
        strokeWidth="5"
        fill="none"
      />
    );
  }
}

export const DrawMap = ({ loading, error, geoJson, location, level = [] }) => {
  if (error) {
    console.error(error);
  }

  const W = 1000;
  const H = 1000;

  const projection = d3.geoEquirectangular().fitSize([W, H], geoJson);
  const path = d3.geoPath().projection(projection);

  return (
    <>
      {loading ? (
        <Text style={styles.info}>Loading from {server}...</Text>
      ) : null}

      {!geoJson ? (
        <Text style={styles.info}>Processing map data...</Text>
      ) : null}

      {error ? <Text style={styles.error}>{error.message}</Text> : null}

      <SvgPanZoom
        canvasHeight={1500}
        canvasWidth={1920}
        minScale={0.1}
        maxScale={1}
        initialZoom={0.7}>
        {/* render with empty jsx tag if geoJson isn't ready, keeps the svg canvas size */}
        {geoJson ? (
          geoJson.features.map((feature, index) => {
            if (parseFloat(feature.properties.level) === parseFloat(level)) {
              // There could be more flexibility with this but
              // Only call this if the filters match the element?
              return DrawMapElement(feature, index, path, projection);
            }
          })
        ) : (
          <></>
        )}

        {/* TODO some other option for no location found */}
        {/* {location ? <DrawMapLocation location={location} proj={projection} /> : <></>} */}
      </SvgPanZoom>
    </>
  );
};
