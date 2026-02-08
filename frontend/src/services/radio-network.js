import axios from 'axios'
import proj4 from 'proj4';

/*******************
| Buildings height |
*******************/

const buildingsClient = axios.create({
    baseURL: 'https://data.geopf.fr/wfs/ows',
    headers: { 'Content-Type': 'application/json' }
});

export function getBuildings(coordinates, page = 0) {
    return buildingsClient.get('', {
        params: {
            service: 'WFS',
            version: '2.0.0',
            request: 'GetFeature',
            typeName: 'BDTOPO_V3:batiment',
            outputFormat: 'application/json',
            srsName: 'EPSG:4326',
            bbox: `${coordinates.minLng},${coordinates.minLat},${coordinates.maxLng},${coordinates.maxLat},EPSG:4326`,
            count: 5000,
            startIndex: page * 5000
        }
    });
}