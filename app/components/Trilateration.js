import LatLon from 'geodesy/latlon-nvector-spherical.js';

const rssiToDistance = (rssi, a, n) => Math.pow(10, (rssi - a) / (-10 * n));

export function trilateration(
  visibleNetworks,
  knownNetworks,
  a,
  n,
  oldPredictedLocation,
) {
  let commonNetworks = [];

  // count of networks on each floor
  let levelCount = [0, 0, 0, 0, 0, 0];

  // for each scanned network, map it to the corresponding read network
  // also embeds the coordinates of the AP for trilateration
  // output of this is placed into commonNetworks
  visibleNetworks.forEach(network => {
    // dont add duplicate networks from same AP
    // this duplicate data completely breaks trilat 90% of the time
    if (
      commonNetworks.filter(net => net.BSSID.startsWith(getNetworkKey(network)))
        .length === 0
    ) {
      // search for networks with same MAC/BSSID - this can return multiple, but they will all be from the same AP
      // this is fine as we only care about its location
      let findKnown = knownNetworks.filter(net =>
        net.BSSID.startsWith(getNetworkKey(network)),
      );
      if (findKnown.length > 0) {
        network.coordinates = findKnown[0].coordinates;
        network.distance = rssiToDistance(network.RSSI, a, n);
        network.level = findKnown[0].level;
        levelCount[network.level] += 1;
        commonNetworks.push(network);
      }
    }
  });

  // get level with the most networks on it
  let predictedLevel = levelCount.indexOf(Math.max.apply(null, levelCount));

  // sort in order of ascending distance from user
  commonNetworks.sort((n1, n2) => n1.distance - n2.distance);

  return startTrilateration(
    commonNetworks,
    predictedLevel,
    oldPredictedLocation,
  );
}

const getNetworkKey = network => network.BSSID.slice(0, -1);

function startTrilateration(networks, level, oldPredictedLocation) {
  // trilat stuff
  // wrapping this in a parent function so we can potentially do more stuff with this
  // i.e. run multiple methods and take smallest error etc

  // maybe turn every coordinates [] into LatLon first as going to be iterating all of them many a time?
  if (networks.length < 3) {
    console.log('TRILAT ERR: not enough networks to trilaterate');
    if (oldPredictedLocation === { point: [] }) {
      return {
        usedNetworks: [],
        predictions: [],
        predictedLocation: {
          point: [-1, -1],
          level: -1,
          error: -1,
          old: true,
        },
      };
    }

    oldPredictedLocation.old = true;
    return {
      usedNetworks: [],
      predictions: [],
      predictedLocation: oldPredictedLocation,
    };
  }

  let data = iterateAll(networks, true);

  // finally set best attributes
  // defined like this for easier adaption in future
  return {
    usedNetworks: data.networks,
    predictions: data.predictions,
    predictedLocation: {
      point: data.pointArr,
      level: level,
      error: data.error,
      old: false,
    },
  };
}

//imlemntion of Haversine formula that finds the distace between 2 latlon points and returns its distace in meters
// function latlonToMeters(lat1, lon1, lat2, lon2) {
//   // generally used geo measurement function
//   let Radius = 6378.137; // Radius of earth in KM
//   let dLat = (lat2 * Math.PI) / 180 - (lat1 * Math.PI) / 180; // lat disatnces
//   let dLon = (lon2 * Math.PI) / 180 - (lon1 * Math.PI) / 180; // lon distances
//   let a = //first part of Haversine formula
//     Math.sin(dLat / 2) * Math.sin(dLat / 2) +
//     Math.cos((lat1 * Math.PI) / 180) *
//       Math.cos((lat2 * Math.PI) / 180) *
//       Math.sin(dLon / 2) *
//       Math.sin(dLon / 2);
//   let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a)); // last part of Haversine formula, in order to make it neater
//   let predDistance = Radius * c * 1000; // calulate default is in km, so is converted to meters here
//   return predDistance;
// }

function trilaterate(networks) {
  let error = -1;
  let pointArr = [-1, -1];

  //console.log(networks);

  let points = networks.map(
    network => new LatLon(network.coordinates[0], network.coordinates[1]),
  );
  let distances = networks.map(network => network.distance);

  try {
    let point = LatLon.trilaterate(
      points[0],
      distances[0],
      points[1],
      distances[1],
      points[2],
      distances[2],
    );
    pointArr = [point.lat, point.lon];
  } catch (e) {
    console.log('TRILAT ERR: ' + e);
  }

  return { pointArr, error, networks };
}

// --------- HEURISTICS ------------------------

// function firstThree(networks) {
//   return trilaterate(networks.slice(0, 3));
// }

// function lastThree(networks) {
//   return trilaterate(networks.slice(0, -3));
// }

function iterateAll(networks, visualise) {
  let allPoints = [];

  for (let i = 0; i < networks.length - 2; i++) {
    for (let j = i + 1; j < networks.length - 1; j++) {
      for (let k = j + 1; k < networks.length; k++) {
        let triplet = [networks[i], networks[j], networks[k]];

        let data = trilaterate(triplet);
        if (data.pointArr[0] !== -1) {
          allPoints.push(data.pointArr);
        }
      }
    }
  }

  let sdCount = 2;
  let pointDifference = 999;

  // console.log('\n\nNETWORK COUNT: ' + networks.length);

  do {
    let originalPointCount = allPoints.length;
    let statData = getStats(allPoints);

    let newPoints = allPoints.filter(point => {
      return distance(statData.avg, point) < sdCount * statData.sd;
    });

    pointDifference = originalPointCount - newPoints.length;

    // if its going to empty the point array, quit out of the loop so we dont divide by 0
    if (pointDifference !== allPoints.length) {
      allPoints = newPoints;
    } else {
      pointDifference = 0;
    }
  } while (pointDifference !== 0);

  let sum = allPoints.reduce((a, b) => [a[0] + b[0], a[1] + b[1]], [0, 0]);
  let averagePoint = [sum[0] / allPoints.length, sum[1] / allPoints.length];

  return {
    pointArr: averagePoint,
    error: -1,
    networks: [],
    predictions: visualise ? allPoints : [],
  };
}

function getStats(dataArr) {
  let sum = dataArr.reduce((a, b) => [a[0] + b[0], a[1] + b[1]]);
  let avg = [sum[0] / dataArr.length, sum[1] / dataArr.length];

  let sumErrSq = dataArr
    .map(point => Math.pow(distance(point, avg), 2))
    .reduce((a, b) => a + b);

  let variance = sumErrSq / dataArr.length;
  let sd = Math.sqrt(variance);

  return {
    avg: avg,
    sd: sd,
  };
}

function distance(point1, point2) {
  return Math.sqrt(
    Math.pow(point1[0] - point2[0], 2) + Math.pow(point1[1] - point2[1], 2),
  );
}
