#!/bin/bash 

# Make output file for cleaned data
touch ms_data.csv

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
   
echo "Found columns: $COLUMNS" 
 
# Debug: Print the columns found 
echo "Selected columns: $COLUMNS" 
if [ -z "$COLUMNS" ]; then 
    echo "Error: Failed to identify required columns"
    exit 1
fi

cut -d ',' -f"$COLUMNS" ms_data_dirty.csv > ms_data.csv

# Create insurance.lst file 
echo -e "insurance_type\nBronze\nSilver\nGold\bPlatinum" > insurance.lst

# Generate summary of processed data 
echo "Total number of visits: $(($(wc -l < ms_data.csv) -1))"
echo "First few records: 
head -n 5 ms_data.csv 