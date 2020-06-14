**Ultra Tesla** utiliza *plugins* para aumentar las funcionalidades del mismo y mejorar la eficiencia de la administración de las redes. Además de su uso propio, los plugins también son muy fácil de crear.

**Plugin Básico**:
```python
information = {
    'description' : 'Mostrar un texto por la salida',
    'commands'    : [
        {
            'positionals' : [
                {
                    'args'    : ('text',),
                    'help'    : 'El texto a mostrar',
                    'default' : 'Hello World!'

                }

            ]

        }

    ],
    'version'     : '1.0.0'

}

def MainParser(args):
	print('Texto:', args.text)
```

Ya guardado en **modules/Cmd/hello.py** simplemente se podría usar en **UTeslaCLI**:

```bash
./UTeslaCLI hello "Hola Mundo"
```

Obteniendo una salida como la siguiente:

```
Hola Mundo
```

## Sintaxis

La sintaxis para crear un *plugin* en el proyecto **Ultra Tesla** es realmente sencilla. Solo se requieren dos factores: Un diccionario que indique la información que se requiere y una función que se le pasarán los parámetros y argumentos proporcionados por el mismo usuario.

Sintaxis del diccionario:

```python
information = {
    'description' : '<Descripción de lo que hará el plugin>',
    'commands'    : [
        {
            '<Nombre del grupo>' : [
                {
                    'args'    : ('<El nombre del parámetro>',)

                }

            ]

        }

    ],
    'version'     : '<Versión de plugin>'

}
```

El poder oculto de todo esto está en **argparse**, ya que básicamente se está configurando de una manera más intuitiva.

* **information**: Es el diccionario que contiene toda la información y es necesario
* **description**: Es una cadena describiendo el plugin (**opcional**)
* **commands**: Es una lista que contiene los grupos que básicamente son diccionarios
* **\<Nombre del grupo\>**: Es una lista que contiene diccionarios, pero lo interesante es que a excepción de '**args**' que es parte de **UTeslaCLI** son los mismos parámetros que se les pasa a **argparse** (**por lo que es recomendable leer antes la documentación o un tutorial**)
* **version**: La versión del *plugin* que es una cadena

```python
def MainParser(args):
	pass
```

Sobre la función. Es necesario el nombre '**MainParser**' y que reciba un argumento (éste puede ser llamado como se desee). El resto es el mismo programador el que decide qué hacer con los parámetros y argumentos proporcinados por el mismo usuario.

## Plugins interesantes

Hay *plugins* que los considero útiles para cualquier administrador del servidor:

* **add**: Permite crear nuevos usuarios
* **del**: Permite borrar los usuarios creados
* **show**: Mostrar los usuarios registrados
* **generate_token**: Obtener un token de un servidor para poder comunicarse con éste
* **generate_keys**: Generar el par de claves RSA
* **add_network**: Agregar los servicios de una red
* **gen_onodo**: Muy útil para crear un gráfico de la red. Este *plugin* genera un .xlsx que debe ser usado en https://onodo.org

Cada plugin tiene su propia ayuda:

```bash
./UTeslaCLI <plugin> --help
```

~ DtxdF
