<div align="center">
  <img src="static/logo-mark.svg" width="104" alt="LectorIA logo">

  # LectorIA

  **Read less noise. Understand more.**

  Bilingual, AI-assisted document analysis for PDFs and plain text.

  [Live demo](https://lectoriia.vercel.app/) · [Repository](https://github.com/MichaelAcostaDev/LectorIA)

  ![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
  ![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)
  ![License](https://img.shields.io/badge/License-MIT-blue.svg)
</div>

## See it in action

Add current screenshots here after capturing them from the live application. No screenshots are included yet.

<!-- Suggested files: docs/images/lectoria-desktop.png and docs/images/lectoria-mobile.png -->

## What it does

- Summarizes PDF and pasted text with a document-wide, chunked analysis.
- Extracts meaningful concepts and classifies the document by topic.
- Answers questions using relevant excerpts and conversation context.
- Preserves PDF page numbers for references where they are available.
- Supports English and Spanish, with browser-language detection and a remembered manual choice.
- Processes uploaded PDFs temporarily; LectorIA does not persist uploaded documents.
- Provides a responsive interface with reduced-motion support.

AI results depend on the configured Hugging Face model and provider. The application returns explicit errors when AI is not configured or a provider request fails; it does not disguise heuristic output as AI analysis.

## Built with

- Python 3.10+
- Flask
- Hugging Face Inference Providers chat-completion API
- pypdf
- HTML, CSS, and vanilla JavaScript
- Vercel Python Functions

## Get started

### Requirements

- Python 3.10 or later
- pip
- A Hugging Face user access token with Inference Providers permission for AI features

### Install and run

```bash
git clone https://github.com/MichaelAcostaDev/LectorIA.git
cd LectorIA

python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env`, add your Hugging Face token, then start Flask:

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000). Without a token, PDF text extraction and the interface work, but AI analysis returns a clear configuration error.

Run the automated tests with:

```bash
python -m unittest discover -s tests -v
```

## Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `HUGGINGFACE_API_TOKEN` | For AI | Fine-grained Hugging Face token with Inference Providers permission. Keep it server-side. |
| `HF_CHAT_MODEL` | No | Chat-completion model ID. Defaults to `Qwen/Qwen2.5-7B-Instruct-1M`. |
| `PORT` | No | Local Flask port; defaults to `5000`. |
| `FLASK_DEBUG` | No | Set to `true` only for local development. |
| `ADSENSE_PUBLISHER_ID` | For ads | Approved AdSense publisher ID, in the `ca-pub-…` format. |
| `ADSENSE_SLOT_HERO` | For that slot | AdSense slot ID for the placement below the hero. |
| `ADSENSE_SLOT_MIDDLE` | For that slot | AdSense slot ID between analysis sections. |
| `ADSENSE_SLOT_SIDEBAR` | For that slot | AdSense slot ID in the document-details sidebar. |
| `ADSENSE_SLOT_FOOTER` | For that slot | AdSense slot ID near the footer. |

Optional ad variables can be left blank. In local development, empty slots show labeled layout placeholders only; in production, unconfigured ad locations stay hidden. The Hugging Face token is never passed to the browser.

## How document analysis works

`ai_utils.py` sends actual `system`, `user`, and (for follow-up questions) `assistant` messages to the [OpenAI-compatible Hugging Face chat-completion endpoint](https://huggingface.co/docs/inference-providers/tasks/chat-completion). The default [Qwen2.5-7B-Instruct-1M](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-1M) is listed in Hugging Face's recommended chat models and is designed for long-context tasks; the [Qwen2.5 model card](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) lists both Spanish and English among supported languages. The model is configurable because provider availability, cost, and performance can change. Confirm the selected model is available to your Hugging Face account before deployment.

Long inputs are split into overlapping excerpts, retain page metadata when available, and are consolidated rather than silently truncated. The application currently caps analysis at 180,000 characters and 32 generated excerpts; larger inputs receive an explicit error. Question answering selects relevant excerpts, includes recent conversation turns, and validates cited page numbers against the pages actually sent to the model.

The app does not use a sentiment model as a topic classifier and does not provide a heuristic answer when the AI provider fails. Scanned PDFs without an extractable text layer are not OCR-processed.

## Project layout

```text
LectorIA/
├── ai_utils.py          # Chat-completion prompts, chunking, and analysis
├── app.py               # Flask API, HTML entry point, and ads.txt response
├── pdf_utils.py         # PDF validation, temporary extraction, and page text
├── requirements.txt
├── vercel.json
├── .env.example
├── LICENSE
├── tests/
│   ├── test_ai_utils.py
│   └── test_app.py
├── static/
│   ├── favicon.svg
│   ├── logo-mark.svg
│   ├── script.js
│   └── style.css
└── templates/
    └── index.html
```

## Deploy to Vercel

1. Import the repository into Vercel and keep the included Python build and catch-all route configuration.
2. Add `HUGGINGFACE_API_TOKEN` as a server-side environment variable in the Vercel project settings. Optionally set `HF_CHAT_MODEL`.
3. Deploy and verify `/api/health`.
4. Before serving ads, obtain AdSense approval, set `ADSENSE_PUBLISHER_ID` and the slot IDs for the placements you want, then redeploy.
5. In AdSense, configure the site's ads and privacy/consent messages. Google requires an approved Google-certified consent management platform for applicable users in the EEA, UK, and Switzerland. This application does not claim to implement that legal consent service itself.

When a valid publisher ID is configured, `/ads.txt` serves the corresponding Google seller declaration. Never enter placeholder or invented IDs. Setting ad environment variables only prepares the integration; ads are not monetizing until AdSense approves the site and serves ads.

## Privacy and security

- Keep Hugging Face and AdSense settings in server-side environment variables; never commit `.env`.
- Uploaded files are size-checked, written to a temporary file for extraction, and removed after processing. Extracted document text is sent to the configured Hugging Face Inference Provider for analysis.
- Do not upload sensitive personal or confidential documents. Review Hugging Face's current inference-provider data-handling terms before use.
- PDF files are limited to 15 MB. The document text analysis limit is 180,000 characters.
- Report a security issue privately to the repository owner rather than posting secrets or exploit details in a public issue.

## Contributing

1. Fork the repository and create a focused branch.
2. Make your changes and add or update tests.
3. Run `python -m unittest discover -s tests -v`.
4. Open a pull request describing the change and any deployment implications.

Please avoid including real documents, API tokens, publisher IDs, or other sensitive data in pull requests.

## Roadmap

- Add OCR for scanned PDFs.
- Add optional document export and richer page-level source navigation.
- Expand automated browser and deployment integration tests.
- Evaluate provider/model latency and quality against a published bilingual document test set.

## License

LectorIA's code is released under the [MIT License](./LICENSE). Model weights, Hugging Face services, and third-party assets remain subject to their own terms and licenses.

<div align="center">
  Made with care for clearer reading.
</div>
