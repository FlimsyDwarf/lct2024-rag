from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyMuPDFLoader
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from typing import List
import os
import requests
from tqdm import tqdm

os.environ['TAVILY_API_KEY'] = "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"
os.environ['OPENAI_API_KEY'] = "YOUR_OPENAI_API_KEY"
tavily_keys = ["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",
               "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",
               "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",
               "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",
               "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",
               "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",
               "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"]


class Pipeline:

    def __init__(self, use_internet: bool, user_sources: str, date_range: str, suffix: str):
        self.workflow = init_graph()
        self.suffix = suffix
        self.user_sources = user_sources.split(
            ',') if user_sources is not None else []
        self.use_internet = use_internet
        self.date_range = date_range.split(
            ',') if date_range is not None else []

    def generate_block(self, query: str) -> dict:
        app = self.workflow.compile()

        list_of_questions = init_question_divide().invoke(
            {"question": query, "date_range": self.date_range_parse()})

        retriever = init_retriever(self.user_sources, self.suffix)
        print(f"""Изначальный запрос: \n{
              query}\n\nВеб-запросы: \n{"\n".join(list_of_questions["questions"])}\n""")

        result = {}
        for q in tqdm(list_of_questions["questions"]):
            print(f'\n\nПоиск ответа на вопрос: {q}')

            documents = retriever.invoke(q)
            inputs = {"question": q, "documents": documents,
                      "generation_count": 3, "use_internet": self.use_internet}
            for output in app.stream(inputs):
                for key, value in output.items():
                    print(f"Finished running: {key}:")
            result[q] = value["generation"]

        return result

    def date_range_parse(self):
        res = ""
        if len(self.date_range) == 1:
            res = f'с {self.date_range[0]}'
        elif len(self.date_range) == 2:
            res = f'с {self.date_range[0]} по {self.date_range[1]}'
        return res


# State
class GraphState(TypedDict):
    """
    Represents the state of our graph.
    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
        generation_count: web search count
    """
    question: str
    generation: str
    web_search: str
    documents: List[str]
    generation_count: int
    use_internet: bool


def init_graph():
    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("web_search_node", web_search_node)  # web search
    workflow.add_node("grade_documents", grade_documents)  # grade documents
    workflow.add_node("generate", generate)  # generatae
    workflow.add_node("transform_query", transform_query)  # generatae

    # Build graph
    workflow.set_entry_point("web_search_node")
    workflow.add_edge("web_search_node", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "transform_query": "transform_query",
            "generate": "generate",
        },
    )
    workflow.add_edge("transform_query", "web_search_node")
    workflow.add_conditional_edges(
        "generate",
        grade_generation_v_documents_and_question,
        {
            "useful": END,
            "not useful": "transform_query",
        },
    )

    return workflow


def web_search_jina(query: str) -> str:
    url = 'https://s.jina.ai/' + query
    response = requests.get(url)
    return response.text


def read_from_source(link: str) -> str:
    url = 'https://r.jina.ai/' + link
    response = requests.get(url)
    return response.text


def get_sources(web_search_res: str) -> list:
    res = []
    shift = 16
    for i in range(1, 6):
        start = web_search_res.find(f'[{i}] URL Source') + shift
        end = start + web_search_res[start:].find('\n')
        res.append(web_search_res[start:end])
    return res


def init_retriever(user_sources, suffix):
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 30

    # hardcoded links
    links = [] + user_sources

    links_content = [Document(read_from_source(link), metadata={
        'source': link}) for link in links]

    # from documents
    txt_loader = DirectoryLoader('./data/' + suffix,
                                 glob="*.txt",
                                 silent_errors=True,
                                 show_progress=True,
                                 loader_cls=TextLoader)

    pdf_loader = DirectoryLoader('./data/' + suffix,
                                 glob="*.pdf",
                                 silent_errors=True,
                                 show_progress=True,
                                 loader_cls=PyMuPDFLoader)

    documents = txt_loader.load() + pdf_loader.load() + links_content

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore = FAISS.from_documents(docs, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={'k': 6})
    return retriever


