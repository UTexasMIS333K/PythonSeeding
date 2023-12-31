# -*- coding: utf-8 -*-
"""SeedFileTutorial.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15lU3OTMz5dAwofHpzZCp18fXojffE9tp

## Install Necessary Python Libraries
 - Only needs to be done once per machine
"""

# Installs Python's pandas library, used for structuring data. If running as a .py file instead of a .ipynb, run "pip install pandas" in command prompt (Windows) or terminal (MacOS)
#!pip install pandas

"""## Import Necessary Libraries"""

import pandas as pd

"""## Tools we will use to make the process much easier

### F strings
- Can be used with doc strings
- If you want to print brackets rather than using brackets to insert variables, type the bracket in the string twice
"""

name = "Derek"
money = 40

print(f"Hello, my name is {name} and I have ${money:.2f}")

# Printing curly brackets inside of f-strings
# You need to double-up any brackets that you aren't using to mark variables
print(f"{{ }}")

"""### Doc strings
- Can be used with F strings
- Allow for multiple-line strings with automatic spacing added in
"""

print('''
Hello


my name is Derek


       WOWWWW!
''')

"""### String addition assignment operator"""

string = "Hello "

string += "Hello2 "

string += "Hello3 "

print(string)

"""### All tools combined"""

prices = [50,45,30,20,15,20,75,35,85]

my_string = ""

for i in range(len(prices)):
  my_string +=f"""
Price number {i}:
     ${prices[i]:.2f}

"""

print(my_string)

"""# Bevo's Tunes Demo (Music Store)

Model Diagram:

Link to Diagram: [Model Diagram](https://drive.google.com/file/d/11nuGf8YaGvQsKWPYelJHRmXUHKU2_sap/view?usp=sharing)

## Bring in the data

- For this example we will use data from last year's project, Bevo's Tunes, an online music store
"""

# Sets the raw url variable to a google drive link
google_drive_url = "https://docs.google.com/spreadsheets/d/1bsS-kbqnXTzT1Lue7DhbhPZjyQLUK79C/edit?usp=sharing&ouid=103600383119382934878&rtpof=true&sd=true"
# Changes the google drive URL to 
raw_url = 'https://drive.google.com/uc?id=' + google_drive_url.split('/')[-2]

# You can also use github repositories files as the URL, as long as the repository is public and you are on the raw file (look for a button that says "raw"). An example csv file link is provided
#raw_url = 'https://raw.githubusercontent.com/curran/data/gh-pages/superstoreSales/superstoreSales.csv'


# If you run the file locally on your computer or upload the data to your session storage, you can just use the name of the file
# raw_url = 'SeedingDataV2.xlsx'

# Declare the sheet names that you are wanting to pull data from
sheet_names = ["Customers",
               "Employees",
               "Songs",
               "Albums",
               "Artists",
               "Genres",
               "Song Reviews",
               "Album Reviews",
               "Artist Reviews",
              ]

# Actually read the data from the URL, creates a dictionary of pandas DataFrame objects
# DataFrames are a pre-made structure for us to easily access our data from
data = pd.read_excel(raw_url, sheet_name = sheet_names)

# Check to see that the data read correctly
data["Customers"]

"""## Iterating through pandas dataframes
- We can use the DataFrame method iterrows() to create a list of the DataFrame rows that we access through variables
"""

# for customer in data["Customers"].to_dict(orient="records"):
#   print(customer["FirstName"])

"""## Actually creating files

### Create Constants/Functions that we use multiple times
"""

# Declare constant PROJECT_NAME for C# using statements
PROJECT_NAME = "SeedingTutorial"

# Declare a function to get the beginning part of the Seeding files
# We do this because each seeding file will need the same using statements
# DRY - Don't Repeat Yourself
def using_statements():
  """Returns the using statements and adds the opening brackets necessary for"""
  
  
  
  return f"""
using {PROJECT_NAME}.DAL;
using {PROJECT_NAME}.Models;
using {PROJECT_NAME}.Utilities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;

namespace {PROJECT_NAME}.Seeding
{{
"""

"""### Creating customers/AppUsers file

Create beginning of customers seeding file
"""

# Instantiate a string to hold the customers seeding text
customers_string = ""

# Adds the using statements necessary for the C# code to work
customers_string += using_statements()

# Adds necessary C# code for adding users, based off of HW3's seeding code.
# No variables are needed so there is no need to make it an f-string
customers_string += """
    public static class SeedUsersTutorial
    {
        public async static Task<IdentityResult> SeedAllUsers(UserManager<AppUser> userManager, AppDbContext context)
        {
            //Create a list of AddUserModels
            List<AddUserModel> AllUsers = new List<AddUserModel>();

"""

