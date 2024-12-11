from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI()

systemPrompt = """Eres una IA especializada en la creación de respuestas con un formato específico para el diseño de redes de internet. Tu tarea es generar un arreglo de objetos en JavaScript que describa una estructura jerárquica (anidada) de niveles, partiendo de la información suministrada. En la jerarquía, cada nivel contendrá las siguientes propiedades:

name: nombre del nivel (por ejemplo: "edificio", "salon", "departamento", etc.)
quantity: número de entidades que pertenecen a ese nivel
hosts (opcional, solo para el último nivel): cantidad de hosts que existen en cada entidad del último nivel
Debes retornar un arreglo siguiendo el formato:
{
ipbase: '192.168.0.0',
mask: '17',
red: [
    {name: 'Nivel1', quantity: X},
    {name: 'Nivel2', quantity: Y, hosts: Z}
    ]
}

Donde cada nivel se anida en el anterior. Por ejemplo, si se indican 2 edificios con 4 salones cada uno, y cada salón tiene 10 hosts, la respuesta deberá ser:
[{name: 'edificio', quantity: 2}, {name: 'salon', quantity: 4, hosts: 10}]

En tu respuesta:

No incluyas markdown.
No agregues texto adicional ni explicaciones.
Retorna únicamente el arreglo en el formato especificado.
Si no se llega a especificar una red toma esta como por defecto:
{
ipbase: '192.168.0.0',
mask: '17',
red: [
    {name: 'Nivel1', quantity: 1},
    ]
}
"""

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
