<div align="center">
  <br>
  <img src="static/logo-mark.svg" width="112" alt="lectoriia">

  <h1>lectoriia</h1>
  <h3>Less noise. More understanding.</h3>

  <p>
    A calmer way to make sense of the documents in front of you.<br>
    Bring a PDF or a piece of text. Find its key ideas, see what it talks about,<br>
    and follow every answer back to the source.
  </p>

  <br>

  <a href="https://lectoriia.vercel.app/">
    <img src="https://img.shields.io/badge/open%20lectoriia-3977A8?style=for-the-badge&logo=readme&logoColor=white" alt="Open lectoriia">
  </a>
  &nbsp;
  <a href="https://github.com/MichaelAcostaDev/LectorIA">
    <img src="https://img.shields.io/badge/EXPLORE%20THE%20PROJECT-202B3A?style=for-the-badge&logo=github&logoColor=white" alt="Explore the project on GitHub">
  </a>

  <br><br>

  <img src="https://img.shields.io/badge/ENGLISH%20%26%20SPANISH-3977A8?style=flat-square" alt="English and Spanish">
  <img src="https://img.shields.io/badge/NO%20EXTERNAL%20AI-3977A8?style=flat-square" alt="No external AI">
  <img src="https://img.shields.io/badge/OPEN%20SOURCE-MIT-3977A8?style=flat-square" alt="Open source under the MIT license">

  <br><br>
</div>

---

<div align="center">

### Documents hold the details.
### lectoriia helps you find your way through them.

</div>

A long report can bury its main point. A useful answer can be hard to trace back to its source. And sometimes, you simply need a clearer first look before deciding what deserves a closer read.

**lectoriia is a small, thoughtful document companion** for that first pass. Add a PDF or paste text, and it brings together a concise extractive summary, recurring concepts, likely topics, and answers selected from relevant passages.

No complicated workflow. Just your document, a clearer view, and a path back to the words that matter.

<br>

## A clearer first read

<table>
  <tr>
    <td width="50%">
      <h3>◉ &nbsp;Find the thread</h3>
      <p>A short, extractive overview surfaces selected sentences from across the document—so you can get oriented before diving into every page.</p>
    </td>
    <td width="50%">
      <h3>⌕ &nbsp;Notice what recurs</h3>
      <p>Frequently used words and phrases offer clues about the document's central concepts and themes.</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>↳ &nbsp;Follow the evidence</h3>
      <p>Ask a question to find relevant sentences in the text. When page information is available, answers can point you back to their source.</p>
    </td>
    <td width="50%">
      <h3>文 &nbsp;Read your way</h3>
      <p>Use the interface in English or Spanish, with document language detection to help keep the analysis in context.</p>
    </td>
  </tr>
</table>

<br>

## Made to be honest about how it works

lectoriia does **not** use a generative AI model or call an external inference service. Its summaries rank source sentences using term importance and redundancy control; its keywords and topic suggestions use local text statistics; its answers use a lightweight BM25-style ranker, local synonym cues, and extractive sentence selection.

That means lectoriia can help you navigate a document, but it does not understand or interpret it like a person. Results are heuristic starting points—not a substitute for reading important passages and checking the original source. Topic scores show relative matches among detected labels; they are not probabilities.

> **No AI account. No model download. No inference API key.**
> The analysis uses application-side text-processing rules rather than a paid or free AI service. No models are downloaded, and no document content is sent to third-party inference.

## Your document stays the point

PDFs are uploaded to the application server so their text can be extracted. The extracted text is analyzed there; it is **not sent to an AI model or inference provider**. Uploaded PDFs are handled temporarily, and lectoriia does not intentionally keep a document library or save analyses for later.

The hosting provider may process requests and technical logs under its own terms. If advertising is enabled, advertising partners may use their own technologies and policies. Please avoid uploading sensitive or confidential material.

<div align="center">
  <a href="https://lectoriia.vercel.app/privacy"><strong>Read the privacy details →</strong></a>
</div>

<br>

## A useful companion, not a magic answer

| What lectoriia can do | What to keep in mind |
|:--|:--|
| Give you a quicker first look at a text-heavy document. | Summaries are assembled from source sentences; they are not AI-generated interpretations. |
| Surface recurring terms and suggest broad topics. | Topic labels and keywords are rule-based suggestions, not definitive classifications. |
| Find and rank passages with BM25-style term relevance, limited local synonym cues, and page references. | Heuristic matching can still miss indirect wording, and answers may be incomplete or require clarification. |
| Show page references when the PDF text extraction preserves them. | Scanned or image-only PDFs are not OCR-processed. |

Text analysis supports documents up to **500,000 characters and 512 sections**, enough for many long manuals. Analysis has no inference-provider fee, though the application and its hosting still have upload-size, execution-time, and usage limits.

<br>

## For the moments when a document feels too dense

lectoriia is here to make the first step easier: to help you see the shape of a text, notice what keeps returning, and find the passages worth reading more closely.

<div align="center">
  <br>
  <a href="https://lectoriia.vercel.app/">
    <img src="https://img.shields.io/badge/BRING%20A%20DOCUMENT.%20FIND%20YOUR%20FOCUS.%20%E2%86%92-3977A8?style=for-the-badge&logoColor=white" alt="Bring a document and find your focus">
  </a>
  <br><br>
  <sub>Made for clearer reading.</sub>
  <br><br>
</div>

---

<div align="center">
  <sub>
    lectoriia is open source under the <a href="LICENSE">MIT License</a>.
    &nbsp;·&nbsp;
    <a href="https://github.com/MichaelAcostaDev/LectorIA">View the project on GitHub</a>
  </sub>
</div>

## Run locally

The application uses Flask, vanilla JavaScript/CSS, and `pypdf`. All document analysis runs in Python on the application server; there is no model download, database, inference API, or analysis credential.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`. The interface supports English and Spanish. Copy `.env.example` to `.env` only if you need to change local configuration; AdSense and the privacy contact are optional configuration, not document-analysis dependencies.

Run the test suite with:

```powershell
python -m unittest discover -s tests -v
```

## Analysis limits and deployment notes

Text analysis is capped at **500,000 characters and 512 chunks**. PDF upload size is capped by the server configuration (15 MB locally and 4 MB on Vercel). Scanned/image-only PDFs are not OCR-processed. Summary and keyword extraction are statistical and extractive; category scores are relative heuristic relevance, not calibrated confidence.

The retrieval index exists only while a question request is being handled. It is built once per request and reused for chunk and sentence ranking; it is not cached across requests because Vercel workers may be short-lived or reused unpredictably. The browser sends the current document for each question, so no database or persistent document storage is needed.