"""Iterating through each customer record and adding it to our string"""

# Iterate through all customers and add the values to the string
for customer in data["Customers"].to_dict(orient="records"):
  # For each customer in the data, create new lines of code that specify the User's properties
  customers_string += f"""
            AllUsers.Add(new AddUserModel()
            {{
                User = new AppUser()
                {{
                    //populate the user properties that are from the 
                    //IdentityUser base class
                    UserName = "{customer["EmailAddress"]}",
                    Email = "{customer["EmailAddress"]}",
                    PhoneNumber = "{customer["Phone"]}",

                    // Add additional fields that you created on the AppUser class
                    //FirstName is included as an example
                    FirstName = "{customer["FirstName"]}",
                    LastName = "{customer["LastName"]}",
                    Address = "{customer["Address"]}",
                    ZipCode = "{customer["ZipCode"]}",
                    Enabled = true,
                    Fired = false,
                }},
                Password = "{customer["Password"]}",
                RoleName = "Customer"
            }});
"""

#print(customers_string)

"""Add the ending part of the string that actually adds each AppUser object that we created in the list previously"""

# After adding each customer to a list of AppUsers to add, we need to add each new AppUser
# to our database with built-in identity functions
# We will also use try{} blocks to catch errors that arise when seeding a customer

customers_string += """
            //create flag to help with errors
            String errorFlag = "Start";

            //create an identity result
            IdentityResult result = new IdentityResult();
            //call the method to seed the user
            try
            {
                foreach (AddUserModel aum in AllUsers)
                {
                    errorFlag = aum.User.Email;
                    // Took Utilities.AddUser from Relational Data Demo -> this is "Utilities/AddUser.cs"
                    result = await Utilities.AddUser.AddUserWithRoleAsync(aum, userManager, context);
                }
            }
            catch (Exception ex)
            {
                throw new Exception("There was a problem adding the user with email: " 
                    + errorFlag, ex);
            }

            return result;

        }
    }
}
"""

#print(customers_string)

"""Write the string to a file"""

file = open("SeedCustomersTutorial.cs", "w")
file.write(customers_string)
file.close()

"""### Create seeding file for Artists

Add the beginning part of the SeedArtists string:
"""

artists_string = ""

artists_string += using_statements()

artists_string += """

    public static class SeedArtistsTutorial
    {
        public static void SeedAllArtists(AppDbContext db)
        {
            List<Artist> AllArtists = new List<Artist>();
    
"""

"""Loop through each artist row in the dataframe and add the artist's name:"""

for artist in data["Artists"].to_dict(orient="records"):
  artists_string += f"""

            AllArtists.Add(new Artist
            {{
                ArtistName = "{artist["Artist"]}",
                ArtistFeatured = false,
            }}) ; 
"""

"""Add the part of the string that actually adds the Artists to the database"""

artists_string += f"""
            //create a counter and flag to help with debugging
            int intArtistID = 0;
            String strArtistName = "Start";

            //we are now going to add the data to the database
            //this could cause errors, so we need to put this code
            //into a Try/Catch block
            try
            {{
                //loop through each of the artists
                foreach (Artist seedArtist in AllArtists)
                {{
                    //updates the counters to get info on where the problem is
                    intArtistID = seedArtist.ArtistID;
                    strArtistName = seedArtist.ArtistName;

                    //try to find the artist in the database
                    Artist dbArtist = db.Artists.FirstOrDefault(c => c.ArtistName == seedArtist.ArtistName);

                    //if the artist isn't in the database, dbArtist will be null
                    if (dbArtist == null)
                    {{
                        //add the Artist to the database
                        db.Artists.Add(seedArtist);
                        db.SaveChanges();
                    }}
                    else //the record is in the database
                    {{
                        //update all the fields
                        //this isn't really needed for artist because it only has one field
                        //but you will need it to re-set seeded data with more fields
                        dbArtist.ArtistName = seedArtist.ArtistName;
                        dbArtist.ArtistFeatured = seedArtist.ArtistFeatured;
                        //you would add other fields here
                        db.SaveChanges();
                    }}

                }}
            }}
            catch (Exception ex) //something about adding to the database caused a problem
            {{
                //create a new instance of the string builder to make building out 
                //our message neater - we don't want a REALLY long line of code for this
                //so we break it up into several lines
                StringBuilder msg = new StringBuilder();

                msg.Append("There was an error adding the ");
                msg.Append(strArtistName);
                msg.Append(" artist (ArtistID = ");
                msg.Append(intArtistID);
                msg.Append(")");

                //have this method throw the exception to the calling method
                //this code wraps the exception from the database with the 
                //custom message we built above. The original error from the
                //database becomes the InnerException
                throw new Exception(msg.ToString(), ex);
            }}
  
        }}
    }}
        
}}
"""

