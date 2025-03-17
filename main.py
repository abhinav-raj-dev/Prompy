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
        """Extract and return a JSON object with key "information" containing 
        list of factual information/preferences from: {input}"""
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
    # Extract data using JSON parsing
    extracted_json = extraction_chain.invoke({"input": user_input})
    extracted_data = UserData.parse_raw(extracted_json)
    
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

# Example usage
if __name__ == "__main__":
    user_query = "I prefer recent AI ethics guidelines. Write about responsible AI development."
    result = process_prompt(user_query)
    print("Stored Data:", result.data_to_store)
    print("Enhanced Prompt:", result.enhanced_prompt)