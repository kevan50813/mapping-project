export function GetRotatedTriangle(x, y, rotation) {
  // Initial triangle coordinates.
  let xs = [-9, 9, 0];
  let ys = [-8, -8, 15];
  let tmp = [0, 0, 0];

  // Convert to radians.
  let angle = rotation * (Math.PI / 180);

  // Rotate triangle.
  for (let i = 0; i < 3; i++) {
    tmp[i] = Math.cos(angle) * xs[i] - Math.sin(angle) * ys[i];
    ys[i] = Math.sin(angle) * xs[i] + Math.cos(angle) * ys[i];
    xs[i] = tmp[i];
  }

  // Move the triangle to the current location.
  for (let i = 0; i < 3; i++) {
    xs[i] += x;
    ys[i] += y;
  }

  // Create points for <Polygon/>
  let points =
    xs[0] + ',' + ys[0] + ' ' + xs[1] + ',' + ys[1] + ' ' + xs[2] + ',' + ys[2];
  return points;
}

export function GetRotatedEquiTriangle(x, y, rotation) {
  // Initial triangle coordinates.
  let xs = [-13, 13, 0];
  let ys = [-13, -13, 13];
  let tmp = [0, 0, 0];

  // Convert to radians.
  let angle = rotation * (Math.PI / 180);

  // Rotate triangle.
  for (let i = 0; i < 3; i++) {
    tmp[i] = Math.cos(angle) * xs[i] - Math.sin(angle) * ys[i];
    ys[i] = Math.sin(angle) * xs[i] + Math.cos(angle) * ys[i];
    xs[i] = tmp[i];
  }

  // Move the triangle to the current location.
  for (let i = 0; i < 3; i++) {
    xs[i] += x;
    ys[i] += y;
  }

  // Create points for <Polygon/>
  let points =
    xs[0] + ',' + ys[0] + ' ' + xs[1] + ',' + ys[1] + ' ' + xs[2] + ',' + ys[2];
  return points;
}
