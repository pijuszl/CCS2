---
license: cc-by-4.0
task_categories:
- text-classification
language:
- lt
tags:
- Prapganda;
- Propaganda techniques
- Propaganda narratives
pretty_name: >-
  HALT-PROP: Human-Annotated Lithuanian Textual Corpus for Propaganda Narratives
  and Techniques
size_categories:
- 1K<n<10K

configs:
  - config_name: annotations
    data_files: "Annotations.csv"
    sep: ";"
  - config_name: primary_filter
    data_files: "PrimaryFilter.csv"
    sep: ";"
---
### About Dataset

The HALT-PROP dataset – the first human-annotated Lithuanian textual propaganda corpus, a pioneering resource not only for Lithuania but also for the broader Baltic region 
and other countries neighbouring Russia. The corpus comprises two complementary datasets: (1) 2870 news articles manually labeled by five experts at the article level to identify 
the presence of propaganda, and (2) a subset of 1000 articles annotated for specific propaganda techniques and narratives using a cross-annotation approach, 
where each article was independently labeled by two of the five experts and finalized through pairwise discussion. 
This resource lays the groundwork for future research in propaganda detection for low-resource languages.

### Content

* File Annotations.csv contains 1000 records with 7 features as follows:
  - index.	An article number
  - heading.	Media outlet article headline.
  - content.	Media outlet article content, without HTML formatting in the Lithuanian language.
  - is_propaganda.	Label for the content. It could be one of the following values:\
		•	“yes” for text marked as propaganda. The text is marked as propaganda only if it contains one or more narratives from the narrative list and one or more techniques from the technique list.\
		•	“no” for text that is not marked as propaganda\
		•	“propagandaCitation” for an article that consists only of propaganda citation\
		•	“nonDeterminable”/“Unclear” for an article that could not be defined as propaganda or not propaganda\
	- narratives.	Narratives found in the content of the article. A detailed description of each narrative can be found in the section “Selection of Propaganda Narratives”. 
					The content could have a few narratives from the list:
		1.	“disinformationAboutTheWarInUkraine”
		2.	“delegitimizationOfTheLithuanianState”
		3.	“underminingTheLithuanianArmedForces”
		4.	“erosionOfTrustInLithuanianInstitutions”
		5.	“attacksOnWesternInstitutionsAndAlliances”
		6.	“declineOfWesternCivilization”
		7.	“authoritarianModelPromotion”
		8.	“U.S.DeclineAndWashingtonHegemony”
		9.	“geopoliticalReorderingAndTheNewWorldOrder”
		10.	“weaponizationOfMigrationAndRefugees”
		11.	“revivalOfLitvinism”
	- custom_narratives.	It could be a list of other narratives in Lithuanian language identified by the annotators
	- techniques.	The list of techniques found in the article content. Each item on the list has a structure as follows:\
		•	“start” – the beginning of the technique\
		•	“end” – the end of the technique\
		•	“technique” – abbreviation of the technique found in Table 2\
		•	“text” – the part of article content corresponding to the technique

* File PrimaryFilter.csv contains 2870 records with 4 features as follows:
	- index.	An article number
	- heading.	Media outlet article headline
	- content.	Media outlet article content, without HTML formatting in the Lithuanian language
	- is_propaganda.	Has the same values as in Annotations.csv


More details about the dataset could be find in the paper:

HALT-PROP: Human-Annotated Lithuanian Textual Corpus for Propaganda Narratives and Techniques 
Ieva Rizgelienė, Vilma Zubaitienė, Nerijus Maliukevičius, Virginijus Marcinkevičius

In the contemporary technological landscape, propaganda has become one of the most pervasive tools in information warfare. 
Social media platforms and entire media ecosystems are leveraged to disseminate hostile propaganda aimed at polarizing societies, 
destabilizing states, and eroding longstanding democratic processes. Malign propaganda is not only common in widely-spoken languages 
but also targets less-spoken languages to maximize its reach and influence. While progress has been made in developing models capable 
of detecting propaganda, most advances have focused on high-resource languages. In contrast, low-resource languages continue 
to face significant limitations, the most critical being the scarcity of annotated datasets. In many regions and countries, 
such resources are entirely absent. To address this gap, we present the HALT-PROP dataset, the first human-annotated Lithuanian textual propaganda corpus. 
The corpus comprises two complementary datasets: (1) 2,870 news articles manually labeled by five experts at the article level to identify the presence of propaganda; 
and (2) a subset of 1,000 articles annotated for specific propaganda techniques and narratives using a cross-annotation approach. 

## Citation
If you use this dataset, please cite:

```bibtex
@Article{Rizgelienė2025,
	author={Rizgelien{\.{e}}, Ieva
	and Zubaitien{\.{e}}, Vilma
	and Maliukevi{\v{c}}ius, Nerijus
	and Marcinkevi{\v{c}}ius, Virginijus},
	title={HALT-PROP: Human-Annotated Lithuanian Textual Corpus for Propaganda Narratives and Techniques},
	journal={Scientific Data},
	year={2025},
	month={Dec},
	day={03},
	abstract={In the contemporary technological landscape, propaganda has become one of the most pervasive tools in information warfare. Social media platforms and entire media ecosystems are leveraged to disseminate hostile propaganda aimed at polarizing societies, destabilizing states, and eroding longstanding democratic processes. Malign propaganda is not only common in widely-spoken languages but also targets less-spoken languages to maximize its reach and influence. While progress has been made in developing models capable of detecting propaganda, most advances have focused on high-resource languages. In contrast, low-resource languages continue to face significant limitations, the most critical being the scarcity of annotated datasets. In many regions and countries, such resources are entirely absent. To address this gap, we present the HALT-PROP dataset, the first human-annotated Lithuanian textual propaganda corpus. The corpus comprises two complementary datasets: (1) 2,870 news articles manually labeled by five experts at the article level to identify the presence of propaganda; and (2) a subset of 1,000 articles annotated for specific propaganda techniques and narratives using a cross-annotation approach.},
	issn={2052-4463},
	doi={10.1038/s41597-025-06367-w},
	url={https://doi.org/10.1038/s41597-025-06367-w}
}
```
