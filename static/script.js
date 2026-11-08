const translations = {
  en: {
    navSummary: 'Summary', navKeywords: 'Keywords', navQuestions: 'Ask questions',
    homeLabel: 'lectoriia home', navLabel: 'Document sections', workspaceLabel: 'Document analysis workspace',
    adLabel: 'Advertisement', languageLabel: 'Interface language', eyebrow: 'Your thoughtful document reader',
    heroTitleFirst: 'Understand every', heroTitleSecond: 'document, faster.',
    heroDescription: 'Analyze PDFs and text with local, rule-based summaries, keywords, topics, and answers. No AI model or external inference service is used.',
    uploadPdf: 'Upload PDF', analyzeText: 'Analyze text', privacyShort: 'Text is processed by the app without sending it to an AI model.',
    localModeBadge: 'Local text analysis · no AI models',
    privacyPolicy: 'Privacy',
    dropZoneLabel: 'Drop a PDF here or choose a file', dropTitle: 'Drop a PDF here',
    dropHint: 'or choose a file from your device', topicScoreHint: 'Relative match among detected topics, not a probability.',
    topicEvidenceLabel: 'Text signals',
    topicScoreA11y: 'Relative topic relevance score',
    sourceLabel: 'Your source', addDocument: 'Add a document', choosePdf: 'Choose PDF',
    textInputLabel: 'Document text', textPlaceholder: 'Paste text from a document here...',
    ready: 'Ready to analyze', analyzeDocument: 'Analyze document', analysisLabel: 'Your analysis',
    resultsTitle: 'Document insights', summaryTitle: 'Summary', runAgain: 'Run again',
    summaryEmpty: 'Your summary will appear here after analysis.', keywordsTitle: 'Key concepts',
    keywordsEmpty: 'No keywords yet', topicTitle: 'Topics', topicEmpty: 'Waiting for analysis',
    questionsLabel: 'Ask the document', questionHeading: 'Get a clear answer',
    questionEmpty: 'Ask anything about the document. Answers are grounded in the text you provided.',
    questionInputLabel: 'Your question', questionPlaceholder: 'What is this document about?',
    askButton: 'Ask', metadataTitle: 'Document details', fileLabel: 'File',
    noDocument: 'No document', pagesLabel: 'Pages', sizeLabel: 'Size',
    footerPrivacy: 'Documents are processed temporarily for analysis. Avoid uploading sensitive personal information.',
    privacyDetailsTitle: 'Privacy and advertising',
    privacyDetails: "PDFs are temporarily extracted and removed after processing. Analysis uses local text-processing rules and does not send document text to an AI model or inference provider. The hosting provider may process requests and technical logs. If ads are enabled, Google may use cookies or similar technologies; the publisher must configure Google's certified consent messaging where required. Avoid uploading sensitive information.",
    footerMade: 'Made for clearer reading.', sourceCode: 'Open source', adPlaceholder: 'Advertisement',
    statusReadingPdf: 'Reading PDF...', statusPdfLoaded: 'PDF loaded', statusAnalyzing: 'Analyzing every section...',
    statusAnalyzed: 'Analysis complete', statusError: 'Analysis failed', statusNeedsAnalysis: 'Changes need analysis',
    statusAsking: 'Finding evidence...', statusQuestionReady: 'Answer ready', statusPdfError: 'Could not load PDF',
    keywordsProcessing: 'Extracting concepts...', retry: 'Try again', summaryLoading: 'Building a document-wide summary...',
    placeholderAnswer: 'Your answer will appear here.', questionLabel: 'You', answerLabel: 'lectoriia',
    questionErrorLabel: 'Could not answer', referenceLabel: 'Source pages', topicNeutral: 'Other',
    alertNoText: 'Add or upload document text before analysis.', questionNoText: 'Add or upload a document before asking a question.',
    errors: {
      local_processing_error: 'Local analysis could not complete. Please retry.',
      document_too_large: 'This document exceeds the 500,000-character or 512-section analysis limit. Split it into smaller documents and retry.',
      empty_document: 'No readable document text was provided.',
      empty_question: 'Write a question before consulting the document.',
      invalid_request: 'The request data is invalid.',
      invalid_file_type: 'Choose a PDF file.',
      empty_file: 'The selected PDF is empty.',
      file_too_large: 'The PDF exceeds the 4 MB production or 15 MB local file size limit.',
      no_extractable_text: 'No readable text could be extracted. The PDF may be scanned or protected.',
      invalid_pdf: 'The PDF could not be read. Check that the file is valid and not protected.',
      missing_file: 'Choose a PDF file first.',
      request_too_large: 'The request exceeds the configured upload limit.',
    },
    topics: {
      Technology: 'Technology', Science: 'Science', Education: 'Education', Business: 'Business',
      History: 'History', Health: 'Health', Finance: 'Finance', Politics: 'Politics',
      Law: 'Law', Literature: 'Literature', Other: 'Other'
    }
  },
  es: {
    navSummary: 'Resumen', navKeywords: 'Palabras clave', navQuestions: 'Preguntas',
    homeLabel: 'Inicio de lectoriia', navLabel: 'Secciones del documento', workspaceLabel: 'Área de análisis del documento',
    adLabel: 'Publicidad', languageLabel: 'Idioma de la interfaz', eyebrow: 'Tu lector inteligente de documentos',
    heroTitleFirst: 'Comprende cada', heroTitleSecond: 'documento, más rápido.',
    heroDescription: 'Analiza PDF y texto con resúmenes, conceptos, temas y respuestas basados en reglas locales. No se usa un modelo de IA ni un servicio externo de inferencia.',
    uploadPdf: 'Subir PDF', analyzeText: 'Analizar texto', privacyShort: 'La aplicación procesa el texto sin enviarlo a un modelo de IA.',
    localModeBadge: 'Análisis local de texto · sin modelos de IA',
    privacyPolicy: 'Privacidad',
    dropZoneLabel: 'Suelta un PDF aquí o elige un archivo', dropTitle: 'Suelta un PDF aquí',
    dropHint: 'o elige un archivo de tu dispositivo', topicScoreHint: 'Coincidencia relativa entre los temas detectados, no una probabilidad.',
    topicEvidenceLabel: 'Señales del texto',
    topicScoreA11y: 'Puntuación relativa de relevancia temática',
    sourceLabel: 'Tu fuente', addDocument: 'Añade un documento', choosePdf: 'Elegir PDF',
    textInputLabel: 'Texto del documento', textPlaceholder: 'Pega aquí el texto de un documento...',
    ready: 'Listo para analizar', analyzeDocument: 'Analizar documento', analysisLabel: 'Tu análisis',
    resultsTitle: 'Información del documento', summaryTitle: 'Resumen', runAgain: 'Volver a analizar',
    summaryEmpty: 'El resumen aparecerá aquí después del análisis.', keywordsTitle: 'Conceptos clave',
    keywordsEmpty: 'Todavía no hay palabras clave', topicTitle: 'Temas', topicEmpty: 'Esperando el análisis',
    questionsLabel: 'Consulta el documento', questionHeading: 'Obtén una respuesta clara',
    questionEmpty: 'Pregunta lo que quieras sobre el documento. Las respuestas se basan en el texto que proporcionaste.',
    questionInputLabel: 'Tu pregunta', questionPlaceholder: '¿De qué trata este documento?',
    askButton: 'Preguntar', metadataTitle: 'Detalles del documento', fileLabel: 'Archivo',
    noDocument: 'Sin documento', pagesLabel: 'Páginas', sizeLabel: 'Tamaño',
    footerPrivacy: 'Los documentos se procesan temporalmente para el análisis. Evita subir información personal sensible.',
    privacyDetailsTitle: 'Privacidad y publicidad',
    privacyDetails: 'Los PDF se extraen temporalmente y se eliminan al terminar el procesamiento. El análisis utiliza reglas locales de procesamiento de texto y no envía el contenido a un modelo de IA ni a un proveedor de inferencia. El proveedor de alojamiento puede procesar solicitudes y registros técnicos. Si se habilitan anuncios, Google puede utilizar cookies o tecnologías similares; el propietario debe configurar los mensajes de consentimiento certificados de Google donde sea necesario. Evita subir información sensible.',
    footerMade: 'Hecho para leer con claridad.', sourceCode: 'Código abierto', adPlaceholder: 'Publicidad',
    statusReadingPdf: 'Leyendo el PDF...', statusPdfLoaded: 'PDF cargado', statusAnalyzing: 'Analizando todas las secciones...',
    statusAnalyzed: 'Análisis completado', statusError: 'El análisis falló', statusNeedsAnalysis: 'Hay cambios por analizar',
    statusAsking: 'Buscando evidencia...', statusQuestionReady: 'Respuesta lista', statusPdfError: 'No se pudo cargar el PDF',
    keywordsProcessing: 'Extrayendo conceptos...', retry: 'Reintentar', summaryLoading: 'Preparando el resumen del documento...',
    placeholderAnswer: 'La respuesta aparecerá aquí.', questionLabel: 'Tú', answerLabel: 'lectoriia',
    questionErrorLabel: 'No se pudo responder', referenceLabel: 'Páginas de referencia', topicNeutral: 'Otro',
    alertNoText: 'Añade o sube texto antes de analizar.', questionNoText: 'Añade o sube un documento antes de hacer una pregunta.',
    errors: {
      local_processing_error: 'El análisis local no pudo completarse. Inténtalo de nuevo.',
      document_too_large: 'El documento supera el límite de 500 000 caracteres o 512 secciones. Divídelo en documentos más pequeños.',
      empty_document: 'No se proporcionó texto legible para analizar.',
      empty_question: 'Escribe una pregunta antes de consultar el documento.',
      invalid_request: 'Los datos de la solicitud no son válidos.',
      invalid_file_type: 'Elige un archivo PDF.',
      empty_file: 'El PDF seleccionado está vacío.',
      file_too_large: 'El PDF supera el límite de 4 MB en producción o 15 MB en local.',
      no_extractable_text: 'No se pudo extraer texto legible. El PDF podría ser una imagen o estar protegido.',
      invalid_pdf: 'No se pudo leer el PDF. Comprueba que sea válido y no esté protegido.',
      missing_file: 'Elige un archivo PDF primero.',
      request_too_large: 'La solicitud supera el límite de carga configurado.',
    },
    topics: {
      Technology: 'Tecnología', Science: 'Ciencia', Education: 'Educación', Business: 'Negocios',
      History: 'Historia', Health: 'Salud', Finance: 'Finanzas', Politics: 'Política',
      Law: 'Derecho', Literature: 'Literatura', Other: 'Otros'
    }
  }
};

