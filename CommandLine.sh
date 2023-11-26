#!/bin/bash

# Print header for Question 1
printf "# Question-1: \n"

# Read the 'merged_courses.tsv' file to count the number of occurrences for each country
# AWK is used for processing the tab-separated values (TSV format)
country_count=$(awk -F'\t' 'NR > 1 { 
    countries[$11]++ 
} 
END { 
    for (country in countries) 
        print "{\"country\": \"" country "\", \"counts\": " countries[country] "}" 
}' merged_courses.tsv)

# Sort the counts for each country in descending order using jq, a command-line JSON processor
sorted_country_count=$(echo "$country_count" | jq -s 'sort_by(-.counts)')

# Display the top 5 countries
echo "$sorted_country_count" | jq '.[:5]'

# Extract the country with the highest count
most_frequent_country=$(echo "$sorted_country_count" | jq -r '.[0].country')

# Print the most frequent country
echo "Most frequent country: $most_frequent_country"

# Process 'merged_courses.tsv' to create a list of cities within the most frequent country
# AWK is used again to filter and count occurrences per city
city_list=$(awk -F'\t' -v country="$most_frequent_country" 'NR > 1 && $11 == country {
    cities[$10]++
}
END {
    for (city in cities) 
        printf "{\"country\": \"%s\", \"city\": \"%s\", \"city_occurrence\": %d}\n", country, city, cities[city]
}' merged_courses.tsv | jq -s '.')

# Sort the list of cities based on the number of occurrences, in descending order
sorted_city_list=$(echo "$city_list" | jq 'sort_by(-.city_occurrence)')

# Display the top 5 cities
echo "$sorted_city_list" | jq '.[:5]'

# Extract the maximum occurrence value among cities
max_occurrence=$(echo "$sorted_city_list" | jq '[.[] | .city_occurrence] | max')

# Find and list the cities with the maximum occurrence
max_cities=$(echo "$sorted_city_list" | jq --arg max_occurrence "$max_occurrence" '[.[] | select(.city_occurrence == ($max_occurrence | tonumber)) | .city]')

# Print the cities with the most Master's Degrees
printf "\nCities with the highest occurrence of Master's Degrees: "
echo "$max_cities"



#!/bin/bash

# Question-2: Count Part-Time Courses
printf "# Question-2: \n"

# Declare an array to hold details of part-time courses
declare -a part_time_courses

# Read through each line of 'merged_courses.tsv'
# Using a while loop to process the file line by line
while IFS=$'\t' read -r course_id course_name course_field study_mode course_location; do
    # Check if the study mode indicates 'Part time'
    # 'study_mode' corresponds to the column where full/part-time status is mentioned
    if [ "$study_mode" = "Part time" ]; then
        # Add the entire line (course details) to the array if it's a part-time course
        part_time_courses+=("$course_id|$course_name|$course_field|$study_mode|$course_location")
    fi
done < merged_courses.tsv

# Calculate the total number of part-time courses
# Counting the number of elements in the part_time_courses array
part_time_count=${#part_time_courses[@]}

# Display the count of part-time courses
echo "Total count of educational institutions providing Part-Time programs: $part_time_count"




#!/bin/bash

# Question-3: Engineering Course Analysis
printf "# Question-3: \n"

# Initialize a counter for courses related to 'Engineering'
engineering_course_count=0

# Process each line in 'merged_courses.tsv'
# Using a while loop to read the file line by line
while IFS=$'\t' read -r course_name course_type course_field course_mode course_location; do
    # Search for 'Engineer' in the course name
    # 'course_name' corresponds to the column containing the name of the course
    if [[ "$course_name" == *"Engineer"* ]]; then
        # Increment the counter for each occurrence
        ((engineering_course_count++))
    fi
done < merged_courses.tsv

# Output the total number of engineering-related courses
echo "Total Engineering courses found: $engineering_course_count"

# Calculate the percentage of engineering courses
# Dividing the count of engineering courses by the total number of courses
# Assuming 6000 as the total number of courses
total_courses=6000
percentage_of_engineering=$(echo "scale=2; $engineering_course_count / $total_courses * 100" | bc)

# Display the percentage of engineering courses
echo "Percentage of courses related to Engineering: $percentage_of_engineering%"

