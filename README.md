# ELT processing ALL in Azure Workspace
<br><br>
Example of the whole process of ingestion, storage, transformation and visualization.

This is an Azure ELT repository for JSON files published by Vitor Franklin de Lacerda Nimschofsky.
The idea of the project is to assemble an ELT from a raw data ingested initially via api https://www.openbrewerydb.org/documentation, so that in the end it can be visualized for analysis in PowerBI.

**SUMMARY:**
<br><br>
● Through a request made on the List Breweries endpoint - https://api.openbrewerydb.org/v1/breweries, I got all the data from all the countries totaling 8206 records in JSON format.

● I stored the records in Azure Blob Storage in a Land container.

● It took the use of Azure Key Vault to create some secrets and hide token and connections in our notebooks, always aiming for compliance and security.

I consumed these JSON files in Azure Databricks to do the Data Lakehouse structuring and also do the necessary transformations.
I used the Delta storage of databricks to structure the medallion architecture, benefiting from the optimization and speed of DBSF.
Still in Azure Databricks I created a bronze table with the initial dataframe without transformations, in the silver layer I partitioned the initial table by countries,
where I created Delta tables in the silver layer for each country separately.
Finally in the gold layer I create a final delta table, to be consumed in Power BI, where some insights will be shown regarding the quantity of "Stores" by type of "Store" and by location.

**ARCHITECTURE:**
<br><br>
![arquitetura](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/db7b526f-2553-4e4a-9e52-3b8bd1b16a62)
<br><br>
**RESOURCE CREATION:**
<br><br>
                                                       **Resource Group -**
<br><br>
![Captura de tela 2023-06-16 165129](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/6d08076c-c7a2-41c3-8484-5aa26a0820b8)
<br><br>
**Azure Data Factory -**
<br><br>
![criação do adf](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/55fbd588-31f6-4ba0-938a-8fbecddc3517)
<br><br>
**Azure Key Vault -** 
<br><br>
![criação da kv](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/7524f247-fff8-4adc-ad60-62a495dc368e)
<br><br>
**Azure Databricks -**
<br><br>
![criação databricks](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/832bac2d-2c3e-40c6-abb6-b0490d5167ed)
<br><br>
**Azure Storage -**
<br><br>
![storage](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/c9ad3cae-a774-4a87-b4c7-c56a5a3dd46c)
<br><br>
**Cluster Databricks -**
<br><br>
![cluster config](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/c5dc6601-1bad-4983-9c65-f5b8fda11afb)
<br><br>

All the architecture was done in Azure cloud, I followed with the following strategy:
<br><br>
● **Azure Data Factory:** I used to do the ingestion of the data coming from the public API, all the data wake is done with the Azure Data Factory tool.
<br><br>
![pipeline](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/38ab5806-6603-46aa-b31e-421612f01029)

The pipeline JSON is in the source-code folder, in this JSON we can see in detail all the pipeline configuration.

As the endpoint of List Brewery - https://api.openbrewerydb.org/v1/breweries returns paged values, it was necessary to use the Until activity to request all the Breweries data,
as long as there were records (data) in the subsequent pages, the request would continue until the request result was empty. Records from all the countries below were requested in this way:

Austria

England

France

Isle of Man

Ireland

Poland

Portugal

Scotland

SouthKorea

United States

In addition to the request with the copy data activity, which makes the request in the source and copies the data to our blob (container land) in the sink,
we used initial set variables for the first page and temporary set variables to update subsequent pages, finalizing the loop (ingestion and storage),
the pipeline runs the three notebooks, bronze, silver and gold in this sequence.
<br><br>
● **Blob Storage:** Here the storage of all JSON files was done. The land container is the destination of the entire Pipeline data stream.
<br><br>
![land](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/4b168860-ff9e-470b-b294-628280b96044)

I created a variable unix_timestamp, which dynamically generates the current date and time in Unix format, this variable will serve to name the JSON file with a sequence of unique numbers.
We also use the date of the day that the pipeline was executed as a subfolder.

The file path for the copy data from the ADF to the blob is the one below:

![path blob](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/4061eee1-351e-404c-9034-f616776a8888)

<br><br>
●**Azure Key Vault:** When creating the mount point it was necessary to use a storage connection token, this token was stored in our secret blob-key.
<br><br>
● **Azure Databricks:** Three notebooks were, created:
<br><br>
Brewery_Bronze reads the blob files and creates a unique dataframe that is written to a delta table called bronze_brewery.

Brewery_Silver reads the bronze_brewery table in the delta and splits this dataframe into dataframes partitioned by country.

Brewery_Gold reads the bronze_brewery table and creates a table with the relevant gold columns, this table will be consumed in power BI.

The code for the three notebooks is shared in the source code folder. 

All code was done in Python and Pyspark.

Below is a screenshot of the tables created in delta.

![armazenamento delta](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/e173cbf9-af5a-4e21-86c3-64f6661267f4)

<br><br>
● **Visualization of the data through a Dashboard in PowerBI:**
<br><br>
To visualize and take some insights from this data scope, I set up a dashboard that shows the aggregation of the amount of Breweries according to their location and their type,
below is the image of the analysis page.

Filtered for all scenarios:
<br><br>
![power bi dashboard total](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/9210b398-2f54-41b6-b3ca-43e8b8f28d01)
<br><br>

Filtered for South Korea:
<br><br>
![power bi dashboard korea](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/f5542219-94ce-455c-9369-f850a17ed3ab)
<br><br>

Filtered by Brewery Type equal to large:
<br><br>
![power bi dashboard type large](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/79e77807-46e2-4df4-8401-c82c0b66a729)
<br><br>
Project Costs: Below is a picture that shows the costs for this ELT made entirely in Azure.
<br><br>
![custo](https://github.com/vitornimschofsky/Open-Brewery-DB_Azure-ELT/assets/89933194/70063c62-10aa-4ccd-925d-768e3f01006a)
<br><br>
