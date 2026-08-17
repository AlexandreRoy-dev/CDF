export const QUESTIONS = [
  {
    id: 'propertyType',
    kind: 'choice',
    title: 'Quel bien occupez-vous actuellement ?',
    subtitle: 'Choisissez la catégorie la plus proche.',
    autoAdvance: true,
    choices: [
      { value: 'maison', label: 'Maison', hint: 'Détachée, jumelée ou en rangée' },
      { value: 'condo', label: 'Copropriété', hint: 'Appartement en copropriété' },
      { value: 'plex', label: 'Immeuble à logements', hint: 'Duplex, triplex ou plus' },
      { value: 'chalet', label: 'Résidence secondaire', hint: 'Chalet ou maison de villégiature' }
    ]
  },
  {
    id: 'sellingMotivation',
    kind: 'choice',
    title: 'Qu’est-ce qui vous amène à regarder une vente ?',
    subtitle: 'On veut comprendre le projet, pas vous pousser.',
    autoAdvance: true,
    choices: [
      { value: 'upsize', label: 'Nous manquons d’espace', hint: 'Maison trop petite' },
      { value: 'downsize', label: 'Nous voulons alléger', hint: 'Moins d’entretien, plus simple' },
      { value: 'relocation', label: 'Nous changeons de secteur', hint: 'Autre ville ou autre région' },
      { value: 'no_sell', label: 'Aucun projet de vente', hint: 'Simple prise de pouls du marché' }
    ]
  },
  {
    id: 'yearsOwned',
    kind: 'number',
    title: 'Depuis combien d’années ce bien est-il à vous ?',
    subtitle: 'Un chiffre rond suffit.',
    min: 0,
    max: 60,
    placeholder: '0'
  },
  {
    id: 'estimatedValue',
    kind: 'currency',
    title: 'Quelle valeur approximative lui donneriez-vous ?',
    subtitle: 'Votre ordre de grandeur, sans expertise.',
    placeholder: '450 000'
  },
  {
    id: 'hasChildren',
    kind: 'boolean',
    title: 'Votre ménage comprend-il des enfants ?',
    subtitle: 'La composition du foyer change souvent le calendrier.',
    autoAdvance: true
  },
  {
    id: 'childrenStatus',
    kind: 'choice',
    title: 'Où en est leur quotidien par rapport à la maison ?',
    subtitle: 'La réponse la plus proche de votre réalité.',
    autoAdvance: true,
    showIf: (answers) => answers.hasChildren === true,
    choices: [
      { value: 'partis', label: 'Ils ont déjà quitté' },
      { value: 'partent_3_ans', label: 'Départ prévu d’ici 3 ans' },
      { value: 'encore_maison', label: 'Ils habitent encore ici' },
      { value: 'manque_espace', label: 'L’espace manque déjà' }
    ]
  },
  {
    id: 'noChildrenPlan',
    kind: 'choice',
    title: 'Envisagez-vous d’agrandir la famille ?',
    subtitle: 'Pour anticiper un besoin d’espace plus tard.',
    autoAdvance: true,
    showIf: (answers) => answers.hasChildren === false,
    choices: [
      { value: 'oui_bientot', label: 'Oui, dans un avenir proche' },
      { value: 'peut_etre', label: 'C’est possible' },
      { value: 'non', label: 'Non' }
    ]
  },
  {
    id: 'financialProfile',
    kind: 'choice',
    title: 'D’où viennent principalement vos revenus ?',
    subtitle: 'Cela aide à juger la flexibilité pour un achat-revente.',
    autoAdvance: true,
    choices: [
      { value: 'salarie', label: 'Salaire d’emploi' },
      { value: 'autonome', label: 'Travail à son compte' },
      { value: 'entrepreneur', label: 'Entreprise' },
      { value: 'placements', label: 'Revenus de placements' },
      { value: 'retraite', label: 'Retraite' },
      { value: 'transition', label: 'Période de transition' }
    ]
  },
  {
    id: 'hasContract',
    kind: 'boolean',
    title: 'Un contrat de courtage est-il déjà signé sur ce bien ?',
    subtitle: 'La loi nous empêche d’intervenir si un autre courtier est déjà lié.',
    autoAdvance: true
  },
  {
    id: 'region',
    kind: 'region',
    title: 'Dans quelle municipalité se trouve le bien ?',
    subtitle: 'Tapez le nom et sélectionnez-le dans la liste Estrie.'
  }
];

export function visibleQuestions(answers) {
  return QUESTIONS.filter((question) => !question.showIf || question.showIf(answers));
}

export function questionIsAnswered(question, answers) {
  const value = answers[question.id];
  if (question.kind === 'boolean') return value === true || value === false;
  if (question.kind === 'number') {
    return typeof value === 'number' && Number.isFinite(value) && value >= 0;
  }
  if (question.kind === 'currency') {
    return typeof value === 'number' && Number.isFinite(value) && value > 0;
  }
  return typeof value === 'string' && value.trim().length > 0;
}
