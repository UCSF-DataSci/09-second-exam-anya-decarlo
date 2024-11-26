#!/bin/bash 

# Make output file for cleaned data
touch ms_data.csv


# Clean raw data and save to ms_data.csv
grep -v '^#' ms_data_dirty.csv | \
sed '/^[[:space:]]*$/d' | \
sed -e 's/,\+/,/g' | \
sed -e 's/^,//g' -e 's/,$//g' |\
head -n 1 

# Get columns
echo "Identifying columns.."

   
echo "Found columns: $COLUMNS" 
# Get columns
echo "Identifying columns.."
COLUMNS=$(grep -v '^#' ms_data_dirty.csv | \
sed '/^[[:space:]]*$/d' | \
sed -e 's/,\+/,/g' | \
sed -e 's/^,//g' -e 's/,$//g' | \
head -n 1 | \
tr ',' '\n' | \
awk '{print NR ":" $0}' | \
grep -E ':(patient_id|visit_date|age|education_level|walking_speed)$' | \
cut -d ':' -f 1 | \
tr '\n' ',' | \
sed 's/,$//')

# Debug: Print the columns found 
echo "Selected columns: $COLUMNS" 
if [ -z "$COLUMNS" ]; then 
    echo "Error: Failed to identify required columns"
    exit 1
fi