# Nodes
def retrieve(state):
    """
    Retrieve documents from vectorstore
    """
    print("---RETRIEVE FROM VECTORSTORE---")
    question = state["question"]

    # Retrieval
    documents = init_retriever().invoke(question)
    return {"documents": documents, "question": question}


def generate(state):
    """
    Generate answer using RAG on retrieved documents
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    prompt = PromptTemplate(
        template="""Вы являетесь помощником при выполнении заданий, связанных с ответами на вопросы. 
    Используйте следующие фрагменты найденного контекста, чтобы ответить на вопрос. 
    Контекст имеет тип Document, который имеет контент и метаданные в виде источника данных.
    Если вы не знаете ответа, просто напишите : Информация не найдена. 
    Дайте развёрнутый ответ, как будто это часть отчёта, обоснуй ответ и подкрепите фактами. 
    При этом дайте только ответ, чтобы его сразу можно было вставить в отчёт. А в конце напиши источник информации. 
    Если ответ сформирован на основе нескольких источников, то укажи все.
    Вопрос: {question} 
    Контекст: {context} """,
        input_variables=["question", "document"],
    )

    # LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Chain
    rag_chain = prompt | llm | StrOutputParser()

    # RAG generation
    generation = rag_chain.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation}


def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question
    """
    print("---CHECK ANY DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    prompt = PromptTemplate(
        template="""Ты - грейдер, оценивающий релевантность найденного документа вопросу пользователя. 
        Если документ содержит ключевые слова, связанные с вопросом пользователя, оцени его как релевантный. 
        Это не обязательно должен быть строгий тест. Цель - отсеять ошибочные запросы.
        Дай бинарную оценку 'да' или 'нет', чтобы указать, релевантен ли документ вопросу.
        Предоставь бинарную оценку: 'да' или 'нет'
        Больше ничего писать не надо. \n
        Вот полученный документ: \n\n {document} \n\n
        Вот вопрос пользователя: {question} \n
        """,
        input_variables=["question", "document"],
    )

    retrieval_grader = prompt | llm | StrOutputParser()

    # Score each doc
    filtered_docs = []
    web_search = "Yes"
    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        # Document relevant
        if score.lower() == "да":
            filtered_docs.append(d)
            web_search = "No"

    return {"documents": filtered_docs, "question": question, "web_search": web_search}


def web_search_node(state):
    """
    Web search based on the question
    """

    question = state["question"]
    documents = state["documents"]
    use_internet = state["use_internet"]
    generation_count = state["generation_count"]
    generation_count = generation_count - 1

    # Web search
    if use_internet:
        print("---WEB SEARCH---")
        web_search_tool = TavilySearchResults(k=3)
        docs = web_search_tool.invoke({"query": question})
        i = 0
        while docs == "HTTPError('400 Client Error: Bad Request for url: https://api.tavily.com/search')":
            os.environ['TAVILY_API_KEY'] = tavily_keys[i]
            docs = web_search_tool.invoke({"query": question})
            i += 1
            if len(tavily_keys) == i:
                print("You must update the Tavily API-KEY, all preset have reached their limits. Internet search is no longer possible.")
                break
        for doc in docs:
            if isinstance(doc, dict):
                d = Document(page_content=doc["content"], metadata={
                    'source': doc["url"]})
                documents.append(d)

    return {"documents": documents, "question": question, "generation_count": generation_count}


def transform_query(state):
    """
    Transform the query to produce a better question.
    """

    print("---TRANSFORM QUERY---")
    question = state["question"]
    documents = state["documents"]

    # Re-write question
    # LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Prompt
    re_write_prompt = PromptTemplate(
        template="""Вы переписываете вопросы, преобразуя их в лучшую версию, оптимизированную для веб-поиска и 
        выдаёте в качестве вопроса только новый запрос, который можно скопировать целиком и вставить в поисковик. 
        Посмотрите на исходный вопрос, определи его семантический смысл/значение. 
        Напечатай ТОЛЬКО улучшенный вопрос в виде строки без всяких вводных и пояснений, который сразу можно вставить в поиск. \n
        Вот первоначальный вопрос: {question}.\n 
        Твой улучшенный запрос, оптимизированный для веб-поиска:\n """,
        input_variables=["generation", "question"],
    )

    question_rewriter = re_write_prompt | llm | StrOutputParser()

    better_question = question_rewriter.invoke({"question": question})
    print(f'New query = {better_question}')
    return {"documents": documents, "question": better_question}


