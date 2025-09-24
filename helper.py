import plotly.express as px
import pandas as pd

df = pd.read_csv("marine_dataset.csv")


def get_specie_df(specie):
  specie_df = df.copy()
  if specie != "Overall":
    specie_df = specie_df[specie_df["Fish_Species"] == specie]
  return specie_df


def yearly_fish_abundance(df, specie):
  fish_abundance_yearly = df.groupby('Year')['Fish_Abundance'].mean().reset_index()
  fig = px.line(fish_abundance_yearly, 
                x='Year', 
                y='Fish_Abundance', 
                title=f'Average Fish Abundance Year by Year ({specie})',
                markers=True)
  return fig


def abundance_vs_water_temp(df, specie):
  fig = px.scatter(df, x="Water_Temp_C", y="Fish_Abundance", size_max=15,
                 title=f"Fish Abundance vs Water Temperature ({specie})")
  return fig


def fish_length_vs_oxygen(df, specie):
  fig_do = px.scatter(df, 
                    x='Dissolved_Oxygen_mgL', 
                    y='Fish_Length_cm',
                    title=f'Fish Length vs Dissolved Oxygen (mg/L) - {specie}')
  return fig_do


def abundance_vs_coord(df, specie):
  fig = px.scatter(df, x="Longitude", y="Latitude", size="Fish_Abundance",
                  hover_data=["Fish_Abundance"], title=f"Fish Abundance Across Locations ({specie})",
                  size_max=30)
  return fig


def yearly_dissolved_oxygen():
  do_yearly = df.groupby('Year')['Dissolved_Oxygen_mgL'].mean().reset_index()
  fig = px.line(do_yearly, 
                x='Year', 
                y='Dissolved_Oxygen_mgL', 
                title='Average Dissolved Oxygen (mg/L) Year by Year',
                markers=True)
  return fig

def get_species_distribution():
  species_count = df['Fish_Species'].value_counts().reset_index()
  species_count.columns = ['Fish_Species', 'Count']
  fig = px.bar(species_count, x="Fish_Species", y="Count", color="Fish_Species",
              title="Species Distribution")
  return fig


species_list = df["Fish_Species"].unique().tolist()
species_list.insert(0, "Overall")