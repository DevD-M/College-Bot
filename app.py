from groq import Groq
from dotenv import load_dotenv
from retriever import retrieve
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(question):
    chunks = retrieve(question)
    context = "\n\n".join(chunks)
    
    prompt = f"""You are CollegeBot, a helpful assistant for Bennett University students.
Use only the context below to answer the question. If the answer is not in the context, say "I don't have that information."

Context:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    print("CollegeBot ready! Type 'quit' to exit\n")
    while True:
        question = input("You: ")
        if question.lower() == "quit":
            break
        answer = ask(question)
        print(f"\nCollegeBot: {answer}\n")