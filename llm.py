from langchain.llms import OpenAI, LlamaCpp, CTransformers
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


class LangModel:
    def __init__(self, api_key=None, model_path=None, model_type=None):
        self.callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        if model_type == "openai":
            assert api_key is not None, "API key must be provided when using OpenAI model"
            import openai
            openai.api_key = api_key
            self.llm = OpenAI(temperature=0)
        elif model_type == "llama":
            assert model_path is not None, "Model path must be provided when using Llama model"
            #self.llm = CTransformers(model=model_path, model_type="mpt")
            self.llm = LlamaCpp(model_path=model_path, callback_manager=self.callback_manager, verbose=True, n_ctx=2048)
        else:
            raise ValueError("Invalid model_type specified. Choose either 'openai' or 'llama'.")

    def generate_summary(self, content):
        chunk_size = 500
        chunk_overlap = 0
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        content = splitter.split_text(content)
        content = [Document(page_content=t) for t in content[:3]]
        chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        return chain.run(content)
