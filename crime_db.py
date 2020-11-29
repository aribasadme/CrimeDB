import pandas as pd
from police_api import PoliceAPI


crime_categories = "https://data.police.uk/api/crime-categories?date=<Date>"
outcomes_for_crimes = "https://data.police.uk/api/outcomes-for-crime/<Crime ID>"
last_updated = "https://data.police.uk/api/crime-last-updated"

def first_job(api, dates, T_current):
	"""
	Creates the tables and populates them with the historical data
	from ​T​_0
​ 	​to ​T​_current
	"""
	# subset of dates
	dates_hist = dates[dates <= T_current]
	
	# crime_categories table
	s_crime_cat = set()
	for date in dates_hist:
		s_crime_cat.update(api.get_crime_categories(date))

	crime_categories['id'] = [c.url for c in s_crime_cat]
	crime_categories['description'] = [c.name for c in s_crime_cat]
	crime_categories.set_index('id', inplace=True)
	
	# To get the crimes for each force and neighbourhood
	cr = []
	for d in date_hist:
			cr.append([api.get_crimes_area(n.boundary,  date=d) for n in s_nb_flat])
	# Flattern the list
	crimes_flat = [c for sublist1 in cr for sublist2 in sublist1 for c in sublist2]
	# Subset for those containing a valid "persistent_id"
	crimes_flat[:] = [c.__dict__ for c in crimes_flat if c.persistent_id!='']
	# Convert to DataFrame
	df_crimes = pd.DataFrame(crimes_flat)
	df_crimes = df_crimes[['month', 'category', 'id', 'persistent_id', 'location', 'context', 'outcome_status']]
	# Get the key values for the objects in each column
	crimes['latitude'] = df_crimes['location'].apply(lambda x: x.latitude)
	crimes['longitude'] = df_crimes['location'].apply(lambda x: x.longitude)
	crimes['street'] = df_crimes['location'].apply(lambda x: x.street)
	
	## outcome_categories table ##
	# Get outcome_status to populate outcome_categories table
	outcome_status = crimes.pop('outcome_status')
	df_outcomes = pd.DataFrame(outcome_status.apply(lambda x: x.__dict__).to_list())
	df_outcomes.pop('api')
	outcome_categories['id'] = df_outcomes['category'].apply(lambda x: x['id'])
	outcome_categories['name'] = df_outcomes['category'].apply(lambda x: x['name'])
	# Drop duplicates
	outcome_categories = outcome_categories.loc[outcome_categories.name.drop_duplicates().index]
	outcome_categories.set_index('id', inplace=True)
	
	### streets table ###
	# Get streets to populate streets table
	s_streets = crimes['street']
	streets['id'] = s_streets.apply(lambda x: x['id'])
	streets['name'] = s_streets.apply(lambda x: x['name'])
	# Drop duplicates
	streets = streets.loc[streets.id.drop_duplicates().index]
	streets.set_index('id', inplace=True)
	
	# Clean crimes table
	crimes['street'] = crimes['street'].apply(lambda x: x['id'])
	# rename 'month' to 'date'
	crimes.rename(columns={"month": "date"}, inplace=True)
	# Ordering columns
	cols = ['persistent_id', 'category', 'street', 'latitude', 'longitude', 'date', 'context']
	crimes = crimes[cols]
	crimes.set_index('persistent_id', inplace=True)
	
	### outcomes table ###
	crime_idx = crimes.index.to_list()
	l_outcomes = [api.get_crime(idx).outcomes for idx in crime_idx]
	l_outcomes_flat = [o for sublist in l_outcomes for o in sublist]
	outcomes['crime'] = [o.crime.id for o in l_outcomes_flat]
	outcomes['category'] = [o.category.id for o in l_outcomes_flat]
	outcomes['date'] = [o.date for o in l_outcomes_flat]
	outcomes['person_id'] = [' ' for o in l_outcomes_flat] # person_id is empty given by the api
	outcomes.drop_duplicates(['crime','category'], inplace=True)
	outcomes.set_index(['crime','category'], inplace=True)
	
