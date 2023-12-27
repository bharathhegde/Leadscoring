##############################################################################
# Import the necessary modules
# #############################################################################

from utils import *

###############################################################################
# Write test cases for load_data_into_db() function
# ##############################################################################

def test_load_data_into_db():
    """_summary_
    This function checks if the load_data_into_db function is working properly by
    comparing its output with test cases provided in the db in a table named
    'loaded_data_test_case'

    INPUTS
        DB_FILE_NAME : Name of the database file 'utils_output.db'
        DB_PATH : path where the db file should be present
        UNIT_TEST_DB_FILE_NAME: Name of the test database file 'unit_test_cases.db'

    SAMPLE USAGE
        output=test_get_data()

    """
    build_dbs()
    load_data_into_db()
    conn = sqlite3.connect(DB_PATH + DB_FILE_NAME)
    df = pd.read_sql('select * from loaded_data', conn)          
    conn.close()
    conn = sqlite3.connect(DB_PATH + UNIT_TEST_DB_FILE_NAME)
    print(DB_PATH + DB_FILE_NAME)
    print (DB_PATH + UNIT_TEST_DB_FILE_NAME)
    reference_df = pd.read_sql('select * from loaded_data_test_case', conn)          
    conn.close()
    assert df.equals(reference_df), "loaded_data doesn't match expected output loaded_data_test_case"
    
    

###############################################################################
# Write test cases for map_city_tier() function
# ##############################################################################
def test_map_city_tier():
    """_summary_
    This function checks if map_city_tier function is working properly by
    comparing its output with test cases provided in the db in a table named
    'city_tier_mapped_test_case'

    INPUTS
        DB_FILE_NAME : Name of the database file 'utils_output.db'
        DB_PATH : path where the db file should be present
        UNIT_TEST_DB_FILE_NAME: Name of the test database file 'unit_test_cases.db'

    SAMPLE USAGE
        output=test_map_city_tier()

    """
    build_dbs()
    load_data_into_db()
    map_city_tier()

    conn = sqlite3.connect(DB_PATH + DB_FILE_NAME)
    df = pd.read_sql('select * from city_tier_mapped', conn)          
    conn.close()
    conn = sqlite3.connect(DB_PATH + UNIT_TEST_DB_FILE_NAME)
    print(DB_PATH + DB_FILE_NAME)
    print (DB_PATH + UNIT_TEST_DB_FILE_NAME)
    reference_df = pd.read_sql('select * from city_tier_mapped_test_case', conn)          
    conn.close()
    assert df.equals(reference_df), "city_tier_mapped doesn't match expected output city_tier_mapped_test_case"
    

###############################################################################
# Write test cases for map_categorical_vars() function
# ##############################################################################    
def test_map_categorical_vars():
    """_summary_
    This function checks if map_cat_vars function is working properly by
    comparing its output with test cases provided in the db in a table named
    'categorical_variables_mapped_test_case'

    INPUTS
        DB_FILE_NAME : Name of the database file 'utils_output.db'
        DB_PATH : path where the db file should be present
        UNIT_TEST_DB_FILE_NAME: Name of the test database file 'unit_test_cases.db'
    
    SAMPLE USAGE
        output=test_map_cat_vars()

    """
    build_dbs()
    load_data_into_db()
    map_city_tier()
    map_categorical_vars()

    conn = sqlite3.connect(DB_PATH + DB_FILE_NAME)
    df = pd.read_sql('select * from categorical_variables_mapped', conn)          
    conn.close()
    conn = sqlite3.connect(DB_PATH + UNIT_TEST_DB_FILE_NAME)
    print(DB_PATH + DB_FILE_NAME)
    print (DB_PATH + UNIT_TEST_DB_FILE_NAME)
    reference_df = pd.read_sql('select * from categorical_variables_mapped_test_case', conn)          
    conn.close()
    assert df.equals(reference_df), "categorical_variables_mapped doesn't match expected output categorical_variables_mapped_test_case"
    

###############################################################################
# Write test cases for interactions_mapping() function
# ##############################################################################    
def test_interactions_mapping():
    """_summary_
    This function checks if test_column_mapping function is working properly by
    comparing its output with test cases provided in the db in a table named
    'interactions_mapped_test_case'

    INPUTS
        DB_FILE_NAME : Name of the database file 'utils_output.db'
        DB_PATH : path where the db file should be present
        UNIT_TEST_DB_FILE_NAME: Name of the test database file 'unit_test_cases.db'

    SAMPLE USAGE
        output=test_column_mapping()

    """ 
    build_dbs()
    load_data_into_db()
    map_city_tier()
    map_categorical_vars()
    interactions_mapping()

    conn = sqlite3.connect(DB_PATH + DB_FILE_NAME)
    df = pd.read_sql('select * from interactions_mapped', conn)          
    conn.close()
    conn = sqlite3.connect(DB_PATH + UNIT_TEST_DB_FILE_NAME)
    print(DB_PATH + DB_FILE_NAME)
    print (DB_PATH + UNIT_TEST_DB_FILE_NAME)
    reference_df = pd.read_sql('select * from interactions_mapped_test_case', conn)          
    conn.close()
  
    assert df.equals(reference_df), "interactions_mapped doesn't match expected output interactions_mapped_test_case"
   