"""Write the string to a file"""

file = open("SeedArtistsTutorial.cs", "w")
file.write(artists_string)
file.close()

"""### Create seeding file for Artist Ratings

Add the beginning of SeedArtistRatings.cs string:
"""

artist_ratings_string = ""

artist_ratings_string += using_statements()

artist_ratings_string += """

    public static class SeedArtistRatingsTutorial
    {
        public static void SeedAllArtistRatings(AppDbContext db)
        {
            List<ArtistRating> AllArtistRatings = new List<ArtistRating>();
    
"""

"""Loop through the artist ratings/reviews in the dataframe"""

for artist_rating in data["Artist Reviews"].to_dict(orient="records"):
  comment = artist_rating["Comment"]
  if str(comment) == "nan":
    comment = ""
  artist_ratings_string += f"""

            AllArtistRatings.Add(new ArtistRating
            {{
                Artist = db.Artists.FirstOrDefault(c => c.ArtistName == "{artist_rating["Artist"]}"),
                AppUser = db.Users.FirstOrDefault(u => u.FirstName + " " + u.LastName == "{artist_rating["Customer"]}"),
                ArtistRatingVal = {artist_rating["Rating"]:.1f}m,
                ArtistReviewDescription = "{comment}",
                ArtistRatingApproved = true,

            }}) ; 
"""
print(artist_ratings_string)

"""Add the code that adds each artist rating to the database"""

artist_ratings_string += f"""
            //create a counter and flag to help with debugging
            int intArtistRatingID = 0;
            String strArtistReviewCustomer = "Start";
            String strArtistReviewArtist = "Start";

            //we are now going to add the data to the database
            //this could cause errors, so we need to put this code
            //into a Try/Catch block
            try
            {{
                //loop through each of the artistRatings
                foreach (ArtistRating seedArtistRating in AllArtistRatings)
                {{
                    //updates the counters to get info on where the problem is
                    intArtistRatingID = seedArtistRating.ArtistRatingID;
                    strArtistReviewCustomer = seedArtistRating.AppUser.FirstName + seedArtistRating.AppUser.LastName;
                    strArtistReviewArtist = seedArtistRating.Artist.ArtistName;

                    //try to find the artistRating in the database based on whether there already exists and artist review with
                    //the same artist name and the same appuser's first + last name associated with it
                    ArtistRating dbArtistRating = db.ArtistRatings.FirstOrDefault(c => (c.Artist.ArtistName == seedArtistRating.Artist.ArtistName) && 
                                                                                       (c.AppUser.FirstName + " " + c.AppUser.LastName == seedArtistRating.AppUser.FullName)
                                                                                  );

                    //if the artistRating isn't in the database, dbArtistRating will be null
                    if (dbArtistRating == null)
                    {{
                        //add the ArtistRating to the database
                        db.ArtistRatings.Add(seedArtistRating);
                        db.SaveChanges();
                    }}
                    else //the record is in the database
                    {{
                        //update all the fields
                        //this isn't really needed for artistRating because it only has one field
                        //but you will need it to re-set seeded data with more fields
                        dbArtistRating.ArtistRatingVal = seedArtistRating.ArtistRatingVal;
                        dbArtistRating.ArtistReviewDescription = seedArtistRating.ArtistReviewDescription;
                        dbArtistRating.ArtistRatingApproved = seedArtistRating.ArtistRatingApproved;


  
                        //you would add other fields here
                        db.SaveChanges();
                    }}
                }}
            }}
            catch (Exception ex) //something about adding to the database caused a problem
            {{
                //create a new instance of the string builder to make building out 
                //our message neater - we don't want a REALLY long line of code for this
                //so we break it up into several lines
                StringBuilder msg = new StringBuilder();

                msg.Append("There was an error adding the ");
                msg.Append(strArtistReviewCustomer);
                msg.Append(strArtistReviewArtist);
                msg.Append(" strArtistReviewCustomer and strArtistReviewArtist (ArtistRatingID = ");
                msg.Append(intArtistRatingID);
                msg.Append(")");

                //have this method throw the exception to the calling method
                //this code wraps the exception from the database with the 
                //custom message we built above. The original error from the
                //database becomes the InnerException
                throw new Exception(msg.ToString(), ex);
            }}
  
        }}
    }}
        
}}
"""

"""Output the string to a file"""

file = open("SeedArtistRatingsTutorial.cs", "w")
file.write(artist_ratings_string)
file.close()