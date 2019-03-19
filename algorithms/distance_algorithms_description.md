# Distance algorithms discription

## Base algorithm

### Preparation

- First, you need a way to define **zones** : a delimited area with a given centroid to separate postcodes.
- Second, fill a database with all the distance between each pair of **zone**, by route and as the crow flies.

### Get distance between postcodes

Given two postcodes (postcode, country iso code) :
1. Get the distance as the crow flies between the two postcodes (named *C*)
2. Find to which group belong each postcode
3. Extract from the database the two kinds of distance between the two *zones* and calculate the ratio *route*/*crow* (named *R*).
4. Finally calculate : *c* * *R*

---

## 2-digits version

The orinal proposal was to use the 2 first digits of the postcodes to define the *zones*. By *"2 first digits"*, I think was meant : *Administrative region* (such as *Bundesland* in Germany, *Département* in France or *State* in the U.S.A.) ; and indeed in France and Germany, these *zones* are indicated by the two first digits of the postcodes.

This, however, cannot be generalized to every country in Europe, so I didn't want to just use the first two digits directly at first. I looked for a way to define admninistrative regions and their contained postcodes but couldn't find a proper solution for that.



- get centroid

## Grid version

---

## Graphhopper problem

Graphhopper has sometimes trouble tracing roads between two points when one of the coordinates are located not enough close from the road or something, **the request returns an error**.

This creates a problem when requesting the distance by road between two *zones*' centroids : an error occurs and the corresponding line is not entered in the database. For this reason, calculating the distance using any of the algorithms from the database won't work.

### Solution

Probably one of the best solutions would be to *circle around* the centroids until we find coordinates that work, that would increase a lot the time spent generating the distance database and it would be difficult to implement.

For these reasons, when these errors happened, I first chose to default to the distance *as the crow flies*. After some tests, I found that, in average, the distance *as the crow flies* is **76%** of the distance by route. So I set the default to **dist_crow / 0.76**.

> Note : This is also applied when the two requested postcodes are in the same *zone*.
