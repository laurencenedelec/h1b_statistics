the python code   hb1_counting.py contain two  function get_h1b and  convert_states. 

description of get_h1b : 
get_h1b (input, output_states, output_occupations)
It create the file top state and top occupation from the file input and write it in the two name file output_states, output_occupations.

example   get_h1b( '/input/h1b_input.csv','output/top_10_states.txt','output/top_10_occupations.txt')

the function convert_states change the abbreviation of state to their full name 
example convert_state(['CA'] ) return California
