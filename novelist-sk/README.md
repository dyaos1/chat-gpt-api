# Semantic Kernel with Chroma: FAILED

24/03/28 

> Expected EmbeddingFunction.__call__ to have the following signature: odict_keys(['self', 'input']), got odict_keys(['args', 'kwargs']) 발생

__call__ method 가 있어야 하고 odict_keys(['self', 'input'])를 받아야 한다는 조건인데,
현재 버전의 Semantic Kernel은 위의 조건을 충족시키지 못함

Semantic Kernel이 Chroma지원할때까지는 
프레임워크 없이 Vanila로 하든지 LangChain을 이용해서 하는 수 밖에 없는것 같다.
