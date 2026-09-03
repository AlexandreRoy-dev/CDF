import { visibleQuestions, questionIsAnswered } from './questions.js';
import { searchRegions, findRegion } from './regions.js';
import { analyzeAnswers } from './score.js';
import { buildLeadPayload, buildWidgetMessagePayload, submitLead } from './lead.js';

const app = document.getElementById('eval-app');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let advanceLock = false;
let advanceTimer = 0;

function withAdvanceLock(fn) {
  if (advanceLock) return;
  advanceLock = true;
  app.classList.add('is-advancing');
  window.clearTimeout(advanceTimer);
  fn();
  advanceTimer = window.setTimeout(() => {
    advanceLock = false;
    app.classList.remove('is-advancing');
  }, 450);
}

const state = {
  screen: 'landing',
  step: 0,
  answers: {},
  analysis: null,
  revealChoice: null,
  lead: { kind: 'idle' },
  regionQuery: '',
  form: { name: '', email: '', phone: '', consent: false, website: '' },
  widget: {
    open: false,
    sending: false,
    sent: false,
    error: '',
    name: '',
    phone: '',
    email: '',
    message: '',
    consent: false
  },
  error: ''
};

function delay(ms) {
  return new Promise((resolve) => window.setTimeout(resolve, reduceMotion ? 0 : ms));
}

function questions() {
  return visibleQuestions(state.answers);
}

