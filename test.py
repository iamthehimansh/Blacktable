from docling.document_converter import DocumentConverter

source = "./Himansh_CV.pdf"  # PDF path or URL
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())

import json
output_file = "output.json"
with open(output_file, "w") as f:
    json.dump(result.document.export_to_dict(), f, indent=2)