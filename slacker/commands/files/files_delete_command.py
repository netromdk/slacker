from slacker.commands.command import Command
from slacker.commands.argument_parser import ArgumentParser
from slacker.utility import ts_add_days
from humanfriendly import format_size
from prompt_toolkit.shortcuts import confirm

class FilesDeleteCommand(Command):
  def name(self):
    return "files.delete"

  def description(self):
    return "Delete files uploaded to and stored on Slack."

  def requires_token(self):
    return True

  def is_destructive(self):
    return True

  def make_parser(self):
    file_types = ["all", "spaces", "snippets", "images", "gdocs", "zips", "pdfs"]
    parser = ArgumentParser(prog = self.name(), description = self.description(),
                            epilog = "NOTE: It is recommended to first use --dry-run to see what "
                                     "will be deleted!")
    parser.add_argument("-n", "--dry-run", action = "store_true",
                        help = "Don't actually delete any files but show which ones would have "
                               "been deleted.")
    parser.add_argument("-t", "--types", nargs = "*", type = str, metavar = "TYPE",
                        choices = file_types, default = "all",
                        help = "Delete files by types (defaults to 'all'). All possible values "
                               "are: {}. Specify multiple like '-t images gdocs'."
                               .format(file_types))
    parser.add_argument("--days-old", type = int, metavar = "DAYS",
                        help = "Delete files with an age in days less than or equal to input "
                               "amount.")
    parser.add_argument("--older-than", type = int, metavar = "DAYS",
                        help = "Delete files that are older than input amount of days.")
    return parser

  def action(self, args = None):
    # If no actual arguments are given (only defaults) then ask to proceed deleting all files.
    if not args.dry_run and args.days_old is None and args.older_than is None:
      if not confirm("Are you sure you want to delete all files? "):
        self.logger.info("Aborting..")
        return

    total_size = 0
    count = 100
    page = 1

    file_types = args.types
    if type(file_types) != type(str):
      file_types = ",".join(args.types)

    older_than = "now"
    if args.older_than:
      older_than = ts_add_days(-1 * args.older_than)
    newer_than = 0
    if args.days_old:
      newer_than = ts_add_days(-1 * args.days_old)

    # Files to delete.
    gathered_files = []

    self.logger.info("Gathering files to delete..")
    while True:
      # Get next page of files.
      data = self.slack_api_post("files.list",
                                   {"count": count,
                                    "page": page,
                                    "types": file_types,
                                    "ts_from": newer_than,
                                    "ts_to": older_than})

      files = data["files"]
      if len(files) == 0:
        break
      for f in files:
        total_size += f["size"]
        gathered_files.append(f)
        self.logger.info("  {:<50} {:>10}".format(f["name"], format_size(f["size"], binary = True)))

      paging = data["paging"]
      if paging["pages"] == page:
        break
      page += 1

    if len(gathered_files) == 0:
      self.logger.info("Nothing to do.")
      return

    self.logger.info("Gathered {} files, {}".format(len(gathered_files),
                                                    format_size(total_size, binary = True)))

    if args.dry_run:
      self.logger.info("Dry run: Not deleting any files!")
      return

    for file in gathered_files:
      self.logger.info("Deleting: {} ({})".format(file["name"], file["id"]))
      self.slack_api_post("files.delete", {"file": file["id"]})

    self.logger.info("Deleted {} files, {}".format(len(gathered_files),
                                                   format_size(total_size, binary = True)))
