export const REGIONS = [
  { id: 'sherbrooke', name: 'Sherbrooke (centre-ville)' },
  { id: 'fleurimont', name: 'Fleurimont' },
  { id: 'lennoxville', name: 'Lennoxville' },
  { id: 'rock-forest', name: 'Rock Forest' },
  { id: 'deauville', name: 'Deauville' },
  { id: 'saint-elie-orford', name: 'Saint-Élie-d’Orford' },
  { id: 'brompton', name: 'Bromptonville (Brompton)' },
  { id: 'ascot', name: 'Ascot' },
  { id: 'mont-bellevue', name: 'Mont-Bellevue' },
  { id: 'magog', name: 'Magog' },
  { id: 'omerville', name: 'Omerville' },
  { id: 'orford', name: 'Orford (Canton d’Orford)' },
  { id: 'austin', name: 'Austin' },
  { id: 'eastman', name: 'Eastman' },
  { id: 'bolton-est', name: 'Bolton-Est' },
  { id: 'potton', name: 'Potton (Mansonville)' },
  { id: 'stanstead', name: 'Stanstead' },
  { id: 'canton-stanstead', name: 'Canton de Stanstead' },
  { id: 'ogden', name: 'Ogden' },
  { id: 'georgeville', name: 'Georgeville' },
  { id: 'ayers-cliff', name: 'Ayer’s Cliff' },
  { id: 'north-hatley', name: 'North Hatley' },
  { id: 'sainte-catherine-hatley', name: 'Sainte-Catherine-de-Hatley' },
  { id: 'hatley', name: 'Hatley' },
  { id: 'canton-hatley', name: 'Canton de Hatley' },
  { id: 'saint-benoit-du-lac', name: 'Saint-Benoît-du-Lac' },
  { id: 'coaticook', name: 'Coaticook' },
  { id: 'compton', name: 'Compton' },
  { id: 'waterville', name: 'Waterville' },
  { id: 'dixville', name: 'Dixville' },
  { id: 'martinville', name: 'Martinville' },
  { id: 'barnston-ouest', name: 'Barnston-Ouest' },
  { id: 'sainte-edwidge-clifton', name: 'Sainte-Edwidge-de-Clifton' },
  { id: 'saint-hermenegilde', name: 'Saint-Herménégilde' },
  { id: 'saint-malo', name: 'Saint-Malo' },
  { id: 'east-hereford', name: 'East Hereford' },
  { id: 'stanstead-est', name: 'Stanstead-Est' },
  { id: 'cookshire-eaton', name: 'Cookshire-Eaton' },
  { id: 'east-angus', name: 'East Angus' },
  { id: 'ascot-corner', name: 'Ascot Corner' },
  { id: 'weedon', name: 'Weedon' },
  { id: 'dudswell', name: 'Dudswell (Marbleton / Bishopton)' },
  { id: 'scotstown', name: 'Scotstown' },
  { id: 'bury', name: 'Bury' },
  { id: 'la-patrie', name: 'La Patrie' },
  { id: 'newport', name: 'Newport' },
  { id: 'lingwick', name: 'Lingwick' },
  { id: 'westbury', name: 'Westbury' },
  { id: 'saint-isidore-clifton', name: 'Saint-Isidore-de-Clifton' },
  { id: 'chartierville', name: 'Chartierville' },
  { id: 'hampden', name: 'Hampden' },
  { id: 'windsor', name: 'Windsor' },
  { id: 'val-joli', name: 'Val-Joli' },
  { id: 'richmond', name: 'Richmond' },
  { id: 'melbourne', name: 'Melbourne' },
  { id: 'cleveland', name: 'Cleveland' },
  { id: 'kingsbury', name: 'Kingsbury' },
  { id: 'stoke', name: 'Stoke' },
  { id: 'racine', name: 'Racine' },
  { id: 'saint-francois-xavier-brompton', name: 'Saint-François-Xavier-de-Brompton' },
  { id: 'saint-denis-brompton', name: 'Saint-Denis-de-Brompton' },
  { id: 'valcourt', name: 'Valcourt' },
  { id: 'canton-valcourt', name: 'Canton de Valcourt' },
  { id: 'bonsecours', name: 'Bonsecours' },
  { id: 'lawrenceville', name: 'Lawrenceville' },
  { id: 'maricourt', name: 'Maricourt' },
  { id: 'sainte-anne-rochelle', name: 'Sainte-Anne-de-la-Rochelle' },
  { id: 'ulverton', name: 'Ulverton' },
  { id: 'val-des-sources', name: 'Val-des-Sources (Asbestos)' },
  { id: 'danville', name: 'Danville' },
  { id: 'saint-georges-windsor', name: 'Saint-Georges-de-Windsor' },
  { id: 'saint-camille', name: 'Saint-Camille' },
  { id: 'saint-adrien', name: 'Saint-Adrien' },
  { id: 'wotton', name: 'Wotton' },
  { id: 'ham-sud', name: 'Ham-Sud' },
  { id: 'lac-megantic', name: 'Lac-Mégantic' },
  { id: 'weedon-lac', name: 'Lac-Drolet' },
  { id: 'sutton', name: 'Sutton' },
  { id: 'bromont', name: 'Bromont' },
  { id: 'lac-brome', name: 'Lac-Brome' }
];

function normalize(value) {
  return value
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}

export function findRegion(id) {
  return REGIONS.find((region) => region.id === id) || null;
}

export function searchRegions(query, limit = 8) {
  const needle = normalize(query.trim());
  if (!needle) return REGIONS.slice(0, limit);

  return REGIONS
    .map((region) => {
      const haystack = normalize(region.name);
      let rank = 0;
      if (haystack.startsWith(needle)) rank = 3;
      else if (haystack.includes(needle)) rank = 2;
      else if (normalize(region.id).includes(needle)) rank = 1;
      return { region, rank };
    })
    .filter((item) => item.rank > 0)
    .sort((a, b) => b.rank - a.rank || a.region.name.localeCompare(b.region.name, 'fr'))
    .slice(0, limit)
    .map((item) => item.region);
}
