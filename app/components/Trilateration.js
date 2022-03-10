import LatLon from 'geodesy/latlon-nvector-spherical.js';

const rssiToDistance = (rssi, a, n) => Math.pow(10, (rssi - a) / (-10 * n));

export function trilateration(visibleNetworks, knownNetworks, a, n) {
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

  return startTrilateration(commonNetworks, predictedLevel);
}

const getNetworkKey = network => network.BSSID.slice(0, -1);

function startTrilateration(networks, level) {
  // trilat stuff
  // wrapping this in a parent function so we can potentially do more stuff with this
  // i.e. run multiple methods and take smallest error etc

  // maybe turn every coordinates [] into LatLon first as going to be iterating all of them many a time?

  if (networks.length < 3) {
    console.log('TRILAT ERR: not enough networks to trilaterate');
    return {
      usedNetworks: [],
      level: level,
      predictedLocation: {
        point: [-1, -1],
        error: -1,
      },
    };
  }

  //let data_all = iterateAll(networks);
  //let data_last = lastThree(networks);
  let data_first = firstThree(networks);

  // do more processing maybe

  let data = data_first;

  /*
  data.networks.forEach(n => {
    console.log(n);
  }); */

  // finally set best attributes
  // defined like this for easier adaption in future
  return {
    usedNetworks: data.networks,
    predictedLocation: {
      point: data.pointArr,
      level: level,
      error: data.error,
    },
  };
}

//imlemntion of Haversine formula that finds the distace between 2 latlon points and returns its distace in meters
function latlonToMeters(lat1, lon1, lat2, lon2) {
  // generally used geo measurement function
  let Radius = 6378.137; // Radius of earth in KM
  let dLat = (lat2 * Math.PI) / 180 - (lat1 * Math.PI) / 180; // lat disatnces
  let dLon = (lon2 * Math.PI) / 180 - (lon1 * Math.PI) / 180; // lon distances
  let a = //first part of Haversine formula
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a)); // last part of Haversine formula, in order to make it neater
  let distance = Radius * c * 1000; // calulate default is in km, so is converted to meters here
  return distance;
}

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

function firstThree(networks) {
  return trilaterate(networks.slice(0, 3));
}

function lastThree(networks) {
  return trilaterate(networks.slice(0, -3));
}

function iterateAll(networks) {
  let combinations = 0;
  let predictedSum = [0, 0];

  for (let i = 0; i < networks.length - 2; i++) {
    for (let j = i + 1; j < networks.length - 1; j++) {
      for (let k = j + 1; k < networks.length; k++) {
        let triplet = [networks[i], networks[j], networks[k]];

        let data = trilaterate(triplet);
        if (data.pointArr[0] !== -1) {
          predictedSum[0] += data.pointArr[0];
          predictedSum[1] += data.pointArr[1];
          combinations++;
        }
      }
    }
  }

  //console.log('----------------');
  //console.log(predictedSum);
  //console.log(combinations);
  let averagePoint = [
    predictedSum[0] / combinations,
    predictedSum[1] / combinations,
  ];
  return { pointArr: averagePoint, error: -1, networks: [] };
}
