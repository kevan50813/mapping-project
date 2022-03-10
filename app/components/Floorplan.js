import React, { useState, useEffect, useContext } from 'react';
import { Modal, Text, View, Button } from 'react-native';
import {
  faAngleUp,
  faAngleDown,
  faLocationCrosshairs,
} from '@fortawesome/free-solid-svg-icons';
import { useLazyQuery } from '@apollo/client';

import { styles } from './styles';
import { NetworkContext } from './NetworkProvider';
import { MapButton } from './MapButton';
import { SearchModal } from './SearchModal';
import { buildGeoJson } from '../lib/geoJson';
import { findNearestNode } from '../lib/findNearestNode';
import { DrawMap } from './DrawMap';
import { qMap } from '../queries/qMap';
import { qPath } from '../queries/qPath';
import { trilateration } from './Trilateration';

export const LoadFloorplan = () => {
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

  const loadKnownNetworks = geo => {
    if (geo == null) {
      return [];
    }

    // get the filter from the queries PoI data here
    const knownWifi = geo.features.filter(
      feature => feature.properties.internet === 'yes',
    );
    return knownWifi.map(({ geometry, properties }) => ({
      coordinates: geometry.coordinates[0],
      name: properties.ssid,
      BSSID: properties.mac_addres, // NB: not a typo, problem with char limits in shapefiles
      level: properties.level,
    }));
  };

  if (geoJson == null && polygons.length > 0) {
    setGeoJson(buildGeoJson(polygons, nodes, walls, pois, edges));
  }

  if (geoJson != null && knownNetworks.length === 0) {
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
  const [modalVisable, setModalVisible] = useState(false);
  const [path, setPath] = useState([]);
  const [destination, setDestination] = useState(2878);
  let predictedLocation = {};
  let nearestNode = null;
  let nearestId = -1;

  const { networks: visibleNetworks, startScan } = useContext(NetworkContext);

  const floor_set = new Set(polygons.map(f => f.level));
  const floor_list = [...floor_set].filter(f => f.indexOf(';') === -1).sort();

  const scan = async () => {
    startScan();
  };

  if (visibleNetworks.length > 0 && knownNetworks.length > 0) {
    let data = trilateration(visibleNetworks, knownNetworks, -50, 3);
    predictedLocation = data.predictedLocation;
    nearestNode = findNearestNode(predictedLocation, geoJson);
    nearestId = nearestNode.properties.queryObject.id;
  }

  const prevFloor = () => {
    setFloorId(floorId - 1 < 0 ? 0 : floorId - 1);
  };

  const nextFloor = () => {
    setFloorId(floorId + 1 < floor_list.length ? floorId + 1 : floorId);
  };

  const [
    getPath,
    { loading, error, data: { find_route: find_route } = { find_route: {} } },
  ] = useLazyQuery(qPath);

  useEffect(() => {
    if (nearestId === -1) {
      return;
    }

    getPath({
      variables: { graph: 'test_bragg', start: nearestId, end: destination },
    });
  }, [getPath, nearestId, destination]);

  useEffect(() => {
    if (error) {
      console.error('Pathfinding error');
    }

    if (!loading && find_route.ids) {
      setPath(find_route.ids);
    }
  }, [error, loading, find_route]);

  return (
    <>
      <Button
        style={styles.button}
        title="MODAL"
        onPress={() => setModalVisible(!modalVisable)}
      />

      <Modal animationType="slide" visible={modalVisable}>
        <SearchModal
          nearestNode={nearestNode}
          setDestination={setDestination}
          setModalVisible={setModalVisible}
        />
      </Modal>

      <View style={styles.background}>
        <DrawMap
          geoJson={geoJson}
          location={predictedLocation}
          level={parseInt(floor_list[floorId], 10)}
          nearestNode={nearestNode}
          currentPath={path}
        />

        <MapButton
          icon={faAngleUp}
          position={{ position: 'absolute', top: 0, right: 0 }}
          onPress={nextFloor}
        />

        <MapButton
          icon={faAngleDown}
          position={{ position: 'absolute', top: 70, right: 0 }}
          onPress={prevFloor}
        />

        <MapButton
          icon={faLocationCrosshairs}
          position={{ position: 'absolute', bottom: 0, right: 0 }}
          onPress={scan}
        />

        <View style={styles.levelView}>
          <Text style={[styles.big, styles.levelViewText]}>
            Level: {floor_list[floorId]}
          </Text>
        </View>
      </View>
    </>
  );
};
