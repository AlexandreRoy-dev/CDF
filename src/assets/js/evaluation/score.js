import { findRegion } from './regions.js';

const PROPERTY_LABELS = {
  maison: 'Maison unifamiliale',
  condo: 'Condo',
  plex: 'Plex',
  chalet: 'Chalet'
};

const MOTIVATION_LABELS = {
  upsize: 'Passer à plus grand',
  downsize: 'Réduire ou simplifier',
  relocation: 'Déménager ailleurs',
  no_sell: 'Curiosité, sans projet de vente'
};

const FINANCIAL_LABELS = {
  salarie: 'Emploi salarié stable',
  autonome: 'Travailleur autonome',
  entrepreneur: 'Entrepreneur',
  placements: 'Revenus de placements',
  retraite: 'Retraité',
  transition: 'En transition'
};

const VERDICTS = {
  favorable: {
    id: 'favorable',
    label: 'Moment idéal',
    headline: 'C’est le moment idéal.',
    tone: 'green'
  },
  moyen: {
    id: 'moyen',
    label: 'Prêt à vendre',
    headline: 'Vous êtes prêt à vendre.',
    tone: 'amber'
  },
  defavorable: {
    id: 'defavorable',
    label: 'Pas encore prêt',
    headline: 'Vous n’êtes pas prêt encore.',
    tone: 'rose'
  }
};

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function formatMoney(value) {
  return new Intl.NumberFormat('fr-CA', {
    style: 'currency',
    currency: 'CAD',
    maximumFractionDigits: 0
  }).format(value);
}

function plusValueBand(years) {
  if (years < 3) return 'faible';
  if (years < 7) return 'modérée';
  return 'forte';
}