function currentQuestion() {
  return questions()[state.step];
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function formatCurrencyInput(raw) {
  const digits = String(raw).replace(/[^\d]/g, '');
  if (!digits) return '';
  return new Intl.NumberFormat('fr-CA').format(Number(digits));
}

function parseCurrency(raw) {
  const digits = String(raw).replace(/[^\d]/g, '');
  return digits ? Number(digits) : null;
}

function setAnswer(id, value) {
  state.answers[id] = value;
  state.error = '';
}

function goNext() {
  const list = questions();
  const question = list[state.step];
  if (!questionIsAnswered(question, state.answers)) {
    state.error = 'Choisissez une réponse pour continuer.';
    render();
    return;
  }

  if (question.id === 'hasContract' && state.answers.hasContract === true) {
    state.screen = 'contract';
    render();
    return;
  }

  if (state.step >= list.length - 1) {
    startAnalysis();
    return;
  }

  state.step += 1;
  state.error = '';
  render();
}

function goBack() {
  if (state.screen === 'contract') {
    state.screen = 'quiz';
    render();
    return;
  }
  if (state.step === 0) {
    state.screen = 'landing';
    render();
    return;
  }
  state.step -= 1;
  state.error = '';
  render();
}

async function startAnalysis() {
  state.screen = 'analyzing';
  render();
  await delay(2200);
  state.analysis = analyzeAnswers(state.answers);
  state.screen = 'gate';
  render();
}

function restart() {
  state.screen = 'landing';
  state.step = 0;
  state.answers = {};
  state.analysis = null;
  state.revealChoice = null;
  state.lead = { kind: 'idle' };
  state.regionQuery = '';
  state.form = { name: '', email: '', phone: '', consent: false, website: '' };
  state.widget = {
    open: false,
    sending: false,
    sent: false,
    error: '',
    name: '',
    phone: '',
    email: '',
    message: '',
    consent: false
  };
  state.error = '';
  render();
}

function icons() {
  return {
    arrow: '<svg class="w-4 h-4" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 10h10M11 6l4 4-4 4" stroke-linecap="round" stroke-linejoin="round"></path></svg>',
    phone: '<svg class="w-4 h-4" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3.5 4.5C3.5 4 4 3.5 4.5 3.5H7L8.5 7L6.5 8.5C7.5 11 9 12.5 11.5 13.5L13 11.5L16.5 13V15.5C16.5 16 16 16.5 15.5 16.5C9 16.5 3.5 11 3.5 4.5Z" stroke-linecap="round" stroke-linejoin="round"></path></svg>',
    message: '<svg class="w-4 h-4" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3.5 5.5h13v9H7l-3.5 2.5V5.5Z" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
  };
}

function logos() {
  return `
    <a href="index.html" class="eval-logo" aria-label="Retour à l’accueil Chiasson de Francesco">
      <img src="./src/assets/logocdf.svg" alt="Chiasson de Francesco" class="h-full w-auto">
    </a>
  `;
}

function callCard() {
  const widget = state.widget;
  const messagePanel = widget.open ? `
    <form class="eval-call-panel" data-form="widget-message" novalidate>
      <div class="flex items-start justify-between gap-3 mb-3">
        <div>
          <p class="font-heading text-lg text-brand-navy leading-tight">Écrire à Pierre-Olivier</p>
          <p class="text-[11px] text-slate-500 mt-0.5">Un message suffit. Il vous reviendra.</p>
        </div>
        <button type="button" class="eval-call-close" data-action="close-message" aria-label="Fermer">×</button>
      </div>
      ${widget.sent ? `
        <p class="text-sm text-emerald-800 bg-emerald-50 rounded-xl px-3 py-2">Message envoyé. Pierre-Olivier vous recontacte sous peu.</p>
      ` : `
        <div class="grid gap-2">
          <label class="sr-only" for="widget-name">Votre nom</label>
          <input class="eval-call-input" id="widget-name" name="widget-name" autocomplete="name" placeholder="Votre nom" value="${escapeHtml(widget.name)}" required>
          <label class="sr-only" for="widget-phone">Votre téléphone</label>
          <input class="eval-call-input" id="widget-phone" name="widget-phone" type="tel" autocomplete="tel" placeholder="Votre téléphone" value="${escapeHtml(widget.phone)}" required>
          <label class="sr-only" for="widget-email">Courriel (optionnel)</label>
          <input class="eval-call-input" id="widget-email" name="widget-email" type="email" autocomplete="email" placeholder="Courriel (optionnel)" value="${escapeHtml(widget.email)}">
          <label class="sr-only" for="widget-message">Votre message</label>
          <textarea class="eval-call-input eval-call-textarea" id="widget-message" name="widget-message" rows="3" placeholder="Votre message" required>${escapeHtml(widget.message)}</textarea>
          <label class="eval-check text-slate-600">
            <input type="checkbox" name="widget-consent" ${widget.consent ? 'checked' : ''}>
            <span>J’accepte d’être contacté au sujet de ce message.</span>
          </label>
        </div>
        ${widget.error ? `<p class="eval-error mt-2">${escapeHtml(widget.error)}</p>` : ''}
        <button type="submit" class="eval-btn eval-btn-primary w-full mt-3" ${widget.sending ? 'disabled' : ''}>
          ${widget.sending ? 'Envoi en cours…' : 'Envoyer le message'}
        </button>
      `}
    </form>
  ` : '';

  return `
    <div class="eval-call-wrap">
      ${messagePanel}
      <div class="eval-call">
        <div class="relative shrink-0">
          <img src="./src/assets/pierre-olivier-chiasson.webp" alt="Pierre-Olivier Chiasson" onerror="this.onerror=null;this.src='./src/assets/images/chiassondefrancescoteam.jpg';">
          <span class="eval-online absolute -bottom-0.5 -right-0.5" aria-hidden="true"></span>
        </div>
        <div class="min-w-0 flex-1">
          <div class="flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
            <span class="text-[10px] font-medium text-emerald-700 uppercase tracking-wide">Disponible maintenant</span>
          </div>
          <p class="font-heading text-base leading-tight text-brand-navy mt-0.5 truncate">Pierre-Olivier Chiasson</p>
          <a class="eval-call-number" href="tel:+18199194631">819-919-4631</a>
          <p class="text-[11px] text-slate-500 truncate">Courtier immobilier, Estrie</p>
        </div>
        <div class="eval-call-actions">
          <a class="eval-call-action eval-call-action--phone" href="tel:+18199194631" aria-label="Appeler Pierre-Olivier au 819-919-4631">
            <span class="eval-call-icon">${icons().phone}</span>
            <span>Appeler</span>
          </a>
          <button type="button" class="eval-call-action eval-call-action--message" data-action="open-message" aria-expanded="${widget.open ? 'true' : 'false'}">
            <span class="eval-call-icon">${icons().message}</span>
            <span>Écrire</span>
          </button>
        </div>
      </div>
    </div>
  `;
}

function landing() {
  return `
    ${logos()}
    <section class="relative min-h-dvh flex flex-col items-center justify-start px-5 sm:px-8 pt-24 sm:pt-28 pb-36">
      <div class="max-w-3xl text-center">
        <div class="eval-badge eval-enter mb-8">
          <span class="eval-dot"></span>
          <span class="font-medium tracking-wide">Lecture de marché Estrie</span>
        </div>
        <h1 class="eval-enter eval-enter-delay font-heading text-4xl sm:text-5xl lg:text-6xl text-white leading-[1.05] tracking-tight text-balance">
          Vendre maintenant, plus tard, ou pas encore ?
        </h1>
        <p class="eval-enter eval-enter-delay-2 mt-6 text-base sm:text-lg text-slate-300 max-w-xl mx-auto leading-relaxed">
          Dix questions sur votre bien, votre projet et votre foyer. L’équipe Chiasson de Francesco vous dit si une mise en marché a du sens aujourd’hui, sans pression.
        </p>
        <div class="eval-rule"></div>
        <div class="eval-enter eval-enter-delay-2 mt-10 flex flex-col items-center gap-3">
          <button type="button" class="eval-btn eval-btn-primary" data-action="start">
            <span>Commencer le questionnaire</span>
            ${icons().arrow}
          </button>
          <p class="text-xs text-slate-400">Environ cinq minutes. Gratuit, sans engagement.</p>
        </div>
      </div>
      <p class="absolute bottom-24 sm:bottom-10 left-1/2 -translate-x-1/2 text-[10px] text-slate-500 uppercase tracking-[0.2em]">Privé · Sans contrat</p>
    </section>
    ${callCard()}
  `;
}

function progressBar() {
  const list = questions();
  const total = list.length;
  const current = Math.min(state.step + 1, total);
  const width = Math.round((current / total) * 100);
  return `
    <div class="w-full max-w-xl mx-auto mb-8">
      <div class="flex items-center justify-between text-[11px] text-slate-400 mb-2 tracking-wide">
        <span class="uppercase">Question <span class="text-white font-medium">${current}</span> / ${total}</span>
        <button type="button" class="eval-back text-slate-400 hover:text-white" data-action="back">Précédent</button>
      </div>
      <div class="eval-progress" aria-hidden="true"><span style="width:${width}%"></span></div>
    </div>
  `;
}

function choiceList(question) {
  const selected = state.answers[question.id];
  return `
    <div class="grid gap-3">
      ${question.choices.map((choice) => `
        <button type="button" class="eval-choice ${selected === choice.value ? 'is-selected' : ''}" data-action="choose" data-id="${question.id}" data-value="${choice.value}">
          <span class="block font-medium text-white">${escapeHtml(choice.label)}</span>
          ${choice.hint ? `<span class="block text-sm text-slate-400 mt-0.5">${escapeHtml(choice.hint)}</span>` : ''}
        </button>
      `).join('')}
    </div>
  `;
}

function booleanList(question) {
  const selected = state.answers[question.id];
  return `
    <div class="grid sm:grid-cols-2 gap-3">
      <button type="button" class="eval-choice ${selected === true ? 'is-selected' : ''}" data-action="choose-bool" data-id="${question.id}" data-value="true">
        <span class="block font-medium text-white">Oui</span>
      </button>
      <button type="button" class="eval-choice ${selected === false ? 'is-selected' : ''}" data-action="choose-bool" data-id="${question.id}" data-value="false">
        <span class="block font-medium text-white">Non</span>
      </button>
    </div>
  `;
}

function numberField(question) {
  const value = state.answers[question.id];
  return `
    <div class="max-w-sm mx-auto">
      <label class="sr-only" for="${question.id}">${escapeHtml(question.title)}</label>
      <input class="eval-input text-center text-2xl tracking-wide" id="${question.id}" inputmode="numeric" data-kind="number" data-id="${question.id}" value="${value ?? ''}" placeholder="${question.placeholder || '0'}">
      <p class="text-center text-xs text-slate-400 mt-3">Années</p>
    </div>
  `;
}

function selectField(question) {
  const value = state.answers[question.id];
  const selected = value == null ? '' : String(value);
  return `
    <div class="max-w-sm mx-auto">
      <label class="sr-only" for="${question.id}">${escapeHtml(question.title)}</label>
      <select class="eval-input eval-select text-center text-xl tracking-wide" id="${question.id}" data-kind="select" data-id="${question.id}">
        <option value="" ${selected === '' ? 'selected' : ''} disabled>${escapeHtml(question.placeholder || 'Sélectionnez')}</option>
        ${(question.choices || []).map((choice) => `
          <option value="${escapeHtml(String(choice.value))}" ${selected === String(choice.value) ? 'selected' : ''}>${escapeHtml(choice.label)}</option>
        `).join('')}
      </select>
      <p class="text-center text-xs text-slate-400 mt-3">Nombre d’années de détention</p>
    </div>
  `;
}

function currencyField(question) {
  const value = state.answers[question.id];
  return `
    <div class="max-w-sm mx-auto">
      <label class="sr-only" for="${question.id}">${escapeHtml(question.title)}</label>
      <div class="relative">
        <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">$</span>
        <input class="eval-input text-center text-2xl tracking-wide pl-8" id="${question.id}" inputmode="numeric" data-kind="currency" data-id="${question.id}" value="${value ? formatCurrencyInput(value) : ''}" placeholder="${question.placeholder || '450 000'}">
      </div>
      <p class="text-center text-xs text-slate-400 mt-3">Votre estimation, en dollars canadiens</p>
    </div>
  `;
}

function regionSuggestions() {
  if (!state.regionQuery.trim()) return '';
  const matches = searchRegions(state.regionQuery);
  return `
    <div class="eval-suggest mt-2" role="listbox">
      ${matches.length ? matches.map((region) => `
        <button type="button" role="option" data-action="choose-region" data-value="${region.id}">${escapeHtml(region.name)}</button>
      `).join('') : `<p class="px-4 py-3 text-sm text-slate-400">Aucun secteur trouvé. Essayez le nom de la ville.</p>`}
    </div>
  `;
}

function regionField(question) {
  const selected = findRegion(state.answers[question.id]);
  if (selected) {
    return `
      <div class="eval-card text-center py-10">
        <p class="text-[11px] uppercase tracking-[0.18em] text-slate-400 mb-2">Votre secteur</p>
        <p class="font-heading text-2xl text-white">${escapeHtml(selected.name)}</p>
        <button type="button" class="mt-5 text-sm text-slate-300 hover:text-white" data-action="clear-region">Modifier ma réponse</button>
      </div>
    `;
  }

  return `
    <div>
      <label class="sr-only" for="region">Secteur</label>
      <input class="eval-input" id="region" data-kind="region" value="${escapeHtml(state.regionQuery)}" placeholder="Écrivez votre secteur (ex. Sherbrooke, Magog.)" autocomplete="off">
      <div id="region-results">${regionSuggestions()}</div>
    </div>
  `;
}

function quiz() {
  const question = currentQuestion();
  let field = '';
  if (question.kind === 'choice') field = choiceList(question);
  if (question.kind === 'boolean') field = booleanList(question);
  if (question.kind === 'number') field = numberField(question);
  if (question.kind === 'select') field = selectField(question);
  if (question.kind === 'currency') field = currencyField(question);
  if (question.kind === 'region') field = regionField(question);

  const canContinue = question.kind !== 'choice' && question.kind !== 'boolean';

  return `
    ${logos()}
    <section class="min-h-dvh px-5 sm:px-8 pt-24 pb-28 max-w-xl mx-auto w-full">
      ${progressBar()}
      <div class="eval-enter">
        <h2 class="font-heading text-3xl sm:text-4xl text-white leading-tight text-balance">${escapeHtml(question.title)}</h2>
        <p class="mt-3 text-slate-300">${escapeHtml(question.subtitle)}</p>
        <div class="mt-8">${field}</div>
        ${state.error ? `<p class="eval-error mt-4">${escapeHtml(state.error)}</p>` : ''}
        ${canContinue ? `
          <div class="mt-8 flex justify-center">
            <button type="button" class="eval-btn eval-btn-primary" data-action="next">
              <span>Suivant</span>
              ${icons().arrow}
            </button>
          </div>
        ` : ''}
      </div>
    </section>
    ${callCard()}
  `;
}

function contract() {
  return `
    ${logos()}
    <section class="min-h-dvh px-5 sm:px-8 pt-28 pb-28 max-w-xl mx-auto w-full">
      <div class="eval-enter eval-card">
        <p class="text-[11px] uppercase tracking-[0.18em] text-[#c4a574]">Cadre professionnel</p>
        <h2 class="font-heading text-2xl sm:text-3xl text-white mt-3 leading-tight">Un courtier est déjà lié à ce bien.</h2>
        <p class="mt-4 text-slate-300 leading-relaxed">Quand un contrat de courtage est en vigueur, nous ne pouvons pas intervenir sur l’évaluation ni sur la mise en marché. C’est une règle de la profession, pour vous et pour le courtier en place.</p>
        <p class="mt-5 text-slate-300 leading-relaxed">Si le mandat se termine bientôt, ou si vous voulez simplement comprendre votre situation, vous pouvez poursuivre le questionnaire.</p>
        <div class="mt-7 flex flex-col gap-3">
          <button type="button" class="eval-btn eval-btn-primary" data-action="continue-contract">Poursuivre le questionnaire</button>
          <button type="button" class="eval-btn eval-btn-ghost" data-action="back">Corriger ma réponse</button>
        </div>
      </div>
    </section>
    ${callCard()}
  `;
}

function analyzing() {
  return `
    ${logos()}
    <section class="min-h-dvh flex items-center justify-center px-5 text-center">
      <div class="eval-enter max-w-lg">
        <p class="text-[11px] uppercase tracking-[0.18em] text-slate-400">Lecture en cours</p>
        <h2 class="font-heading italic text-3xl sm:text-5xl text-white mt-4 leading-tight">On croise vos réponses</h2>
        <p class="mt-8 text-sm text-slate-300">Quelques secondes. Durée de détention, secteur et projet de vie, pour une lecture claire plutôt qu’un slogan.</p>
        <div class="mt-10 flex justify-center gap-2" aria-hidden="true">
          <span class="eval-dot"></span>
          <span class="eval-dot" style="animation-delay:.2s"></span>
          <span class="eval-dot" style="animation-delay:.4s"></span>
        </div>
      </div>
    </section>
  `;
}

function gate() {
  return `
    ${logos()}
    <section class="min-h-dvh px-5 sm:px-8 py-24 max-w-xl mx-auto w-full text-center">
      <div class="eval-enter">
        <p class="text-[11px] uppercase tracking-[0.18em] text-slate-400">Résultat disponible</p>
        <h2 class="font-heading text-3xl sm:text-4xl text-white mt-4">Votre lecture est prête.</h2>
        <p class="mt-5 text-slate-300">Souhaitez-vous qu’un courtier de l’équipe vous la présente, avec un appel de suivi ?</p>
        <div class="mt-8 grid gap-3">
          <button type="button" class="eval-btn eval-btn-primary" data-action="reveal" data-value="yes">Oui, je veux le détail et un appel</button>
          <button type="button" class="eval-btn eval-btn-ghost" data-action="reveal" data-value="no">Non, le verdict seul me suffit</button>
        </div>
        <p class="mt-6 text-xs text-slate-500">Vous restez libre. Aucune mise en marché n’est lancée.</p>
      </div>
    </section>
  `;
}

function leadForm(gated) {
  const analysis = state.analysis;
  const heading = gated
    ? 'Recevoir le détail'
    : analysis.scoring.verdict === 'defavorable'
      ? 'Suivi de secteur'
      : 'Appel de l’équipe';

  const blurb = gated
    ? 'Vos coordonnées débloquent le détail et un appel avec Pierre-Olivier, Marco ou Jade.'
    : analysis.scoring.verdict === 'defavorable'
      ? 'Recevez un suivi des ventes dans votre secteur, sans pression de mise en marché.'
      : 'Un courtier vous rappelle pour commenter le résultat.';

  const busy = state.lead.kind === 'submitting';

  return `
    <form class="eval-card mt-10 text-left" data-form="lead" novalidate>
      <p class="text-[11px] uppercase tracking-[0.18em] text-[#c4a574]">${heading}</p>
      <p class="mt-2 text-slate-300">${blurb}</p>
      <div class="sr-only-hp" aria-hidden="true">
        <label>Site web<input name="website" tabindex="-1" autocomplete="off"></label>
      </div>
      <div class="mt-5 grid gap-3">
        <label class="block">
          <span class="sr-only">Votre prénom</span>
          <input class="eval-input" name="name" autocomplete="name" placeholder="Votre prénom" value="${escapeHtml(state.form.name)}" required>
        </label>
        <label class="block">
          <span class="sr-only">Courriel</span>
          <input class="eval-input" name="email" type="email" autocomplete="email" placeholder="marie@exemple.ca" value="${escapeHtml(state.form.email)}" required>
        </label>
        <label class="block">
          <span class="sr-only">Téléphone</span>
          <input class="eval-input" name="phone" type="tel" autocomplete="tel" placeholder="(819) 555-0123" value="${escapeHtml(state.form.phone)}" required>
        </label>
        <label class="eval-check">
          <input type="checkbox" name="consent" ${state.form.consent ? 'checked' : ''}>
          <span>J’accepte d’être contacté par l’équipe Chiasson de Francesco au sujet de cette évaluation. Consultez notre <a class="underline hover:text-white" href="confidentialite.html">politique de confidentialité</a>.</span>
        </label>
      </div>
      ${state.error ? `<p class="eval-error mt-3">${escapeHtml(state.error)}</p>` : ''}
      <button type="submit" class="eval-btn eval-btn-primary w-full mt-5" ${busy ? 'disabled' : ''}>
        ${busy ? 'Envoi en cours…' : gated ? 'Voir le détail' : 'Être rappelé par l’équipe'}
      </button>
    </form>
  `;
}

function leadThanks() {
  return `
    <div class="eval-card mt-10 text-center">
      <p class="font-heading text-2xl text-white">Bien reçu.</p>
      <p class="mt-3 text-slate-300">Votre analyse est prête ci-dessous. Un courtier vous appellera pour confirmer les résultats.</p>
    </div>
  `;
}

function results() {
  const { scoring, report } = state.analysis;
  const gatedPending = state.revealChoice === 'yes' && state.lead.kind !== 'done';

  if (gatedPending) {
    return `
      ${logos()}
      <section class="min-h-dvh px-5 sm:px-8 py-24 max-w-xl mx-auto w-full">
        <div class="eval-enter text-center">
          <p class="text-[11px] uppercase tracking-[0.18em] text-slate-400">Détail disponible</p>
          <h2 class="font-heading text-3xl text-white mt-4">On peut vous la présenter.</h2>
          <p class="mt-4 text-slate-300">Laissez vos coordonnées. Pierre-Olivier, Marco ou Jade vous rappellent pour commenter le résultat.</p>
          ${leadForm(true)}
          <button type="button" class="mt-8 text-xs text-slate-500 hover:text-white" data-action="restart">Retour à l’accueil</button>
        </div>
      </section>
      ${callCard()}
    `;
  }

  return `
    ${logos()}
    <section class="min-h-dvh px-5 sm:px-8 pt-24 pb-36 max-w-3xl mx-auto w-full">
      <div class="eval-enter text-center">
        <p class="text-[11px] uppercase tracking-[0.18em] text-slate-400">${escapeHtml(scoring.label)}</p>
        <h2 class="font-heading text-4xl sm:text-5xl text-white mt-3">${escapeHtml(scoring.headline)}</h2>
        <p class="mt-6 text-slate-300 max-w-2xl mx-auto leading-relaxed">${escapeHtml(report.summary)}</p>
      </div>
      <div class="eval-score rounded-3xl p-7 sm:p-9 mt-10 text-center eval-enter">
        <p class="text-[11px] uppercase tracking-[0.18em] text-slate-300">Score d’opportunité</p>
        <p class="font-heading text-6xl text-white mt-2">${scoring.score}<span class="text-2xl text-slate-400">/100</span></p>
        <p class="mt-3 text-sm text-slate-300">${escapeHtml(scoring.label)}</p>
      </div>
      <p class="text-center text-xs text-slate-500 italic mt-3">Un courtier vous appellera pour confirmer les résultats.</p>
      ${state.lead.kind === 'done' ? leadThanks() : leadForm(false)}
      <div class="grid sm:grid-cols-3 gap-3 mt-10">
        ${report.stats.slice(1, 4).map((stat) => `
          <article class="eval-card">
            <p class="text-[11px] uppercase tracking-[0.18em] text-slate-400">${escapeHtml(stat.label)}</p>
            <p class="mt-2 font-heading text-xl text-white">${escapeHtml(stat.value)}</p>
          </article>
        `).join('')}
      </div>
      <div class="eval-card mt-6">
        <p class="text-[11px] uppercase tracking-[0.18em] text-slate-400">Facteurs détectés</p>
        <ul class="mt-4 space-y-4">
          ${report.factors.map((factor) => `
            <li>
              <p class="text-sm font-semibold text-white">${escapeHtml(factor.label)}</p>
              <p class="text-sm text-slate-300 mt-1">${escapeHtml(factor.text)}</p>
            </li>
          `).join('')}
        </ul>
      </div>
      <div class="eval-card mt-6">
        <p class="text-[11px] uppercase tracking-[0.18em] text-slate-400">Prochaines étapes</p>
        <ol class="mt-4 space-y-3 text-slate-300 text-sm list-decimal pl-5">
          ${report.nextSteps.map((step) => `<li>${escapeHtml(step)}</li>`).join('')}
        </ol>
      </div>
      <div class="text-center mt-10 pb-16">
        <button type="button" class="text-sm text-slate-400 hover:text-white" data-action="restart">Recommencer le questionnaire</button>
        <p class="mt-4 text-xs text-slate-500">
          <a class="hover:text-white" href="confidentialite.html">Politique de confidentialité</a>
        </p>
      </div>
    </section>
    ${callCard()}
  `;
}

function declined() {
  return `
    ${logos()}
    <section class="min-h-dvh px-5 sm:px-8 py-24 max-w-xl mx-auto w-full text-center">
      <div class="eval-enter">
        <p class="text-[11px] uppercase tracking-[0.18em] text-slate-400">Bien noté</p>
        <h2 class="font-heading text-3xl text-white mt-4">Pas pressé de vendre ? Aucun souci.</h2>
        <p class="mt-4 text-slate-300">Voici tout de même votre lecture de timing. Vous pourrez revenir quand le projet sera plus concret.</p>
        <button type="button" class="eval-btn eval-btn-primary mt-8" data-action="show-results">Voir mon analyse</button>
        <div>
          <button type="button" class="mt-4 text-xs text-slate-500 hover:text-white" data-action="restart">Retour à l’accueil</button>
        </div>
      </div>
    </section>
    ${callCard()}
  `;
}

function render() {
  let html = landing();
  if (state.screen === 'quiz') html = quiz();
  if (state.screen === 'contract') html = contract();
  if (state.screen === 'analyzing') html = analyzing();
  if (state.screen === 'gate') html = gate();
  if (state.screen === 'declined') html = declined();
  if (state.screen === 'results') html = results();
  app.innerHTML = html;
}

function validateLead(form) {
  if (form.website) return 'ignored';
  if (!form.name.trim()) return 'Votre nom est requis.';
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim())) return 'Format de courriel invalide.';
  if (form.phone.replace(/\D/g, '').length < 10) return 'Numéro de téléphone invalide.';
  if (!form.consent) return 'Merci de cocher la case de consentement.';
  return '';
}

