import sublime, sublime_plugin
import os
import sys

current_working_directory = os.getcwd() 																#current working directory 
sys.path.append("/home/vac/.config/sublime-text-3/Packages/User" + "/lib/python3.4/site-packages")		#Tells sublime python interpreter where modules are store

from git import *	

#settings = sublime.load_settings("ProperCheckRepo.sublime-settings")

class myOpener(sublime_plugin.EventListener):		
	global file_push_counter
	file_push_counter = {}
	
	def on_post_save(self,view):

		temp_dir = str(view.file_name())

		if temp_dir in file_push_counter :
			file_push_counter[temp_dir] += 1
		else :
			file_push_counter[temp_dir] = 1


		def repo_check(temp_dir):															#code checks for .git in the folder	
			global repo
			repo = Repo(temp_dir,search_parent_directories=True)
			repo_commit()
			

		def repo_commit():
			sublime.message_dialog("on_post_save")
			sublime.message_dialog(str(repo.git.status()))
			#sublime.message_dialog("You have saved the file")

			sublime.message_dialog(str(repo.git.add( '--all' )))
			sublime.message_dialog(str(repo.git.commit( m='committed all' )))

			#sublime.message_dialog("and now it has been committed")
			sublime.message_dialog(str(repo.git.status()))

		def repo_push():
				forwd_slash_index = temp_dir.rfind('/', 0, len(temp_dir))   				#finds index of last forward slash
				new_dir = temp_dir[0:forwd_slash_index]
				repo = Repo(new_dir)
				o = repo.remotes.origin
				o.pull()	
				o.push()
				sublime.message_dialog("repository pushed")	

		repo_check(temp_dir)																#function call to repo_check
		
		if file_push_counter[temp_dir] == 3 :
			file_push_counter[temp_dir] = 0
			repo_push()																			#function call to repo_push