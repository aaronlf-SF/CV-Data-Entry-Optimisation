import re
import colorama
colorama.init()

from skills import skills


#======================================================================


def find_word_in_string(text,keyword):
	'''
	Given a keyword, this fucntion returns the starting 
	and ending indices of this keyword within a given text string
	'''
	occurrences = []
	for m in re.finditer(keyword, text.casefold()):
         occurrences.append([m.start(),m.end()])
	return occurrences
	
	
	
	
def print_with_highlights(text,indices):#sentence_dict):
	'''
	This prints the sentence with the keyword(s) highlighted cyan.
	'''
	#text = sentence_dict['text']
	#indices = sentence_dict['indices']
	normalTextStart = 0
	
	for array in indices:	
		print(text[normalTextStart:array[0]],end='') #printing normal text
		print('\x1b[1;36;40m' + text[array[0]:array[1]] + '\x1b[0m',end='') #printing highlighted text
		normalTextStart = array[1]
		if array == indices[-1]: # last highlighted word
			print(text[normalTextStart:])
		
		
		
			
def sentence_finder(text,indices):

	beginIndex = indices[0]
	endIndex = indices[1]
	keyword = text[beginIndex:endIndex]
	
	while beginIndex > 0:
		if text[beginIndex] == '.' and text[beginIndex + 1] == ' ':
			beginIndex += 2
			break
		elif text[beginIndex] == '\n':
			beginIndex += 1
			break
		else:
			beginIndex -= 1
			
	while endIndex < len(text):
		if text[endIndex] == ' ' and text[endIndex - 1] == '.':
			break
		elif text[endIndex] == '\n':
			break
		else:
			endIndex += 1
			
	sentence = text[beginIndex:endIndex]
	#new_indices = find_word_in_string(sentence_text,keyword)
	
	return sentence #{'text': sentence_text, 'indices': new_indices} #SHOULD THIS RETURN KEYWORD INSTEAD OF INDICES? ...OR NONE AT ALL??
	

#======================================================================


text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text \
ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only \
five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the \
release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."



def display_sentences_for_skill(text,skill,name_of_skill,toPrintBroadSkill): #skill variable is simply a list of the keywords 
	
	sentences = []
	skill_occurrence_count = 0
	
	for keyword in skill: 
		occurrences = find_word_in_string(text,keyword)
		skill_occurrence_count += len(occurrences)
		
		for occurrence in occurrences:
			sentence = sentence_finder(text,occurrence)
			if sentence not in sentences:
				sentences.append(sentence)
				
	if skill_occurrence_count > 0:
		if toPrintBroadSkill[0] == True:
			print('\n\n\n\x1b[1;33;40m' + '~~~ '+ toPrintBroadSkill[1] + ' ~~~' + '\x1b[0m')
		print('\n\x1b[1;32;40m' + name_of_skill.upper() + ' - NUMBER OF OCCURRENCES: ' + str(skill_occurrence_count) + '\x1b[0m') #GREEN OUTPUT
	for sentence in sentences:
	
		highlight_indices = []	
		for keyword in skill:
			for index_array in find_word_in_string(sentence,keyword):
				highlight_indices.append(index_array)
		print('   ',end='')
		print_with_highlights(sentence,highlight_indices)
	return skill_occurrence_count
	
	



def process_text_and_print_results(text):
	listToPrint = []
	for broadSkill in skills:
		toPrintBroadSkill = [True,broadSkill]
		
		# broad skill keywords
		broad_occurrence_count = display_sentences_for_skill(text,skills[broadSkill]['broadKeyWords'],broadSkill,toPrintBroadSkill)
		if broad_occurrence_count > 0: #If there are keywords in specific skills but not necessarily any broad keywords
			broad_occurrence_count = display_sentences_for_skill(text,skills[broadSkill]['broadKeyWords'],broadSkill)
			listToPrint.append({'skill_name':broadSkill,'occurrences':broad_occurrence_count,'broad':True})
			toPrintBroadSkill[0] = False
		
		#specific skill keywords
		for specificSkill in skills[broadSkill]['specificSkills']:
			specific_occurrence_count = display_sentences_for_skill(text,skills[broadSkill]['specificSkills'][specificSkill],specificSkill,toPrintBroadSkill)
			if specific_occurrence_count > 0:
			
				if broad_occurrence_count == 0:
					listToPrint.append({'skill_name':broadSkill,'occurrences':'','broad':True})
					broad_occurrence_count += 1 #this ensures the broad skill won't be printed many times
					
				listToPrint.append({'skill_name':specificSkill,'occurrences':specific_occurrence_count,'broad':False})
				toPrintBroadSkill[0] = False
		
	
	print('\n\n\n\n--------------------------------------------------------------------------------\n\n' + 'POSSIBLE SKILLS FOUND: \n')
	
	for item in listToPrint:
		if item['broad'] == True:
			firstChar = '\n '
		else:
			firstChar = '    '
		print('\x1b[1;37;40m' + firstChar + item['skill_name'] + ' (' + str(item['occurrences']) + ')' + '\x1b[0m') #BRIGHT WHITE OUTPUT
		
	if len(listToPrint) == 0:
		print('\x1b[1;31;40m' + "No relevant keywords found!" + '\x1b[0m') #RED OUTPUT
		
		
def main():
	text = input('Paste text below:\n\n')
	print('\n\n--------------------------------------------------------------------------------')
	process_text_and_print_results(text)
	print('\n\n\n\n\n')

	
if __name__ == '__main__':
	main()
