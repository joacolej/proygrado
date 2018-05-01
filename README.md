# Proyecto de grado 2018

## Instalación
1. **Clonar repositorio**: `git clone https://github.com/joacolej/proygrado.git`
2. **Descargar e instalar [Python 3.6.5](https://www.python.org/downloads/)**
3. **Instalar dependencias:** `pip3 install -r requirements.txt`
4. **Instalar [pattern](https://github.com/clips/pattern):**

  ```
    git clone -b development https://github.com/clips/pattern
    cd pattern
    sudo python3 setup.py install
  ```
5. **Instalar [mongoDB Community Edition](https://docs.mongodb.com/manual/administration/install-community/)**

## MongoDB
**Importar base de datos**

```
mongoimport --db diccionario_db --collection definiciones --file definiciones.json
```


**Exportar base de datos**

```
mongoexport --db diccionario_db --collection definiciones --out definiciones.json
```
