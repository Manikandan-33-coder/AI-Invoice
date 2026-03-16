# AI-Powered Invoice Processing System

## Overview
This project is an **AI-powered invoice processing system** built with Python and Flask.  
It automatically extracts key invoice data from PDF and image files using a combination of **ML models (LayoutLMv3)** and **OCR (Tesseract)**.  
The system provides field-level confidence scores and allows users to save extracted invoices.

---

## Features

- Upload and process **PDF, JPG, PNG** invoices
- Extract key fields:
  - Invoice Number
  - Invoice Date
  - Vendor Name
  - Bill To / Ship To
  - Subtotal, Tax, Total
- AI/ML extraction using **LayoutLMv3**
- OCR fallback for scanned/poor-quality invoices
- Field-level confidence scoring
- Autofill form for easy saving
- Supports multi-page invoices
- Ready for **PWA deployment** (installable on desktop/mobile)

---

## Folder Structure
