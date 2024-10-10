from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

import os
from dotenv import load_dotenv

load_dotenv()
service_endpoint = os.getenv("doc-endpoint")
service_key = os.getenv("doc-key")
docurl=os.getenv("documentURL")

#connect the service
document_analysis_client = DocumentAnalysisClient(
                endpoint=service_endpoint, 
                credential=AzureKeyCredential(service_key)
)
poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-read",docurl)
result = poller.result()

for page in result.pages:
    print(f"Document Page {page.page_number} has {len(page.lines)} lines and {len(page.words)} words.")

    for i, line in enumerate(page.lines):
        print("Line {}:{}".format(i+1,line.content))
    for word in page.words:
        print("Word '{}' has a confidence of {}".format(word.content,word.confidence))
    

print ("-----------------")
for paragraph in result.paragraphs:
    print(f"{paragraph.role}:{paragraph.content}")
