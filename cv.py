import re

import colorama
colorama.init()

import textwrap

from skills import skills


#======================================================================

'''
main() defined, line 31

get_user_input() defined, line 43

find_word_in_string() defined, line 61
sentence_finder() defined, line 72
print_with_highlights() defined, line 101

display_sentences_for_skill() defined, line 119

process_text_and_print_results() defined, line 154
'''

#======================================================================



def main():
	text = get_user_input()
	print('\n\n----------------------------------------------------------------------',end='')
	process_text_and_print_results(text)
	print('\n\n')



#======================================================================



def get_user_input():
	input1 = input('Paste text below:\n\n')
	inputs = [input1]
	while True:
		try:
			input1 = input()
			inputs.append(input1)
		except EOFError:
			break
	text = '\n'.join(inputs)
	return text
	
	

#======================================================================



def find_word_in_string(text,keyword):
	'''
	Given a keyword, this function returns the starting 
	and ending indices of this keyword within a given text string
	'''
	occurrences = []
	print(re.escape(keyword))
	for m in re.finditer(re.escape(keyword), text.casefold()):
         occurrences.append([m.start(),m.end()])
	return occurrences
	

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
	
	return sentence

	
def print_with_highlights(text,indices):
	'''
	This prints the sentence with the keyword(s) highlighted cyan.
	'''
	wrapper = textwrap.TextWrapper(width=65,initial_indent=' - ',subsequent_indent='   ')
	wrapped_text = '\n' + wrapper.fill(text) 
	
	new_indices = []
	for arr in indices:
		word = text[arr[0]:arr[1]].casefold()
		new_arr = find_word_in_string(wrapped_text,word)
		for x in new_arr:
			new_indices.append(x)
	new_indices = [i for n,i in enumerate(new_indices) if i not in new_indices[:n]]
	new_indices.sort(key = lambda x: x[1])
	
	normalTextStart = 0
	for array in new_indices:	
		print(wrapped_text[normalTextStart:array[0]],end='') #printing normal text
		print('\x1b[1;36;40m' + wrapped_text[array[0]:array[1]] + '\x1b[0m',end='') #printing highlighted text
		normalTextStart = array[1]
		if array == new_indices[-1]: # last highlighted word
			print(wrapped_text[normalTextStart:])

					
	
	
#======================================================================


def display_sentences_for_skill(text,skill,name_of_skill,toPrintBroadSkill,skillType): #skill variable is simply a list of the keywords 
	
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
			print('\n\n\n\n\n\x1b[1;33;40m' + ('~~~~~~~~~  '+ toPrintBroadSkill[1] + '  ~~~~~~~~~').center(70) + '\x1b[0m') #YELLOW OUTPUT
		if skillType == 'specific':
			print('\n\n\x1b[1;32;40m' + ' ' + name_of_skill.upper() + ' - NUMBER OF OCCURRENCES: ' + str(skill_occurrence_count) + '\x1b[0m',end='') #GREEN OUTPUT
		elif skillType == 'broad':
			print('\n\n\x1b[1;33;40m' + ' ' + name_of_skill.upper() + ' - NUMBER OF OCCURRENCES: ' + str(skill_occurrence_count) + '\x1b[0m',end='' ) #YELLOW OUTPUT
	
	for sentence in sentences:
	
		highlight_indices = []	
		for keyword in skill:
			for index_array in find_word_in_string(sentence,keyword):
				highlight_indices.append(index_array)
		print('   ',end='')
		print_with_highlights(sentence,highlight_indices)
	return skill_occurrence_count
	


#======================================================================



def process_text_and_print_results(text):
	listToPrint = []
	for broadSkill in skills:
		toPrintBroadSkill = [True,broadSkill]
		
		# broad skill keywords
		broad_occurrence_count = display_sentences_for_skill(text,skills[broadSkill]['broadKeyWords'],broadSkill,toPrintBroadSkill,'broad')
		if broad_occurrence_count > 0: #If there are keywords in specific skills but not necessarily any broad keywords
			listToPrint.append({'skill_name':broadSkill,'occurrences':broad_occurrence_count,'broad':True})
			toPrintBroadSkill[0] = False
		
		#specific skill keywords
		for specificSkill in skills[broadSkill]['specificSkills']:
			specific_occurrence_count = display_sentences_for_skill(text,skills[broadSkill]['specificSkills'][specificSkill],specificSkill,toPrintBroadSkill,'specific')
			if specific_occurrence_count > 0:
			
				if broad_occurrence_count == 0:
					listToPrint.append({'skill_name':broadSkill,'occurrences':'','broad':True})
					broad_occurrence_count += 1 #this ensures the broad skill won't be printed many times
					
				listToPrint.append({'skill_name':specificSkill,'occurrences':specific_occurrence_count,'broad':False})
				toPrintBroadSkill[0] = False
		
	
	print('\n\n\n\n----------------------------------------------------------------------'+'\n\n\n'+'POSSIBLE SKILLS FOUND: \n')
	
	for item in listToPrint:
		if item['broad'] == True:
			firstChar = '\n  '
		else:
			firstChar = '    '
		print('\x1b[1;37;40m' + firstChar + item['skill_name'] + ' (' + str(item['occurrences']) + ')' + '\x1b[0m') #BRIGHT WHITE OUTPUT
		
	if len(listToPrint) == 0:
		print('\x1b[1;31;40m' + "No relevant keywords found!" + '\x1b[0m') #RED OUTPUT
		

		
#======================================================================



if __name__ == '__main__':
	main()

	
	
#======================================================================