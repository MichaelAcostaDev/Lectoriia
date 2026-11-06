const textInput = document.getElementById('text-input');
const pdfInput = document.getElementById('pdf-input');
const summaryOutput = document.getElementById('summary-output');
const keywordsOutput = document.getElementById('keywords-output');
const classificationOutput = document.getElementById('classification-output');
const answerOutput = document.getElementById('answer-output');
const questionForm = document.getElementById('question-form');
const questionInput = document.getElementById('question-input');
const statusBadge = document.getElementById('status-badge');
const docFile = document.getElementById('doc-file');
const docPages = document.getElementById('doc-pages');
const docSize = document.getElementById('doc-size');

const uploadTrigger = document.getElementById('upload-trigger');
const pdfButton = document.getElementById('pdf-button');
const analyzeButton = document.getElementById('analyze-button');
const manualAnalyzeButton = document.getElementById('manual-analyze');

let currentDocumentText = '';

const setStatus = (message) => {
  statusBadge.textContent = message;
};

const formatBytes = (bytes) => {
  if (!bytes) return '0 KB';
  const value = bytes / 1024;
  return value >= 1024 ? `${(value / 1024).toFixed(1)} MB` : `${Math.round(value)} KB`;
};

const renderKeywords = (keywords) => {
  const list = Array.isArray(keywords) ? keywords : [];
  if (!list.length) {
    keywordsOutput.innerHTML = '<span class="chip placeholder">Sin resultados</span>';
    return;
  }

  keywordsOutput.innerHTML = list
    .slice(0, 10)
    .map((keyword) => `<span class="chip">${keyword}</span>`)
    .join('');
};

const renderClassification = (labels) => {
  const list = Array.isArray(labels) ? labels : [];
  if (!list.length) {
    classificationOutput.innerHTML = '<div class="score-row placeholder">Sin clasificación disponible</div>';
    return;
  }

  const ordered = [...list].sort((a, b) => (b.score || 0) - (a.score || 0));
  classificationOutput.innerHTML = ordered
    .slice(0, 5)
    .map((item) => {
      const score = Number(item.score || 0);
      const safeLabel = item.label || 'sin etiqueta';
      return `
        <div class="score-row">
          <label>${safeLabel}</label>
          <div class="score-bar"><span class="score-fill" style="width:${Math.max(6, score * 100)}%"></span></div>
          <strong>${score.toFixed(2)}</strong>
        </div>
      `;
    })
    .join('');
};

const analyzeText = async () => {
  const text = (textInput.value || '').trim();
  if (!text) {
    setStatus('Necesitas introducir texto');
    return;
  }

  setStatus('Analizando texto...');
  try {
    const response = await fetch('/api/analyze-text', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'No se pudo analizar el texto');
    }

    currentDocumentText = text;
    summaryOutput.textContent = data.summary?.summary || 'No se pudo generar un resumen.';
    renderKeywords(data.keywords?.keywords || []);
    renderClassification(data.classification?.labels || []);
    setStatus('Texto analizado');
  } catch (error) {
    setStatus('Error de análisis');
    summaryOutput.textContent = error.message || 'No se pudo completar el análisis.';
  }
};

const uploadPdf = async (event) => {
  const file = event.target.files && event.target.files[0];
  if (!file) return;

  setStatus('Leyendo PDF...');
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/upload-pdf', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'No se pudo leer el PDF');
    }

    currentDocumentText = data.text || '';
    textInput.value = currentDocumentText;
    summaryOutput.textContent = 'PDF cargado. El resumen y otras respuestas se calcularán según el contenido extraído.';
    docFile.textContent = data.file_name || 'Sin documento';
    docPages.textContent = String(data.page_count || 0);
    docSize.textContent = formatBytes(data.size_bytes || 0);
    setStatus('PDF cargado');

    const analysisResponse = await fetch('/api/analyze-text', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: currentDocumentText }),
    });

    const analysisData = await analysisResponse.json();
    if (analysisResponse.ok) {
      summaryOutput.textContent = analysisData.summary?.summary || 'Se cargó el documento correctamente.';
      renderKeywords(analysisData.keywords?.keywords || []);
      renderClassification(analysisData.classification?.labels || []);
      setStatus('Documento analizado');
    }
  } catch (error) {
    setStatus('Fallo al cargar PDF');
    summaryOutput.textContent = error.message || 'No se pudo procesar el archivo PDF.';
  }
};

questionForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const question = questionInput.value.trim();
  const context = (currentDocumentText || textInput.value || '').trim();

  if (!question) {
    answerOutput.textContent = 'Escribe una pregunta para consultar el documento.';
    return;
  }

  if (!context) {
    answerOutput.textContent = 'Primero añade texto o sube un PDF para consultar su contenido.';
    return;
  }

  try {
    const response = await fetch('/api/ask-question', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, context }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'No se pudo responder la pregunta');
    }

    answerOutput.textContent = data.answer || 'No se pudo obtener una respuesta precisa.';
  } catch (error) {
    answerOutput.textContent = error.message || 'No se pudo responder la pregunta.';
  }
});

uploadTrigger.addEventListener('click', () => pdfInput.click());
pdfButton.addEventListener('click', () => pdfInput.click());
analyzeButton.addEventListener('click', analyzeText);
manualAnalyzeButton.addEventListener('click', analyzeText);
pdfInput.addEventListener('change', uploadPdf);
