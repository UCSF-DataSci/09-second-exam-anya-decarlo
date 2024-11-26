#!/bin/bash 

# Make output file for cleaned data
touch ms_data.csv


# Clean raw data and save to ms_data.csv
grep -v '^#' ms_data_dirty.csv | \
sed '/^[[:space:]]*$/d' | \
sed -e 's/,\+/,/g' | \
sed -e 's/^,//g' -e 's/,$//g' |\

head -n 1 ms_data_dirty.csv

# Get columns
echo "Identifying columns.."
COLUMNS=$(head -n 1 ms_data_dirty.csv |\
tr ',' '\n' |\
awk '{print NR ":" $0}' |\
grep -E ':(patient_id|visit_date|age|education_level|walking_speed)$' |\
cut -d ':' -f 1 |\
tr '\n' ',' |\
sed 's/,$//')
   
echo "Found columns: $COLUMNS" 

# Debug: Print the columns found 
echo "Selected columns: $COLUMNS" 
if [ -z "$COLUMNS" ]; then 
    echo "Error: Failed to identify required columns"
    exit 1
fi