const configNode = document.getElementById('lectoria-config');
const appConfig = configNode ? JSON.parse(configNode.textContent) : { locale: 'en', adsense: {}, developmentAds: false, maxUploadBytes: 15 * 1024 * 1024 };
const textInput = document.getElementById('text-input');
const pdfInput = document.getElementById('pdf-input');
const summaryOutput = document.getElementById('summary-output');
const keywordsOutput = document.getElementById('keywords-output');
const classificationOutput = document.getElementById('classification-output');
const questionForm = document.getElementById('question-form');
const questionInput = document.getElementById('question-input');
const questionHistory = document.getElementById('question-history');
const statusText = document.getElementById('status-text');
const statusBadge = document.getElementById('status-badge');
const progressWrap = document.getElementById('progress-wrap');
const docFile = document.getElementById('doc-file');
const docPages = document.getElementById('doc-pages');
const docSize = document.getElementById('doc-size');
const summaryReferences = document.getElementById('summary-references');
const keywordsState = document.getElementById('keywords-state');
const modelBadge = document.getElementById('analysis-model');
const analyzeButton = document.getElementById('analyze-button');
const manualAnalyzeButton = document.getElementById('manual-analyze');
const questionSubmit = document.getElementById('question-submit');
const languageSelect = document.getElementById('language-select');
const dropZone = document.getElementById('drop-zone');
const uploadTrigger = document.getElementById('upload-trigger');

