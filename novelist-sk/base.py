import semantic_kernel as sk
import os
from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

load_dotenv()
CUR_DIR = os.path.dirname(os.path.abspath(__file__))

async def main():
    kernel = sk.Kernel()
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="default",
            ai_model_id="gpt-3.5-turbo",
            api_key=os.getenv("API_KEY")
        )
    )

    characters = "홍길동"
    news_text = """한국 K-POP(케이팝)이 역대급 호황을 누리고 있지만, 케이팝만 믿고 한국 연예 기획사에 투자하는 것은 위험하다는 외신 보도가 나왔다. 
    소속 연예인의 사생활이 기획사 투자의 위험 요인이라는 이유에서다. 실제로 연예인의 연애 소식에 따라 기획사 주가가 출렁이는 경우가 많다.
    케이팝은 전 세계적인 인기를 끌며 관련 시장도 급성장하고 있다. 엔터 시장 규모가 큰 미국의 빌보드 메인 차드에 한국 아이돌 그룹이 자주 진입하면서 한국 엔터테인먼트 산업은 몸집을 불렸다. 
    블룸버그에 따르면 케이팝 시장은 50억 달러(약 6조7550억원) 규모로 성장했다.

    그러나 블룸버그는 케이팝의 잠재력만 믿고 관련 주식에 투자하는 것은 위험할 수 있다고 평가했다. 
    블룸버그는 “한국 엔터테인먼트 업계는 몇몇 주요 기업에 크게 의존하고 있다”면서 “큰 기업마저도 소속 연예인의 부정적인 소식에 수백만 달러의 가치를 잃곤 한다”라고 설명했다.
    """
    genre="스릴러"

    prompt_plugins = kernel.import_plugin_from_prompt_directory(os.path.join(CUR_DIR, 'plugins'), "Novelist")

    extract_idea = prompt_plugins["ExtractIdea"]

    result = await kernel.invoke(extract_idea, sk.KernelArguments(
        characters=characters,
        news_text=news_text,
        genre=genre
    ))
    return result

if __name__ == '__main__':
    import asyncio
    result = asyncio.run(main())
    print(result)
    