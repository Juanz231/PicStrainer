#importar librerías
import os
import openai
from dotenv import load_dotenv, find_dotenv

#Se lee del archivo .env la api key de openai
_ = load_dotenv('openAI.env')
openai.api_key  = os.environ['openAI_api_key']

#Se genera una función auxiliar que ayudará a la comunicación con la api de openai
#Esta función recibe el prompt y el modelo a utilizar (por defecto gpt-3.5-turbo)
#devuelve la consulta hecha a la api

def get_completion(frase, model="gpt-3.5-turbo"):
    instruction = "Dado el siguiente prompt, tu tarea es analizar la frase y devolver los valores válidos  \
    para las siguientes variables: edadMin, edadMax, raza, emocion y genero. En caso de que no se especifique el valor, se debe retornar null. Los valores deben estar separados por comas. \
    Posibles razas: (asian, white, middle eastern, indian, latino y black) unicamente usa estas para el retorno, sin embargo la frase puede tener indicacione sdiferentes, por ejemplo colombiano (retorna latino) o europeo(white)\
    Posibles emociones: (angry, fear, neutral, sad, disgust, happy y surprise) unicamente usa estas en el retorno \
    Posibles generos: (Woman, Man) unicamente usar estos \
    Si la frase menciona específicamente una edad, la edadMin debería ser la edad especificada - 5 y la edadMax debería ser la edad especificada + 5 para tener un margen de error.  \
    Si la frase contiene una etapa de la vida ejemplo: niño, adulto,joven,etc. La edad min y max será el rango de esta etapa, por ejemplo niño seria de 3 a 12 años o lo que veas mas correcto, en caso de no estar en esta lista infierela \
    Ejemplos:  \
    Joven colombiano riendo: 15,25,latino,happy,null  \
    Mujer depresiva adulta: 20,35,null,sad,Woman  \
    Solo debes retornar un renglon con los siguerntes parametros edadMin/edadMax/raza/emocion/genero \
    Si alguno de los parametros tiene mas de un dato irá separado por comas, recuerda que unicamente es valido este formato: edadmin,edadmax,raza,emocion,genero. No retornes nada mas ya que generaria un error"

    #Definimos el prompt
    prompt = f"{instruction} la frase es: {frase}"

    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]