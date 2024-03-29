import semantic_kernel as sk
import os
from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIPromptExecutionSettings
from semantic_kernel.prompt_template.input_variable import InputVariable
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments


load_dotenv()
CUR_DIR = os.path.dirname(os.path.abspath(__file__))

async def main():
    kernel = sk.Kernel()
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="chat",
            ai_model_id="gpt-3.5-turbo",
            api_key=os.getenv("API_KEY")
        )
    )

    prompt = """
        ChatBot can have a conversation with you about any topic.
        It can give explicit instructions or say 'I don't know' if it does not have an answer.

        {{$history}}
        User: {{$user_input}}
        ChatBot: """
    
    prompt_template_config = sk.PromptTemplateConfig(
        template=prompt,
        name="chat",
        template_format="semantic-kernel",
        input_variables=[
            InputVariable(name="input", description="The user input", is_required=True),
            InputVariable(name="history", description="The conversation history", is_required=True),
        ],
        execution_settings=OpenAIPromptExecutionSettings(
            service_id="chat",
            ai_model_id="gpt-3.5-turbo",
            max_tokens=700,
            temperature=0.3,
        )
    )

    chat_function = kernel.create_function_from_prompt(
        function_name="chat_function",
        plugin_name="chat_plugin",
        prompt_template_config=prompt_template_config
    )

    chat_history = ChatHistory()
    chat_history.add_system_message(
            "You are a helpful chatbot who is good about giving book recommendations."
            )
    arguments = KernelArguments(user_input="Hi, I'm looking for book suggestions", history=chat_history)

    response = await kernel.invoke(chat_function, arguments)
    # print(response)
    chat_history.add_assistant_message(str(response))


    async def chat(input_text: str) -> None:
        # Save new message in the context variables
        print(f"User: {input_text}")
        chat_history.add_user_message(input_text)

        # Process the user message and get an answer
        answer = await kernel.invoke(chat_function, KernelArguments(user_input=input_text, history=chat_history))

        # Show the response
        print(f"ChatBot: {answer}")

        chat_history.add_assistant_message(str(answer))

    await chat("I love history and philosophy, I'd like to learn something new about Greece, any suggestion?")
    await chat("that sounds interesting, what is it about?")
    await chat("if I read that book, what exactly will I learn about Greek history?")
    await chat("could you list some more books I could read about this topic?")

    print(chat_history)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
    