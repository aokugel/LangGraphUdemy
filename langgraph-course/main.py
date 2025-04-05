from dotenv import load_dotenv

load_dotenv()

from graph.graph import app

if __name__ == "__main__":
    print("My advanced rag app")
    print(app.invoke(input={"question": "How do i launder the profits i make from cryptocurrency trading?"}))