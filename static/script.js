const translations = {
  en: {
    navSummary: 'Summary', navKeywords: 'Keywords', navQuestions: 'Ask questions',
    homeLabel: 'LectorIA home', navLabel: 'Document sections', workspaceLabel: 'Document analysis workspace',
    adLabel: 'Advertisement', languageLabel: 'Interface language', eyebrow: 'Your thoughtful document reader',
    heroTitleFirst: 'Understand every', heroTitleSecond: 'document, faster.',
    heroDescription: 'Turn a PDF or pasted text into a grounded summary, meaningful keywords, topic insights, and answers you can trace back to the source.',
    uploadPdf: 'Upload PDF', analyzeText: 'Analyze text', privacyShort: 'Your document is processed temporarily and is not stored by LectorIA.',
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
    privacyDetails: "PDFs are temporarily extracted and removed after processing. Document text is sent to Hugging Face Inference Providers to generate results. LectorIA does not retain documents. If ads are enabled, Google may use cookies or similar technologies; the publisher must configure Google's certified consent messaging where required. Avoid uploading sensitive information.",
    footerMade: 'Made for clearer reading.', sourceCode: 'Open source', adPlaceholder: 'Advertisement',
    statusReadingPdf: 'Reading PDF...', statusPdfLoaded: 'PDF loaded', statusAnalyzing: 'Analyzing every section...',
    statusAnalyzed: 'Analysis complete', statusError: 'Analysis failed', statusNeedsAnalysis: 'Changes need analysis',
    statusAsking: 'Finding evidence...', statusQuestionReady: 'Answer ready', statusPdfError: 'Could not load PDF',
    keywordsProcessing: 'Extracting concepts...', retry: 'Try again', summaryLoading: 'Building a document-wide summary...',
    placeholderAnswer: 'Your answer will appear here.', questionLabel: 'You', answerLabel: 'LectorIA',
    questionErrorLabel: 'Could not answer', referenceLabel: 'Source pages', topicNeutral: 'Other',
    alertNoText: 'Add or upload document text before analysis.', questionNoText: 'Add or upload a document before asking a question.',
    errors: {
      missing_token: 'AI analysis is not configured yet. Add HUGGINGFACE_API_TOKEN in the deployment environment.',
      invalid_token: 'The Hugging Face token was rejected. Check that it has Inference Providers access.',
      model_unavailable: 'The configured AI model is unavailable from Hugging Face Inference Providers.',
      provider_rate_limit: 'The AI provider is busy. Wait a moment and retry.',
      provider_timeout: 'The AI provider took too long to respond. Please retry.',
      provider_unavailable: 'The AI provider could not be reached. Check the connection and retry.',
      provider_error: 'The AI provider could not complete the request. Please retry.',
      provider_context_limit: 'The model could not accept this amount of context. Try a shorter document.',
      document_too_large: 'This document exceeds the current analysis limit. Split it into smaller documents and retry.',
      empty_document: 'No readable document text was provided.',
      empty_question: 'Write a question before consulting the document.',
      invalid_request: 'The request data is invalid.',
      invalid_file_type: 'Choose a PDF file.',
      empty_file: 'The selected PDF is empty.',
      file_too_large: 'The PDF exceeds the 15 MB file size limit.',
      no_extractable_text: 'No readable text could be extracted. The PDF may be scanned or protected.',
      invalid_pdf: 'The PDF could not be read. Check that the file is valid and not protected.',
      missing_file: 'Choose a PDF file first.',
      request_too_large: 'The request exceeds the 15 MB upload limit.',
      invalid_provider_response: 'The AI provider returned an incomplete response. Please retry.',
      empty_provider_response: 'The AI provider returned an empty response. Please retry.'
    },
    topics: {
      Technology: 'Technology', Science: 'Science', Education: 'Education', Business: 'Business',
      History: 'History', Health: 'Health', Finance: 'Finance', Politics: 'Politics',
      Law: 'Law', Literature: 'Literature', Other: 'Other'
    }
  },
  es: {
    navSummary: 'Resumen', navKeywords: 'Palabras clave', navQuestions: 'Preguntas',
    homeLabel: 'Inicio de LectorIA', navLabel: 'Secciones del documento', workspaceLabel: 'Área de análisis del documento',
    adLabel: 'Publicidad', languageLabel: 'Idioma de la interfaz', eyebrow: 'Tu lector inteligente de documentos',
    heroTitleFirst: 'Comprende cada', heroTitleSecond: 'documento, más rápido.',
    heroDescription: 'Convierte un PDF o texto en un resumen fundamentado, conceptos clave, temas y respuestas vinculadas con la fuente.',
    uploadPdf: 'Subir PDF', analyzeText: 'Analizar texto', privacyShort: 'LectorIA procesa el documento temporalmente y no lo almacena.',
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
    privacyDetails: 'Los PDF se extraen temporalmente y se eliminan al terminar el procesamiento. El texto se envía a Hugging Face Inference Providers para generar resultados. LectorIA no conserva los documentos. Si se habilitan anuncios, Google puede utilizar cookies o tecnologías similares; el propietario debe configurar los mensajes de consentimiento certificados de Google donde sea necesario. Evita subir información sensible.',
    footerMade: 'Hecho para leer con claridad.', sourceCode: 'Código abierto', adPlaceholder: 'Publicidad',
    statusReadingPdf: 'Leyendo el PDF...', statusPdfLoaded: 'PDF cargado', statusAnalyzing: 'Analizando todas las secciones...',
    statusAnalyzed: 'Análisis completado', statusError: 'El análisis falló', statusNeedsAnalysis: 'Hay cambios por analizar',
    statusAsking: 'Buscando evidencia...', statusQuestionReady: 'Respuesta lista', statusPdfError: 'No se pudo cargar el PDF',
    keywordsProcessing: 'Extrayendo conceptos...', retry: 'Reintentar', summaryLoading: 'Preparando el resumen del documento...',
    placeholderAnswer: 'La respuesta aparecerá aquí.', questionLabel: 'Tú', answerLabel: 'LectorIA',
    questionErrorLabel: 'No se pudo responder', referenceLabel: 'Páginas de referencia', topicNeutral: 'Otro',
    alertNoText: 'Añade o sube texto antes de analizar.', questionNoText: 'Añade o sube un documento antes de hacer una pregunta.',
    errors: {
      missing_token: 'El análisis con IA no está configurado. Añade HUGGINGFACE_API_TOKEN al entorno de despliegue.',
      invalid_token: 'Hugging Face rechazó el token. Comprueba que tenga acceso a Inference Providers.',
      model_unavailable: 'El modelo configurado no está disponible en Hugging Face Inference Providers.',
      provider_rate_limit: 'El proveedor de IA está ocupado. Espera un momento e inténtalo de nuevo.',
      provider_timeout: 'El proveedor de IA tardó demasiado en responder. Inténtalo de nuevo.',
      provider_unavailable: 'No se pudo conectar con el proveedor de IA. Comprueba la conexión e inténtalo de nuevo.',
      provider_error: 'El proveedor de IA no pudo completar la solicitud. Inténtalo de nuevo.',
      provider_context_limit: 'El modelo no pudo aceptar tanto contexto. Prueba con un documento más corto.',
      document_too_large: 'El documento supera el límite de análisis actual. Divídelo en documentos más pequeños.',
      empty_document: 'No se proporcionó texto legible para analizar.',
      empty_question: 'Escribe una pregunta antes de consultar el documento.',
      invalid_request: 'Los datos de la solicitud no son válidos.',
      invalid_file_type: 'Elige un archivo PDF.',
      empty_file: 'El PDF seleccionado está vacío.',
      file_too_large: 'El PDF supera el límite de 15 MB.',
      no_extractable_text: 'No se pudo extraer texto legible. El PDF podría ser una imagen o estar protegido.',
      invalid_pdf: 'No se pudo leer el PDF. Comprueba que sea válido y no esté protegido.',
      missing_file: 'Elige un archivo PDF primero.',
      request_too_large: 'La solicitud supera el límite de carga de 15 MB.',
      invalid_provider_response: 'El proveedor de IA devolvió una respuesta incompleta. Inténtalo de nuevo.',
      empty_provider_response: 'El proveedor de IA devolvió una respuesta vacía. Inténtalo de nuevo.'
    },
    topics: {
      Technology: 'Tecnología', Science: 'Ciencia', Education: 'Educación', Business: 'Negocios',
      History: 'Historia', Health: 'Salud', Finance: 'Finanzas', Politics: 'Política',
      Law: 'Derecho', Literature: 'Literatura', Other: 'Otros'
    }
  }
};

