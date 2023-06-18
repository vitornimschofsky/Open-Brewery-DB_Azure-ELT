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
![arquitetura](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/017904eb-59b0-4208-9c9b-100043c0764a)
