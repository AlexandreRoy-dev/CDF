const LOCATION_ID = process.env.GHL_LOCATION_ID || 'MJs18WfGQbOuO6E9SzIJ';
const PIPELINE_ID = process.env.GHL_PIPELINE_ID || 'Ucqx5cCwaC2nPYP6FBsD';
const PIPELINE_STAGE_ID = process.env.GHL_PIPELINE_STAGE_ID || 'c3a9748c-c1d2-431a-b3f8-076b486ec6b9';
const GHL_BASE = 'https://services.leadconnectorhq.com';
const GHL_VERSION = '2021-07-28';

const FIELDS = {
  message: 'T9wpOOLRk5ACYlgPHmm5',
  raison: 'ahIrcCe03xROz3TMXxrh',
  timeline: 'yYB06uYc7V0OTBwylVdY',
  typeDeContact: '4zQR0GZQZLCMujxJyRNr',
  interessePar: 'qxdLPECH3T0E9GfCjqi9',
  langue: 'vL1JGOmzLjyIyu7BFIIZ',
  propertyType: '2dCSk0tB9HRRknAKMUo0',
  estimatedValue: 'Pn3F2SUInFPvlh8gaoGt',
  hasContract: 'Ziu6VlGXCFzjUXNPXZ5I',
  yearsOwned: 'gVlaNphtDqMkojnO4YYB',
  financialProfile: 'hI1spxaKjr4xKwxVZRWF',
  verdict: 'juOYr3h0BYDWV0oqobO0',
  hasChildren: 'lblu9G2ZuVDHN1drQFZm',
  score: 'q2aAqIwfD7l3CvYMi3sa'
};

const ALLOWED_ORIGINS = [
  'https://chiassondefrancesco.ca',
  'https://www.chiassondefrancesco.ca',
  'http://localhost:3000',
  'http://localhost:4173',
  'http://localhost:5173',
  'http://127.0.0.1:3000',
  'http://127.0.0.1:4173',
  'http://127.0.0.1:5500'
];

function cors(origin) {
  const allow = ALLOWED_ORIGINS.includes(origin) || (origin && origin.endsWith('.vercel.app'));
  return {
    'Access-Control-Allow-Origin': allow ? origin : ALLOWED_ORIGINS[0],
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400'
  };
}

async function readBody(req) {
  if (req.body && typeof req.body === 'object' && !Buffer.isBuffer(req.body)) {
    return req.body;
  }
  if (typeof req.body === 'string') {
    return req.body ? JSON.parse(req.body) : {};
  }
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  const raw = Buffer.concat(chunks).toString('utf8').trim();
  return raw ? JSON.parse(raw) : {};
}

function json(res, status, body, origin) {
  const headers = { 'Content-Type': 'application/json', ...cors(origin) };
  res.writeHead(status, headers);
  res.end(JSON.stringify(body));
}

function normalizePhone(raw) {
  const digits = String(raw || '').replace(/\D/g, '');
  if (digits.length === 10) return `+1${digits}`;
  if (digits.length === 11 && digits.startsWith('1')) return `+${digits}`;
  if (String(raw || '').startsWith('+') && digits.length >= 10) return `+${digits}`;
  return '';
}

function ghlHeaders() {
  const token = process.env.GHL_PIT;
  if (!token) throw new Error('missing_token');
  return {
    Authorization: `Bearer ${token}`,
    Version: GHL_VERSION,
    Accept: 'application/json',
    'Content-Type': 'application/json'
  };
}

async function ghl(path, options = {}) {
  const response = await fetch(`${GHL_BASE}${path}`, {
    ...options,
    headers: { ...ghlHeaders(), ...(options.headers || {}) }
  });
  const text = await response.text();
  let data = {};
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { raw: text };
  }
  if (!response.ok) {
    const error = new Error(`ghl_${response.status}`);
    error.status = response.status;
    error.details = data;
    throw error;
  }
  return data;
}