let locale = 'en';
let currentDocumentText = '';
let currentPages = null;
let currentFileSize = 0;
let analyzedText = '';
let analysisPromise = null;
let analysisPromiseText = '';
let analysisController = null;
let uploadController = null;
let documentRequestId = 0;
let questionInFlight = false;
let currentStatusKey = 'ready';
let latestAnalysis = null;
let analysisErrorCode = null;
let conversation = [];
let renderedMessages = [];

const t = (key) => translations[locale][key] || translations.en[key] || key;
const errorText = (code) => translations[locale].errors[code] || translations.en.errors[code] || t('statusError');

const preferredLocale = () => {
  try {
    const saved = localStorage.getItem('lectoriia-locale') || localStorage.getItem('lectoria-locale');
    if (saved === 'en' || saved === 'es') return saved;
  } catch (error) {
    console.warn('Could not read the saved language preference.', error);
  }
  const preferences = [
    ...(Array.isArray(navigator.languages) ? navigator.languages : []),
    navigator.language,
    appConfig.locale
  ].filter(Boolean);
  for (const preference of preferences) {
    const language = preference.toLowerCase().split(/[-_]/)[0];
    if (language === 'es' || language === 'en') return language;
  }
  return 'en';
};

const applyTranslations = () => {
  document.documentElement.lang = locale;
  document.title = locale === 'es' ? 'lectoriia — Lectura documental, más clara' : 'lectoriia — Document reading, made clearer';
  document.querySelector('meta[name="description"]').content = locale === 'es'
    ? 'lectoriia convierte PDF y texto en resúmenes extractivos, conceptos clave, temas sugeridos y respuestas fundamentadas con procesamiento local.'
    : 'lectoriia turns PDFs and text into extractive summaries, key concepts, topic suggestions, and evidence-based answers using local text processing.';
  document.querySelectorAll('[data-i18n]').forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {
    element.placeholder = t(element.dataset.i18nPlaceholder);
  });
  document.querySelectorAll('[data-i18n-aria-label]').forEach((element) => {
    element.setAttribute('aria-label', t(element.dataset.i18nAriaLabel));
  });
  languageSelect.value = locale;
  statusText.textContent = t(currentStatusKey);
  if (latestAnalysis) {
    renderAnalysis(latestAnalysis);
  } else if (analysisErrorCode) {
    summaryOutput.textContent = errorText(analysisErrorCode);
  } else if (!statusBadge.classList.contains('is-busy')) {
    summaryOutput.textContent = t('summaryEmpty');
    renderKeywords([]);
    renderClassification([]);
  }
  renderChatHistory();
};

