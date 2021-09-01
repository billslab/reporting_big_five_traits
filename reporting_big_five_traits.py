#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser
import pandas as pd
from scipy import stats
from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import sys
import warnings

# Ignore the future deprecation warning
warnings.simplefilter("ignore", category=FutureWarning)

args = ArgumentParser('./reporting_big_five_traits.py', description="""This program has been designed to generate PDF files containing plots with
	graphs of the individual's big five inventory scores plotted on top of the distribution of scores for the other students in the class.
	At this time, the program will not send emails, just generate the reports.
	Example usage: ./reporting_big_five_traits.py -p OpeningParagraph.txt -i big_five_results.csv -t tmp -o GeneratedReports""")

args.add_argument(
	'--opening_paragraph',
	'-p',
	help="This is a text file containing the text for the opening paragraph. Do not use a Microsoft Word document.",
	default=None
)

args.add_argument(
	'--input',
	'-i',
	help="""Input file containing the scores from each individual person. The overall scores for each of the five categories should be
	present in this file. This should be in csv format.""",
	default=None
)

args.add_argument(
	'--tmp',
	'-t',
	help="""This is the name of a temporary folder that will be used for generating all of the individual plots. This folder will
	be deleted after the program has finished generating the reports.""",
	default='tmp'
)

args.add_argument(
	'--output_folder',
	'-o',
	help="""This is the name of the output folder where you would like the reports to be saved.""",
	default='BFI_reports'
)

def error_message():
	print()
	print("""\tWelcome to reporting_big_five_traits.py. This program has been designed to generate PDF files containing plots with
	graphs of the individual's big five inventory scores plotted on top of the distribution of scores for the other students in the class.
	Example usage: ./reporting_big_five_traits.py -p OpeningParagraph.txt -i big_five_results.csv -t tmp -o GeneratedReports""")
	print()

args = args.parse_args()

if args.opening_paragraph == None:
	error_message()
	print("""\tYou have not entered a text file containing the text that should be used for the opening paragraph.
	Please add a file using the -p option.""")
	print()
	text_files = glob.glob('*.txt')
	if len(text_files) == 0:
		print("\tNo text files are present in your current working directory. ")
	else:
		print("\tText files that are present in your current working directory:")
		for file in text_files:
			print("\t\t"+file)
	print()
	sys.exit(1)

if args.input == None:
	error_message()
	print("""\tYou have not entered an input csv file containing the individual scores for each person for the big five traits.
	Please add a csv file using the -i option.""")
	print()
	csv_files = glob.glob('*.csv')
	if len(csv_files) == 0:
		print("\tNo csv files are present in your current working directory. ")
	else:
		print("\tcsv files that are present in your current working directory:")
		for file in csv_files:
			print("\t\t"+file)
	print()
	sys.exit(1)

all_scores = pd.read_csv(args.input, header = 0)
needed_columns = ['Name', 'Extraversion Score', 'Agreeableness Score', 'Conscientiousness Score', 'Neuroticism Score', 'Openness Score']
input_columns = all_scores.columns
all_present = True
for column in needed_columns:
	if column not in input_columns:
		all_present = False
		break

if all_present == False:
	error_message()
	print("""\tThe input csv file that you have provided did not have labeled columns for each of the five categories.
	Please relabel your column headers for the total scores and ensure the following labels are all accounted for:""")
	print()
	for column in needed_columns:
		print("\t"+column)
	print()
	sys.exit(1)


extra_scores = []
agree_scores = []
consc_scores = []
neuro_scores = []
open_scores = []

scores = []

for index, row in all_scores.iterrows():
	# email = row['Email'] # Not current planning to use this, but will use this if we end up using python to email them
	name = row['Name']
	extra_score = row['Extraversion Score']
	agree_score = row['Agreeableness Score']
	consc_score = row['Conscientiousness Score']
	neuro_score = row['Neuroticism Score']
	open_score = row['Openness Score']
	scores.append(
		{
			'name': name,
			#'email': email,
			'extra_score': extra_score,
			'agree_score': agree_score,
			'consc_score': consc_score,
			'neuro_score': neuro_score,
			'open_score': open_score
		}
	)
	extra_scores.append(extra_score)
	agree_scores.append(agree_score)
	consc_scores.append(consc_score)
	neuro_scores.append(neuro_score)
	open_scores.append(open_score)

