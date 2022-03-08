import React, { useState, useEffect, useContext } from 'react';
import { Text, Button, View, TouchableOpacity } from 'react-native';
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import {
  faAngleUp,
  faAngleDown,
  faLocationCrosshairs,
} from '@fortawesome/free-solid-svg-icons';
import Toast from 'react-native-simple-toast';
import { useLazyQuery, gql } from '@apollo/client';

import { styles } from './styles';
import { NetworkContext } from './NetworkProvider';
import { buildGeoJson } from '../lib/geoJson';
import { DrawMap } from './DrawMap';
import { trilateration } from './Trilateration';

export const LoadFloorplan = () => {
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

  const [geoJson, setGeoJson] = useState(null);
  const [knownNetworks, setKnownNetworks] = useState([]);

  const loadKnownNetworks = geoJson => {
    if (geoJson == null) {
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
      level: properties.level,
    }));
  };

  if (geoJson == null && polygons.length > 0) {
    setGeoJson(buildGeoJson(polygons, nodes, walls, pois, edges));
  }

  if (geoJson != null && knownNetworks.length == 0) {
    const networks = loadKnownNetworks(geoJson);
    setKnownNetworks(networks);
  }

  return loading ? (
    <Text style={styles.info}>Loading Floorplan...</Text>
  ) : (
    <Floorplan
      polygons={polygons}
      loading={loading}
      error={error}
      geoJson={geoJson}
      knownNetworks={knownNetworks}
    />
  );
};

export const Floorplan = ({ polygons, geoJson, knownNetworks }) => {
  const [floorId, setFloorId] = useState(2);
  const [shownToast, setShownToast] = useState(false);
  let predictedLocation = {};

  const {
    networks: visibleNetworks,
    state: { scanning },
    startScan,
  } = useContext(NetworkContext);

  const scan = async () => {
    startScan();
  };

  if (visibleNetworks.length > 0 && knownNetworks.length > 0) {
    let data = trilateration(visibleNetworks, knownNetworks, -50, 3);
    console.log(data);
    console.log(data.predictedLocation);
    predictedLocation = data.predictedLocation;
  }

  const floor_set = new Set(polygons.map(f => f.level));
  const floor_list = [...floor_set].filter(f => f.indexOf(';') === -1).sort();

  const prevFloor = () => {
    setFloorId(floorId - 1 < 0 ? 0 : floorId - 1);
  };

  const nextFloor = () => {
    setFloorId(floorId + 1 < floor_list.length ? floorId + 1 : floorId);
  };

  if (!scanning && visibleNetworks.length > 0 && !shownToast) {
    Toast.show('Network scan successful.', Toast.LONG);
    setShownToast(true);
  }

  if (scanning) {
    Toast.show('Scanning Wifi APs...', Toast.LONG);
  }

  return (
    <>
      <View style={styles.background}>
        <DrawMap
          geoJson={geoJson}
          location={predictedLocation}
          level={parseInt(floor_list[floorId], 10)}
        />

        <TouchableOpacity
          onPress={nextFloor}
          style={[styles.mapButton, { position: 'absolute', top: 0, left: 0 }]}>
          <FontAwesomeIcon
            icon={faAngleUp}
            size={styles.mapButtonIcon.size}
            style={styles.mapButtonIcon}
          />
        </TouchableOpacity>

        <TouchableOpacity
          onPress={prevFloor}
          style={[
            styles.mapButton,
            { position: 'absolute', top: 70, left: 0 },
          ]}>
          <FontAwesomeIcon
            icon={faAngleDown}
            size={styles.mapButtonIcon.size}
            style={styles.mapButtonIcon}
          />
        </TouchableOpacity>

        <TouchableOpacity
          onPress={scan}
          style={[
            styles.mapButton,
            { position: 'absolute', bottom: 0, left: 0 },
          ]}>
          <FontAwesomeIcon
            icon={faLocationCrosshairs}
            size={styles.mapButtonIcon.size}
            style={styles.mapButtonIcon}
          />
        </TouchableOpacity>
      </View>

      <Text style={{ color: 'black', paddingLeft: '5%' }}>
        Floor id: {floor_list[floorId]}
      </Text>
    </>
  );
};