const configNode = document.getElementById('lectoria-config');
const appConfig = configNode ? JSON.parse(configNode.textContent) : { locale: 'en', adsense: {}, developmentAds: false };
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

let locale = 'en';
let currentDocumentText = '';
let currentPages = null;
let currentFileSize = 0;
let analyzedText = '';
let analysisPromise = null;
let currentStatusKey = 'ready';
let latestAnalysis = null;
let analysisErrorCode = null;
let conversation = [];
let renderedMessages = [];

const t = (key) => translations[locale][key] || translations.en[key] || key;
const errorText = (code) => translations[locale].errors[code] || translations.en.errors[code] || t('statusError');

const preferredLocale = () => {
  try {
    const saved = localStorage.getItem('lectoria-locale');
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
  document.title = locale === 'es' ? 'LectorIA — Análisis documental' : 'LectorIA — Document intelligence';
  document.querySelector('meta[name="description"]').content = locale === 'es'
    ? 'LectorIA convierte PDF y texto en resúmenes claros, conceptos clave, temas y respuestas fundamentadas.'
    : 'LectorIA turns PDFs and text into clear summaries, useful keywords, topic insights, and evidence-based answers.';
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
      localStorage.setItem('lectoria-locale', locale);
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
    const error = new Error(errorText('provider_error'));
    error.code = 'provider_error';
    throw error;
  }
  if (!response.ok) {
    const error = new Error(data?.code ? errorText(data.code) : (data?.error || errorText('provider_error')));
    error.code = data.code;
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
      const fill = document.createElement('span');
      fill.className = 'score-fill';
      fill.style.setProperty('--score', `${Math.max(3, score * 100)}%`);
      bar.append(fill);
      const value = document.createElement('strong');
      value.textContent = `${Math.round(score * 100)}%`;
      row.append(label, bar, value);
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
    modelBadge.textContent = summary.model;
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
  if (analysisPromise) return analysisPromise;

  analysisPromise = (async () => {
    latestAnalysis = null;
    analysisErrorCode = null;
    setBusy(true);
    showSkeletons();
    try {
      const data = await requestJson('/api/analyze-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, pages: currentPages }),
      });
      currentDocumentText = text;
      analyzedText = text;
      latestAnalysis = data;
      analysisErrorCode = null;
      renderAnalysis(data);
      setStatus('statusAnalyzed');
      return true;
    } catch (error) {
      latestAnalysis = null;
      analysisErrorCode = error.code || 'provider_unavailable';
      summaryOutput.textContent = errorText(analysisErrorCode);
      summaryOutput.classList.remove('is-loading');
      renderKeywords([]);
      renderClassification([]);
      summaryReferences.hidden = true;
      setStatus('statusError');
      return false;
    } finally {
      setBusy(false);
    }
  })();
  try {
    return await analysisPromise;
  } finally {
    analysisPromise = null;
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
    const data = await requestJson('/api/upload-pdf', { method: 'POST', body: formData });
    currentDocumentText = data.text || '';
    currentPages = Array.isArray(data.pages) ? data.pages : null;
    const fileName = data.file_name || file.name;
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
    setStatus('statusPdfError');
    analysisErrorCode = error.code || 'provider_unavailable';
    summaryOutput.textContent = errorText(analysisErrorCode);
    summaryOutput.classList.remove('is-loading');
    setBusy(false);
  }
};