# Now calculate percentiles for each individual score
for person in scores:
	percent_extra = round(stats.percentileofscore(extra_scores, person['extra_score']), 2)
	percent_agree = round(stats.percentileofscore(agree_scores, person['agree_score']), 2)
	percent_consc = round(stats.percentileofscore(consc_scores, person['consc_score']), 2)
	percent_neuro = round(stats.percentileofscore(neuro_scores, person['neuro_score']), 2)
	percent_open = round(stats.percentileofscore(open_scores, person['open_score']), 2)
	person['extra_percent'] = percent_extra
	person['agree_percent'] = percent_agree
	person['consc_percent'] = percent_consc
	person['neuro_percent'] = percent_neuro
	person['open_percent'] = percent_open


with open (args.opening_paragraph, 'r') as file:
    opening_paragraph = file.read()

tmp_directory = args.tmp
output_directory = args.output_folder
os.makedirs(tmp_directory, exist_ok=True)
os.makedirs(output_directory, exist_ok=True)

# define the class to create the PDF objects
class PDF(FPDF):
	def opening_paragraph(self, name):
		self.set_xy(25.4,25.4)
		self.set_font('Arial', '', 12)
		self.cell(w=159.2, h=8, align='L', txt='Dear '+name+',', border=0)
		# I tried changing the alignment to 'J' but it stays left.
		self.set_xy(25.4,35.4)
		self.multi_cell(w=159.2, h=6, align='L', txt=opening_paragraph, border=0)
	def extraversion(self, extra_score, extra_percentile, name):
		self.set_font('Arial', 'B', 12)
		self.set_xy(25.4,121.4)
		self.cell(w=159.2, h=6, align='L', txt='Extraversion:', border=0)
		self.set_xy(25.4,127.4)
		self.set_font('Arial', '', 12)
		self.multi_cell(w=159.2, h=6, align='L', txt="Your score for extraversion: "+str(extra_score), border=0)
		self.set_xy(25.4,134.4)
		self.multi_cell(w=159.2, h=6, align='L', txt="Your percentile among students for extraversion: "+str(extra_percentile), border=0)
		self.set_xy(12,140)
		pdf.image(tmp_directory+'/'+name+' Extraversion.png', x = None, y = None, w = 177.8, h = 101.6, type = '', link = '')
	def agreeableness(self, agree_score, agree_percent, name):
		self.set_xy(12,38.4)
		pdf.image(tmp_directory+'/'+name+' Agreeableness.png', x = None, y = None, w = 177.8, h = 101.6, type = '', link = '')
		self.set_font('Arial', 'B', 12)
		self.set_xy(25.4,25.4)
		self.cell(w=159.2, h=6, align='L', txt='Agreeableness:', border=0)
		self.set_xy(25.4,31.4)
		self.set_font('Arial', '', 12)
		self.multi_cell(w=159.2, h=6, align='L', txt="Your score for agreeableness: "+str(agree_score), border=0)
		self.set_xy(25.4,37.4)
		self.multi_cell(w=159.2, h=6, align='L', txt="Your percentile among students for agreeableness: "+str(agree_percent), border=0)
	def conscientiousness(self, consc_score, consc_percent, name):
		self.set_xy(12,157.4)
		pdf.image(tmp_directory+'/'+name+' Conscientiousness.png', x = None, y = None, w = 177.8, h = 101.6, type = '', link = '')
		self.set_font('Arial', 'B', 12)
		self.set_xy(25.4,144.4)
		self.cell(w=159.2, h=6, align='L', txt='Conscientiousness:', border=0)
		self.set_xy(25.4,150.4)
		self.set_font('Arial', '', 12)
		self.multi_cell(w=159.2, h=6, align='L', txt="Your score for conscientiousness: "+str(consc_score), border=0)
		self.set_xy(25.4,156.4)
		self.multi_cell(w=159.2, h=6, align='L', txt="Your percentile among students for conscientiousness: "+str(consc_percent), border=0)
	def neuroticism(self, neuro_score, neuro_percent, name):
		self.set_xy(12,38.4)
		pdf.image(tmp_directory+'/'+name+' Neuroticism.png', x = None, y = None, w = 177.8, h = 101.6, type = '', link = '')
		self.set_xy(25.4,38.4)
		self.multi_cell(w=159.2, h=6, align='L', txt="Your percentile among students for neuroticism: "+str(neuro_percent), border=0)
		self.set_font('Arial', 'B', 12)
		self.set_xy(25.4,25.4)
		self.cell(w=159.2, h=6, align='L', txt='Neuroticism:', border=0)
		self.set_xy(25.4,31.4)
		self.set_font('Arial', '', 12)
		self.multi_cell(w=159.2, h=6, align='L', txt="Your score for neuroticism: "+str(neuro_score), border=0)
	def openness(self, open_score, open_percent, name):
		self.set_xy(12,157.4)
		pdf.image(tmp_directory+'/'+name+' Openness.png', x = None, y = None, w = 177.8, h = 101.6, type = '', link = '')
		self.set_font('Arial', 'B', 12)
		self.set_xy(25.4,144.4)
		self.cell(w=159.2, h=6, align='L', txt='Openness:', border=0)
		self.set_xy(25.4,150.4)
		self.set_font('Arial', '', 12)
		self.multi_cell(w=159.2, h=6, align='L', txt="Your score for openness: "+str(open_score), border=0)
		self.set_xy(25.4,156.4)
		self.multi_cell(w=159.2, h=6, align='L', txt="Your percentile among students for openness: "+str(open_percent), border=0)