const setLocale = (value, remember = true) => {
  locale = value === 'es' ? 'es' : 'en';
  applyTranslations();
  if (remember) {
    try {
      localStorage.setItem('lectoriia-locale', locale);
    } catch (error) {
      console.warn('Could not save the language preference.', error);
    }
  }
};

const setStatus = (key) => {
  currentStatusKey = key;
  statusText.textContent = t(key);
};

const setBusy = (busy, statusKey = 'statusAnalyzing') => {
  statusBadge.classList.toggle('is-busy', busy);
  progressWrap.hidden = !busy;
  progressWrap.setAttribute('aria-hidden', String(!busy));
  analyzeButton.disabled = busy;
  manualAnalyzeButton.disabled = busy;
  questionSubmit.disabled = busy;
  textInput.disabled = busy;
  uploadTrigger.disabled = busy;
  document.getElementById('pdf-button').disabled = busy;
  dropZone.setAttribute('aria-disabled', String(busy));
  if (busy) setStatus(statusKey);
};

const formatBytes = (bytes) => {
  if (!bytes) return '0 KB';
  const value = bytes / 1024;
  return value >= 1024 ? `${(value / 1024).toFixed(1)} MB` : `${Math.round(value)} KB`;
};

const requestJson = async (url, options) => {
  const response = await fetch(url, options);
  let data;
  try {
    data = await response.json();
  } catch {
    const error = new Error(errorText('local_processing_error'));
    error.code = 'local_processing_error';
    throw error;
  }
  if (!response.ok) {
    const error = new Error(data?.code ? errorText(data.code) : (data?.error || errorText('local_processing_error')));
    error.code = data.code;
    throw error;
  }
  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    const error = new Error(errorText('invalid_request'));
    error.code = 'invalid_request';
    throw error;
  }
  return data;
};

const validateAnalysis = (data) => {
  if (
    !data.summary || typeof data.summary.summary !== 'string'
    || !data.keywords || !Array.isArray(data.keywords.keywords)
    || !data.classification || !Array.isArray(data.classification.labels)
  ) {
    const error = new Error(errorText('invalid_request'));
    error.code = 'invalid_request';
    throw error;
  }
  data.keywords.keywords = data.keywords.keywords.filter((item) => typeof item === 'string').slice(0, 10);
  data.classification.labels = data.classification.labels
    .filter((item) => item && typeof item === 'object' && typeof item.label === 'string')
    .slice(0, 3)
    .map((item) => ({
      label: item.label.slice(0, 80),
      score: Number.isFinite(Number(item.score)) ? Number(item.score) : 0,
      evidence: Array.isArray(item.evidence) ? item.evidence.filter((term) => typeof term === 'string').slice(0, 5) : [],
    }));
  data.summary.references = Array.isArray(data.summary.references)
    ? data.summary.references.filter((page) => Number.isInteger(page) && page > 0)
    : [];
  return data;
};