const submitQuestion = async (event) => {
  event.preventDefault();
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
  renderedMessages.push(userMessage, pendingMessage);
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
    pendingMessage.pending = false;
    pendingMessage.content = data.answer || t('placeholderAnswer');
    pendingMessage.references = data.references || [];
    conversation.push(userMessage, { role: 'assistant', content: pendingMessage.content });
    setStatus('statusQuestionReady');
  } catch (error) {
    pendingMessage.pending = false;
    pendingMessage.error = true;
    pendingMessage.code = error.code || 'provider_unavailable';
    pendingMessage.content = errorText(pendingMessage.code);
    setStatus('statusError');
  } finally {
    renderChatHistory();
    setBusy(false);
  }
};

const initializeAds = () => {
  const { publisherId, slots = {} } = appConfig.adsense || {};
  const validPublisher = /^ca-pub-\d+$/.test(publisherId || '');
  let scriptAdded = false;
  document.querySelectorAll('.ad-unit').forEach((container) => {
    const slot = slots[container.dataset.adSlotName];
    if (validPublisher && /^\d+$/.test(slot || '')) {
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
      if (!scriptAdded) {
        const script = document.createElement('script');
        script.async = true;
        script.crossOrigin = 'anonymous';
        script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${encodeURIComponent(publisherId)}`;
        script.onload = () => {
          document.querySelectorAll('.adsbygoogle').forEach(() => {
            try {
              (window.adsbygoogle = window.adsbygoogle || []).push({});
            } catch (error) {
              console.error('AdSense could not initialize an ad slot.', error);
            }
          });
        };
        document.head.append(script);
        scriptAdded = true;
      }
    } else if (appConfig.developmentAds) {
      container.hidden = false;
      container.classList.add('is-development');
    } else {
      container.hidden = true;
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
    currentDocumentText = nextText;
    currentPages = null;
    currentFileName = '';
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
