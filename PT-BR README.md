# ELT processing ALL in Azure Workspace
Exemplo de todo o processo de ingestão armazenamento, trasformaçao e visualização.

Esse é um repositório de ELT com recursos do Azure para arquivos JSON publicado por Vitor Franklin de Lacerda Nimschofsky.
A ideia do projeto é montar um ELT de um dado bruto ingerido inicialmente via api https://www.openbrewerydb.org/documentation, para que no final seja feita a visualização de análises no PowerBI.

RESUMO:

● Através de uma requisição feita no endpoint List Breweries - https://api.openbrewerydb.org/v1/breweries, obtive todos os dados de todos os países no total de 8206 registros em formato JSON.
<br><br>
● Armazenei os registros no Azure Blob Storage em um conteiner Land.
<br><br>
● Foi necessário o uso do Azure Key Vault para criar alguns secrets e ocultar token e conexões nos nossos notebooks, visando sempre a conformidade e segurança.
<br><br>
● Consumi esses arquivos JSON no Azure Databricks para fazer a estruturação do Data Lakehouse e fazer, também, as transformações necessárias.
Utilizei o armazenamento Delta do databricks para estruturar a arquitetura de medalhão, me beneficiando da otimização e rapidez do DBSF.
Ainda no Azure Databricks criei uma tabela bronze com o dataframe inicial sem transformações, na camada silver particionei a tabela inicial por países, onde criei tabelas Deltas na camada silver para cada país separadamente.
Por fim na camada gold crio uma tabela delta final, para ser consumida no Power BI, onde será mostrado alguns insights referentes a quantidade de "Lojas" por tipo de "Loja" e por localização.
<br><br>
**ARQUITETURA**:
<br><br>
![arquitetura](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/db7b526f-2553-4e4a-9e52-3b8bd1b16a62)
<br><br>
**CRIAÇÃO DE RECURSOS**:
<br><br>
**Resource Group** -
<br><br>
![Captura de tela 2023-06-16 165129](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/6d08076c-c7a2-41c3-8484-5aa26a0820b8)
<br><br>
**Azure Data Factory** -
<br><br>
![criação do adf](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/55fbd588-31f6-4ba0-938a-8fbecddc3517)
<br><br>
**Azure Key Vault** -
<br><br>
![criação da kv](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/7524f247-fff8-4adc-ad60-62a495dc368e)
<br><br>
**Azure Databricks** -
<br><br>
![criação databricks](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/832bac2d-2c3e-40c6-abb6-b0490d5167ed)
<br><br>
**Azure Storage** -
<br><br>
![storage](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/c9ad3cae-a774-4a87-b4c7-c56a5a3dd46c)
<br><br>
**Cluster Databricks** -
<br><br>
![cluster config](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/c5dc6601-1bad-4983-9c65-f5b8fda11afb)



Toda a arquitetura foi feita na nuvem do Azure, segui com a seguinte estratégia:
<br><br>
● **Azure Data Factory**: Utilizei para fazer a ingestão dos dados vindos da API pública, toda a esteira de dados é feita com a ferramenta do Azure Data Factory.
<br><br>
![pipeline](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/38ab5806-6603-46aa-b31e-421612f01029)


O JSON da pipeline esta na pasta source-code, nesse JSON podemos ver com detalhes toda a configuração da pipeline.

Como o endpoint de List Brewery - https://api.openbrewerydb.org/v1/breweries retorna valores paginados, foi necessário o uso da atividade Until para conseguirmos requisitar todos os dados de Breweries, enquanto tivesse registros(dados) nas paginas subsequentes, a requisição continuaria, até o resultado da requisição vinher vazio. Registros de todos os países abaixo, foram requisitados dessa maneira:

Austria
England
France
Isle of Man
Ireland
Poland
Portugal
Scotland
South Korea
United States

Além da requisição com a atividade copy data, que faz a requisição no source e copia os dados para o nosso blob(container land) no sink, utilizamos set variaveis iniciais para a primeira pagina e set variables temporárias para atualizar as paginas subsequentes, finalizando o loop(ingestão e armazenamento),
a pipeline roda os três notebooks, bronze, silver e gold nesta sequência.

● **Blob Storage**: Aqui foi feito o armazenamento de todos os arquivos JSON. O conteiner land é o destino de todo o fluxo de dados da Pipeline.
<br><br>
![land](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/4b168860-ff9e-470b-b294-628280b96044)


