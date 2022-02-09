import React from 'react';
import { ScrollView, View } from 'react-native';
import { styles } from './styles';
import Plot from 'react-native-plotly';

export const Trilateration = () => {
  const data = {
    x: [1, 2, 3, 4, 5],
    y: [1, 2, 3, 4, 8],
    type: 'scatter',
  };
  const layout = { width: 500, height: 500, title: 'Trilateration scatter plot' ,
    xaxis: {
      title: 'LAT',
    },
    yaxis: {
      title: 'LON',
    }
  };

  return (
    <View style={styles.background}>
      <ScrollView contentInsetAdjustmentBehavior="automatic">
        <Plot
          data={data}
          layout={layout}
          onLoad={() => console.log('graph loaded')}
        />
      </ScrollView>
    </View>
  );
  
};