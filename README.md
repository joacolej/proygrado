# Proyecto de grado 2018 :notebook: :uk:

## Instalación
1. **Clonar repositorio**: `git clone https://github.com/joacolej/proygrado.git`
2. **Descargar e instalar [Python 2.7](https://www.python.org/downloads/)**
3. **Instalar dependencias:** `pip install -r requirements.txt`
4. **Instalar [kenlm](https://github.com/kpu/kenlm):**

  ```bash
    pip install https://github.com/kpu/kenlm/archive/master.zip
  ```
5. **Agregar variables de entorno**

Crear .env file y ubicarlo en la carpeta raiz.
```
LANGUAGE_MODEL_PATH=/path/to/language_model
EMBEDDINGS_MODEL_PATH=/path/to/embeddings_model
```

6. **Instalar [MongoDB Community Edition](https://docs.mongodb.com/manual/administration/install-community/)**

## MongoDB
**Iniciar MongoDB**
```bash
mongod
```

**Importar base de datos**

```bash
mongoimport --db diccionario_db --collection definiciones --file recursos/definiciones_backup.json
```


**Exportar base de datos**

```bash
mongoexport --db diccionario_db --collection definiciones --out recursos/definiciones_backup.json
```

## Modelo de lenguaje
Para generar el modelo de lenguaje ir a https://github.com/bernabe9/modelo-lenguaje

## Modelo de words embeddings

```python
import gensim

file = open('../path_del_corpus.txt.bz2', 'r+')
lines = file.readlines()
lines = [gensim.utils.simple_preprocess(line) for line in lines]
model = gensim.models.Word2Vec(lines, size=100, window=5, min_count=1, workers=4)
model.save('./model-word-embeddings')

```

## POS tagger
Por defecto se utiliza el pos tagger de NLTK. Este POS tagger no es muy preciso, por eso se puede cambiar por el POS tagger de Stanford. Tenga en cuenta que el POS tagger de Stanford es más lento y va a impactar en la performance.

Siga estos pasos para activarlo:
1. Descargar el POS tagger de stanford: https://nlp.stanford.edu/software/stanford-postagger-2018-10-16.zip
2. Descomprimirlo
3. Agregar la variable en `src/.env` con la path hacia la carpeta: `STANFORD_POS_TAGGER=/Users/bernabegonzalez/Projects/stanford-postagger-2018-10-16`
4. Agregar una variable en `src/.env` para indicar que se quiere usar Stanford y no NLTK como POS tagger: `POS_TAGGER=STANFORD`

## Servidor Web
**Ejecutar servidor**

```bash
gunicorn wgsi:app
```

**Reiniciar servidor**

```bash
./restart_server.sh
```
