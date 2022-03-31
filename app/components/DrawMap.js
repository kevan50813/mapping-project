import React, { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';
import 'react-native-get-random-values';
import { v4 as uuidv4 } from 'uuid';
import { Path, Polygon, Circle, Text } from 'react-native-svg';
import SvgPanZoom from 'react-native-svg-pan-zoom';
import { styles } from './styles';
import { onLevel } from '../lib/geoJson';
import CompassHeading from 'react-native-compass-heading';
import { GetRotatedEquiTriangle, GetRotatedTriangle } from '../lib/drawShapes';
import { TSpan } from 'react-native-svg';

function getVector(angle, length) {
  angle = (angle * Math.PI) / 180;
  return {
    x: length * Math.sin(angle),
    y: length * Math.cos(angle),
  };
}

export const Marker = ({ x, y, rotation, fill }) => (
  <Polygon
    key={uuidv4()}
    points={GetRotatedTriangle(x, y, rotation)}
    fill={fill ? fill : styles.location.fill}
    stroke={styles.location.innerStroke}
    strokeWidth="3"
  />
);

const DrawMapLocation = ({ location, projection, level, isMoving }) => {
  // State and effect for compass rotation.
  const [compassHeading, setCompassHeading] = useState(0);
  const offset = useRef({ x: 0, y: 0 });

  // add x component, add y component
  if (isMoving) {
    const angledVector = getVector(compassHeading + 180, 0.5);
    offset.current = {
      x: offset.current.x - angledVector.x,
      y: offset.current.y + angledVector.y,
    };
  }

  useEffect(() => {
    offset.current = { x: 0, y: 0 };
  }, [location]);

  useEffect(() => {
    const degree_update_rate = 3;

    // Accuracy is hardcoded to 1 in the library.
    CompassHeading.start(degree_update_rate, ({ heading, accuracy }) => {
      setCompassHeading(heading);
    });

    return () => {
      CompassHeading.stop();
    };
  }, []);

  if (level !== location.level) {
    return null;
  }

  let radius = 100;
  if (Object.keys(location).length === 0) {
    return null;
  }

  const point = projection(location.point);
  const old = location.old;
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
        key={uuidv4()}
        r={radius}
        stroke={old ? styles.locationOld.stroke : styles.location.stroke}
        strokeWidth={3}
      />
      <Circle
        cx={x}
        cy={y}
        key={uuidv4()}
        r={radius}
        fill={old ? styles.locationOld.fill : styles.location.fill}
        opacity={0.5}
      />
      <Circle
        cx={x}
        cy={y}
        key={uuidv4()}
        stroke={'white'}
        strokeWidth={3}
        r={10}
        fill={old ? styles.locationOld.fill : styles.location.fill}
      />
      <Marker
        x={x + offset.current.x}
        y={y + offset.current.y}
        rotation={compassHeading + 180}
      />
    </>
  );
};

function DrawPolygonElement(
  feature,
  featurePath,
  centroid,
  area,
  index,
  currentRoom,
  finalRoom,
  showLabels,
  zoom,
) {
  let fill =
    feature.properties.indoor === 'room'
      ? styles.room.fill
      : styles.hallway.fill;

  let opacity = 1;

  if (feature.properties.queryObject.id === currentRoom) {
    fill = styles.currentRoom.fill;
    opacity = 0.5;
  }

  if (feature.properties.queryObject.id === finalRoom) {
    fill = styles.currentRoom.fill;
    opacity = 0.5;
  }

  let roomString = `${feature.properties.queryObject.tags['room-name']}\n${feature.properties.queryObject.tags['room-no']}`;
  roomString = roomString.replace(/(.{10}[^ ]* )/g, '$1\n');
  let roomParts = roomString.split('\n');

  if (area < 1700) {
    roomParts = [roomParts[roomParts.length - 1]];
    // showLabels = false;
  }

  return (
    <>
      <Path
        d={featurePath}
        key={index}
        fill={fill}
        opacity={opacity}
        stroke={
          feature.properties.indoor === 'room'
            ? styles.room.stroke
            : styles.hallway.stroke
        }
      />
      {showLabels ? (
        <Text
          fill="black"
          key={uuidv4()}
          fontWeight={800}
          x={centroid[0]}
          y={centroid[1] - 15}
          fontSize={10 * (1 - zoom.current) + 10}
          textAnchor="middle">
          {roomParts.map(part => {
            return (
              <TSpan x={centroid[0]} dy="15" key={uuidv4()}>
                {part}
              </TSpan>
            );
          })}
        </Text>
      ) : null}
    </>
  );
}