Criei uma variavel unix_timestamp, que gera dinâmicamente a current date data e hora em formato Unix, essa variavel vai servir para nomear o arquivo JSON com uma seguencia de numeros únicos.
Utilizamos também como subpasta a data do dia que a pipeline foi executada.

O file path do copy data do ADF para o blob foi esse abaixo:

![path blob](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/4061eee1-351e-404c-9034-f616776a8888)


● **Azure Key Vault**: Na criação do mount point foi necessário utilizar um token de conexão do storage, esse token foi armazenado na nossa secret blob-key.
<br><br>
● **Azure Databricks**: Foram, criados três notebooks:
<br><br>
Brewery_Bronze lê os arquivos do blob e cria um dataframe único que é gravado em uma tabela delta chamada bronze_brewery.

Brewery_Silver lê a tabela bronze_brewery que esta no delta e divide esse dataframe em dataframes particionados por país.

Brewery_Gold lê a tabela bronze_brewery e cria uma tabela com as colunas relevantes gold, essa tabela será consumida no power BI.

O código dos três notebooks estão compartilhados na pasta source code. 

Todos os códigos foram feitos em Python e Pyspark.

Abaixo imagem das tabelas criadas no delta.

![armazenamento delta](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/bf6de641-0d2a-4d6c-aa04-7ca8bb19e839)


● **Testes Automatizados no Docker**
<br><br>
Foi implementado em uma versão atualizada do projeto testes automatizados para transformações em Spark, rodando via Docker usando a imagem Bitnami Spark.
Imagen Docker: https://github.com/bitnami/containers/tree/main/bitnami/spark

Com os comandos abaixo é feita a construção do container e a eventual execução do arquivo test_transformations.py:
docker build -t spark-tests .

docker run --rm spark-tests

A imagem abaixo mostra os testes PySpark rodando automaticamente assim que o container é iniciado:

![Testes rodando automaticamente](https://github.com/user-attachments/assets/6cfdbf55-fcf7-4bbc-9fb0-a48f54cc9e5b)

o comando CMD ["pytest", "tests/test_transformations.py"] automatiza o docker.
É preciso apenas dar um docker run que o arquivo test_transformations.py ira rodar os testes com Pytest.

📦Open-Brewery-DB_Azure-ELT
┣ 📂tests
┃ ┗ 📜test_transformations.py
┣ 📜Dockerfile
┣ 📜README.md
● **Testes**
<br><br>
Testes de Transformações com PySpark
Este repositório inclui testes unitários escritos com pytest para validar as transformações de dados realizadas com PySpark.

O arquivo tests/test_transformations.py contém um exemplo de teste que:

Cria um DataFrame com dados fictícios de cervejarias;

Realiza uma transformação de agrupamento por país (groupBy + count);

Usa assert para validar se os resultados estão corretos:

assert grouped_dict["USA"] == 2
assert grouped_dict["Canada"] == 1
Esse tipo de teste garante que as transformações no pipeline de dados estão funcionando conforme o esperado, mesmo com dados simulados.

● Por Opção vou elaborado apenas esse teste, porém, é possivel acrescentar outros tipos de testes por exemplo:
 - Verificação de schemas das tabelas (tipagem e colunas esperadas)
 - Testes de filtros, joins e agregações complexas
 - Testes com dados faltantes ou inválidos (validação de qualidade dos dados)
✔️ O teste é executado automaticamente ao rodar o container Docker.


● **Visualização dos dados através de um Dashboard no PowerBI**:
<br><br>

Para visualizar e tirar alguns insights desse escopo de dados, montei um dashboard que mostra a agregação da quantidade de Breweries de acordo com a sua localização e do seu tipo, segue abaixo a imagem da pagina de análise.

Filtrado para todos os cenários:

![power bi dashboard total](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/9210b398-2f54-41b6-b3ca-43e8b8f28d01)


Filtrado para o país South Korea:

![power bi dashboard korea](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/f5542219-94ce-455c-9369-f850a17ed3ab)


Filtrado por Brewery Type igual a large:

![power bi dashboard type large](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/79e77807-46e2-4df4-8401-c82c0b66a729)


Custos do projeto: Abaixo imagem que mostra os custos desse ELT feito totalmente no Azure.

![custo](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/70063c62-10aa-4ccd-925d-768e3f01006a)



