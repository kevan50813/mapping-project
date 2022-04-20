import React, { useState, useEffect, useRef } from 'react';
import { useDeviceMotion } from '@use-expo/sensors';
import { useNavigation } from '@react-navigation/native';
import { FileSystem } from 'react-native-file-access';
import {
  TouchableOpacity,
  BackHandler,
  Text,
  View,
  Vibration,
} from 'react-native';
import { SearchBar } from 'react-native-elements';
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import RNReactLogging from 'react-native-file-log';
import Toast from 'react-native-simple-toast';

import {
  faAngleUp,
  faMagnifyingGlassLocation,
  faXmark,
  faAngleDown,
  faTags,
  faLocationDot,
  faMapLocation,
  faMapLocationDot,
} from '@fortawesome/free-solid-svg-icons';

import { styles } from './styles';
import { MapButton } from './MapButton';
import { SearchModal } from './SearchModal';
import { DrawMap } from './DrawMap';

export const Floorplan = ({
  polygons,
  geoJson,
  setDestination,
  destination,
  currentPath,
  scan,
  predictedLocation,
  nearestNode,
}) => {
  const [floorId, setFloorId] = useState(0);
  const [modalVisable, setModalVisible] = useState(false);
  const [search, setSearch] = useState('');
  const [showLabels, setShowLabels] = useState(false);
  const [showPoIs, setShowPoIs] = useState(false);
  const [showWifi, setShowWifi] = useState(false);
  const [following, setFollowing] = useState(true);
  const navigation = useNavigation();
  const [accData, accAvailable] = useDeviceMotion({ interval: 1000 });
  const moving = useRef(false);
  const motion = useRef({ x: 0, y: 0, z: 0 });
  RNReactLogging.setTag('FLOORPLAN');

  let locationSearch = React.createRef();

  const floor_set = new Set(polygons.map(f => f.level));
  const floor_list = [...floor_set].filter(f => f.indexOf(';') === -1).sort();

  useEffect(() => {
    const timer = setTimeout(() => scan(), 5000);
    return () => clearTimeout(timer);
  }, [scan]);

  if (accAvailable && accData && accData.acceleration) {
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

  const backAction = () => {
    if (modalVisable) {
      setModalVisible(false);
      return true;
    }
    // navigation.pop();
    return true;
  };

  BackHandler.addEventListener('hardwareBackPress', backAction);

  const prevFloor = () => {
    Vibration.vibrate(20);
    RNReactLogging.printLog('User down floor');
    setFloorId(floorId - 1 < 0 ? 0 : floorId - 1);
    setFollowing(false);
  };

  const nextFloor = () => {
    Vibration.vibrate(20);
    RNReactLogging.printLog('User up floor');
    setFloorId(floorId + 1 < floor_list.length ? floorId + 1 : floorId);
    setFollowing(false);
  };

  const updateSearch = newSearch => {
    RNReactLogging.printLog('Updated search');
    setSearch(newSearch);
  };

  const saveLog = async () => {
    RNReactLogging.setTag('LOG SAVE');
    RNReactLogging.printLog(`Saving Log at ${Date.now()}`);
    RNReactLogging.listAllLogFiles().then(paths => {
      var decodedURL = decodeURIComponent(paths[0]);
      const fileName = 'LOG_' + Date.now() + '.txt';
      FileSystem.cpExternal(decodedURL, fileName, 'downloads').then(
        console.log('Saved Log'),
      );
      FileSystem.unlink(decodedURL).then(console.log('Deleted old log'));
    });
  };

  useEffect(() => {
    if (
      predictedLocation.level !== undefined &&
      predictedLocation.level !== -1 &&
      floor_list.indexOf(predictedLocation.level.toString()) === floorId
    ) {
      setFollowing(true);
    }

    if (
      predictedLocation.level !== undefined &&
      predictedLocation.level !== -1 &&
      following
    ) {
      if (floor_list.indexOf(predictedLocation.level.toString()) !== floorId) {
        Toast.show(`Changed floor to ${predictedLocation.level}`);
        setFloorId(floor_list.indexOf(predictedLocation.level.toString()));
      }
    }
  }, [floor_list, following, predictedLocation.level]);

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
          showWifi={showWifi}
          destination={destination}
        />

        <MapButton
          icon={faTags}
          position={{ position: 'absolute', top: 70, left: 0 }}
          onPress={() => {
            Vibration.vibrate(20);
            setShowLabels(!showLabels);
          }}
        />

        <MapButton
          icon={faLocationDot}
          position={{ position: 'absolute', top: 140, left: 0 }}
          onPress={() => {
            Vibration.vibrate(20);
            setShowPoIs(!showPoIs);
          }}
          onLongPress={() => {
            Vibration.vibrate(50);
            setShowWifi(!showWifi);
          }}
        />

        <MapButton
          icon={faAngleUp}
          position={{ position: 'absolute', top: 70, right: 0 }}
          onPress={nextFloor}
        />

        <MapButton
          icon={faAngleDown}
          position={{ position: 'absolute', top: 140, right: 0 }}
          onPress={prevFloor}
        />

        <View style={styles.levelView}>
          <TouchableOpacity onLongPress={saveLog}>
            <Text style={[styles.big, styles.levelViewText]}>
              Level: {floor_list[floorId]}
            </Text>
          </TouchableOpacity>
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