# Conditional edge

def decide_to_generate(state):
    """
    Determines whether to generate an answer, or add web search
    """

    print("---ASSESS GRADED DOCUMENTS---")
    web_search = state["web_search"]
    generation_count = state["generation_count"]

    if generation_count <= 0:
        return "generate"

    if web_search == "Yes":
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        print("---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY AND WEB SEARCH AGAIN---")
        return "transform_query"
    else:
        # We have relevant documents, so generate answer
        print("---DECISION: GENERATE---")
        return "generate"


# Conditional edge
def grade_generation_v_documents_and_question(state):
    """
    Determines whether the generation is grounded in the document and answers question.
    """

    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]
    generation_count = state["generation_count"]
    use_internet = state["use_internet"]

    if not use_internet:
        return "useful"

    print("---CHECK HALLUCINATIONS---")
    if generation_count == 0:
        print("---LIMIT EXED: LAST GENERATION WILL BE USED AS ANSWER---")
        return "useful"

    score = init_hallucination_grader().invoke(
        {"documents": documents, "generation": generation}
    )
    score = score.lower()

    # Check hallucination
    if score == "да":
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        # Check question-answering
        print("---GRADE GENERATION vs QUESTION---")
        score = init_answer_grader().invoke(
            {"question": question, "generation": generation})
        score = score.lower()
        if score == "да":
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
    return "not useful"


def init_answer_grader():

    # LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Prompt
    prompt = PromptTemplate(
        template="""Ты оцениваешь, насколько ответ полезен для решения вопроса. 
        Дай бинарную оценку 'да' или 'нет', чтобы указать, является ли ответ полезен для решения вопроса. 
        Предоставьте бинарную оценку: 'да' или 'нет' 
        Больше ничего писать не надо.
        Вот ответ полезность которого надо оценить:
        \n ------- \n
        {generation} 
        \n ------- \n
        Вот вопрос: {question}""",
        input_variables=["generation", "question"],
    )

    answer_grader = prompt | llm | StrOutputParser()
    return answer_grader


def init_hallucination_grader():

    # LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Prompt
    prompt = PromptTemplate(
        template=""" Ты - оценщик, оценивающий, насколько ответ обоснован и подкреплен набором фактом. 
        Дай бинарную оценку 'да' или 'нет', чтобы указать, обоснован ли ответ / подкреплен ли он набором фактов.
        Предоставь бинарную оценку: 'да' или 'нет' 
        Больше ничего писать не надо.
        Вот факты:\n
        {documents} 
        \n ------- \n
        Вот ответ: {generation}""",
        input_variables=["generation", "documents"],
    )

    hallucination_grader = prompt | llm | StrOutputParser()
    return hallucination_grader


def init_question_divide():
    # LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Prompt
    divide_prompt = PromptTemplate(
        template="""Вы профессионал в поиске информации в интернете. Вам на вход подаётся текст. 
        Посмотрите на исходный текст, определите его семантический смысл, 
        и какие веб-запросы требуется написать, чтобы найти информацию по этому тексту в инетрнете.
        Напишите один или несколько веб-запросов, которые помогут найти абсолютно всю информацию, о которой говорится в тексте. 
        Веб-запросы должны быть независимы, то есть их буду выплнять в любом порядке. Если указаны временные рамки, добавь их к каждому веб-запросу если они применимы по смыслу.\n
        Ответ дай в виде JSON в одну строку с одним ключом 'questions' и ничего больше. Без символов переноса строк. \n
        Вот текст: {question}.\n 
        Временные рамки: {date_range}.\n
        Твой JSON:\n """,
        input_variables=["date_range", "question"],
    )

    question_divide = divide_prompt | llm | JsonOutputParser()
    return question_divide
