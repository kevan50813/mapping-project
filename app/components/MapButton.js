import React from 'react';
import { Text, TouchableOpacity } from 'react-native';
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';

import { styles } from './styles';

export const MapButton = ({ icon, position, onPress }) => {
  return (
    <TouchableOpacity onPress={onPress} style={[styles.mapButton, position]}>
      <Text style={styles.mapButtonIcon}>
        <FontAwesomeIcon
          icon={icon}
          size={styles.mapButtonIcon.size}
          style={styles.mapButtonIcon}
        />
      </Text>
    </TouchableOpacity>
  );
};
