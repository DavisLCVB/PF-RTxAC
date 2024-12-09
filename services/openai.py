from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI()

systemPrompt = "Eres una IA que proporcionará un formato específico para el diseño de una red de internet, no deberas responder a un usuario solo deberas responder el formato que se te especifique. Tu objetivo será que, a partir de la información que se te mande, logres identificar una estructura de anidamiento, luego, la cantidad de estas estructuras. Por ejemplo: 2 edificios y 4 salones, significa que hay 2 edificios con 4 salones cada uno, es decir, que 2 'objetos' del mismo orden de anidamiento comparten la misma información de los niveles siguientes en el anidamiento. Deberas responder siguiendo un arreglo de javascript con la siguiente estructura: [Level, Level, Level], donde Level es un objeto del tipo interface Level {name: string, quantity: number, hosts?:number}, name es el nombre del nivel (area, edificio, salon, etc), quantity es la cantidad de niveles de ese tipo y hosts es la cantidad de hosts que tiene el ultimo nivel (salon en el ejemplo). asi, un ejemplo de respuesta sería: [{name: 'edificio', quantity: 2}, {name: 'salon', quantity: 4, hosts: 10}] que significa que hay 2 edificios con 4 salones cada uno y cada salon tiene 10 hosts. (solo el ultimo nivel puede tener hosts). El formato dalo quitando el markdown, texto plano"

model = os.getenv("MODEL")


def generateResponse(prompt: str) -> str:
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content
