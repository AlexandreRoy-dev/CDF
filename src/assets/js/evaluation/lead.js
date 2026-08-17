import { formatAnswersForCrm } from './score.js';
import { findRegion } from './regions.js';

export const LEAD_CONFIG = {
  source: 'Évaluation timing vente',
  formName: 'CDF evaluation timing',
  endpoint: (typeof window !== 'undefined' && window.CDF_LEAD_ENDPOINT) || '/api/lead'
};

function readUtms() {
  const params = new URLSearchParams(window.location.search);
  const keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'fbclid', 'gclid'];
  const utm = {};
  keys.forEach((key) => {
    const value = params.get(key);
    if (value) utm[key] = value;
  });
  return utm;
}

function splitName(fullName) {
  const parts = fullName.trim().split(/\s+/);
  return {
    firstName: parts[0] || '',
    lastName: parts.slice(1).join(' ') || ''
  };
}

export function buildLeadPayload({ name, email, phone, consent, answers, analysis, leadType }) {
  const { firstName, lastName } = splitName(name);
  const region = findRegion(answers.region);
  const utm = readUtms();
  const verdict = analysis?.scoring?.verdict || 'defavorable';

  return {
    firstName,
    lastName,
    name: name.trim(),
    email: email.trim(),
    phone: phone.trim(),
    city: region ? region.name : '',
    source: LEAD_CONFIG.source,
    tags: ['form-eval', LEAD_CONFIG.source, `verdict-${verdict}`, leadType].filter(Boolean),
    consent,
    leadType,
    landingPage: window.location.href.split('?')[0],
    utm,
    custom: {
      verdict,
      score: analysis?.scoring?.score ?? null,
      propertyType: answers.propertyType || '',
      sellingMotivation: answers.sellingMotivation || '',
      yearsOwned: answers.yearsOwned ?? '',
      estimatedValue: answers.estimatedValue ?? '',
      region: region ? region.name : answers.region || '',
      hasContract: answers.hasContract === true ? 'Oui' : 'Non'
    },
    notes: [
      `Formulaire: ${LEAD_CONFIG.formName}`,
      `Verdict: ${analysis?.scoring?.label || 'n/d'} (${analysis?.scoring?.score ?? 'n/d'}/100)`,
      '',
      formatAnswersForCrm(answers)
    ].join('\n')
  };
}

export function buildWidgetMessagePayload({ name, email, phone, message, consent }) {
  const { firstName, lastName } = splitName(name);
  const utm = readUtms();

  return {
    firstName,
    lastName,
    name: name.trim(),
    email: (email || '').trim(),
    phone: phone.trim(),
    source: LEAD_CONFIG.source,
    tags: ['form-eval', 'évaluation-timing', 'widget-message', 'Lead Vendeur'],
    consent,
    leadType: 'widget-message',
    landingPage: window.location.href.split('?')[0],
    utm,
    custom: {
      sellingMotivation: '',
      verdict: '',
      score: null
    },
    notes: [
      'Formulaire: widget message Pierre-Olivier',
      '',
      message.trim()
    ].join('\n')
  };
}

export async function submitLead(payload) {
  const response = await fetch(LEAD_CONFIG.endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  let data = {};
  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok || !data.stored) {
    throw new Error(data.error || 'Lead request failed');
  }

  return { stored: true, ...data };
}