async function handleLeadSubmit(formEl) {
  const data = new FormData(formEl);
  state.form = {
    name: String(data.get('name') || ''),
    email: String(data.get('email') || ''),
    phone: String(data.get('phone') || ''),
    consent: data.get('consent') === 'on',
    website: String(data.get('website') || '')
  };

  const error = validateLead(state.form);
  if (error === 'ignored') return;
  if (error) {
    state.error = error;
    render();
    return;
  }

  state.lead = { kind: 'submitting' };
  state.error = '';
  render();

  const payload = buildLeadPayload({
    ...state.form,
    answers: state.answers,
    analysis: state.analysis,
    leadType: state.revealChoice === 'yes' || state.analysis.scoring.verdict !== 'defavorable'
      ? 'evaluation'
      : 'market_info'
  });

  try {
    const result = await submitLead(payload);
    if (typeof window.cdfTrackLead === 'function') {
      window.cdfTrackLead('evaluation');
    }
    state.lead = { kind: 'done', stored: !!result.stored, firstName: payload.firstName };
    state.screen = 'results';
    render();
  } catch {
    state.lead = { kind: 'idle' };
    state.error = 'Une erreur est survenue. Réessayez dans quelques secondes.';
    render();
  }
}

async function handleWidgetMessage(formEl) {
  const data = new FormData(formEl);
  state.widget.name = String(data.get('widget-name') || '');
  state.widget.phone = String(data.get('widget-phone') || '');
  state.widget.email = String(data.get('widget-email') || '');
  state.widget.message = String(data.get('widget-message') || '');
  state.widget.consent = data.get('widget-consent') === 'on';

  if (!state.widget.name.trim()) {
    state.widget.error = 'Votre nom est requis.';
    render();
    return;
  }
  if (state.widget.phone.replace(/\D/g, '').length < 10) {
    state.widget.error = 'Numéro de téléphone invalide.';
    render();
    return;
  }
  if (state.widget.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(state.widget.email.trim())) {
    state.widget.error = 'Format de courriel invalide.';
    render();
    return;
  }
  if (!state.widget.message.trim()) {
    state.widget.error = 'Écrivez un court message.';
    render();
    return;
  }
  if (!state.widget.consent) {
    state.widget.error = 'Merci de cocher la case de consentement.';
    render();
    return;
  }

  state.widget.sending = true;
  state.widget.error = '';
  render();

  try {
    await submitLead(buildWidgetMessagePayload(state.widget));
    if (typeof window.cdfTrackLead === 'function') {
      window.cdfTrackLead('evaluation_widget');
    }
    state.widget.sending = false;
    state.widget.sent = true;
    render();
  } catch {
    state.widget.sending = false;
    state.widget.error = 'Une erreur est survenue. Réessayez dans quelques secondes.';
    render();
  }
}

