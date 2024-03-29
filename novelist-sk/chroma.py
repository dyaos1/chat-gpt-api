from semantic_kernel.connectors.memory.chroma import ChromaMemoryStore
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin

from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAITextEmbedding
from semantic_kernel.prompt_template.prompt_template_config import PromptTemplateConfig
import semantic_kernel as sk

import os
from dotenv import load_dotenv

load_dotenv()

async def main():

    ## init kernal
    kernel = sk.Kernel()
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="default",
            ai_model_id="gpt-3.5-turbo",
            api_key=os.getenv("API_KEY")
        )
    )

    ## init embedding service
    kernel.add_service(
        OpenAITextEmbedding(
            ai_model_id="text-embedding-ada-002",
            api_key=os.getenv("API_KEY")
        ))


    ## issue solve
    class CustomOpenAIEmbeddings(OpenAITextEmbedding):
        def __init__(self, api_key, *args, **kwargs):
            super().__init__(api_key=api_key, *args, **kwargs)
            
        def _embed_documents(self, texts):
            return super().generate_embeddings(texts)  # <--- use OpenAIEmbedding's embedding function

        def __call__(self, **kwargs):
            return self._embed_documents(kwargs.get("input"))     # <--- get the embeddings


    ## set up vector database
    CUR_DIR = os.path.dirname(os.path.abspath(__file__))
    CHROMA_PERSIST_DIR = os.path.join(CUR_DIR, "chroma-persist")
    memory = SemanticTextMemory(
        storage=ChromaMemoryStore(
            persist_directory=CHROMA_PERSIST_DIR
        ),
        embeddings_generator=CustomOpenAIEmbeddings(
            ai_model_id="text-embedding-ada-002",
            api_key=os.getenv("API_KEY")
        )
    )
    kernel.import_plugin_from_object(TextMemoryPlugin(memory), "TextMemoryPlugin")


    ## adding function
    async def populate_memory(memory: SemanticTextMemory) -> None:
        await memory.save_information(collection="generic2", id="info1", text="Your budget for 2024 is $100,000", description="", additional_metadata="")
        await memory.save_information(collection="generic2", id="info2", text="Your savings from 2023 are $50,000", description="", additional_metadata="")
        await memory.save_information(collection="generic2", id="info3", text="Your investments are $80,000", description="", additional_metadata="")

    await populate_memory(memory)


    ## search memory example
    async def search_memory_examples(memory: SemanticTextMemory) -> None:
        questions = ["What is my budget for 2024?", "What are my savings from 2023?", "What are my investments?"]

        for question in questions:
            print(f"Question: {question}")
            result = await memory.search("generic2", question)
            print(f"Answer: {result[0].text}\n")

    # await search_memory_examples(memory)



    # async def setup_chat_with_memory(
    #     kernel: sk.Kernel,
    #     service_id: str,
    # ) -> sk.KernelFunction:
    #     prompt = """
    #     ChatBot can have a conversation with you about any topic.
    #     It can give explicit instructions or say 'I don't know' if
    #     it does not have an answer.

    #     Information about me, from previous conversations:
    #     - {{recall 'budget by year'}} What is my budget for 2024?
    #     - {{recall 'savings from previous year'}} What are my savings from 2023?
    #     - {{recall 'investments'}} What are my investments?

    #     {{$request}}
    #     """.strip()

    #     prompt_template_config = PromptTemplateConfig(
    #         template=prompt,
    #         execution_settings={
    #             service_id: kernel.get_service(service_id).get_prompt_execution_settings_class()(service_id=service_id)
    #         },
    #     )

    #     chat_func = kernel.create_function_from_prompt(
    #         function_name="chat_with_memory",
    #         plugin_name="chat",
    #         prompt_template_config=prompt_template_config,
    #     )

    #     return chat_func


if __name__ == '__main__':
    import asyncio
    result = asyncio.run(main())
    print(result)