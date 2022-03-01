import React, { useState, useEffect, useContext } from 'react';
import { Text, Button, View } from 'react-native';
import { useLazyQuery, gql } from '@apollo/client';
import { styles } from './styles';
import { NetworkContext } from './NetworkProvider';
import { buildGeoJson } from '../lib/buildGeoJson';
import { DrawMap } from './DrawMap';
import { trilateration } from './Trilateration';

export const Floorplan = () => {
  const [floorId, setFloorId] = useState(2);
  const [geoJson, setGeoJson] = useState(null);
  const [knownNetworks, setKnownNetworks] = useState([]);
  let predictedLocation = {};

  const {
    networks: visibleNetworks,
    state: { scanning },
    startScan,
  } = useContext(NetworkContext);

  const loadKnownNetworks = geoJson => {
    if (!geoJson) {
      return [];
    }

    // get the filter from the queries PoI data here
    const nodes = geoJson.features.filter(
      feature => feature.properties.internet === 'yes',
    );
    return nodes.map(({ geometry, properties }) => ({
      coordinates: geometry.coordinates[0],
      name: properties.ssid,
      BSSID: properties.mac_addres, // NB: not a typo, problem with char limits in shapefiles
    }));
  };

  const scan = async () => {
    startScan();
  };

  if (visibleNetworks.length > 0 && knownNetworks.length > 0) {
    let data = trilateration(visibleNetworks, knownNetworks);
    console.log(data);
    // console.log(data.predictedLocation);
    predictedLocation = data.predictedLocation;
  }

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
    const networks = loadKnownNetworks(geoJson);
    setKnownNetworks(networks);
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
      <View style={styles.background}>
        <Button style={styles.button} title="Scan Networks" onPress={scan} />
        {knownNetworks.length > 0 ? (
          <Text style={styles.info}>Loaded network data from JSON.</Text>
        ) : null}
        {visibleNetworks.length > 0 ? (
          <Text style={styles.info}>Network scan successful.</Text>
        ) : null}
        {scanning ? <Text style={styles.info}>Scanning...</Text> : null}
      </View>

      <DrawMap
        loading={loading}
        error={error}
        geoJson={geoJson}
        location={predictedLocation}
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
