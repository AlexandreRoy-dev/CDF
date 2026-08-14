export const QUESTIONS = [
  {
    id: 'propertyType',
    kind: 'choice',
    title: 'Quel type de propriété possédez-vous ?',
    subtitle: 'On commence par le plus simple.',
    autoAdvance: true,
    choices: [
      { value: 'maison', label: 'Maison unifamiliale', hint: 'Détachée ou jumelée' },
      { value: 'condo', label: 'Condo', hint: 'Copropriété' },
      { value: 'plex', label: 'Plex', hint: 'Duplex, triplex, multilogement' },
      { value: 'chalet', label: 'Chalet', hint: 'Résidence secondaire' }
    ]
  },
  {
    id: 'sellingMotivation',
    kind: 'choice',
    title: 'Pourquoi pensez-vous vendre ?',
    subtitle: 'C’est ce qui motive votre réflexion.',
    autoAdvance: true,
    choices: [
      { value: 'upsize', label: 'Pour passer à plus grand', hint: 'Besoin de plus d’espace' },
      { value: 'downsize', label: 'Pour réduire ou simplifier', hint: 'Moins d’entretien, moins grand' },
      { value: 'relocation', label: 'Pour déménager ailleurs', hint: 'Autre secteur ou autre région' },
      { value: 'no_sell', label: 'Je ne veux pas vendre', hint: 'Je suis simplement curieux' }
    ]
  },
  {
    id: 'yearsOwned',
    kind: 'number',
    title: 'Depuis combien d’années êtes-vous propriétaire ?',
    subtitle: 'Une estimation suffit.',
    min: 0,
    max: 60,
    placeholder: '0'
  },
  {
    id: 'estimatedValue',
    kind: 'currency',
    title: 'Combien pensez-vous qu’elle vaut aujourd’hui ?',
    subtitle: 'Votre estimation, pas besoin d’être exact.',
    placeholder: '450 000'
  },
  {
    id: 'hasChildren',
    kind: 'boolean',
    title: 'Avez-vous des enfants ?',
    subtitle: 'La dynamique familiale est un facteur clé.',
    autoAdvance: true
  },
  {
    id: 'childrenStatus',
    kind: 'choice',
    title: 'Où en sont-ils ?',
    subtitle: 'Choisissez ce qui vous ressemble le plus.',
    autoAdvance: true,
    showIf: (answers) => answers.hasChildren === true,
    choices: [
      { value: 'partis', label: 'Déjà partis du nid' },
      { value: 'partent_3_ans', label: 'Ils partent d’ici 3 ans' },
      { value: 'encore_maison', label: 'Encore à la maison' },
      { value: 'manque_espace', label: 'On manque d’espace' }
    ]
  },
  {
    id: 'noChildrenPlan',
    kind: 'choice',
    title: 'Pensez-vous en avoir bientôt et agrandir ?',
    subtitle: 'Pour mieux anticiper vos besoins d’espace.',
    autoAdvance: true,
    showIf: (answers) => answers.hasChildren === false,
    choices: [
      { value: 'oui_bientot', label: 'Oui, bientôt' },
      { value: 'peut_etre', label: 'Peut-être' },
      { value: 'non', label: 'Non' }
    ]
  },
  {
    id: 'financialProfile',
    kind: 'choice',
    title: 'Quelle est votre situation financière ?',
    subtitle: 'Pour évaluer votre flexibilité face aux prêteurs.',
    autoAdvance: true,
    choices: [
      { value: 'salarie', label: 'Emploi stable (salarié)' },
      { value: 'autonome', label: 'Travailleur autonome' },
      { value: 'entrepreneur', label: 'Entrepreneur' },
      { value: 'placements', label: 'Revenus de placements' },
      { value: 'retraite', label: 'Retraité' },
      { value: 'transition', label: 'En transition' }
    ]
  },
  {
    id: 'hasContract',
    kind: 'boolean',
    title: 'Travaillez-vous déjà avec un courtier ?',
    subtitle: 'Question légale : on ne peut pas évaluer une propriété déjà sous contrat.',
    autoAdvance: true
  },
  {
    id: 'region',
    kind: 'region',
    title: 'Dans quel secteur se trouve votre propriété ?',
    subtitle: 'Écrivez votre secteur et choisissez-le dans la liste.'
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
