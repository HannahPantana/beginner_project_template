import pandas as pd

sayings = pd.DataFrame(
    {
        "Bob": ["I liked it.", "It was bad."],
        "Jerry": ["There goes that man.", "Oh my goodness!"],
    }
)

kaggle_sayings = pd.DataFrame(
    {"Bob": ["I liked it.", "It was awful."], "Sue": ["Pretty good.", "Bland."]},
    index=["Product A", "Product B"],
)

sample_series = pd.Series([1, 2, 3, 4, 5])

# create a series to represent sales year-by-year for one product

# defines name of series as Product A Sales, 2020-2022
# each row represents revenue for the year
# there is no column
ProductA_Sales = pd.Series(
    [100, 200, 300],
    index=["2020 Sales", "2021 Sales", "2022 Sales"],
    name="Product A Sales, 2020-2022",
)

# read the csv into a dataframe for wine_reviews
wine_reviews = pd.read_csv(
    "C:/Users/jpan0/Documents/Repositories/LearningPandas/data/raw/winemag-data-130k-v2.csv",
    index_col=0,
)

# tells us how many rows and columns are in the dataframe wine_reviews
wine_reviews.shape

# shows first 5 rows
wine_reviews.head()

# shows last five rows
wine_reviews.iloc[-5:]

# Shows first 5 rows (0-4 index) and only the following listed columns
wine_reviews.loc[:4, ["country", "taster_name", "taster_twitter_handle", "points"]]

# finds all rows where country is US
wine_reviews.loc[wine_reviews.country == "US"]

# finds all rows where country is Italy or France and the wine review points exceeds 98
wine_reviews.loc[
    (wine_reviews.country.isin(["Italy", "France"])) & (wine_reviews.points > 98)
]

# finds all rows where price is <= 5 and points >= 80
wine_reviews.loc[(wine_reviews.price <= 5) & (wine_reviews.points >= 80)]

# create new column called backwards index that indexes in descending order
wine_reviews["backwards_index"] = range(len(wine_reviews), 0, -1)
wine_reviews["backwards_index"]


# create a DataFrame fruits that has row 0, columns Apple, Banana
# 30 apples, 21 bananas
fruits = pd.DataFrame({"Apples": [30], "Bananas": [21]})

fruit_sales = pd.DataFrame(
    {"Apples": [35, 41], "Bananas": [21, 34]}, index=["2017 Sales", "2018 Sales"]
)

# create a Series that shows ingredients and the quantity we need. Both are string values
ingredients = pd.Series(
    ["4 cups", "1 cup", "2 large", "1 can"],
    index=["Flour", "Milk", "Eggs", "Spam"],
    name="Dinner",
)

# create a DataFrame called animals and save it to a specific file location
animals = pd.DataFrame(
    {"Cows": [12, 20], "Goats": [22, 19]}, index=["Year 1", "Year 2"]
)
animals_file_location = "../data/raw/cows_and_goats.csv"
animals.to_csv(animals_file_location, index=True)

# kaggle exercises for Pandas lesson 2
# Select the description column from reviews and assign the result to the variable desc
desc = wine_reviews.loc[:, "description"]

# Now select the first row that shows just the description
first_desc = desc[0]

# or you can do

first_desc_alternative = wine_reviews.loc[0, "description"]

# or even
first_desc_another_alternative = wine_reviews.description.iloc[0]

# select first row
first_review = wine_reviews.iloc[0]

# show first 10 descriptions
first_10_descriptions = pd.Series(desc[:10])

# show the rows with index 1,2,3,5,8
sample_reviews = wine_reviews.iloc[[1, 2, 3, 5, 8]]

# get rows 0, 1, 10, 100 and only show country, province, region1, region 2
sample_reviews_2 = wine_reviews.loc[
    [0, 1, 10, 100], ["country", "province", "region_1", "region_2"]
]

# get first 100 rows containing country and variety
first_100_country_variety = wine_reviews.loc[0:99, ["country", "variety"]]

# find reviews of only Italian wines
italian_wine_reviews = wine_reviews.loc[wine_reviews.country == "Italy"]

# find 95+ point reviews of only Aus/NZ wines
top_oceania_wines = wine_reviews.loc[
    (wine_reviews.country.isin(["Australia", "New Zealand"]))
    & (wine_reviews.points >= 95)
]

# function to get an overview of a column
wine_reviews.taster_name.describe()

# function to get just the mean for wine points
wine_reviews.points.mean()

# function to get unique names for tasters
wine_reviews.taster_name.unique()

