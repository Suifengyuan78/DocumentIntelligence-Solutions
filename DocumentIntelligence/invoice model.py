from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

import os
from dotenv import load_dotenv

load_dotenv()
service_endpoint = os.getenv("doc-endpoint")
service_key = os.getenv("doc-key")
filename = os.getenv("localfile")

#connect the service
document_analysis_client = DocumentAnalysisClient(
                endpoint=service_endpoint, 
                credential=AzureKeyCredential(service_key)
)


with open(filename,"rb") as stream:

   poller = document_analysis_client.begin_analyze_document("prebuilt-layout",stream)
result = poller.result()

for page in result.pages:
    print(f"Document Page {page.page_number} has {len(page.lines)} lines and {len(page.words)} words.")

    for i, line in enumerate(page.lines):
        print("Line {}:{}".format(i+1,line.content))

    for word in page.words:
        if word.confidence < 0.9:
           print("Word '{}' has a confidence of {}".format(word.content,word.confidence))

    for i, selectionMark in enumerate(page.selection_marks):
        print("selectionMark {}:{}:{}".format(i+1, selectionMark.state,selectionMark.confidence))

print ("-----------------")
for paragraph in result.paragraphs:
    print(f"{paragraph.role}:{paragraph.content}")