const validateUpload = (data) => {
  if (
    typeof data.text !== 'string'
    || !Array.isArray(data.pages)
    || data.pages.some((page) => typeof page !== 'string')
    || !Number.isInteger(data.page_count)
  ) {
    const error = new Error(errorText('invalid_request'));
    error.code = 'invalid_request';
    throw error;
  }
  if (!data.text.trim()) {
    const error = new Error(errorText('no_extractable_text'));
    error.code = 'no_extractable_text';
    throw error;
  }
  return data;
};

const showSkeletons = () => {
  summaryOutput.textContent = t('summaryLoading');
  summaryOutput.classList.add('is-loading');
  keywordsState.textContent = t('keywordsProcessing');
  keywordsOutput.replaceChildren();
  for (let index = 0; index < 4; index += 1) {
    const skeleton = document.createElement('span');
    skeleton.className = 'chip skeleton';
    skeleton.setAttribute('aria-hidden', 'true');
    keywordsOutput.append(skeleton);
  }
  classificationOutput.replaceChildren();
  const skeletonRow = document.createElement('div');
  skeletonRow.className = 'score-row skeleton-row';
  skeletonRow.setAttribute('aria-hidden', 'true');
  classificationOutput.append(skeletonRow);
};

const renderReferences = (container, references) => {
  container.replaceChildren();
  if (!Array.isArray(references) || !references.length) {
    container.hidden = true;
    return;
  }
  container.hidden = false;
  const label = document.createElement('span');
  label.className = 'reference-label';
  label.textContent = `${t('referenceLabel')}:`;
  container.append(label);
  references.forEach((page) => {
    const reference = document.createElement('span');
    reference.className = 'reference-chip';
    reference.textContent = locale === 'es' ? `p. ${page}` : `p. ${page}`;
    container.append(reference);
  });
};

const renderKeywords = (keywords) => {
  keywordsState.textContent = '';
  keywordsOutput.replaceChildren();
  if (!Array.isArray(keywords) || !keywords.length) {
    const placeholder = document.createElement('span');
    placeholder.className = 'chip placeholder';
    placeholder.textContent = t('keywordsEmpty');
    keywordsOutput.append(placeholder);
    return;
  }
  keywords.slice(0, 10).forEach((keyword, index) => {
    const chip = document.createElement('span');
    chip.className = 'chip keyword-chip';
    chip.style.setProperty('--item-index', index);
    chip.textContent = keyword;
    keywordsOutput.append(chip);
  });
};

const renderClassification = (labels) => {
  classificationOutput.replaceChildren();
  if (!Array.isArray(labels) || !labels.length) {
    const empty = document.createElement('div');
    empty.className = 'score-row placeholder';
    empty.textContent = t('topicEmpty');
    classificationOutput.append(empty);
    return;
  }
  [...labels]
    .sort((a, b) => Number(b.score || 0) - Number(a.score || 0))
    .slice(0, 3)
    .forEach((item, index) => {
      const score = Math.max(0, Math.min(1, Number(item.score) || 0));
      const row = document.createElement('div');
      row.className = 'score-row';
      row.style.setProperty('--item-index', index);
      const label = document.createElement('label');
      label.textContent = translations[locale].topics[item.label] || item.label;
      const bar = document.createElement('div');
      bar.className = 'score-bar';
      bar.setAttribute('role', 'meter');
      bar.setAttribute('aria-valuemin', '0');
      bar.setAttribute('aria-valuemax', '100');
      bar.setAttribute('aria-valuenow', String(Math.round(score * 100)));
      bar.setAttribute('aria-valuetext', `${t('topicScoreA11y')}: ${Math.round(score * 100)} / 100`);
      const fill = document.createElement('span');
      fill.className = 'score-fill';
      fill.style.setProperty('--score', `${score * 100}%`);
      bar.append(fill);
      const value = document.createElement('strong');
      value.textContent = `${Math.round(score * 100)} / 100`;
      row.append(label, bar, value);
      if (Array.isArray(item.evidence) && item.evidence.length) {
        const evidence = document.createElement('small');
        evidence.className = 'score-evidence';
        const terms = item.evidence
          .filter((term) => typeof term === 'string')
          .slice(0, 5)
          .map((term) => term.slice(0, 80));
        if (terms.length) {
          evidence.textContent = `${t('topicEvidenceLabel')}: ${terms.join(', ')}`;
          row.append(evidence);
        }
      }
      classificationOutput.append(row);
    });
};

