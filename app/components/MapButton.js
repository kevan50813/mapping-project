import React from 'react';
import { Text, TouchableOpacity } from 'react-native';
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';

import { styles } from './styles';

export const MapButton = ({ icon, position, onPress, onLongPress, text }) => {
  return (
    <TouchableOpacity
      onPress={onPress}
      onLongPress={onLongPress}
      style={[styles.mapButton, position]}>
      <Text style={styles.mapButtonIcon}>
        {icon ? (
          <FontAwesomeIcon
            icon={icon}
            size={styles.mapButtonIconSvg.size}
            style={styles.mapButtonIcon}
          />
        ) : null}

        {text ? text : null}
      </Text>
    </TouchableOpacity>
  );
};
