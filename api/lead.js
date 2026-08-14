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
  langue: 'vL1JGOmzLjyIyu7BFIIZ'
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

function customFieldsFromPayload(payload) {
  const custom = payload.custom || {};
  const lookingTo = custom.sellingMotivation === 'no_sell'
    ? 'Recevoir une évaluation gratuite'
    : 'Vendre une propriété';

  return [
    { id: FIELDS.message, fieldValue: payload.notes || '' },
    { id: FIELDS.raison, fieldValue: String(custom.sellingMotivation || '') },
    { id: FIELDS.timeline, fieldValue: `${custom.verdict || ''} ${custom.score != null ? `(${custom.score}/100)` : ''}`.trim() },
    { id: FIELDS.typeDeContact, fieldValue: 'Lead Vendeur' },
    { id: FIELDS.interessePar, fieldValue: lookingTo },
    { id: FIELDS.langue, fieldValue: 'Français' }
  ].filter((field) => field.fieldValue);
}

function tagsFromPayload(payload) {
  const verdict = payload.custom?.verdict || 'defavorable';
  return [
    'évaluation-timing',
    'Lead Vendeur',
    `verdict-${verdict}`,
    payload.leadType || 'evaluation'
  ];
}

async function addTags(contactId, tags) {
  try {
    await ghl(`/contacts/${contactId}/tags`, {
      method: 'POST',
      body: JSON.stringify({ tags })
    });
  } catch {
    // Existing contacts may already have tags. Do not fail the lead.
  }
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
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
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
        email,
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

    await addTags(contactId, tagsFromPayload(payload));
    await addNote(contactId, payload.notes);
    const opportunity = await createOpportunity(contactId, payload);

    json(res, 200, { stored: true, contactId, opportunity }, origin);
  } catch (error) {
    json(res, 502, { stored: false, error: 'CRM request failed' }, origin);
  }
};