const renderAnalysis = (data) => {
  const summary = data.summary || {};
  summaryOutput.textContent = summary.summary || t('summaryEmpty');
  summaryOutput.classList.remove('is-loading');
  renderReferences(summaryReferences, summary.references);
  renderKeywords(data.keywords?.keywords || []);
  renderClassification(data.classification?.labels || []);
  if (summary.model) {
    modelBadge.textContent = summary.source === 'local' ? t('localModeBadge') : summary.model;
    modelBadge.hidden = false;
  }
};

const clearConversation = () => {
  conversation = [];
  renderedMessages = [];
  renderChatHistory();
};

const renderChatHistory = () => {
  questionHistory.replaceChildren();
  if (!renderedMessages.length) {
    const empty = document.createElement('p');
    empty.className = 'history-empty';
    empty.textContent = t('questionEmpty');
    questionHistory.append(empty);
    return;
  }
  renderedMessages.forEach((message) => {
    const article = document.createElement('article');
    article.className = `chat-message ${message.role === 'user' ? 'chat-user' : 'chat-assistant'}`;
    const label = document.createElement('span');
    label.className = 'chat-label';
    label.textContent = message.role === 'user' ? t('questionLabel') : (message.error ? t('questionErrorLabel') : t('answerLabel'));
    const content = document.createElement('p');
    content.className = 'chat-content';
    content.textContent = message.code
      ? errorText(message.code)
      : (message.content || (message.pending ? t('statusAsking') : ''));
    if (message.pending) content.classList.add('is-loading');
    article.append(label, content);
    if (message.references?.length) {
      const refs = document.createElement('div');
      refs.className = 'reference-list';
      renderReferences(refs, message.references);
      article.append(refs);
    }
    questionHistory.append(article);
  });
  questionHistory.scrollTop = questionHistory.scrollHeight;
};

const analyzeText = async () => {
  const text = textInput.value.trim();
  if (!text) {
    setStatus('statusNeedsAnalysis');
    window.alert(t('alertNoText'));
    return false;
  }
  if (analysisPromise && analysisPromiseText === text) return analysisPromise;
  analysisController?.abort();
  const operationId = documentRequestId;
  const controller = new AbortController();
  analysisController = controller;
  analysisPromiseText = text;
  const promise = (async () => {
    latestAnalysis = null;
    analysisErrorCode = null;
    analyzedText = '';
    setBusy(true);
    showSkeletons();
    try {
      const data = await requestJson('/api/analyze-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, pages: currentPages }),
        signal: controller.signal,
      });
      if (operationId !== documentRequestId || text !== textInput.value.trim()) return false;
      validateAnalysis(data);
      currentDocumentText = text;
      analyzedText = text;
      latestAnalysis = data;
      analysisErrorCode = null;
      renderAnalysis(data);
      setStatus('statusAnalyzed');
      return true;
    } catch (error) {
      if (operationId !== documentRequestId || error.name === 'AbortError') return false;
      latestAnalysis = null;
      analysisErrorCode = error.code || 'local_processing_error';
      summaryOutput.textContent = errorText(analysisErrorCode);
      summaryOutput.classList.remove('is-loading');
      renderKeywords([]);
      renderClassification([]);
      summaryReferences.hidden = true;
      setStatus('statusError');
      return false;
    } finally {
      if (operationId === documentRequestId) setBusy(false);
    }
  })();
  analysisPromise = promise;
  try {
    return await promise;
  } finally {
    if (analysisPromise === promise) {
      analysisPromise = null;
      analysisPromiseText = '';
      if (analysisController === controller) analysisController = null;
    }
  }
};

const ensureAnalysis = async () => {
  if (analyzedText !== textInput.value.trim()) return analyzeText();
  return Boolean(analyzedText);
};