# To see a list of unique values and how often they occur in the dataset, we can use the value_counts() method:
wine_reviews.taster_name.value_counts()

# let's say we wanted to change value of points column to show the difference of the specific wine's points
# versus the mean
# first, we need to find the mean point
wine_reviews_points_mean = wine_reviews.points.mean()

# second, using map, we create a lambda function to take in single parameter p (point)
# and find difference between that and the mean variable we calculated
wine_reviews.points.map(lambda p: p - wine_reviews_points_mean)


# another method we can use is apply function
def remean_points(row):
    row.points = row.points - wine_reviews_points_mean
    return row


wine_reviews.apply(remean_points, axis=1)

# another low-code method to find difference between
wine_reviews.points - wine_reviews_points_mean

# you can use variable and concatenate/add them to each other
wine_reviews.country + " - " + wine_reviews.region_1
wine_reviews.points + wine_reviews.price

# find median of points
wine_reviews_points_median = wine_reviews.points.median()

# Problem: Find the wine with the highest points-to-price ratio.

# first, create a variable bargain_score that calculates for each row
# the points-to-price ratio
bargain_score = wine_reviews.points / wine_reviews.price

# create a column called bargain_score
wine_reviews["bargain_score"] = bargain_score

# find row with the max bargain score while excluding null values
max_bargain_score = wine_reviews.bargain_score.max(skipna=True)
bargain_wine = wine_reviews.loc[wine_reviews.bargain_score == max_bargain_score]
bargain_wine_title = bargain_wine.title.iloc[0]

# the method from Kaggle
kaggle_bargain_idx = (wine_reviews.points / wine_reviews.price).idxmax()
kaggle_bargain_wine = wine_reviews.loc[kaggle_bargain_idx, "title"]

# find out how often the words "tropical" or "fruity" appear. This can be case-sensitive

# first, calculate the occurences of each word
wine_reviews["tropical_count"] = wine_reviews["description"].str.count(r"\btropical\b")
wine_reviews["fruity_count"] = wine_reviews["description"].str.count(r"\bfruity\b")

wine_reviews.loc[0, "description"] = (
    "I love the tropical tropical tropical fruity taste. It's not too tropical though."
)

descriptor_counts_tropical_fruity = pd.Series(
    {
        "tropical": wine_reviews.tropical_count.sum(),
        "fruity": wine_reviews.fruity_count.sum(),
    }
)

# Kaggle's method, which leverages map function
kaggle_n_tropical = wine_reviews.description.map(lambda desc: "tropical" in desc).sum()
kaggle_n_fruity = wine_reviews.description.map(lambda desc: "fruity" in desc).sum()

kaggle_descriptor_counts = pd.Series(
    {"tropical": kaggle_n_tropical, "fruity": kaggle_n_fruity}
)

# translate each wine to have it's own star-rating
# any wine from Canada is 3 stars
# any wine >= 95 points is 3 stars
# any wine (not Canadia) below 85 is 1 star
# any wine (not Canadian) that is >= 85 but below 95 is 2 stars

# first initialize a new column
wine_reviews["Stars"] = None


# second create a function to assign stars for a row. Then apply it.
def assign_star(row):
    if row.country == "Canada":
        return 3
    elif row.points >= 95:
        return 3
    elif row.points >= 85 and row.points < 95:
        return 2
    elif row.points < 85:
        return 1


wine_reviews["Stars"] = wine_reviews.apply(assign_star, axis=1)

star_ratings = pd.Series(wine_reviews["Stars"])

# using groupby function to see how many wines there are for each point
wine_reviews.groupby("points").points.value_counts()

# we can also see what the cheapest price for a bottle there is for each point grouping
wine_reviews.groupby("points").price.min()

# using apply and groupby function, we can see what the first wine reviewed is for each winery
wine_reviews.groupby("winery").apply(lambda df: df.title.iloc[0])

# group by country and provice, and then show the highest-rated wine for each grouping
wine_reviews.groupby(["country", "province"]).apply(
    lambda df: df.loc[df.points.idxmax()]
)

# we can even use an agg() for groups
wine_reviews.groupby("country").price.agg([len, min, max])

# multi-index exmaple below
country_province_reviewed = wine_reviews.groupby(
    ["country", "province"]
).description.agg([len])
type(country_province_reviewed)


mi_example1 = country_province_reviewed.index
type(mi_example1)

# mi_example1 output spits out all combinations of country-province
mi_example1

# see what reset index does. compare w/ the prior variable
country_province_reviewed_indexed = country_province_reviewed.reset_index()

# type is a dataframe now
type(country_province_reviewed_indexed)

