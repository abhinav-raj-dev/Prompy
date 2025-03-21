import sys
from typing import List
from pydantic.v1 import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Define Pydantic v1 models
class UserData(BaseModel):
    information: List[str] = Field(
        ..., 
        description="List of factual information or preferences from the user input"
    )
    
class ResponseModel(BaseModel):
    data_to_store: UserData
    enhanced_prompt: str

# Initialize components
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# Initialize ChromaDB
vector_store = Chroma(
    collection_name="user_data",
    embedding_function=embedding,
    persist_directory="./chroma_db"
)

# Define prompt templates
refinement_template = """Analyze and improve this prompt. Consider:
- User's information preferences: {context}
- Clear output requirements
- Specificity and focus areas
- Domain-specific terminology

Original prompt: {user_input}
Improved prompt:"""

# Create extraction chain using JSON mode
extraction_chain = (
    ChatPromptTemplate.from_template(
        """Extract and return PURE JSON (no markdown) with key "information" 
        containing list of factual information/preferences from: {input}"""
    )
    | llm
    | StrOutputParser()
)

# Refinement chain
refinement_chain = (
    RunnablePassthrough.assign(
        context=lambda x: vector_store.similarity_search(x["user_input"], k=3)
    )
    | ChatPromptTemplate.from_template(refinement_template)
    | llm
    | StrOutputParser()
)

def process_prompt(user_input: str) -> ResponseModel:
    # Extract data with markdown stripping
    extracted_response = extraction_chain.invoke({"input": user_input})
    
    # Clean JSON response
    json_str = extracted_response.strip().replace('```json', '').replace('```', '')
    
    try:
        extracted_data = UserData.parse_raw(json_str)
    except Exception as e:
        print(f"Failed to parse JSON: {json_str}")
        raise
    
    # Refine prompt
    refined_prompt = refinement_chain.invoke({"user_input": user_input})
    
    # Store data
    if extracted_data.information:
        docs = [
            Document(
                page_content=info,
                metadata={"source": "user_input"}
            ) for info in extracted_data.information
        ]
        vector_store.add_documents(docs)
    
    # Store refined prompt
    vector_store.add_documents([
        Document(
            page_content=refined_prompt,
            metadata={"source": "enhanced_prompt"}
        )
    ])
    
    return ResponseModel(
        data_to_store=extracted_data,
        enhanced_prompt=refined_prompt
    )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as a command-line argument.")
        print("Usage: python script.py '<your prompt>'")
        sys.exit(1)
    
    user_input = sys.argv[1]
    result = process_prompt(user_input)
    print("Stored Data:", result.data_to_store)
    print("\n Enhanced Prompt:", result.enhanced_prompt)