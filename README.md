# ELT processing ALL in Azure Workspace
Exemplo de todo o processo de ingestão armazenamento, trasformaçao e visualização.

Esse é um repositório de ELT com recursos do Azure para arquivos JSON publicado por Vitor Franklin de Lacerda Nimschofsky.
A ideia do projeto é montar um ELT de um dado bruto ingerido inicialmente via api https://www.openbrewerydb.org/documentation, para que no final seja feita a visualização de análises no PowerBI.

RESUMO:

● Através de uma requisição feita no endpoint List Breweries - https://api.openbrewerydb.org/v1/breweries, obtive todos os dados de todos os países no total de 8206 registros em formato JSON.

● Armazenei os registros no Azure Blob Storage em um conteiner Land.

● Foi necessário o uso do Azure Key Vault para criar alguns secrets e ocultar token e conexões nos nossos notebooks, visando sempre a conformidade e segurança.

● Consumi esses arquivos JSON no Azure Databricks para fazer a estruturação do Data Lakehouse e fazer, também, as transformações necessárias.
Utilizei o armazenamento Delta do databricks para estruturar a arquitetura de medalhão, me beneficiando da otimização e rapidez do DBSF.
Ainda no Azure Databricks criei uma tabela bronze com o dataframe inicial sem transformações, na camada silver particionei a tabela inicial por países, onde criei tabelas Deltas na camada silver para cada país separadamente.
Por fim na camada gold crio uma tabela delta final, para ser consumida no Power BI, onde será mostrado alguns insights referentes a quantidade de "Lojas" por tipo de "Loja" e por localização.

ARQUITETURA:

![arquitetura](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/db7b526f-2553-4e4a-9e52-3b8bd1b16a62)


Toda a arquitetura foi feita na nuvem do Azure, segui com a seguinte estratégia:

● Azure Data Factory: Utilizei para fazer a ingestão dos dados vindos da API pública, toda a esteira de dados é feita com a ferramenta do Azure Data Factory.

![pipeline](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/8d852f34-91a7-4b7f-8287-f81e6d396f46)

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

● Blob Storage: Aqui foi feito o armazenamento de todos os arquivos JSON. O conteiner land é o destino de todo o fluxo de dados da Pipeline.
![land](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/6aa2023f-b246-427c-84dc-b08a8f1ae521)

Criei uma variavel unix_timestamp, que gera dinâmicamente a current date data e hora em formato Unix, essa variavel vai servir para nomear o arquivo JSON com uma seguencia de numeros únicos.
Utilizamos também como subpasta a data do dia que a pipeline foi executada.

O file path do copy data do ADF para o blob foi esse abaixo:

![path blob](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/2c7fe9c8-10f2-43ed-a0c7-132bc800dd21)

● Azure Key Vault: Na criação do mount point foi necessário utilizar um token de conexão do storage, esse token foi armazenado na nossa secret blob-key.

● Azure Databricks: Foram, criados três notebooks:

Brewery_Bronze lê os arquivos do blob e cria um dataframe único que é gravado em uma tabela delta chamada bronze_brewery.

Brewery_Silver lê a tabela bronze_brewery que esta no delta e divide esse dataframe em dataframes particionados por país.

Brewery_Gold lê a tabela bronze_brewery e cria uma tabela com as colunas relevantes gold, essa tabela será consumida no power BI.

O código dos três notebooks estão compartilhados na pasta source code. 

Todos os códigos foram feitos em Python e Pyspark.

Abaixo imagem das tabelas criadas no delta.
![armazenamento delta](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/2277cf7c-c4f2-430e-8522-266f275d6452)


● Visualização dos dados através de um Dashboard no PowerBI:

Para visualizar e tirar alguns insights desse escopo de dados, montei um dashboard que mostra a agregação da quantidade de Breweries de acordo com a sua localização e do seu tipo, segue abaixo a imagem da pagina de análise.

Filtrado para todos os cenários:

![power bi dashboard total](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/8dcb56b8-7667-4175-a631-622930a0884f)

Filtrado para o país South Korea:

![power bi dashboard korea](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/6977f5aa-359a-45a9-87ac-0c7368de312a)

Filtrado por Brewery Type igual a large:

![power bi dashboard type large](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/3aaca854-eb1e-40db-88bd-6a3f46f4c47f)

Custos do projeto: Abaixo imagem que mostra os custos desse ELT feito no totalmente no Azure.

![custo](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/3acc17bb-f225-448d-9749-1e885bee4b94)


