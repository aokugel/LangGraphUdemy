from typing import List, TypedDict

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
    
    """

    question: str
    generation: str
    web_search: bool
    documents: List[str]

if __name__=='__main__':
    test_state = GraphState()
    
    test_state['question'] = "what if god was one of us?"
    print(test_state)