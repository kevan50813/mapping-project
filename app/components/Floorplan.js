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

const DrawMap = ({ loading, error, geoJson, level = [] }) => {
  if (error) {
    console.error(error);
  }

  if (!geoJson) {
    return <Text style={styles.info}>Processing GeoJson...</Text>;
  }

  const projection = d3.geoEquirectangular().fitSize([W, H], geoJson);
  const path = d3.geoPath().projection(projection);

  return (
    <>
      {loading ? (
        <Text style={styles.info}>Loading from {server}...</Text>
      ) : null}

      {!geoJson ? (
        <Text style={styles.info}>Loading from {server}...</Text>
      ) : null}

      {error ? <Text style={styles.error}>{error.message}</Text> : null}

      <SvgPanZoom
        canvasHeight={1500}
        canvasWidth={1920}
        minScale={0.1}
        maxScale={1}
        initialZoom={0.7}>
        {geoJson.features.map((feature, index) => {
          if (parseFloat(feature.properties.level) === parseFloat(level)) {
            const featurePath = path(feature);

            if (feature.geometry.type === 'Polygon') {
              return (
                <Path
                  d={featurePath}
                  key={index}
                  fill={
                    feature.properties.indoor === 'room'
                      ? 'lightblue'
                      : 'lightgrey'
                  }
                  stroke={
                    feature.properties.indoor === 'room' ? 'blue' : 'black'
                  }
                />
              );
            } else if (feature.geometry.type === 'Point') {
              // TODO point render
              <Circle />;
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
        })}
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
      data: { polygons: polygons, edges: edges, nodes: nodes, walls: walls } = {
        polygons: [],
        edges: [],
        nodes: [],
        walls: [],
      },
    },
  ] = useLazyQuery(qMap);

  useEffect(() => {
    getMap({ variables: { graph: 'test_bragg' } });
    setGeoJson(buildGeoJson(polygons, nodes, walls, edges));
  }, [getMap]);

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
