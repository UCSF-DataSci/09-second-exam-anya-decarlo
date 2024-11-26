#!/bin/bash 

# Make output file for cleaned data
touch ms_data.csv


# Clean raw data and save to ms_data.csv
grep -v '^#' ms_data_dirty.csv | \		# Remove comment lines
sed '/^[[:space:]]*$/d' | \             # Remove empty lines
sed -e 's/,\+/,/g' | \                  # Replace commas
sed -e 's/^,//g' -e 's/,$//g'           # Remove leading/trailing commas 
