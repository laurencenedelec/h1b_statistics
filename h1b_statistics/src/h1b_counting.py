
def convert_states(input) :
    states_dict = {'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
        }
    return [ states_dict.get(item,item) for item in input ]


def get_h1b(input, output_states, output_occupations):
    """For a given year , download the data as an CSV file
    """
    import pandas, csv,re,os.path
    import numpy as np
    pathos=os.getcwd()
    #from openpyxl import load_workbook
    #wb = load_workbook('input/H1.xlsx')
    #data_dec = data.decode('latin-1')
    #xls_data = io.BytesIO(decoded_data)
    #data = wb.worksheets[0]
    #change format test2 change input for real
       
    # an investigation of one of the .csv files shows that
    # the information we want is in the < CASE_NUMBER > <CASE_STATUS>  < WORKSITE_STATE>  <SOC_CODE>
    # <SOC_NAME> (same as SOC_CODE but in string) tags, and   <CASE_STATUS> to test  CERTIFIED
    #read the data, fail for byte ,ok for test
    data=pandas.read_csv(pathos+'/'+input,delimiter=';',dtype=object,error_bad_lines=False)
    #create the column name that contain this information  and change name
    column_name=data.columns[0:]
    indexlist=['.*SOC_CODE*','.*SOC_NAME*','.*WORK.*STATE*','.*STATUS*','.*CASE_NUMBER*']
    column_real=[]
    for i in indexlist:
        regex=re.compile(i)
        name_real = list(filter(regex.match, column_name))[0]
        column_real.append(name_real)
    df=data[column_real]
    df.columns=['SOC_CODE','SOC_NAME','WORKSITE_STATE','CASE_STATUS','CASE_NUMBER']
    #remove the case not certified
    df=df[df.CASE_STATUS == 'CERTIFIED']
    #
    #
    #create occupations and states 'output' with loop
    for type in [('states','WORKSITE_STATE','TOP_STATES'),('occupations','SOC_NAME','TOP_OCCUPATIONS')]:
       #create count and percentage
       stat=df.set_index(['%s' %(type[1]),'CASE_STATUS']).count(level='%s' %(type[1]))
       stat=stat[['CASE_NUMBER']]
       stat['PERCENTAGE']= 100*(stat['CASE_NUMBER']/ stat['CASE_NUMBER'].sum())
       stat.reset_index(level=0, inplace=True)
       #name columns
       stat.columns = [type[2],'NUMBER_CERTIFIED_APPLICATIONS','PERCENTAGE']
       #sort two way
       stat.sort_values(by=[type[2]])
       stat=stat.sort_values(by=['PERCENTAGE'],ascending=False)
       #presentation of percentage as float  1 decimal place
       def approx(x):
          return(round(x,1))
       stat['PERCENTAGE']=stat['PERCENTAGE'].apply(approx)
       #keep only 10 first
       stat=stat[:10]
       #print output
      
       if type[0]=='states':
           stat['TOP_STATES']=convert_states(stat['TOP_STATES'])
           stat.to_csv(pathos+'/'+output_states, sep=';', index=False)
       else:
           stat.to_csv(pathos+'/'+output_occupations , sep=';', index=False)

#add the arguments and run get_h1b
import sys
get_h1b( sys.argv[1],sys.argv[2],sys.argv[3])