const MOTIVATION_LABELS = {
  upsize: 'Passer à plus grand',
  downsize: 'Réduire ou simplifier',
  relocation: 'Déménager ailleurs',
  no_sell: 'Curiosité, sans projet de vente'
};

const VERDICT_LABELS = {
  favorable: 'Moment idéal',
  moyen: 'Prêt à vendre',
  defavorable: 'Pas encore prêt'
};

const PROPERTY_LABELS = {
  maison: 'Maison unifamiliale',
  condo: 'Condo',
  plex: 'Plex',
  chalet: 'Chalet'
};

const FINANCIAL_LABELS = {
  salarie: 'Salarié',
  autonome: 'Autonome',
  entrepreneur: 'Entrepreneur',
  placements: 'Placements',
  retraite: 'Retraité',
  transition: 'En transition'
};

function addField(fields, id, value) {
  if (value === undefined || value === null || value === '') return;
  fields.push({ id, fieldValue: value });
}

function yesNo(value) {
  if (value === true || value === 'Oui' || value === 'oui') return 'Oui';
  if (value === false || value === 'Non' || value === 'non') return 'Non';
  return '';
}

function customFieldsFromPayload(payload) {
  const custom = payload.custom || {};
  const isQuiz = payload.leadType !== 'widget-message';
  const lookingTo = custom.sellingMotivation === 'no_sell'
    ? 'Recevoir une évaluation gratuite'
    : 'Vendre une propriété';
  const motivation = MOTIVATION_LABELS[custom.sellingMotivation] || custom.sellingMotivation || '';
  const verdict = VERDICT_LABELS[custom.verdict] || '';
  const scoreNumber = Number(custom.score);
  const scoreLabel = Number.isFinite(scoreNumber) ? `${scoreNumber}/100` : '';
  const timeline = [verdict, scoreLabel].filter(Boolean).join(' · ');
  const yearsOwned = Number(custom.yearsOwned);
  const estimatedValue = Number(custom.estimatedValue);
  const fields = [];

  addField(fields, FIELDS.message, payload.notes || '');
  addField(fields, FIELDS.raison, motivation);
  addField(fields, FIELDS.timeline, timeline);
  addField(fields, FIELDS.typeDeContact, 'Lead Vendeur');
  addField(fields, FIELDS.langue, 'Français');

  if (isQuiz) {
    addField(fields, FIELDS.interessePar, lookingTo);
    addField(fields, FIELDS.propertyType, PROPERTY_LABELS[custom.propertyType] || '');
    addField(fields, FIELDS.yearsOwned, Number.isFinite(yearsOwned) ? yearsOwned : '');
    addField(fields, FIELDS.estimatedValue, Number.isFinite(estimatedValue) && estimatedValue > 0 ? estimatedValue : '');
    addField(fields, FIELDS.verdict, verdict);
    addField(fields, FIELDS.score, Number.isFinite(scoreNumber) ? scoreNumber : '');
    addField(fields, FIELDS.hasContract, yesNo(custom.hasContract));
    addField(fields, FIELDS.hasChildren, yesNo(custom.hasChildren));
    addField(fields, FIELDS.financialProfile, FINANCIAL_LABELS[custom.financialProfile] || '');
  }

  return fields;
}

const FORM_EVAL_TAG = 'form-eval';

function tagsFromPayload(payload) {
  const tags = new Set([FORM_EVAL_TAG]);
  if (Array.isArray(payload.tags)) {
    payload.tags.filter(Boolean).forEach((tag) => tags.add(tag));
  }
  tags.add('évaluation-timing');
  tags.add('Lead Vendeur');
  if (payload.leadType) tags.add(payload.leadType);
  if (payload.leadType !== 'widget-message' && payload.custom?.verdict) {
    tags.add(`verdict-${payload.custom.verdict}`);
  }
  return [...tags];
}

