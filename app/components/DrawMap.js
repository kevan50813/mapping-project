import React from 'react';
import * as d3 from 'd3';
import { Path, G } from 'react-native-svg';
import SvgPanZoom from 'react-native-svg-pan-zoom';
import { styles } from './styles';
import { Circle } from 'react-native-svg';
import { onLevel } from '../lib/geoJson';

function GetRotatedTriangle(x, y, rotation) {
  // Initial triangle coordinates.
  let xs = [-9,  9, 0];
  let ys = [-8, -8, 15];
  let tmp = [0, 0, 0];

  // Convert to radians.
  let angle = rotation * (Math.PI / 180);

  // Rotate triangle.
  for (let i = 0; i < 3; i++) {
    tmp[i] = Math.cos(angle) * xs[i] - Math.sin(angle) * ys[i];
    ys[i] = Math.sin(angle) * xs[i] + Math.cos(angle) * ys[i];
    xs[i] = tmp[i];
  }

  // Move the triangle to the current location.
  for (let i = 0; i < 3; i++) {
    xs[i] += x;
    ys[i] += y;
  }

  // Create path for <Path/>
  let path =
    "M "  + xs[0] + " " + ys[0] +
    " L " + xs[1] + " " + ys[1] +
    " L " + xs[2] + " " + ys[2] + " z";
  return path;
}

export const Marker = ({ x, y, rotation }) => (
  <Path
    d={GetRotatedTriangle(x, y, rotation)}
    fill={styles.location.fill}
    stroke={styles.location.innerStroke}
    strokeWidth="3"
  />
);

const DrawMapLocation = ({ location, projection, level }) => {
  if (level !== location.level) {
    return null;
  }

  let radius = 100;
  if (Object.keys(location).length === 0) {
    return null;
  }

  const point = projection(location.point);
  // TODO - confirm this? had to reverse it on merge to make results make sense...
  // Longitude, Latitude -> y, x
  const [x, y] = point;
  if (location.error !== -1) {
    radius = projection(location.error);
  }

  // A stacked set of 2 circles and a triangle that represent the location,
  // facing direction, and the error.
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
      {/* <Circle
        cx={x}
        cy={y}
        r="10"
        fill={styles.location.fill}
        stroke={styles.location.innerStroke}
        strokeWidth={5}
      /> */}
      <Marker
        x={x}
        y={y}
        rotation={90}
      />
    </>
  );
};

function DrawMapElement(
  feature,
  index,
  path,
  projection,
  currentRoom,
  finalRoom,
  currentPath,
) {
  const featurePath = path(feature);
  if (feature.geometry.type === 'Polygon') {
    var fill =
      feature.properties.indoor === 'room'
        ? styles.room.fill
        : styles.hallway.fill;

    if (feature.properties.queryObject.id === currentRoom) {
      fill = styles.currentRoom.fill;
    }

    if (feature.properties.queryObject.id === finalRoom) {
      fill = styles.currentRoom.fill;
    }

    return (
      <Path
        d={featurePath}
        key={index}
        fill={fill}
        stroke={
          feature.properties.indoor === 'room'
            ? styles.room.stroke
            : styles.hallway.stroke
        }
      />
    );
  } else if (feature.geometry.type === 'Point') {
    const point = projection(feature.geometry.coordinates[0]);
    return feature.properties.indoor === 'way' ||
      feature.properties.indoor === 'door' ? null : (
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
    let stroke = styles.walls.stroke;

    if (feature.properties.indoor === 'wall') {
      return (
        <Path
          d={featurePath}
          key={index}
          stroke={stroke}
          strokeWidth="5"
          fill="none"
          strokeLinecap="round"
        />
      );
    } else if (
      currentPath &&
      feature.properties.edge.every(f => currentPath.includes(f))
    ) {
      return (
        <Path
          d={featurePath}
          key={index}
          stroke="#f00"
          strokeWidth="5"
          fill="none"
          strokeLinecap="round"
        />
      );
    }
  }
}

export const DrawMap = ({
  geoJson,
  location,
  level = 0,
  nearestNode,
  currentPath,
}) => {
  const W = 1000;
  const H = 1000;
  let currentRoom = null;
  let finalNodeId = null;
  let finalRoom = null;

  if (nearestNode) {
    currentRoom = nearestNode.properties.queryObject.polygon.id;
  }

  if (currentPath && geoJson) {
    finalNodeId = currentPath[currentPath.length - 1];
    const finalNode = geoJson.features.filter(feature => {
      if (!feature.properties.queryObject) {
        return false;
      }
      return (
        feature.geometry.type === 'Point' &&
        feature.properties.queryObject.id === finalNodeId
      );
    })[0];
    if (finalNode) {
      finalRoom = finalNode.properties.queryObject.polygon.id;
    }
  }

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
        {geoJson
          ? // There could be more flexibility with this but
            // Only call this if the filters match the element?
            geoJson.features
              .filter(onLevel(level))
              .map((feature, index) =>
                DrawMapElement(
                  feature,
                  index,
                  path,
                  projection,
                  currentRoom,
                  finalRoom,
                  currentPath,
                ),
              )
          : null}

        {/* TODO some other option for no location found */}
        {location ? (
          <DrawMapLocation
            location={location}
            projection={projection}
            level={level}
          />
        ) : null}
      </SvgPanZoom>
    </>
  );
};
