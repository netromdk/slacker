from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.utility import ts_add_days
from slacker.environment.config import Config
from humanfriendly import format_size

class FilesListCommand(Command):
  def name(self):
    return "files.list"

  def description(self):
    return "Displays info about files on Slack."

  def requires_token(self):
    return True

  def is_destructive(self):
    return False

  def make_parser(self):
    file_types = ['all', 'spaces', 'snippets', 'images', 'gdocs', 'zips', 'pdfs']
    parser = ArgumentParser(prog = self.name(), description = self.description())
    parser.add_argument("-a", "--all", action = "store_true",
                        help = "Return all files. This will disregard --page but still respects "
                               "filtering.")
    parser.add_argument("-c", "--count", type = int, choices = range(1, 500), default = 100,
                        metavar = 'COUNT',
                        help = "Number of items to return per page between 1 and 500 "
                               "(defaults to 100).")
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
    parser.add_argument('--total-size', action = 'store_true',
                        help = 'Compute total file size and don\'t print file names. Implies '
                               '--all and disregards filtering. Disables --download.')
    parser.add_argument('-u', '--user', type = str,
                        help = "Filter for files uploaded by a specific user.")
    parser.add_argument('-d', '--download', type = str, metavar = 'DIR',
                        help = 'Download filtered files to a specific folder. Disables '
                               '--total-size.')
    return parser

  def action(self, args = None):
    if args.total_size and args.download:
      self.logger.error('Cannot specify --total-size and --download at the same time!')
      return

    if not args.total_size:
      self.logger.info("Listing files..")
    else:
      args.all = True

    file_types = args.types
    if type(file_types) != type(str):
      file_types = ",".join(args.types)
    totalFiles = 0
    totalSize = 0
    page = args.page if not args.all else 1
    older_than = 'now'
    if args.older_than and not args.total_size:
      older_than = ts_add_days(-1 * args.older_than)
    newer_than = 0
    if args.days_old and not args.total_size:
      newer_than = ts_add_days(-1 * args.days_old)

    # Create folder to download to if it doesn't exist already.
    if args.download:
      self.logger.info('Files will be downloaded to {}'.format(args.download))

    while True:
      # Get next page of files.
      data = self.slack_api_post('files.list',
                                 {"types": file_types,
                                  "count": args.count,
                                  "page": page,
                                  "ts_from": newer_than,
                                  "ts_to": older_than,
                                  'user': args.user})

      files = data["files"]
      if len(files) == 0:
        break
      for f in files:
        if not args.total_size:
          self.logger.info('  {:<50} {:>10}'.format(f['name'],
                                                    format_size(f['size'], binary = True)))
        totalFiles += 1
        totalSize += f['size']
        if args.download:
          slack_api.download_file(f['id'], args.download)

      # Stop when reaching the last page if args.all is set.
      if args.all:
        paging = data["paging"]
        if paging["pages"] == page:
          break
        page += 1
      else: break

    self.logger.info("{} files, {}".format(totalFiles, format_size(totalSize, binary = True)))