def second_job (api, dates, T_last_update, T_current):
	dates_upd = dates[dates <= T_current && dates >= T_current]
	
	s_crime_cat = set()
	for date in dates_upd:
		s_crime_cat.update(api.get_crime_categories(date))
	url = [c.url for c in s_crime_cat]
	name = [c.name for c in s_crime_cat]
	df_crime_categories = pd.DataFrame.from_dict({'id': url, 'description': name})
	df_crime_categories.set_index('id')
	
	crime_categories.append(df_crime_categories, ignore_index=True)
	
	cr = []
	for d in dates_upd:
			cr.append([api.get_crimes_area(n.boundary,  date=d) for n in s_nb_flat])
	# Flattern the list
	crimes_flat = [c for sublist1 in cr for sublist2 in sublist1 for c in sublist2]
	# Subset for those containing a valid "persistent_id"
	crimes_flat[:] = [c.__dict__ for c in crimes_flat if c.persistent_id!='']
	# Convert to DataFrame
	df_crimes = pd.DataFrame(crimes_flat)
	df_crimes = df_crimes[['month', 'category', 'id', 'persistent_id', 'location', 'context', 'outcome_status']]
	# Get the key values for the objects in each column
	df_crimes['latitude'] = df_crimes['location'].apply(lambda x: x.latitude)
	df_crimes['longitude'] = df_crimes['location'].apply(lambda x: x.longitude)
	df_crimes['street'] = df_crimes['location'].apply(lambda x: x.street)
	
	
	## outcome_categories table ##
	# Get outcome_status to populate outcome_categories table
	outcome_status = df_crimes.pop('outcome_status')
	df_outcomes = pd.DataFrame(outcome_status.apply(lambda x: x.__dict__).to_list())
	df_outcomes.pop('api')
	df_outcome_categories = pd.DataFrame({'id': [], 'description': []})
	df_outcome_categories['id'] = df_outcomes['category'].apply(lambda x: x['id'])
	df_outcome_categories['description'] = df_outcomes['category'].apply(lambda x: x['name'])
	# Drop duplicates
	df_outcome_categories = df_outcome_categories.loc[df_outcome_categoriesdf_outcome_categories.name.drop_duplicates().index]
	df_outcome_categories.set_index('id', inplace=True)
	
	outcome_categories.append(df_outcome_categories, ignore_index=True)
	

	### streets table ###
	# Get streets to populate streets table
	s_streets = crimes['street']
	df_streets = pd.DataFrame({'id': [], 'name': []})
	df_streets['id'] = s_streets.apply(lambda x: x['id'])
	df_streets['name'] = s_streets.apply(lambda x: x['name'])
	# Drop duplicates
	df_streets = df_streets.loc[df_streets.id.drop_duplicates().index]
	df_streets.set_index('id', inplace=True)
	streets.append(df_streets, ignore_index=True)
	
	# Clean crimes table
	df_crimes['street'] = df_crimes['street'].apply(lambda x: x['id'])
	# rename 'month' to 'date'
	df_crimes.rename(columns={"month": "date"}, inplace=True)
	# Ordering columns
	cols = ['persistent_id', 'category', 'street', 'latitude', 'longitude', 'date', 'context']
	df_crimes = crimes[cols]
	df_crimes.set_index('persistent_id', inplace=True)
	
	crimes.append(df_crimes, ignore_index=True)

	### outcomes table ###
	crime_idx = crimes.index.to_list()
	l_outcomes = [api.get_crime(idx).outcomes for idx in crime_idx]
	l_outcomes_flat = [o for sublist in l_outcomes for o in sublist]
	df_outcomes = pd.DataFrame({'crime': [], 'category': [], 'date': [], 'person_id': []})
	df_outcomes['crime'] = [o.crime.id for o in l_outcomes_flat]
	df_outcomes['category'] = [o.category.id for o in l_outcomes_flat]
	df_outcomes['date'] = [o.date for o in l_outcomes_flat]
	df_outcomes['person_id'] = [' ' for o in l_outcomes_flat] # person_id is empty given by the api
	df_outcomes.drop_duplicates(['crime','category'], inplace=True)
	df_outcomes.set_index(['crime','category'], inplace=True)
	
	outcomes.append(df_outcomes, ignore_index=True)
	
