import sublime, sublime_plugin

class FoldFileComments(sublime_plugin.EventListener):
    def on_load(self, view):
        view.fold(view.find_by_selector('comment'))

class FoldCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.fold(
            map(
                (lambda x: sublime.Region(x.a, x.b - (0 if self.view.substr(sublime.Region(x.b - 2, x.b)) == '*/' else 1))),
                self.view.find_by_selector('comment')
            )
        )

class UnfoldCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.unfold(
            map(
                (lambda x: sublime.Region(x.a, x.b - (0 if self.view.substr(sublime.Region(x.b - 2, x.b)) == '*/' else 1))),
                self.view.find_by_selector('comment')
            )
        )