# Now loop through each student. Generate the plots, then generate the PDF, then remove the plots


for person in scores:
	# First make the plots
	plt.rcParams['figure.figsize'] = (14, 8)
	# Extraversion
	sns.distplot(extra_scores, hist = True, bins=26, kde = True, kde_kws = {'linewidth': 1}, label = 'Extraversion Scores', color='b')
	plt.axvline(x=person['extra_score'], color='red')
	plt.xlabel("Extraversion Score")
	plt.xlim([1,5])
	plt.savefig(tmp_directory+'/'+person['name']+' Extraversion.png')
	plt.clf()

	# Agreeableness
	sns.distplot(agree_scores, hist = True, bins=26, kde = True, kde_kws = {'linewidth': 1}, label = 'Agreeableness Scores', color='b')
	plt.axvline(x=person['agree_score'], color='red')
	plt.xlabel("Agreeableness Score")
	plt.xlim([1,5])
	plt.savefig(tmp_directory+'/'+person['name']+' Agreeableness.png')
	plt.clf()

	# Conscientiousness
	sns.distplot(consc_scores, hist = True, bins=26, kde = True, kde_kws = {'linewidth': 1}, label = 'Conscientiousness Scores', color='b')
	plt.axvline(x=person['consc_score'], color='red')
	plt.xlabel("Conscientiousness Score")
	plt.xlim([1,5])
	plt.savefig(tmp_directory+'/'+person['name']+' Conscientiousness.png')
	plt.clf()

	# Neuroticism
	sns.distplot(neuro_scores, hist = True, bins=26, kde = True, kde_kws = {'linewidth': 1}, label = 'Neuroticism Scores', color='b')
	plt.axvline(x=person['neuro_score'], color='red')
	plt.xlabel("Neuroticism Score")
	plt.xlim([1,5])
	plt.savefig(tmp_directory+'/'+person['name']+' Neuroticism.png')
	plt.clf()

	# Openness
	sns.distplot(open_scores, hist = True, bins=26, kde = True, kde_kws = {'linewidth': 1}, label = 'Openness Scores', color='b')
	plt.axvline(x=person['open_score'], color='red')
	plt.xlabel("Openness Score")
	plt.xlim([1,5])
	plt.savefig(tmp_directory+'/'+person['name']+' Openness.png')
	plt.clf()

	print("Created individual figures for "+person['name'])
	# Now make a PDF that includes these
	pdf = PDF(orientation='P', unit='mm', format='Letter')#pdf object
	# page 1
	pdf.add_page()
	pdf.opening_paragraph(person['name'])
	pdf.extraversion(person['extra_score'], person['extra_percent'], person['name'])
	# page 2
	pdf.add_page()
	pdf.agreeableness(person['agree_score'], person['agree_percent'], person['name'])
	pdf.conscientiousness(person['consc_score'], person['consc_percent'], person['name'])
	# page 3
	pdf.add_page()
	pdf.neuroticism(person['neuro_score'], person['neuro_percent'], person['name'])
	pdf.openness(person['open_score'], person['open_percent'], person['name'])

	pdf.output(output_directory+'/'+person['name']+' BFI Report.pdf','F')
	print("Created PDF for "+person['name'])

	# Now remove the individual plots
	os.remove(tmp_directory+'/'+person['name']+' Extraversion.png')
	os.remove(tmp_directory+'/'+person['name']+' Agreeableness.png')
	os.remove(tmp_directory+'/'+person['name']+' Conscientiousness.png')
	os.remove(tmp_directory+'/'+person['name']+' Neuroticism.png')
	os.remove(tmp_directory+'/'+person['name']+' Openness.png')

# Now I can get rid of the tmp folder
os.rmdir(tmp_directory)
print("Done!")
