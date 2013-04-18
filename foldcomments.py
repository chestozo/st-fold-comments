import sublime, sublime_plugin, re

def region_fix(self, region):
    if self.view.substr(sublime.Region(region.b - 2, region.b)) == '*/':
        return region
    else:
        return sublime.Region(region.a, region.b - 1)

# class FoldFileComments(sublime_plugin.EventListener):
#     def on_load(self, view):
#         view.fold(view.find_by_selector('comment'))

class FoldCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
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
        # print regions

        self.view.fold(regions)

# class UnfoldCommentsCommand(sublime_plugin.TextCommand):
#     def run(self, edit):
#         self.view.unfold(
#             map(
#                 (lambda x: sublime.Region(x.a, x.b - (0 if self.view.substr(sublime.Region(x.b - 2, x.b)) == '*/' else 1))),
#                 self.view.find_by_selector('comment')
#             )
#         )
