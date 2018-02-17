# Whitelist of symbols that are in use and shouldn't be reported by Vulture.

from vulture.whitelists.whitelist_utils import Whitelist

wl = Whitelist()
wl.Registrar
wl.Registrar.commands
wl.Registrar.names

# Commands
wl.ApiTestCommand
wl.AuthTestCommand
wl.ChannelsInviteCommand
wl.ChannelsListCommand
wl.ChatMeMessageCommand
wl.ChatPostEphemeralCommand
wl.ChatPostMessageCommand
wl.Command
wl.ConfigCommand
wl.EmojiListCommand
wl.ExitCommand
wl.FilesDeleteCommand
wl.FilesListCommand
wl.LogCommand
wl.UsersListCommand
wl.WorkspaceCommand