app.addEventListener('click', (event) => {
  const target = event.target.closest('[data-action]');
  if (!target) return;
  const action = target.getAttribute('data-action');
  const autoAdvance = action === 'choose' || action === 'choose-bool' || action === 'choose-region';
  if (advanceLock && autoAdvance) {
    event.preventDefault();
    event.stopPropagation();
    return;
  }

  if (action === 'start') {
    state.screen = 'quiz';
    state.step = 0;
    render();
    return;
  }
  if (action === 'back') {
    goBack();
    return;
  }
  if (action === 'next') {
    goNext();
    return;
  }
  if (action === 'restart') {
    restart();
    return;
  }
  if (action === 'show-results') {
    state.screen = 'results';
    render();
    return;
  }
  if (action === 'continue-contract') {
    const list = questions();
    const idx = list.findIndex((item) => item.id === 'hasContract');
    state.step = idx + 1;
    state.screen = 'quiz';
    render();
    return;
  }
  if (action === 'choose') {
    event.preventDefault();
    event.stopPropagation();
    withAdvanceLock(() => {
      setAnswer(target.dataset.id, target.dataset.value);
      goNext();
    });
    return;
  }
  if (action === 'choose-bool') {
    event.preventDefault();
    event.stopPropagation();
    withAdvanceLock(() => {
      setAnswer(target.dataset.id, target.dataset.value === 'true');
      goNext();
    });
    return;
  }
  if (action === 'choose-region') {
    event.preventDefault();
    event.stopPropagation();
    withAdvanceLock(() => {
      setAnswer('region', target.dataset.value);
      state.regionQuery = '';
      goNext();
    });
    return;
  }
  if (action === 'clear-region') {
    delete state.answers.region;
    state.regionQuery = '';
    render();
    document.getElementById('region')?.focus();
    return;
  }
  if (action === 'reveal') {
    state.revealChoice = target.dataset.value;
    state.screen = target.dataset.value === 'no' ? 'declined' : 'results';
    render();
  }
  if (action === 'open-message') {
    state.widget.open = true;
    state.widget.sent = false;
    state.widget.error = '';
    render();
    document.getElementById('widget-name')?.focus();
  }
  if (action === 'close-message') {
    state.widget.open = false;
    render();
  }
});

