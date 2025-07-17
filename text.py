from langchain_community.document_loaders import TextLoader, UnstructuredURLLoader

# Load from local text file
text_loader = TextLoader("data.txt")
text_data = text_loader.load()
print(text_data[0].metadata)

# Load from URL
url_loader = UnstructuredURLLoader(urls=[
    "https://www.geeksforgeeks.org/problems/largest-bst/1"
])
url_data = url_loader.load()
print(url_data[0].page_content)



from langchain.text_splitter import RecursiveCharacterTextSplitter

chunk_size = 100
chunk_overlap = 20

text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

chunks = text_splitter.split_documents(url_data)

print(chunks)
print(len(chunks))

for chunk in chunks:
    print(len(chunk.page_content))







