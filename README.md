## Dataset Overview

This dataset explores cats listed for adoption from the RescueGroups Public API, and how long they took to be adopted from the time they became available. 
The goal is to find correlations between cat characteristics and the number of days a cat spends in adoption care.

API Documentation: https://api.rescuegroups.org/v5/public/docs#schema-reference

**Dependent variable:** `length_of_stay` — the number of days between `availableDate` and `adoptionDate`.

**Type:** Quantitative

**Independent variables (24 total, mix of quantitative and categorical):**

- Sex
- sizeCurrent
- sizeGroup
- ageGroup
- ageString
- breedString
- colorDetails
- vocalLevel
- sheddingLevel
- energyLevel
- exerciseNeeds
- isSpecialNeeds
- isMicrochipped
- isCurrentVaccinations
- isDeclawed
- isHousetrained
- isKidsOK
- isSeniorsOk
- adultSexesOk
- obedienceTraining
- ownerExperience
- newPeopleReaction
- pictureCount
- videoCount

Variables of focus will be decided later on.

**Dataset size:** 11,929 rows (cleaned)
