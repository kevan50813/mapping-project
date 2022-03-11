import React, { useState } from 'react';
import { Modal, Text, View, Button } from 'react-native';
import {
  faAngleUp,
  faAngleDown,
  faLocationCrosshairs,
} from '@fortawesome/free-solid-svg-icons';

import { styles } from './styles';
import { MapButton } from './MapButton';
import { SearchModal } from './SearchModal';
import { DrawMap } from './DrawMap';

export const Floorplan = ({
  polygons,
  geoJson,
  setDestination,
  path,
  scan,
  predictedLocation,
  nearestNode,
}) => {
  const [floorId, setFloorId] = useState(2);
  const [modalVisable, setModalVisible] = useState(false);

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
