import React, { useState, Component } from 'react';
import * as d3 from 'd3';
import polygons from './Polygons.json'; // assert { type: 'json' }
import { Svg, G, Path } from 'react-native-svg';
import { Button, View } from 'react-native';
import { Circle } from 'react-native-svg';
import SvgPanZoom, { SvgPanZoomElement } from 'react-native-svg-pan-zoom';

const features = polygons.features;
const rooms = features.map(f => f.geometry.coordinates[0]);
const floor_set = new Set(features.map(f => f.properties.level));
const floor_list = [...floor_set].filter(f => f.indexOf(';') === -1).sort();

const minX = rooms.reduce(
  (m, room) => Math.min(m, ...room.map(r => r[0])),
  Infinity,
);
const maxX = rooms.reduce(
  (m, room) => Math.max(m, ...room.map(r => r[0])),
  -Infinity,
);
const minY = rooms.reduce(
  (m, room) => Math.min(m, ...room.map(r => r[1])),
  Infinity,
);
const maxY = rooms.reduce(
  (m, room) => Math.max(m, ...room.map(r => r[1])),
  -Infinity,
);

//const map = d3.select('#d3').append('svg').attr('width', W).attr('height', H)

/*
map
  .selectAll('path')
  .data(features)
  .enter()
  .append('path')
  .attr('d', path)
  .attr('opacity', '0.5')
  .attr('fill', (room) =>
    room.properties.type === 'Room' ? 'lightblue' : 'none'
  )
  .attr('stroke', (room) =>
    room.properties.type === 'Room' ? 'blue' : 'black'
  )
*/

export const Floorplan = () => {
  const [floorId, setFloorId] = useState(2);

  const prevFloor = () => {
    setFloorId(floorId - 1 < 0 ? 0 : floorId - 1);
  };

  const nextFloor = () => {
    setFloorId(floorId + 1 < floor_list.length ? floorId + 1 : floorId);
  };

  const W = 640;
  const H = 480;
  const scaleX = d3.scaleLinear([minX, maxX], [20, 620]);
  const scaleY = d3.scaleLinear([minY, maxY], [460, 20]);
  const projection = d3.geoEquirectangular().fitSize([W / 2, H / 2], polygons);
  const path = d3.geoPath().projection(projection);

  return (
    <>
      <SvgPanZoom
        canvasHeight  = {500}
        canvasWidth   = {500}
        minScale      = {0.1}
        maxScale      = {2}
        initialZoom   = {0.7}
      >
        <SvgPanZoomElement>
          <G>
          {features.map((feature, index) => {
            if (feature.properties.level == floor_list[floorId]) {
              return (
                <Path
                  d={path(feature)}
                  key={index}
                  opacity={0.2}
                  fill={
                    feature.properties.type === 'Room' ? 'lightblue' : 'none'
                  }
                  stroke={feature.properties.type === 'Room' ? 'blue' : 'black'}
                />
              );
            }
          })}
        </G>
      </SvgPanZoomElement>
    </SvgPanZoom>
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
