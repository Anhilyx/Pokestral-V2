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

/**************
| Roads speed |
**************/

const roadsClient = axios.create({
    baseURL: 'https://overpass-api.de/api',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
});

export function getRoads(coordinates) {
    const bbox = `${coordinates.minLat},${coordinates.minLng},${coordinates.maxLat},${coordinates.maxLng}`;
    const query = `[out:json][timeout:25];(way["highway"](${bbox}););out body;>;out skel qt;`;
    return roadsClient.post('/interpreter', `data=${encodeURIComponent(query)}`);
}

/*********************
| Population density |
*********************/

const populationClient = axios.create({
    baseURL: 'https://geo.api.gouv.fr',
    headers: { 'Content-Type': 'application/json' }
});

export function getPopulation(coordinates) {
    // Calcul du centre de la bounding box pour interroger l'API
    const centerLat = (coordinates.minLat + coordinates.maxLat) / 2;
    const centerLng = (coordinates.minLng + coordinates.maxLng) / 2;

    return populationClient.get('/communes', {
        params: {
            lat: centerLat,
            lon: centerLng,
            fields: 'nom,population,surface',
            format: 'json',
            geometry: 'centre'
        }
    });
}