async function addTags(contactId, tags) {
  await ghl(`/contacts/${contactId}/tags`, {
    method: 'POST',
    body: JSON.stringify({ tags })
  });
}

async function addNote(contactId, body) {
  if (!body) return;
  try {
    await ghl(`/contacts/${contactId}/notes`, {
      method: 'POST',
      body: JSON.stringify({ body })
    });
  } catch {
    // Notes scope is optional on some PITs.
  }
}

async function createOpportunity(contactId, payload) {
  const name = `Évaluation timing - ${payload.name || payload.firstName || 'Sans nom'}`;
  const value = Number(payload.custom?.estimatedValue);
  try {
    await ghl('/opportunities/', {
      method: 'POST',
      body: JSON.stringify({
        locationId: LOCATION_ID,
        pipelineId: PIPELINE_ID,
        pipelineStageId: PIPELINE_STAGE_ID,
        contactId,
        name,
        status: 'open',
        source: payload.source || 'Évaluation timing vente',
        monetaryValue: Number.isFinite(value) && value > 0 ? value : undefined
      })
    });
    return true;
  } catch {
    return false;
  }
}

module.exports = async function handler(req, res) {
  const origin = req.headers.origin || '';

  if (req.method === 'OPTIONS') {
    res.writeHead(204, cors(origin));
    res.end();
    return;
  }

  if (req.method !== 'POST') {
    json(res, 405, { stored: false, error: 'Method not allowed' }, origin);
    return;
  }

  let payload;
  try {
    payload = await readBody(req);
  } catch {
    json(res, 400, { stored: false, error: 'Invalid JSON' }, origin);
    return;
  }

  if (!payload || typeof payload !== 'object') {
    json(res, 400, { stored: false, error: 'Missing body' }, origin);
    return;
  }

  if (payload.website) {
    json(res, 200, { stored: false, ignored: true }, origin);
    return;
  }

  const email = String(payload.email || '').trim();
  const phone = normalizePhone(payload.phone);
  const firstName = String(payload.firstName || '').trim();
  const lastName = String(payload.lastName || '').trim();

  if (!firstName) {
    json(res, 400, { stored: false, error: 'Name required' }, origin);
    return;
  }
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    json(res, 400, { stored: false, error: 'Invalid email' }, origin);
    return;
  }
  if (!phone) {
    json(res, 400, { stored: false, error: 'Invalid phone' }, origin);
    return;
  }
  if (!payload.consent) {
    json(res, 400, { stored: false, error: 'Consent required' }, origin);
    return;
  }

  if (!process.env.GHL_PIT) {
    json(res, 500, { stored: false, error: 'Server not configured' }, origin);
    return;
  }

  try {
    const upserted = await ghl('/contacts/upsert', {
      method: 'POST',
      body: JSON.stringify({
        locationId: LOCATION_ID,
        firstName,
        lastName: lastName || undefined,
        name: payload.name || `${firstName} ${lastName}`.trim(),
        email: email || undefined,
        phone,
        city: payload.city || undefined,
        state: 'QC',
        country: 'CA',
        source: payload.source || 'Évaluation timing vente',
        timezone: 'America/New_York',
        customFields: customFieldsFromPayload(payload)
      })
    });

    const contact = upserted.contact || upserted;
    const contactId = contact.id;
    if (!contactId) {
      json(res, 502, { stored: false, error: 'Contact not returned' }, origin);
      return;
    }

    let tagged = false;
    try {
      await addTags(contactId, tagsFromPayload(payload));
      tagged = true;
    } catch {
      try {
        await addTags(contactId, [FORM_EVAL_TAG]);
        tagged = true;
      } catch {
        tagged = false;
      }
    }
    await addNote(contactId, payload.notes);
    const opportunity = await createOpportunity(contactId, payload);

    json(res, 200, { stored: true, contactId, tagged, opportunity }, origin);
  } catch (error) {
    json(res, 502, { stored: false, error: 'CRM request failed' }, origin);
  }
};