function readSelectAnswer(el) {
  if (!el.value) {
    setAnswer(el.dataset.id, null);
    return;
  }
  const asNumber = Number(el.value);
  setAnswer(el.dataset.id, Number.isFinite(asNumber) ? asNumber : el.value);
}

app.addEventListener('change', (event) => {
  const el = event.target;
  if (el.dataset?.kind === 'select') readSelectAnswer(el);
});

app.addEventListener('input', (event) => {
  const el = event.target;
  if (el.dataset.kind === 'number') {
    const value = el.value.replace(/[^\d]/g, '');
    el.value = value;
    setAnswer(el.dataset.id, value === '' ? null : Number(value));
  }
  if (el.dataset.kind === 'select') {
    readSelectAnswer(el);
  }
  if (el.dataset.kind === 'currency') {
    const amount = parseCurrency(el.value);
    el.value = amount == null ? '' : formatCurrencyInput(amount);
    setAnswer(el.dataset.id, amount);
  }
  if (el.dataset.kind === 'region') {
    state.regionQuery = el.value;
    const host = document.getElementById('region-results');
    if (host) host.innerHTML = regionSuggestions();
  }
  if (el.name && ['name', 'email', 'phone'].includes(el.name)) {
    state.form[el.name] = el.value;
  }
  if (el.name === 'consent') {
    state.form.consent = el.checked;
  }
  if (el.name === 'widget-name') state.widget.name = el.value;
  if (el.name === 'widget-phone') state.widget.phone = el.value;
  if (el.name === 'widget-email') state.widget.email = el.value;
  if (el.name === 'widget-message') state.widget.message = el.value;
  if (el.name === 'widget-consent') state.widget.consent = el.checked;
});

app.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && event.target.dataset?.kind) {
    event.preventDefault();
    goNext();
  }
});

app.addEventListener('submit', (event) => {
  if (event.target.matches('[data-form="lead"]')) {
    event.preventDefault();
    handleLeadSubmit(event.target);
  }
  if (event.target.matches('[data-form="widget-message"]')) {
    event.preventDefault();
    handleWidgetMessage(event.target);
  }
});

render();
