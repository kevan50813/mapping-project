export class Trilateration {
  static getNetworkKey = n => n.BSSID.slice(0, -1);

  trilaterate(networks) {
    let point = [-1, -1];
    let error = -1;

    return { point, error, networks };
  }

  constructor(visibleNetworks, knownNetworks) {
    // safeguard against null/undefined
    this.visibleNetworks = visibleNetworks ? visibleNetworks : [];
    this.knownNetworks = knownNetworks ? knownNetworks : [];

    this.commonNetworks = []; // networks we scanned that are in the JSON file networks
    this.usedNetworks = []; // networks used by the final trilateration
    this.predictedLocation = [-999, -999];

    // for each scanned network, map it to the corresponding read network
    // also embeds the coordinates of the AP for trilateration
    // output of this is placed into commonNetworks
    this.visibleNetworks.forEach(network => {
      // search for networks with same MAC/BSSID - this can return multiple, but they will all be from the same AP
      let other = this.knownNetworks.filter(n =>
        n.BSSID.startsWith(Trilateration.getNetworkKey(network)),
      );
      if (other.length > 0) {
        network.coordinates = other[0].coordinates;
        this.commonNetworks.push(network);
      }
    });
  }

  startTrilateration() {
    // trilat stuff
    // wrapping this in a parent function so we can potentially do more stuff with this
    // i.e. run multiple methods and take smallest error etc

    // data in form { point, error, networks }
    let data = this.firstThree();

    // do more processing maybe

    // finally set best attributes
    this.predictedLocation = data.point;
    this.usedNetworks = data.networks;
  }

  getUsedNetworks() {
    return this.usedNetworks;
  }

  getPredictedLocation() {
    return this.predictedLocation;
  }

  // ------- HEURISTICS --------------

  firstThree() {
    return this.trilaterate(
      this.commonNetworks.sort((a, b) => a.level - b.level).slice(0, 3),
    );
  }

  lastThree() {
    return this.trilaterate(
      this.commonNetworks.sort((a, b) => b.level - a.level).slice(0, 3),
    );
  }

  iterateAll() {}
}
