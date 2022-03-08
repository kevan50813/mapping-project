import React from 'react';
import { Text } from 'react-native';
import * as d3 from 'd3';
import { Path } from 'react-native-svg';
import SvgPanZoom from 'react-native-svg-pan-zoom';
import { styles } from './styles';
import { Circle } from 'react-native-svg';
import { onLevel } from '../lib/geoJson';

const DrawMapLocation = ({ location, projection }) => {
  let radius = 100;
  if (Object.keys(location).length === 0) {
    return null;
  }

  const point = projection(location.point);
  // TODO - confirm this? had to reverse it on merge to make results make sense...
  // Longitude, Latitude -> y, x
  const [x, y] = point;
  console.log(point, x, y);
  if (location.error !== -1) {
    radius = projection(location.error);
  }

  // Hopefully, a stacked set of 3 circles that represent the location and the error.
  return (
    <>
      <Circle
        cx={x}
        cy={y}
        r={radius}
        stroke={styles.location.stroke}
        strokeWidth={3}
      />
      <Circle
        cx={x}
        cy={y}
        r={radius}
        fill={styles.location.fill}
        opacity={0.5}
      />
      <Circle
        cx={x}
        cy={y}
        r="10"
        fill={styles.location.fill}
        stroke={styles.location.innerStroke}
        strokeWidth={5}
      />
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
        fill={
          feature.properties.indoor === 'room'
            ? styles.room.fill
            : styles.hallway.fill
        }
        stroke={
          feature.properties.indoor === 'room'
            ? styles.room.stroke
            : styles.hallway.stroke
        }
      />
    );
  } else if (feature.geometry.type === 'Point') {
    const point = projection(feature.geometry.coordinates[0]);
    return (
      <Circle
        cx={point[0]}
        cy={point[1]}
        r="7"
        key={index}
        fill={styles.poi.fill}
        stroke={styles.poi.stroke}
        strokeWidth="3"
      />
    );
  } else if (feature.geometry.type === 'LineString') {
    return (
      <Path
        d={featurePath}
        key={index}
        stroke={styles.walls.stroke}
        strokeWidth="5"
        fill="none"
        strokeLinecap="round"
      />
    );
  }
}

export const DrawMap = ({ geoJson, location, level = 0 }) => {
  const W = 1000;
  const H = 1000;

  const projection = d3.geoEquirectangular().fitSize([W, H], geoJson);
  const path = d3.geoPath().projection(projection);

  return (
    <>
      <SvgPanZoom
        canvasHeight={1500}
        canvasWidth={1920}
        minScale={0.1}
        maxScale={1}
        initialZoom={0.7}>
        {/* render with empty jsx tag if geoJson isn't ready, keeps the svg canvas size */}
        {geoJson
          ? // There could be more flexibility with this but
            // Only call this if the filters match the element?
            geoJson.features
              .filter(onLevel(level))
              .map((feature, index) =>
                DrawMapElement(feature, index, path, projection),
              )
          : null}

        {/* TODO some other option for no location found */}
        {location ? (
          <DrawMapLocation location={location} projection={projection} />
        ) : null}
      </SvgPanZoom>
    </>
  );
};