function DrawPointElement(
  feature,
  projection,
  index,
  up,
  down,
  showPoIs,
  showWifi,
  finalNodeId,
) {
  if (feature.properties.amenity === 'wap' && !showWifi) {
    return null;
  }

  const point = projection(feature.geometry.coordinates[0]);
  const [x, y] = point;

  if (up.includes(feature.properties.queryObject.id)) {
    return (
      <Polygon
        points={GetRotatedEquiTriangle(x, y, 0)}
        fill="#f00"
        stroke="#900"
        strokeWidth="3"
        key={index}
      />
    );
  }

  if (down.includes(feature.properties.queryObject.id)) {
    return (
      <Polygon
        points={GetRotatedEquiTriangle(x, y, 180)}
        fill="#f00"
        stroke="#900"
        strokeWidth="3"
        key={index}
      />
    );
  }

  if (feature.properties.queryObject.id === finalNodeId) {
    return (
      <Circle
        cx={x}
        cy={y}
        r="7"
        key={index}
        fill="#f00"
        stroke="#900"
        strokeWidth="3"
      />
    );
  }

  if (showPoIs) {
    return feature.properties.indoor === 'way' ||
      feature.properties.indoor === 'door' ? null : (
      <Circle
        cx={x}
        cy={y}
        r="7"
        key={index}
        fill={
          feature.properties.amenity === 'wap'
            ? styles.ap.fill
            : styles.poi.fill
        }
        stroke={styles.poi.stroke}
        strokeWidth="3"
      />
    );
  }
}

function DrawLineStringElement(feature, featurePath, index, currentPath) {
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

function DrawMapElement(
  feature,
  index,
  path,
  projection,
  currentRoom,
  finalRoom,
  currentPath,
  showLabels,
  showPoIs,
  showWifi,
  up,
  down,
  zoom,
  finalNodeId,
) {
  const featurePath = path(feature);
  const centroid = path.centroid(feature);
  const area = path.area(feature);

  if (feature.geometry.type === 'Polygon') {
    return DrawPolygonElement(
      feature,
      featurePath,
      centroid,
      area,
      index,
      currentRoom,
      finalRoom,
      showLabels,
      zoom,
    );
  } else if (feature.geometry.type === 'Point') {
    return DrawPointElement(
      feature,
      projection,
      index,
      up,
      down,
      showPoIs,
      showWifi,
      finalNodeId,
    );
  } else if (feature.geometry.type === 'LineString') {
    return DrawLineStringElement(feature, featurePath, index, currentPath);
  }
}

export const DrawMap = ({
  geoJson,
  location,
  level = 0,
  nearestNode,
  currentPath,
  showLabels,
  showPoIs,
  showWifi,
  moving,
  destination,
}) => {
  const W = 1000;
  const H = 1000;
  let currentRoom = null;
  let finalNodeId = null;
  let up = [];
  let down = [];
  let finalRoom = null;
  const projection = d3.geoEquirectangular().fitSize([W, H], geoJson);
  const path = d3.geoPath().projection(projection);
  let zoom = useRef(0.7);

  if (nearestNode && nearestNode.properties.queryObject.polygon) {
    currentRoom = nearestNode.properties.queryObject.polygon.id;
  }

  if (destination && geoJson) {
    finalNodeId = destination;

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

  if (currentPath && geoJson && currentPath.length > 1) {
    let nodeLookup = {};
    const nodes = geoJson.features.filter(
      feature =>
        feature.geometry.type === 'Point' &&
        feature.properties.indoor === 'way',
    );
    nodes.map(n => (nodeLookup[n.properties.queryObject.id] = n));

    for (let i = 0; i < currentPath.length; i++) {
      if (i === 0) {
        continue;
      }
      const current = currentPath[i];
      const previous = currentPath[i - 1];

      const currentLevel = nodeLookup[current].properties.level[0];
      const previousLevel = nodeLookup[previous].properties.level[0];

      if (currentLevel < previousLevel) {
        up.push(previous);
      } else if (currentLevel > previousLevel) {
        down.push(previous);
      }
    }
  }

  return (
    <>
      <SvgPanZoom
        canvasHeight={1500}
        canvasWidth={1920}
        minScale={0.1}
        maxScale={1}
        onZoom={newZoom => {
          zoom.current = newZoom;
        }}
        initialZoom={zoom.current}>
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
                  showLabels,
                  showPoIs,
                  showWifi,
                  up,
                  down,
                  zoom,
                  finalNodeId,
                ),
              )
          : null}

        {/* TODO some other option for no location found */}
        {location ? (
          <DrawMapLocation
            location={location}
            projection={projection}
            level={level}
            isMoving={moving}
          />
        ) : null}
      </SvgPanZoom>
    </>
  );
};
