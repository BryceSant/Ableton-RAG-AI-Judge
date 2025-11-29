from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama #To avoid using my tokens
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from os import getenv
load_dotenv()


MODEL = "openai/gpt-5" #model that will be used
#MODEL = "qwen2.5:14b-instruct" #model that will be used FOR TESTING PURPOSES
TEMPERATURE = 0.0 #model's temperature
PROMPT = """ 
You are an evaluation model.
Your task is to strictly score an answer to an Ableton Live 12 question.
You must be harsh, conservative, and literal when assigning scores.

General Rules:

If the answer mentions other DAWs, plugins, or software (e.g., FL Studio, Audacity, GarageBand, Logic), deduct heavily from:
- Relevance
- Specificity to Ableton
- Clarity

If the answer does not mention Ableton terminology, menus, or features, the score for Specificity to Ableton must be 1.0–2.0 maximum.

If the answer is generic, vague, or applies to any DAW, its Relevance and Depth scores must drop significantly.

When in doubt, choose the lower score.

Scoring Rules:

Score each criterion from 1.0 to 5.0, using 0.5 increments only.

You must grade conservatively (do NOT give mid or high scores unless the answer clearly deserves them).

CRITERIA:
Relevance — Must be strictly about Ableton and the question asked.
Depth — Must show real reasoning or alternative approaches.
Specificity to Ableton — Must include actual Ableton terminology, menus, devices, actions, shortcuts, or paths.
Clarity — Must be structured, readable, and instructional.
Hallucinations — Check for any incorrect Ableton claims. If unsure, lower the score.

REQUIRED OUTPUT

Provide:

Five numeric scores (1.0–5.0, .5 increments)

A total_score equal to their sum

A brief explanation (≤ 200 words)

Additional Rules:

If an answer does not reference Ableton at all → Specificity to Ableton = 1.0

If an answer mentions other DAWs → cap Relevance ≤ 3.0

If an answer includes software NOT requested → subtract at least 1–2 points from Relevance & Clarity

If an answer describes generic audio concepts without Ableton context → Depth ≤ 2.5

Instructions:

You will be given:
- The original question
- The model’s answer

Evaluate the answer strictly according to the rules above.
Be harsh.
Do not rewrite or fix the answer.
Do not include chain-of-thought.
""" 

QUESTION = "How do I make my entire song slow down or speed up?"

model = ChatOpenAI(    
    api_key=getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model = MODEL,
    temperature = TEMPERATURE,
)

#Model that will be used FOR TESTING PURPOSES
# model = ChatOllama(    
#     model = MODEL,
#     temperature = TEMPERATURE,
# )

while True:
    print("\n")
    ai_response = input("Please write the AI's response, or q to quit: \n")
    print("\n")
    
    if ai_response.lower() == 'q':
        print("Exiting the loop.")
        break

    else:
        prompt = ChatPromptTemplate.from_template(f"""
            {PROMPT}
            Question: {QUESTION}
            Answer: {{answer}}
            """
        )

        chain = prompt | model

        response = chain.invoke({
            "answer": ai_response
        })

        print("Judge's verdict: \n")

        print(response.content)












