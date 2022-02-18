import React, { useState, useEffect } from 'react';
import { Text, Button, View } from 'react-native';
import * as d3 from 'd3';
import { Path, Text as SvgText } from 'react-native-svg';
import SvgPanZoom from 'react-native-svg-pan-zoom';
import { useLazyQuery, gql } from '@apollo/client';
import { styles } from './styles';
import { server } from './App';

const W = 1000;
const H = 1000;

function buildGeoJson(polygons, nodes, walls) {
  // Create a GeoJson object
  var geoJson = {
    type: 'FeatureCollection',
    name: 'Polygons',
    crs: {
      type: 'name',
      properties: { name: 'urn:ogc:def:crs:OGC:1.3:CRS84' },
    },
    features: [],
  };

  for (var i = 0; i < polygons.length; i++) {
    const feature = {
      type: 'Feature',
      properties: {},
      geometry: {
        type: 'Polygon',
        coordinates: [],
      },
    };

    const vertices = polygons[i].vertices.map(v => [v[1], v[0]]);
    feature.geometry.coordinates = [vertices];
    feature.properties.level = polygons[i].level;
    feature.properties.indoor = polygons[i].tags.indoor;
    geoJson.features.push(feature);
  }

  //TODO add nodes & walls 

  return geoJson;
}

const DrawMap = ({ loading, error, geoJson, level = [] }) => {
  if (error) {
    console.error(error);
  }

  const projection = d3.geoEquirectangular().fitSize([W, H], geoJson);
  const path = d3.geoPath().projection(projection);

  return (
    <>
      {loading ? (
        <Text style={styles.info}>Loading from {server}...</Text>
      ) : null}
      {error ? <Text style={styles.error}>{error.message}</Text> : null}
      <SvgPanZoom
        canvasHeight={1500}
        canvasWidth={1920}
        minScale={0.1}
        maxScale={1}
        initialZoom={0.7}
      >
        {geoJson.features.map((feature, index) => {
          if (feature.properties.level == level) {
            const featurePath = path(feature);
            return (
              <Path
                d={featurePath}
                key={index}
                fill={
                  feature.properties.indoor === 'room'
                    ? 'lightblue'
                    : 'lightgrey'
                }
                stroke={feature.properties.indoor === 'room' ? 'blue' : 'black'}
              />
            );
          }
        })}
      </SvgPanZoom>
    </>
  );
};

// const rooms = features.map(f => f.geometry.coordinates[0]);

// const minX = rooms.reduce(
//   (m, room) => Math.min(m, ...room.map(r => r[0])),
//   Infinity,
// );
// const maxX = rooms.reduce(
//   (m, room) => Math.max(m, ...room.map(r => r[0])),
//   -Infinity,
// );
// const minY = rooms.reduce(
//   (m, room) => Math.min(m, ...room.map(r => r[1])),
//   Infinity,
// );
// const maxY = rooms.reduce(
//   (m, room) => Math.max(m, ...room.map(r => r[1])),
//   -Infinity,
// );

export const Floorplan = () => {
  const [floorId, setFloorId] = useState(2);

  const qMap = gql`
    query get_map ($graph: String!) {
      polygons(graph: $graph) {
        id
        vertices
        level
        tags
      }

      edges (graph: $graph) {
        edge
      }

      nodes (graph: $graph) {
        id
        level
        lat
        lon
        tags
      }

      walls (graph: $graph) {
        id
        level
        lat
        lon
        tags
      }
    }
  `;

  const [
    getMap,
    { loading, 
      error, 
      data: { polygons: polygons, 
              edges: edges, 
              nodes: nodes, 
              walls: walls 
            } = { polygons: [], 
                  edges: [], 
                  nodes: [], 
                  walls: [] 
                } 
    },
  ] = useLazyQuery(qMap);

  useEffect(() => {
    getMap({variables = {graph: "test_bragg"}});
  }, [getMap]);

  const geoJson = buildGeoJson(polygons, nodes, walls);

  // const features = polygons.features;
  const floor_set = new Set(polygons.map(f => f.level));
  const floor_list = [...floor_set].filter(f => f.indexOf(';') === -1).sort();

  const prevFloor = () => {
    setFloorId(floorId - 1 < 0 ? 0 : floorId - 1);
  };

  const nextFloor = () => {
    setFloorId(floorId + 1 < floor_list.length ? floorId + 1 : floorId);
  };

  // const scaleX = d3.scaleLinear([minX, maxX], [20, 620]);
  // const scaleY = d3.scaleLinear([minY, maxY], [460, 20]);

  return (
    <>
      <DrawMap
        loading={loading}
        error={error}
        geoJson={geoJson}
        level={floor_list[floorId]}
      />

      <Text style={{ color: 'black', paddingLeft: '5%' }}>
        Floor id: {floor_list[floorId]}
      </Text>
      <View style={{ flexDirection: 'row' }}>
        <View style={{ width: '50%', paddingLeft: '5%', paddingRight: '2.5%' }}>
          <Button onPress={prevFloor} title="Previous floor" />
        </View>
        <View style={{ width: '50%', paddingLeft: '2.5%', paddingRight: '5%' }}>
          <Button onPress={nextFloor} title="Next floor" />
        </View>
      </View>
    </>
  );
};
