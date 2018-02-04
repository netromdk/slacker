from .command import Command
from slacker.commands.argument_parser import ArgumentParser
from humanfriendly import format_size
from slacker.utility import ts_add_days
from slacker.slack_api import SlackAPI

class FilesListCommand(Command):
  def name(self):
    return "files.list"

  def description(self):
    return "Displays info about files on Slack."

  def aliases(self):
    return ["files"]

  def make_parser(self):
    file_types = ['all', 'spaces', 'snippets', 'images', 'gdocs', 'zips', 'pdfs']
    parser = ArgumentParser(prog = self.name(), description = self.description())
    parser.add_argument("-a", "--all", action = "store_true",
                        help = "Return all files. This will disregard --page but still respects "
                               "filtering.")
    parser.add_argument("-c", "--count", type = int, default = 100,
                        help = "Number of items to return per page (defaults to 100).")
    parser.add_argument("-p", "--page", type = int, default = 1,
                        help = "Page number of results to return (defaults to 1).")
    parser.add_argument("-t", "--types", nargs = '*', type = str, metavar = "TYPE",
                        choices = file_types, default = 'all',
                        help = "Filter files by types (defaults to 'all'). All possible values "
                               "are: {}. Specify multiple like '-t images gdocs'."
                               .format(file_types))
    parser.add_argument("--days-old", type = int, metavar = "DAYS",
                        help = "Show only files with an age in days less than or equal to input "
                               "amount.")
    parser.add_argument("--older-than", type = int, metavar = "DAYS",
                        help = "Show only files that are older than input amount of days.")
    return parser

  def action(self, args = None):
    print("Listing files..")
    file_types = args.types
    if type(file_types) != type(str):
      file_types = ",".join(args.types)
    totalFiles = 0
    totalSize = 0
    page = args.page if not args.all else 1
    older_than = 'now'
    if args.older_than:
      older_than = ts_add_days(-1 * args.older_than)
    newer_than = 0
    if args.days_old:
      newer_than = ts_add_days(-1 * args.days_old)

    slack_api = SlackAPI()
    while True:
      # Get next page of files.
      data = slack_api.post('files.list',
                            {"types": file_types,
                             "count": args.count,
                             "page": page,
                             "ts_from": newer_than,
                             "ts_to": older_than})
      if "error" in data:
        print("Error: {}".format(data["error"]))
        return

      files = data["files"]
      if len(files) == 0:
        break
      for f in files:
        print("  {:<50} {:>10}".format(f["name"], format_size(f["size"], binary = True)))
        totalFiles += 1
        totalSize += f["size"]

      # Stop when reaching the last page if args.all is set.
      if args.all:
        paging = data["paging"]
        if paging["pages"] == page:
          break
        page += 1
      else: break

    print("{} files, {}".format(totalFiles, format_size(totalSize, binary = True)))