export function analyzeAnswers(answers) {
  const years = Number(answers.yearsOwned) || 0;
  const value = Number(answers.estimatedValue) || 0;
  let score = 52;
  const factors = [];

  if (years < 3) {
    score -= 16;
    factors.push({
      label: 'Plus-value',
      text: 'Moins de 3 ans de détention. Les frais de vente peuvent encore manger une bonne part du gain.'
    });
  } else if (years < 7) {
    score += 6;
    factors.push({
      label: 'Plus-value',
      text: `${years} ans de détention. Une plus-value est probable, à confirmer avec des comparables du secteur.`
    });
  } else {
    score += 20;
    factors.push({
      label: 'Plus-value',
      text: `${years} ans de détention. La fenêtre de plus-value est généralement plus confortable.`
    });
  }

  switch (answers.sellingMotivation) {
    case 'relocation':
      score += 14;
      factors.push({ label: 'Motivation', text: 'Un déménagement crée une vraie échéance. Le timing dépend surtout de votre prochaine étape.' });
      break;
    case 'upsize':
      score += 12;
      factors.push({ label: 'Motivation', text: 'Passer à plus grand est un projet concret. Le marché actuel permet souvent de lier vente et achat.' });
      break;
    case 'downsize':
      score += 10;
      factors.push({ label: 'Motivation', text: 'Réduire ou simplifier est un bon moment pour tester le marché, surtout si l’entretien pèse déjà.' });
      break;
    case 'no_sell':
      score -= 24;
      factors.push({ label: 'Motivation', text: 'Pas de projet de vente. L’exercice reste utile, mais le timing n’est pas urgent.' });
      break;
    default:
      break;
  }

  if (answers.childrenStatus === 'manque_espace') {
    score += 12;
    factors.push({ label: 'Famille', text: 'Le manque d’espace accélère souvent la décision. Mieux vaut préparer la vente avant d’être coincé.' });
  } else if (answers.childrenStatus === 'partent_3_ans') {
    score += 8;
    factors.push({ label: 'Famille', text: 'Les 24 à 36 prochains mois sont une fenêtre naturelle pour vendre ou revoir le besoin d’espace.' });
  } else if (answers.childrenStatus === 'partis') {
    score += 6;
    factors.push({ label: 'Famille', text: 'Nid vide : beaucoup de propriétaires vendent trop tard. C’est souvent le bon moment pour simplifier.' });
  } else if (answers.childrenStatus === 'encore_maison') {
    score -= 4;
    factors.push({ label: 'Famille', text: 'Les enfants sont encore à la maison. Vendre reste possible, mais le projet doit coller au quotidien.' });
  } else if (answers.noChildrenPlan === 'oui_bientot') {
    score -= 10;
    factors.push({ label: 'Famille', text: 'Un agrandissement bientôt peut justifier d’attendre, ou de vendre pour acheter plus grand tout de suite.' });
  } else if (answers.noChildrenPlan === 'non') {
    score += 3;
  }

  switch (answers.financialProfile) {
    case 'salarie':
      score += 8;
      factors.push({ label: 'Finances', text: 'Un emploi salarié stable facilite souvent le prochain financement, même dans un marché plus sélectif.' });
      break;
    case 'placements':
      score += 9;
      factors.push({ label: 'Finances', text: 'Des revenus de placements donnent de la flexibilité pour choisir le bon moment, pas le premier offreur.' });
      break;
    case 'retraite':
      score += 6;
      factors.push({ label: 'Finances', text: 'À la retraite, réduire les coûts d’occupation et l’entretien a souvent plus d’impact qu’attendre un sommet de marché.' });
      break;
    case 'entrepreneur':
      score += 2;
      factors.push({ label: 'Finances', text: 'Profil entrepreneur : les prêteurs regardent de plus près. Une préparation en amont évite les mauvaises surprises.' });
      break;
    case 'autonome':
      score += 0;
      factors.push({ label: 'Finances', text: 'Travailleur autonome : préparez vos documents avant de lier une vente à un achat.' });
      break;
    case 'transition':
      score -= 12;
      factors.push({ label: 'Finances', text: 'Une transition de revenus rend le timing plus fragile. Mieux vaut stabiliser avant de forcer une vente.' });
      break;
    default:
      break;
  }

  if (answers.propertyType === 'plex') score += 4;
  if (answers.propertyType === 'chalet') score -= 2;

  if (answers.sellingMotivation === 'no_sell') {
    score = Math.min(score, 44);
  }

  score = Math.round(clamp(score, 18, 96));

  let verdictId = 'defavorable';
  if (score >= 70) verdictId = 'favorable';
  else if (score >= 48) verdictId = 'moyen';

  const verdict = VERDICTS[verdictId];
  const region = findRegion(answers.region);
  const regionName = region ? region.name : 'Estrie';
  const propertyLabel = PROPERTY_LABELS[answers.propertyType] || 'Propriété';
  const valueLabel = value > 0 ? formatMoney(value) : 'non précisée';

  const summaries = {
    favorable: `Avec ${years} an${years > 1 ? 's' : ''} de détention, une ${propertyLabel.toLowerCase()} à ${regionName} et un projet clair, les conditions sont réunies pour vendre dans de bonnes conditions. La plus-value potentielle est ${plusValueBand(years)}, et votre situation actuelle soutient une mise en marché soignée plutôt qu’une vente précipitée.`,
    moyen: `Vous avez les bases pour vendre, sans que tout soit aligné à 100 %. ${years} an${years > 1 ? 's' : ''} de détention à ${regionName} et une valeur estimée à ${valueLabel} méritent une lecture précise du secteur avant de fixer un prix. Un courtier pourra vous dire si le marché actuel paie vraiment votre type de propriété.`,
    defavorable: `Le portrait actuel penche vers l’attente, ou vers une préparation plus poussée avant une mise en marché. ${years < 3 ? 'La courte durée de détention pèse sur le gain net. ' : ''}Ce n’est pas un non définitif : c’est un signal pour clarifier le projet, les finances et le prix avant de vous engager.`
  };

  const nextSteps = {
    favorable: [
      'Valider le prix avec des ventes récentes du même secteur, pas seulement une estimation en ligne.',
      'Préparer la propriété (réparations visibles, photos, timing de l’annonce) avant de tester le marché.',
      'Parler stratégie d’achat-revente si vous devez aussi trouver votre prochaine adresse.'
    ],
    moyen: [
      'Faire une lecture honnête des comparables avant de décider d’une date de mise en marché.',
      'Vérifier votre capacité d’emprunt ou de relogement pour éviter de vendre trop tôt, ou trop tard.',
      'Identifier 2 ou 3 correctifs qui changeraient vraiment le prix, plutôt que de tout rénover.'
    ],
    defavorable: [
      'Garder un œil sur les ventes de votre secteur au cours des 90 prochains jours.',
      'Stabiliser le projet (famille, financement, prochaine adresse) avant de signer un contrat.',
      'Revenir nous voir quand la date de vente sera plus claire. L’analyse restera un bon point de départ.'
    ]
  };

  return {
    scoring: {
      score,
      verdict: verdictId,
      label: verdict.label,
      headline: verdict.headline,
      tone: verdict.tone
    },
    report: {
      summary: summaries[verdictId],
      factors,
      nextSteps: nextSteps[verdictId],
      stats: [
        { label: 'Score d’opportunité', value: `${score}/100` },
        { label: 'Secteur', value: regionName },
        { label: 'Type', value: propertyLabel },
        { label: 'Détention', value: `${years} an${years > 1 ? 's' : ''}` },
        { label: 'Valeur estimée', value: valueLabel },
        { label: 'Motivation', value: MOTIVATION_LABELS[answers.sellingMotivation] || 'Non précisée' },
        { label: 'Finances', value: FINANCIAL_LABELS[answers.financialProfile] || 'Non précisée' }
      ]
    }
  };
}

export function formatAnswersForCrm(answers) {
  const region = findRegion(answers.region);
  const lines = [
    `Type: ${PROPERTY_LABELS[answers.propertyType] || answers.propertyType || 'n/d'}`,
    `Motivation: ${MOTIVATION_LABELS[answers.sellingMotivation] || answers.sellingMotivation || 'n/d'}`,
    `Années propriétaire: ${answers.yearsOwned ?? 'n/d'}`,
    `Valeur estimée: ${answers.estimatedValue ? formatMoney(answers.estimatedValue) : 'n/d'}`,
    `Enfants: ${answers.hasChildren === true ? 'oui' : answers.hasChildren === false ? 'non' : 'n/d'}`,
    answers.childrenStatus ? `Situation enfants: ${answers.childrenStatus}` : null,
    answers.noChildrenPlan ? `Projet d’agrandir: ${answers.noChildrenPlan}` : null,
    `Finances: ${FINANCIAL_LABELS[answers.financialProfile] || answers.financialProfile || 'n/d'}`,
    `Déjà avec un courtier: ${answers.hasContract === true ? 'oui' : answers.hasContract === false ? 'non' : 'n/d'}`,
    `Secteur: ${region ? region.name : answers.region || 'n/d'}`
  ];

  return lines.filter(Boolean).join('\n');
}
