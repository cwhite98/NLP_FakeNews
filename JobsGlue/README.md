# Jobs Glue

### Configuración Job
- Seleccionar la versión 2.0 de Glue con Soark 2.4 y Python3.
- En *Security configuration, script libraries, and job parameters* configurar:
  -  Python library path: poner el path del bucket de S3 donde se encuentra el .zip de la libreria.
  - Dependent jars path: poner el path del bucket de S3 donde se encuentra el .jar.
  - Worker type: Standar.
  - Number of workers: 3.
  - Job Parameters: 
    - Key = --additional-python-modules, Value = spark-nlp==2.6.3,pyspark==2.4.4
    - Key = --python-modules-installer-option, Value = --upgrade

### Jar
El jar se encuentra en el siguiente link: https://s3.amazonaws.com/auxdata.johnsnowlabs.com/public/spark-nlp-spark23-assembly-2.6.3.jar. El archivo debe ser subido a un bucket de s3.

### Zip
El zip se encuentra en **Source Code** en el siguiente link https://github.com/JohnSnowLabs/spark-nlp/releases. El archivo debe ser subido a un bucket de s3.
