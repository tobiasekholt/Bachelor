    const base_url = 'https://ws.geonorge.no/transformering/v1/';

    async function getAvailableProjections() {
    const url = `${base_url}/projeksjoner`;
    const response = await fetch(url);
    const projections = await response.json();
    return projections;
    }

    async function transformSingleCoordinate(x, y, from_epsg, to_epsg) {
    const url = `${base_url}/transformer?x=${x}&y=${y}&fra=${from_epsg}&til=${to_epsg}`;
    const response = await fetch(url);
    const transformedCoordinate = await response.json();
    return transformedCoordinate;
    }

    async function transformMultipleCoordinates(coordinates, from_epsg, to_epsg) {
    const transformedCoordinates = [];
    for (const coordinate of coordinates) {
        const transformedCoordinate = await transformSingleCoordinate(
        coordinate.x,
        coordinate.y,
        from_epsg,
        to_epsg
        );
        transformedCoordinates.push(transformedCoordinate);
    }
    return transformedCoordinates;
    }

    async function transformCoordinates(coordinates, from_epsg, to_epsg) {
    if (!Array.isArray(coordinates) || coordinates.length === 0) {
        throw new Error('Invalid coordinates array');
    }

    if (coordinates.length === 1) {
        const { x, y } = coordinates[0];
        const transformedCoordinate = await transformSingleCoordinate(x, y, from_epsg, to_epsg);
        return [transformedCoordinate];
    }

    return transformMultipleCoordinates(coordinates, from_epsg, to_epsg);
    }

    module.exports = {
    getAvailableProjections,
    transformCoordinates
    };