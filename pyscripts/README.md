
# Nordic Microalgae - data layer

Source code and static data for the Nordic Microalgae data layer. 

Instructions for a new system. 

Database setup:

- Install MySql and create a database called "nordicmicroalgae".
 
- Copy nordicmicroalgae_settings_TEMPLATE.py to nordicmicroalgae_settings.py

- Edit nordicmicroalgae_settings.py.

Deploy the database by running those scripts:

- prod_01_create_dbtables.py

- prod_10_import_static_content.py

- prod_11_import_taxa.py

- prod_12_import_external_facts.py

- prod_20_generate_search_tables.py

- prod_91_import_from_backup.py (optional)

Set up a cron job running the scripts below each night:

- cron_01_export_to_downloads

- cron_02_export_to_backup

- cron_03_generate_search_tables.py

