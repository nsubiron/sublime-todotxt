import sublime, sublime_plugin

class IterateTodoCommand(sublime_plugin.TextCommand):
    def run(
          self,
          edit,
          iterlist=['x ', '(A) ', '(B) ', '(C) '],
          reverse=False,
          on_indent=True):
        """Replace the line's begin by the next value on ``iterlist``.
          * ``reverse`` Iterate ``iterlist`` on reversed order
          * ``on_indent`` Keep indentation. This will indent line in order to
            fit the next value on ``iterlist``"""
        if reverse:
          iterlist = list(reversed(iterlist))
        iterlist = iterlist + ['']
        for region in self.view.sel():
          line = self.view.line(region)
          data = self.view.substr(line)
          for i, value in enumerate(iterlist):
            if data.startswith(value):
              self.view.erase(edit, sublime.Region(line.begin(), line.begin() + len(value)))
              break
          next = iterlist[(i+1)%len(iterlist)]
          if on_indent:
            indent = len(self.view.substr(line)) - len(self.view.substr(line).lstrip(' '))
            next = next.ljust(len(value) + indent)
            self.view.erase(edit, sublime.Region(line.begin(), line.begin() + indent))
          self.view.insert(edit, line.begin(), next)