# use sort_values to sort the indexed above
country_province_reviewed_indexed.sort_values(by="len", ascending=False)

# use sort_index to sort by index
country_province_reviewed_indexed.sort_index()

# sort by more than one column
country_province_reviewed_indexed.sort_values(by=["country", "province", "len"])

# Kaggle Pandas Lesson 4 Exercises

# find the most common reviewers. Use twitter handle as the index.
reviewer_list = wine_reviews.groupby(
    ["taster_twitter_handle"]
).taster_twitter_handle.value_counts()
reviewer_list_indexed = reviewer_list.reset_index()

# group by price and find the highest-rated wine per price
best_wine_per_price = wine_reviews.groupby(["price"]).points.max()

# create dataframe that shows for each variety, what min and max price are
variety_min_max = (
    wine_reviews.groupby("variety")
    .price.agg(["min", "max"])
    .sort_values(by=["min", "max"], ascending=False)
)

# display the mean points review for each reviewr

reviewer_mean_ratings = wine_reviews.groupby("taster_name").points.mean()
reviewer_mean_ratings.describe()

# what country-variety is most common?

country_variety = wine_reviews.groupby(["country", "variety"]).description.agg([len])
country_variety_indexed = country_variety.reset_index()
country_variety_indexed_sorted = country_variety_indexed.sort_values(
    by="len", ascending=False
)

# get the type of price
wine_reviews.price.dtype

# get all types in the dataframe
wine_reviews.dtypes

# convert points column from int to float
wine_reviews.points.astype("float64")

wine_reviews.index.dtype

# what if we wanted to find all records where price is nulL?
wine_reviews[pd.isnull(wine_reviews.country)]

# let's fill all the records w/ NaN country w/ "Unknown"
wine_reviews.country.fillna("Unknown")

# or what if someone's twitter handle changed?
wine_reviews.taster_twitter_handle.replace("@kerinokeefe", "@kerino")

# create a series that shows most common wine-producing regions (use region 1)
# have NaN field be "unknown"
wine_reviews.region_1.fillna("Unknown").value_counts().sort_values(ascending=False)

# rename a column. In this case, let's rename points column to score
wine_reviews.rename(columns={"points": "score"})

# rename() can also take in index or column parameter to change specific rows
wine_reviews.rename(index={0: "firstEntry", 1: "secondEntry"})

# rename_axis() can assign names to the row and column indexes
wine_reviews.rename_axis("wines", axis="rows").rename_axis("fields", axis="columns")

# to practice joining, we will create two new dataframes from two files
# representing US and CA YouTube trending stats

ca_youtube = pd.read_csv("../data/raw/CAvideos.csv/CAvideos.csv")
us_youtube = pd.read_csv("../data/raw/USvideos.csv/USvideos.csv")

ca_us_youtube = pd.concat([ca_youtube, us_youtube])

# do a join! potential common PKs are trending_date and video_id

# but before I do this, I want to run some tests to see how many trending dates there are for specific video ids. Let's sort by video id
ca_youtube.sort_values(by=["video_id"], ascending=False)
# judging by this output, you can see that there is a one-to-many relationship between video id and trending date

# let's set the variable for the set_index function on each of the CA and US dataframes
ca_youtube_set_index = ca_youtube.set_index(["video_id", "trending_date"])
us_youtube_set_index = us_youtube.set_index(["video_id", "trending_date"])

# now, let's join!
ca_us_joined_youtube = ca_youtube_set_index.join(
    us_youtube_set_index, lsuffix="_CA", rsuffix="_US"
)

# let's pull the CA views, CA likes, US views, US likes for video_id n1WpP7iowLc on 17.14.11
ca_us_joined_youtube.loc[(video_id == "n1WpP7iowLc") & (trending_date == "17.14.11")]
# the above does NOT work, because video_id and trending_date are not columns/fields, but indexes

ca_us_joined_youtube.loc[
    ("n1WpP7iowLc", "17.14.11"), ["views_CA", "likes_CA", "views_US", "likes_US"]
]

# Kaggle Pandas Tutorial: Renaming and Combining Exercises
wine_reviews.head()

# region_1 and region_2 rename to region and locale, respectively
region_locale_renamed = wine_reviews.rename(
    columns={"region_1": "region", "region_2": "locale"}
)

# set the index to the "wines" column, since each row represents exactly one wine, and there can only be one occurence of the wine in the dataframe
title_renamed = wine_reviews.rename(columns={"title": "wines"})
wine_reindexed = title_renamed.set_index(["wines"])
