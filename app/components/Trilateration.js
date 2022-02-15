export function trilateration(visibleNetworks, knownNetworks) {
  let commonNetworks = [];

  // for each scanned network, map it to the corresponding read network
  // also embeds the coordinates of the AP for trilateration
  // output of this is placed into commonNetworks
  visibleNetworks.forEach(network => {
    // search for networks with same MAC/BSSID - this can return multiple, but they will all be from the same AP
    let other = knownNetworks.filter(n =>
      n.BSSID.startsWith(getNetworkKey(network)),
    );
    if (other.length > 0) {
      network.coordinates = other[0].coordinates;
      commonNetworks.push(network);
    }
  });

  return startTrilateration(commonNetworks);
}

const getNetworkKey = n => n.BSSID.slice(0, -1);

function startTrilateration(networks) {
  // trilat stuff
  // wrapping this in a parent function so we can potentially do more stuff with this
  // i.e. run multiple methods and take smallest error etc

  // data in form { point, error, networks }
  let data = firstThree(networks);

  // do more processing maybe

  // finally set best attributes
  // defined like this for easier adaption in future
  return {
    usedNetworks: data.networks,
    predictedLocation: {
      point: data.point,
      error: data.error,
    },
  };
}

function trilaterate(networks) {
  let point = [-1, -1];
  let error = -1;

  return { point, error, networks };
}

// --------- HEURISTICS ------------------------

function firstThree(networks) {
  return trilaterate(networks.sort((a, b) => a.level - b.level).slice(0, 3));
}

/*
function lastThree(networks) {
  return trilaterate(networks.sort((a, b) => b.level - a.level).slice(0, 3));
}

function iterateAll(networks) {}
*/
