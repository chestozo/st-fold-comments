import sublime, sublime_plugin, re

def region_fix(self, region):
    if self.view.substr(sublime.Region(region.b - 2, region.b)) == '*/':
        return region
    else:
        return sublime.Region(region.a, region.b - 1)

def fold_comments(self):
    comments = self.view.find_by_selector('comment')
    comments.reverse()
    comments_reversed = comments

    # Current region:
    # we try to group neighbours
    cur_region = comments_reversed[0]

    # Regions to fold
    regions = []

    # going backword like so: [(100,120), (80,90)]
    for i, region in enumerate(comments_reversed):
        if i == 0:
            # skip first one
            continue

        # get string in between two comments
        str = self.view.substr(sublime.Region(region.b, cur_region.a))
        if re.match(r"^(\s|\n)*$", str):
            # join this two
            cur_region = sublime.Region(region.a, cur_region.b)
        else:
            # add current as region
            regions.append(region_fix(self, cur_region))
            # and continue with the one
            cur_region = region

    # do not forget about the current
    regions.append(region_fix(self, cur_region))

    self.view.fold(regions)

def unfold_comments(self):
    self.view.unfold(self.view.find_by_selector('comment'))

def remove_comments(self, edit):
    comments = self.view.find_by_selector('comment')
    comments.reverse()

    for c in comments:
        self.view.erase(edit, c)

class FoldCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fold_comments(self)

class UnfoldCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        unfold_comments(self)

class RemoveCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        remove_comments(self, edit)
