# from src.models.retriever import Retriever, FAISSRetriever
# from src.models.generator import TextGenerator

# class QueryHandler:
#     def __init__(self):
#         self.retriever = Retriever(FAISSRetriever())
#         self.generator = TextGenerator()

#     def get_response(self, query):
#         docs = self.retriever.search(query)
#         prompt = f"Context: {docs}. Answer this: {query}"
#         return self.generator.generate(prompt)
