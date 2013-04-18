import sublime, sublime_plugin, re

def comment_region(self, region):
    if self.view.substr(sublime.Region(region.b - 2, region.b)) == '*/':
        return region
    else:
        return sublime.Region(region.a, region.b - 1)

class FoldFileComments(sublime_plugin.EventListener):
    def on_load(self, view):
        view.fold(view.find_by_selector('comment'))

class FoldCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        comments = self.view.find_by_selector('comment')
        comments.reverse()
        comments_reversed = comments

        # Regions to fold
        regions = []

        for region in comments_reversed:
            regions.append(region)
        self.view.fold(regions)

class UnfoldCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.unfold(
            map(
                (lambda x: sublime.Region(x.a, x.b - (0 if self.view.substr(sublime.Region(x.b - 2, x.b)) == '*/' else 1))),
                self.view.find_by_selector('comment')
            )
        )
