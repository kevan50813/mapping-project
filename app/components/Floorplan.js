import React, { useState, useEffect } from 'react';
import { Text, Button, View } from 'react-native';
import * as d3 from 'd3';
import { Path, Text as SvgText } from 'react-native-svg';
import SvgPanZoom from 'react-native-svg-pan-zoom';
import { useLazyQuery, gql } from '@apollo/client';
import { styles } from './styles';
import { server } from './App';
import { buildGeoJson } from './buildGeoJson';
import { Circle } from 'react-native-svg';

const W = 1000;
const H = 1000;

function DrawMapElement(feature, index, path, projection) {
  // TODO make this work with level ranges
  const featurePath = path(feature);

  if (feature.geometry.type === 'Polygon') {
    return (
      <Path
        d={featurePath}
        key={index}
        fill={feature.properties.indoor === 'room'
          ? 'lightblue'
          : 'lightgrey'}
        stroke={feature.properties.indoor === 'room' ? 'blue' : 'black'} />
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
        strokeWidth="1" />
    );
  } else if (feature.geometry.type === 'LineString') {
    return (
      <Path
        d={featurePath}
        key={index}
        stroke="black"
        strokeWidth="5"
        fill="none" />
    );
  }
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
        {geoJson ? geoJson.features.map((feature, index) => {
          if (parseFloat(feature.properties.level) === parseFloat(level)) {
            // There could be more flexibility with this but
            // Only call this if the filters match the element?
            return DrawMapElement(feature, index, path, projection);
          }
        }) : <></>}

      </SvgPanZoom>
    </>
  );
};

export const Floorplan = () => {
  const [floorId, setFloorId] = useState(2);
  const [geoJson, setGeoJson] = useState(null);

  const qMap = gql`
    query get_map($graph: String!) {
      polygons(graph: $graph) {
        id
        vertices
        level
        tags
      }

      edges(graph: $graph) {
        edge
      }

      pois(graph: $graph) {
        id
        level
        lat
        lon
        tags
      }

      nodes(graph: $graph) {
        id
        level
        lat
        lon
        tags
      }

      walls(graph: $graph) {
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
    {
      loading,
      error,
      data: {
        polygons: polygons,
        edges: edges,
        nodes: nodes,
        walls: walls,
        pois: pois,
      } = {
        polygons: [],
        edges: [],
        nodes: [],
        walls: [],
        pois: [],
      },
    },
  ] = useLazyQuery(qMap);

  useEffect(() => {
    getMap({ variables: { graph: 'test_bragg' } });
  }, [getMap]);

  useEffect(() => {
    setGeoJson(buildGeoJson(polygons, nodes, walls, pois, edges));
  }, [loading]);


  const floor_set = new Set(polygons.map(f => f.level));
  const floor_list = [...floor_set].filter(f => f.indexOf(';') === -1).sort();

  const prevFloor = () => {
    setFloorId(floorId - 1 < 0 ? 0 : floorId - 1);
  };

  const nextFloor = () => {
    setFloorId(floorId + 1 < floor_list.length ? floorId + 1 : floorId);
  };

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
