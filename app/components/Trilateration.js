import LatLon from 'geodesy/latlon-nvector-spherical.js';

let a = -40;
let n = 2;
const rssiToDistance = rssi => Math.pow(10, (rssi - a) / (-10 * n));

export function trilateration(visibleNetworks, knownNetworks) {
  let commonNetworks = [];

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
        network.distance = rssiToDistance(network.RSSI);
        console.log(network);
        commonNetworks.push(network);
      }
    }
  });

  return startTrilateration(commonNetworks);
}

const getNetworkKey = network => network.BSSID.slice(0, -1);

function startTrilateration(networks) {
  // trilat stuff
  // wrapping this in a parent function so we can potentially do more stuff with this
  // i.e. run multiple methods and take smallest error etc

  // maybe turn every coordinates [] into LatLon first as going to be interating all of them many a time?

  // data in form { point, error, networks }
  let data = firstThree(networks);

  // do more processing maybe

  // finally set best attributes
  // defined like this for easier adaption in future
  return {
    usedNetworks: data.networks,
    predictedLocation: {
      point: data.pointArr,
      error: data.error,
    },
  };
}

function trilaterate(networks) {
  let error = -1;

  let points = networks.map(
    network => new LatLon(network.coordinates[0], network.coordinates[1]),
  );
  let distances = networks.map(network => network.distance);

  let point = LatLon.trilaterate(
    points[0],
    distances[0],
    points[1],
    distances[1],
    points[2],
    distances[2],
  );
  let pointArr = [-1, -1];

  console.log();
  console.log('TRILATERATING');
  try {
    pointArr = [point.lat, point.lon];
  } catch (e) {
    console.log(e);
  }
  console.log(point);

  return { pointArr, error, networks };
}

// --------- HEURISTICS ------------------------

function firstThree(networks) {
  return trilaterate(
    networks.sort((n1, n2) => n1.level - n2.level).slice(0, 3),
  );
}

/*
function lastThree(networks) {
  return trilaterate(networks.sort((a, b) => b.level - a.level).slice(0, 3));
}

function iterateAll(networks) {}
*/
