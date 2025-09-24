// Script Power Query pour Power BI - Connexion BigQuery

let
    Source = GoogleBigQuery.Database(),
    Navigation = Source{[Name="techshop-data-pipeline-2025"]}[Data],
    analytics_marts = Navigation{[Name="analytics_marts"]}[Data],
    fct_sales = analytics_marts{[Name="fct_sales"]}[Data],
    
    // Transformation des types de données
    TransformTypes = Table.TransformColumnTypes(fct_sales,{
        {"order_date", type date},
        {"total_price", type number},
        {"total_margin", type number},
        {"quantity", Int64.Type},
        {"unit_price", type number}
    }),
    
    // Ajout de colonnes calculées
    AddCalculatedColumns = Table.AddColumn(
        TransformTypes, 
        "Year", 
        each Date.Year([order_date]), 
        Int64.Type
    ),
    
    AddMonth = Table.AddColumn(
        AddCalculatedColumns, 
        "Month", 
        each Date.Month([order_date]), 
        Int64.Type
    ),
    
    AddQuarter = Table.AddColumn(
        AddMonth, 
        "Quarter", 
        each Date.QuarterOfYear([order_date]), 
        Int64.Type
    )
in
    AddQuarter
