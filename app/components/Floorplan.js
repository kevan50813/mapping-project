import React, { useState, useEffect, useRef } from 'react';
import { useDeviceMotion } from '@use-expo/sensors';
import { useNavigation } from '@react-navigation/native';
import { BackHandler, Text, View } from 'react-native';
import { SearchBar } from 'react-native-elements';
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';

import {
  faAngleUp,
  faMagnifyingGlassLocation,
  faXmark,
  faAngleDown,
  faLocationCrosshairs,
  faTags,
  faLocationDot,
} from '@fortawesome/free-solid-svg-icons';

import { styles } from './styles';
import { MapButton } from './MapButton';
import { SearchModal } from './SearchModal';
import { DrawMap } from './DrawMap';

export const Floorplan = ({
  polygons,
  geoJson,
  setDestination,
  currentPath,
  scan,
  predictedLocation,
  nearestNode,
}) => {
  const [floorId, setFloorId] = useState(2);
  const [modalVisable, setModalVisible] = useState(false);
  const [search, setSearch] = useState('');
  const [showLabels, setShowLabels] = useState(false);
  const [showPoIs, setShowPoIs] = useState(false);
  const navigation = useNavigation();
  const [accData, accAvailable] = useDeviceMotion({ interval: 1000 });
  const moving = useRef(false);
  const motion = useRef({ x: 0, y: 0, z: 0 });

  let locationSearch = React.createRef();

  const floor_set = new Set(polygons.map(f => f.level));
  const floor_list = [...floor_set].filter(f => f.indexOf(';') === -1).sort();

  if (accAvailable && accData) {
    motion.current = {
      x: motion.current.x * 0.4 + accData.acceleration.x * 0.6,
      y: motion.current.y * 0.4 + accData.acceleration.y * 0.6,
      z: motion.current.z * 0.4 + accData.acceleration.z * 0.6,
    };
  }

  if (
    Math.abs(motion.current.x) > 0.7 ||
    Math.abs(motion.current.y) > 0.7 ||
    Math.abs(motion.current.z) > 0.7
  ) {
    moving.current = true;
  } else {
    moving.current = false;
  }

  useEffect(() => {
    const timer = setTimeout(() => scan(), 5000);
    return () => clearTimeout(timer);
  });

  const backAction = () => {
    if (modalVisable) {
      setModalVisible(false);
      return true;
    }
    navigation.pop();
    return true;
  };

  BackHandler.addEventListener('hardwareBackPress', backAction);

  const prevFloor = () => {
    setFloorId(floorId - 1 < 0 ? 0 : floorId - 1);
  };

  const nextFloor = () => {
    setFloorId(floorId + 1 < floor_list.length ? floorId + 1 : floorId);
  };

  const centerFloor = () => {
    if (predictedLocation.level && predictedLocation.level !== -1) {
      setFloorId(floor_list.indexOf(predictedLocation.level.toString()));
    }
  };

  const updateSearch = newSearch => {
    setSearch(newSearch);
  };

  const handleScanButton = () => {
    // dispatch a scan
    scan();

    // toggle centering
    // Then we can do some sort of centering
  };

  return (
    <>
      <View style={styles.background}>
        <DrawMap
          geoJson={geoJson}
          location={predictedLocation}
          level={parseInt(floor_list[floorId], 10)}
          nearestNode={nearestNode}
          currentPath={currentPath}
          moving={moving}
          showLabels={showLabels}
          showPoIs={showPoIs}
        />

        <MapButton
          icon={faTags}
          position={{ position: 'absolute', top: 70, left: 0 }}
          onPress={() => {
            setShowLabels(!showLabels);
          }}
        />

        <MapButton
          icon={faLocationDot}
          position={{ position: 'absolute', top: 140, left: 0 }}
          onPress={() => {
            setShowPoIs(!showPoIs);
          }}
        />

        <MapButton
          icon={faAngleUp}
          position={{ position: 'absolute', top: 70, right: 0 }}
          onPress={nextFloor}
        />

        <MapButton
          text={
            predictedLocation.level !== undefined
              ? predictedLocation.level
              : floor_list[floorId]
          }
          position={{ position: 'absolute', top: 140, right: 0 }}
          onPress={centerFloor}
        />

        <MapButton
          icon={faAngleDown}
          position={{ position: 'absolute', top: 210, right: 0 }}
          onPress={prevFloor}
        />

        <MapButton
          icon={faLocationCrosshairs}
          position={{ position: 'absolute', bottom: 0, right: 0 }}
          onPress={handleScanButton}
        />

        <View style={styles.levelView}>
          <Text style={[styles.big, styles.levelViewText]}>
            Level: {floor_list[floorId]}
          </Text>
        </View>
      </View>
      <View style={styles.searchBar}>
        <SearchBar
          ref={s => (locationSearch = s)}
          value={search}
          style={styles.search}
          placeholder="Enter destination..."
          onChangeText={updateSearch}
          onCancel={() => setModalVisible(false)}
          onClear={() => {
            setModalVisible(false);
            setSearch('');
          }}
          lightTheme={true}
          searchIcon={<FontAwesomeIcon icon={faMagnifyingGlassLocation} />}
          clearIcon={
            <FontAwesomeIcon
              icon={faXmark}
              onPress={() => locationSearch.clear()}
            />
          }
          onPressIn={() => setModalVisible(true)}
        />

        {modalVisable ? (
          <SearchModal
            nearestNode={nearestNode}
            setDestination={setDestination}
            setModalVisible={setModalVisible}
            search={search}
          />
        ) : null}
      </View>
    </>
  );
};
