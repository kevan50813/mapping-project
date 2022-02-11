import { Network } from './Scan';

export class TrilaterationHeuristics {
  static firstThree(networks) {
    const index = [0, 1, 2];

    // do trilateration
    let point = Trilateration.trilaterate(
      networks[index[0]],
      networks[index[1]],
      networks[index[2]],
    );

    for (let i in index) {
      networks[i].type = Network.USED;
    }

    return {
      networks: networks,
      point: point,
    };
  }
}

export class Trilateration {
  trilaterate(n1, n2, n3) {
    let point = [];

    return point;
  }
}
