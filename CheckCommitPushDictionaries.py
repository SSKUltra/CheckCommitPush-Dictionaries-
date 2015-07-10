import sublime, sublime_plugin
import os
import sys

if sublime.platform() == 'Linux' :
	current_working_directory = os.getcwd() 											#current working directory for linux platform
	sys.path.append(current_working_directory + "/lib/python3.4/site-packages")			#Tells sublime python interpreter where modules are store

from git import *																		#import git into sublime plugin

settings = sublime.load_settings("CheckCommitPushDictionaries.sublime-settings")		#Setting preferences

class myOpener(sublime_plugin.EventListener):											
	
	global file_push_counter															#dictionary defination. Empty dictionary.
	file_push_counter = {}
	
	def on_post_save(self,view):														#on_post_save is called when a file is saved

		sublime.message_dialog("on_post_save")

		file_dir = str(view.file_name())												#file_dir contains the file location

		if file_dir in file_push_counter :												#check if file is in the dictionary, 
			file_push_counter[file_dir] += 1											#increments or adds accordingly
		else :
			file_push_counter[file_dir] = 1


		def repo_check(file_dir):														#code checks for .git in the folder and calls commit
			global repo 																#OR an exception is called
			repo = Repo(file_dir,search_parent_directories=True)
			repo_commit()
			

		def repo_commit():																#function adds and commits the file
			
			sublime.message_dialog("Git Status : \n" + str(repo.git.status()))			#Git status

			sublime.message_dialog("File Added" + str(repo.git.add( file_dir )))		#Git add
			sublime.message_dialog("Commit the file : \n" + str(repo.git.commit( m='committed all' ))) 		#Git commit

			#sublime.message_dialog("and now it has been committed")
			sublime.message_dialog("Git Status : \n" + str(repo.git.status()))			#Git statuss

		def repo_push():
				forwd_slash_index = file_dir.rfind('/', 0, len(file_dir))   			#finds index of last forward slash
				new_dir = file_dir[0:forwd_slash_index]									#new_dir stores the directory of the file folder
				repo = Repo(new_dir)													#Represents a valid git repository
				o = repo.remotes.origin													#repo remote is stored in variable 'o'
				o.pull()																#pulls the repo from origin master
				o.push()																#pushes the repo to origin master
				sublime.message_dialog("Repository pushed")	


		repo_check(file_dir)															#function call to repo_check
		
		if file_push_counter[file_dir] == settings.get("X_SAVES_Push") :				#checks directory for value equal to preferences
			file_push_counter[file_dir] = 0												#sets the value back to zero
			repo_push()																	#function call to repo_push