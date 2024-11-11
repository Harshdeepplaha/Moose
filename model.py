from langchain_community.llms import Ollama

def initialize_llm(model_name="llama3.2"):
    """
    Initializes and returns the LLM instance with the specified model name.
    
    Parameters:
    - model_name (str): The name of the model to use (default: "llama2").
    
    Returns:
    - Ollama: An instance of the Ollama model.
    """
    return Ollama(model=model_name)
