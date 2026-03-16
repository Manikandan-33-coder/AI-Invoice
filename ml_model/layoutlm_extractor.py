from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification
from PIL import Image
import torch
import pdf2image

processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=True)
model = LayoutLMv3ForTokenClassification.from_pretrained("microsoft/layoutlmv3-base", num_labels=9)

FIELD_LABELS = {
    0: "O",
    1: "invoice_number",
    2: "date",
    3: "vendor_name",
    4: "bill_to",
    5: "ship_to",
    6: "subtotal",
    7: "tax",
    8: "total"
}

def ml_extract_fields(file_path):
    images = []
    if file_path.lower().endswith(".pdf"):
        images = pdf2image.convert_from_path(file_path, dpi=300)
    else:
        images = [Image.open(file_path)]

    extracted_fields = {}
    confidence_scores = {}

    for img in images:
        encoding = processor(img, return_tensors="pt")
        outputs = model(**encoding)
        logits = outputs.logits.squeeze(0)
        probs = torch.softmax(logits, dim=-1)

        predictions = torch.argmax(probs, dim=-1).tolist()
        max_probs = torch.max(probs, dim=-1).values.tolist()

        for idx, label_id in enumerate(predictions):
            field = FIELD_LABELS.get(label_id, "O")
            if field != "O":
                token_text = processor.tokenizer.decode(encoding.input_ids[0][idx])
                if field in extracted_fields:
                    extracted_fields[field] += " " + token_text
                    confidence_scores[field] = max(confidence_scores[field], max_probs[idx])
                else:
                    extracted_fields[field] = token_text
                    confidence_scores[field] = max_probs[idx]

    for f in FIELD_LABELS.values():
        if f != "O" and f not in extracted_fields:
            extracted_fields[f] = "Not Found"
            confidence_scores[f] = 0.0

    for k in confidence_scores:
        confidence_scores[k] = round(confidence_scores[k]*100, 2)

    return extracted_fields, confidence_scores