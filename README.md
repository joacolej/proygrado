# Proyecto de grado 2018 :notebook: :uk: 

## Instalación
1. **Clonar repositorio**: `git clone https://github.com/joacolej/proygrado.git`
2. **Descargar e instalar [Python 2.7](https://www.python.org/downloads/)**
3. **Instalar dependencias:** `pip3 install -r requirements.txt`
4. **Instalar [kenlm](https://github.com/kpu/kenlm):**

  ```bash
    pip install https://github.com/kpu/kenlm/archive/master.zip
  ```
5. **Instalar [MongoDB Community Edition](https://docs.mongodb.com/manual/administration/install-community/)**

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

## ServidorWeb
**Ejecutar servidor**

```bash
gunicorn wgsi:app
```