def last_job(api, T_current):
	dates_upd = dates[dates == T_current]
	
	s_crime_cat = set()
	for date in dates_upd:
		s_crime_cat.update(api.get_crime_categories(date))
	url = [c.url for c in s_crime_cat]
	name = [c.name for c in s_crime_cat]
	df_crime_categories = pd.DataFrame.from_dict({'id': url, 'description': name})
	df_crime_categories.set_index('id')
	
	crime_categories.append(df_crime_categories, ignore_index=True)
	
	cr = []
	for d in dates_upd:
			cr.append([api.get_crimes_area(n.boundary,  date=d) for n in s_nb_flat])
	# Flattern the list
	crimes_flat = [c for sublist1 in cr for sublist2 in sublist1 for c in sublist2]
	# Subset for those containing a valid "persistent_id"
	crimes_flat[:] = [c.__dict__ for c in crimes_flat if c.persistent_id!='']
	# Convert to DataFrame
	df_crimes = pd.DataFrame(crimes_flat)
	df_crimes = df_crimes[['month', 'category', 'id', 'persistent_id', 'location', 'context', 'outcome_status']]
	# Get the key values for the objects in each column
	df_crimes['latitude'] = df_crimes['location'].apply(lambda x: x.latitude)
	df_crimes['longitude'] = df_crimes['location'].apply(lambda x: x.longitude)
	df_crimes['street'] = df_crimes['location'].apply(lambda x: x.street)
	
	
	## outcome_categories table ##
	# Get outcome_status to populate outcome_categories table
	outcome_status = df_crimes.pop('outcome_status')
	df_outcomes = pd.DataFrame(outcome_status.apply(lambda x: x.__dict__).to_list())
	df_outcomes.pop('api')
	df_outcome_categories = pd.DataFrame({'id': [], 'description': []})
	df_outcome_categories['id'] = df_outcomes['category'].apply(lambda x: x['id'])
	df_outcome_categories['description'] = df_outcomes['category'].apply(lambda x: x['name'])
	# Drop duplicates
	df_outcome_categories = df_outcome_categories.loc[df_outcome_categoriesdf_outcome_categories.name.drop_duplicates().index]
	df_outcome_categories.set_index('id', inplace=True)
	
	outcome_categories.append(df_outcome_categories, ignore_index=True)
	

	### streets table ###
	# Get streets to populate streets table
	s_streets = crimes['street']
	df_streets = pd.DataFrame({'id': [], 'name': []})
	df_streets['id'] = s_streets.apply(lambda x: x['id'])
	df_streets['name'] = s_streets.apply(lambda x: x['name'])
	# Drop duplicates
	df_streets = df_streets.loc[df_streets.id.drop_duplicates().index]
	df_streets.set_index('id', inplace=True)
	streets.append(df_streets, ignore_index=True)
	
	# Clean crimes table
	df_crimes['street'] = df_crimes['street'].apply(lambda x: x['id'])
	# rename 'month' to 'date'
	df_crimes.rename(columns={"month": "date"}, inplace=True)
	# Ordering columns
	cols = ['persistent_id', 'category', 'street', 'latitude', 'longitude', 'date', 'context']
	df_crimes = crimes[cols]
	df_crimes.set_index('persistent_id', inplace=True)
	
	crimes.append(df_crimes, ignore_index=True)

	### outcomes table ###
	crime_idx = crimes.index.to_list()
	l_outcomes = [api.get_crime(idx).outcomes for idx in crime_idx]
	l_outcomes_flat = [o for sublist in l_outcomes for o in sublist]
	df_outcomes = pd.DataFrame({'crime': [], 'category': [], 'date': [], 'person_id': []})
	df_outcomes['crime'] = [o.crime.id for o in l_outcomes_flat]
	df_outcomes['category'] = [o.category.id for o in l_outcomes_flat]
	df_outcomes['date'] = [o.date for o in l_outcomes_flat]
	df_outcomes['person_id'] = [' ' for o in l_outcomes_flat] # person_id is empty given by the api
	df_outcomes.drop_duplicates(['crime','category'], inplace=True)
	df_outcomes.set_index(['crime','category'], inplace=True)
	
	outcomes.append(df_outcomes, ignore_index=True)




def main(T_current):
	# Call the police API
	api = PoliceAPI()
	
	# Define tables
	crime_categories = pd.DataFrame({'id': [], 'description': []})
	outcome_categories = pd.DataFrame({'id': [], 'description': []})
	streets = pd.DataFrame({'id': [], 'name': []})
	crimes = pd.DataFrame({'persistent_id': [], 'category': [], 'street': [], 'city': [], 'latitude': [], 'longitude': [], 'date': [], 'context': []})
	outcomes = pd.DataFrame({'crime': [], 'category': [], 'date': [], 'person_id': []})
	
	# Transform dates into pandas Series for better manipulation
	dates = pd.Series(api.get_dates())
	
	# Get Forces
	forces = api.get_forces()
	# Get neighbourhoods
	neighbourhoods = [f.neighbourhoods for f in forces]
	nb_flat = [n for sublist in neighbourhoods for n in sublist]
	s_nb_flat = pd.Series(nb_flat).unique()
	
	first_job(api, dates, T_current)
	
	t_last_update = api.get_latest_date()
	second_job(api, dates, t_last_update, T_current)

	last_job(api, T_current)
	
	
	
if __name__ == "__main__":
    main(t_current)
