import pandas as pd
import find_org_funcs
import numpy as np




bacteria = pd.read_excel(r"..\bacteria.xlsx", na_values = "no value")
virus = pd.read_excel(r"..\viruses.xlsx", na_values = "no value")
#parasites = pd.read_excel(r"C:\Users\nilsh\OneDrive\Desktop\microbiology medical\parasites.xlsx", na_values = "no value")
all_orgs = pd.merge(bacteria, virus, how = "outer")
all_orgs = pd.concat([all_orgs, parasites])
bacteria = pd.read_excel(r"..\bacteria.xlsx")


bacteria["Travelling"].fillna("No", inplace=True)
bacteria = bacteria[bacteria["Vaccination"]=="Yes"]
bacteria = bacteria[bacteria["Travelling"]!="No"]
bacteria = bacteria[bacteria["Gram"] == "Positive"]
bacteria = bacteria[bacteria["shape"] == "rod"]
bacteria = bacteria[bacteria["Laboratory Identification"] == "Gram-positive cocci"]
bacteria = bacteria[bacteria["Hemolytic"] == "beta"]
bacteria = bacteria[bacteria["Growth Characteristics"].str.contains('rod')]
bacteria = bacteria[bacteria["People infected"].str.contains('food')]
bacteria = bacteria[~bacteria["People infected"].str.contains('food')]
bacteria = bacteria[bacteria["Symptoms"].str.contains('fever')]
bacteria = bacteria[bacteria["Group of People Infected"].str.contains('UTI') | bacteria['Symptoms'].str.contains('tract') | bacteria["Other Characteristics"].str.contains("tract")]
bacteria = bacteria[bacteria["Growth Characteristics"].str.contains("diplo")]
selected_organism = bacteria[bacteria["People infected"].str.contains("healthcare settings")]




# Define the patient attributes
##default

newborns = "newborns"
hospital = "healthcare settings"
"poor sanitation"
"sexually active"
patient_attributes = ['Organism',"Temperature: ",]
patient_attributes = ['Organism',"food", "accident", "wound", "hospital", "vomit", "fever", "distress", "dizzy", "swollen", "pus", "rash", "cocci"]

inverted_counts = find_org_funcs.count_frequency(case3)

# Find the most probable organism(s) for the patient
found_scores, found_organisms = find_org_funcs.find_most_probable_organisms(patient_attributes, case3 ,inverted_counts, n=8)

print(found_organisms)
selected_organisms = all_orgs[all_orgs["organism"].isin(found_organisms)]
first_organism = found_organisms[0]
organism_choice = selected_organisms[selected_organisms["organism"] == first_organism]

if __name__ == '__main__':
    bacteria = pd.read_excel(r"C:\Users\nilsh\OneDrive\Desktop\microbiology medical\bacteria.xlsx")
    virus = pd.read_excel(r"C:\Users\nilsh\OneDrive\Desktop\microbiology medical\viruses.xlsx")
    all = pd.merge(bacteria, virus, how="outer")
    virulence_factors = pd.read_excel(r"C:\Users\nilsh\OneDrive\Desktop\microbiology medical\bacterias_virulence_factors.xlsx")
    asked_temp = False
    while True:
        if asked_temp != True:
            temp = input("Do you have a temperature indication? Enter N/n for no or the temperature as number.")
            asked_temp = True
            if temp not in ["N", "n"]:
                patient_attributes.append("Temperature: " + temp)
            else:
                pass
        else:
            attribute = input("Enter an attribute or write done to finish.")
            if attribute == "done":
                break
            else:
                patient_attributes.append(attribute)
    travel = input("Has your patient travelled recently? Y/n")
    if travel in ["Y", "y"]:
        travel = "Yes"
    else:
        travel = None
    gram = input("Have you done a gram test? Y/n")
    if gram == True:
        which_gram = input("Is your organism gram positive or gram negative? +/-")
    else:
        which_gram = None
    found_scores, found_organisms = find_org_funcs.find_most_probable_organisms(patient_attributes,
                                                                                all,
                                                                                inverted_counts,
                                                                                travelling=travel,
                                                                                gram = None,
                                                                                n=10)
    first_organism = found_organisms[0]
    organism_choice = selected_organisms[selected_organisms["organism"] == first_organism]
    print("Found Organism: " + organism_choice["organism"] == first_organism)
    print("Transmission: " + organism_choice["Transmission"])
    print("Laboratory Identification: " + organism_choice["Laboratory Identification"])
    print("Treatment: " + organism_choice["Treatment"])
    org_vir_factors = virulence_factors[virulence_factors["Organism"] == first_organism]
    print("Common virulence Factors: " + org_vir_factors)
