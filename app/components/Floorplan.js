import React, { useState, useContext, useEffect } from 'react';
import { Modal, Text, View } from 'react-native';
import { SearchBar } from 'react-native-elements';
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import { NetworkContext } from './NetworkProvider';

import {
  faAngleUp,
  faMagnifyingGlassLocation,
  faXmark,
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
  const [search, setSearch] = useState('');

  let locationSearch = React.createRef();

  const floor_set = new Set(polygons.map(f => f.level));
  const floor_list = [...floor_set].filter(f => f.indexOf(';') === -1).sort();

  const prevFloor = () => {
    setFloorId(floorId - 1 < 0 ? 0 : floorId - 1);
  };

  const nextFloor = () => {
    setFloorId(floorId + 1 < floor_list.length ? floorId + 1 : floorId);
  };

  const updateSearch = newSearch => {
    setSearch(newSearch);
  };

  return (
    <>
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
          position={{ position: 'absolute', top: 70, right: 0 }}
          onPress={nextFloor}
        />

        <MapButton
          icon={faAngleDown}
          position={{ position: 'absolute', top: 140, right: 0 }}
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
      <View style={{ position: 'absolute', top: 0, width: '100%' }}>
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
