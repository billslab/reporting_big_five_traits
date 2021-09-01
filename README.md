## Reporting Big Five Traits

This program has been designed to generate PDF files containing plots with graphs of the
individual's big five inventory scores plotted on top of the distribution of scores for the
other students in the class. This test is based upon the work of Dr. Oliver P. John at the
Berkeley Personality Lab. As the name suggests, there are five sections to this personality
test. Scores will be between 1 and 5 for each category, where a score of 1 indicates that
you have very little of this trait and 5 indicates that you strongly exhibit this trait.
The five categories are extraversion, agreeableness, conscientiousness, neuroticism, and
openness. This was designed specifically for the Noorda College of Osteopathic Medicine,
and the inaugural class of students have taken the test. This program will most likely be
updated next year to include information from multiple classes of students in the normalization
and percentile calculation, but generate reports only for the current students.

The input csv file must contain the overall scores for the five individual traits.
At this time, the program will not send emails, just generate the reports.
Example usage: `./reporting_big_five_traits.py -p OpeningParagraph.txt -i big_five_results.csv -t tmp -o GeneratedReports`

optional arguments:

  -h, --help            

                        show this help message and exit

  --opening_paragraph OPENING_PARAGRAPH, -p OPENING_PARAGRAPH

                        This is a text file containing the text for the opening paragraph. Do not use a Microsoft
                        Word document.

  --input INPUT, -i INPUT

                        Input file containing the scores from each individual person. The overall scores for each of the
                        five categories should be present in this file. This should be in csv format.

  --tmp TMP, -t TMP     

                        This is the name of a temporary folder that will be used for generating all of the individual plots.
                        This folder will be deleted after the program has finished generating the reports.

  --output_folder OUTPUT_FOLDER, -o OUTPUT_FOLDER

                        This is the name of the output folder where you would like the reports to be saved.