const uploadPdf = async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;
  pdfInput.value = '';
  const isPdfName = file.name.toLowerCase().endsWith('.pdf');
  const hasPdfType = !file.type || file.type === 'application/pdf';
  if (!isPdfName || !hasPdfType) {
    analysisErrorCode = 'invalid_file_type';
    summaryOutput.textContent = errorText(analysisErrorCode);
    setStatus('statusPdfError');
    return;
  }
  if (file.size > Number(appConfig.maxUploadBytes || 0)) {
    analysisErrorCode = 'file_too_large';
    summaryOutput.textContent = errorText(analysisErrorCode);
    setStatus('statusPdfError');
    return;
  }
  uploadController?.abort();
  analysisController?.abort();
  const operationId = ++documentRequestId;
  const controller = new AbortController();
  uploadController = controller;
  setBusy(true, 'statusReadingPdf');
  currentDocumentText = '';
  currentPages = null;
  currentFileSize = 0;
  analyzedText = '';
  clearConversation();
  docFile.textContent = t('noDocument');
  docPages.textContent = '0';
  docSize.textContent = '0 KB';
  summaryOutput.textContent = t('summaryEmpty');
  summaryReferences.hidden = true;
  renderKeywords([]);
  renderClassification([]);
  modelBadge.hidden = true;
  const formData = new FormData();
  formData.append('file', file);
  latestAnalysis = null;
  analysisErrorCode = null;
  try {
    const data = validateUpload(await requestJson('/api/upload-pdf', {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    }));
    if (operationId !== documentRequestId) return;
    currentDocumentText = data.text;
    currentPages = data.pages;
    const fileName = typeof data.file_name === 'string' ? data.file_name.slice(0, 255) : file.name;
    currentFileSize = data.size_bytes || file.size;
    analyzedText = '';
    textInput.value = currentDocumentText;
    docFile.textContent = fileName;
    docPages.textContent = String(data.page_count || 0);
    docSize.textContent = formatBytes(currentFileSize);
    setBusy(false);
    const completed = await analyzeText();
    if (!completed) return;
  } catch (error) {
    if (operationId !== documentRequestId || error.name === 'AbortError') return;
    setStatus('statusPdfError');
    analysisErrorCode = error.code || 'local_processing_error';
    summaryOutput.textContent = errorText(analysisErrorCode);
    summaryOutput.classList.remove('is-loading');
    setBusy(false);
  } finally {
    if (uploadController === controller) uploadController = null;
  }
};

const submitQuestion = async (event) => {
  event.preventDefault();
  if (questionInFlight) return;
  const question = questionInput.value.trim();
  const context = (currentDocumentText || textInput.value).trim();
  if (!context) {
    setStatus('statusNeedsAnalysis');
    window.alert(t('questionNoText'));
    return;
  }
  if (!question) {
    questionInput.focus();
    return;
  }

  const priorConversation = conversation.slice(-8).map(({ role, content }) => ({ role, content }));
  const userMessage = { role: 'user', content: question };
  const pendingMessage = { role: 'assistant', pending: true, content: '' };
  questionInFlight = true;
  renderedMessages.push(userMessage, pendingMessage);
  renderedMessages = renderedMessages.slice(-24);
  conversation.push(userMessage);
  conversation = conversation.slice(-8);
  renderChatHistory();
  questionInput.value = '';
  setBusy(true, 'statusAsking');
  try {
    const data = await requestJson('/api/ask-question', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question,
        context,
        pages: currentPages,
        history: priorConversation,
      }),
    });
    if (typeof data.answer !== 'string') {
      const error = new Error(errorText('invalid_request'));
      error.code = 'invalid_request';
      throw error;
    }
    pendingMessage.pending = false;
    pendingMessage.content = data.answer || t('placeholderAnswer');
    pendingMessage.references = Array.isArray(data.references)
      ? data.references.filter((page) => Number.isInteger(page) && page > 0)
      : [];
    conversation.push({ role: 'assistant', content: pendingMessage.content });
    conversation = conversation.slice(-8);
    setStatus('statusQuestionReady');
  } catch (error) {
    pendingMessage.pending = false;
    pendingMessage.error = true;
    pendingMessage.code = error.code || 'local_processing_error';
    pendingMessage.content = errorText(pendingMessage.code);
    setStatus('statusError');
  } finally {
    renderChatHistory();
    questionInFlight = false;
    setBusy(false);
  }
};

