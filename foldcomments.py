import sublime, sublime_plugin

class FoldFileComments(sublime_plugin.EventListener):
    def on_load(self, view):
        view.fold(view.find_by_selector('comment'))

class FoldCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.fold(self.view.find_by_selector('comment'))

class UnfoldCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.find_by_selector('comment'):
            self.view.unfold(region)