const initializeAds = () => {
  if (initializeAds.initialized) return;
  initializeAds.initialized = true;
  const { publisherId, slots = {} } = appConfig.adsense || {};
  const validPublisher = /^ca-pub-\d+$/.test(publisherId || '');
  let hasManualAd = false;
  document.querySelectorAll('.ad-unit').forEach((container) => {
    const slot = slots[container.dataset.adSlotName];
    if (validPublisher && /^\d+$/.test(slot || '')) {
      hasManualAd = true;
      container.hidden = false;
      container.replaceChildren();
      const ad = document.createElement('ins');
      ad.className = 'adsbygoogle';
      ad.style.display = 'block';
      ad.dataset.adClient = publisherId;
      ad.dataset.adSlot = slot;
      ad.dataset.adFormat = 'auto';
      ad.dataset.fullWidthResponsive = 'true';
      container.append(ad);
    } else if (appConfig.developmentAds) {
      container.hidden = false;
      container.classList.add('is-development');
    } else {
      container.hidden = true;
    }
  });
  if (!validPublisher || !hasManualAd) return;

  document.querySelectorAll('.adsbygoogle').forEach((ad) => {
    if (ad.dataset.initialized) return;
    ad.dataset.initialized = 'true';
    try {
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    } catch (error) {
      console.error('AdSense could not initialize an ad slot.', error);
    }
  });
};

document.querySelectorAll('[data-nav-target]').forEach((button) => {
  button.addEventListener('click', async () => {
    const target = document.getElementById(button.dataset.navTarget);
    document.querySelectorAll('[data-nav-target]').forEach((navButton) => {
      navButton.classList.toggle('active', navButton === button);
    });
    if (button.dataset.navTarget === 'summary-section' || button.dataset.navTarget === 'keywords-section') {
      const ready = await ensureAnalysis();
      if (!ready) return;
    }
    target?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (button.dataset.navTarget === 'question-section') {
      window.setTimeout(() => questionInput.focus({ preventScroll: true }), 250);
    }
  });
});

document.querySelectorAll('[data-repeat-analysis]').forEach((button) => {
  button.addEventListener('click', analyzeText);
});

document.getElementById('upload-trigger').addEventListener('click', () => pdfInput.click());
document.getElementById('pdf-button').addEventListener('click', () => pdfInput.click());
dropZone.addEventListener('click', () => {
  if (dropZone.getAttribute('aria-disabled') !== 'true') pdfInput.click();
});
dropZone.addEventListener('keydown', (event) => {
  if ((event.key === 'Enter' || event.key === ' ') && dropZone.getAttribute('aria-disabled') !== 'true') {
    event.preventDefault();
    pdfInput.click();
  }
});
dropZone.addEventListener('dragover', (event) => {
  event.preventDefault();
  if (dropZone.getAttribute('aria-disabled') !== 'true') dropZone.classList.add('is-dragging');
});
dropZone.addEventListener('dragleave', (event) => {
  if (!dropZone.contains(event.relatedTarget)) dropZone.classList.remove('is-dragging');
});
dropZone.addEventListener('drop', (event) => {
  event.preventDefault();
  dropZone.classList.remove('is-dragging');
  if (dropZone.getAttribute('aria-disabled') === 'true') return;
  const file = [...(event.dataTransfer?.files || [])].find((item) => item.name.toLowerCase().endsWith('.pdf'));
  if (file) uploadPdf({ target: { files: [file] } });
});
analyzeButton.addEventListener('click', analyzeText);
manualAnalyzeButton.addEventListener('click', () => {
  analyzeText();
});
pdfInput.addEventListener('change', uploadPdf);
questionForm.addEventListener('submit', submitQuestion);
languageSelect.addEventListener('change', () => setLocale(languageSelect.value));
textInput.addEventListener('input', () => {
  const nextText = textInput.value.trim();
  if (nextText !== currentDocumentText) {
    documentRequestId += 1;
    analysisController?.abort();
    uploadController?.abort();
    currentDocumentText = nextText;
    currentPages = null;
    analyzedText = '';
    docFile.textContent = t('noDocument');
    docPages.textContent = '0';
    docSize.textContent = '0 KB';
    clearConversation();
    setStatus(nextText ? 'statusNeedsAnalysis' : 'ready');
  }
});

setLocale(preferredLocale(), false);
initializeAds();
