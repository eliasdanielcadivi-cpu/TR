# Control kitty from scripts

*kitty* can be controlled from scripts or the shell prompt. You can open new windows, send arbitrary text input to any window, change the title of windows and tabs, etc.

Let’s walk through a few examples of controlling *kitty*.

# Tutorial

Start by running *kitty* as:

kitty -o allow_remote_control=yes -o enabled_layouts=tall

In order for control to work, [`allow_remote_control`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.allow_remote_control) or [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password) must be enabled in `kitty.conf`. Here we turn it on explicitly at the command line.

Now, in the new *kitty* window, enter the command:

kitten @ launch --title Output --keep-focus cat

This will open a new window, running the **cat** program that will appear next to the current window.

Let’s send some text to this new window:

kitten @ send-text --match cmdline:cat Hello, World

This will make `Hello, World` show up in the window running the **cat** program. The [`kitten @ send-text --match`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-send-text-match) option is very powerful, it allows selecting windows by their titles, the command line of the program running in the window, the working directory of the program running in the window, etc. See [kitten @ send-text --help](https://sw.kovidgoyal.net/kitty/remote-control/#at-send-text) for details.

More usefully, you can pipe the output of a command running in one window to another window, for example:

ls | kitten @ send-text --match 'title:^Output' --stdin

This will show the output of **ls** in the output window instead of the current window. You can use this technique to, for example, show the output of running **make** in your editor in a different window. The possibilities are endless.

You can even have things you type show up in a different window. Run:

kitten @ send-text --match 'title:^Output' --stdin

And type some text, it will show up in the output window, instead of the current window. Type Ctrl+D when you are ready to stop.

Now, let’s open a new tab:

kitten @ launch --type=tab --tab-title "My Tab" --keep-focus bash

This will open a new tab running the bash shell with the title “My Tab”. We can change the title of the tab to “New Title” with:

kitten @ set-tab-title --match 'title:^My' New Title

Let’s change the title of the current tab:

kitten @ set-tab-title Master Tab

Now lets switch to the newly opened tab:

kitten @ focus-tab --match 'title:^New'

Similarly, to focus the previously opened output window (which will also switch back to the old tab, automatically):

kitten @ focus-window --match 'title:^Output'

You can get a listing of available tabs and windows, by running:

kitten @ ls

This outputs a tree of data in JSON format. The top level of the tree is all [OS windows](https://sw.kovidgoyal.net/kitty/glossary/#term-os_window). Each OS window has an id and a list of [tabs](https://sw.kovidgoyal.net/kitty/glossary/#term-tab). Each tab has its own id, a title and a list of [kitty windows](https://sw.kovidgoyal.net/kitty/glossary/#term-window). Each window has an id, title, current working directory, process id (PID) and command-line of the process running in the window. You can use this information with [`kitten @ focus-window --match`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-focus-window-match) to control individual windows.

As you can see, it is very easy to control *kitty* using the `kitten @` messaging system. This tutorial touches only the surface of what is possible. See `kitten @ --help` for more details.

In the example’s above, `kitten @` messaging works only when run inside a *kitty* window, not anywhere. But, within a *kitty* window it even works over SSH. If you want to control *kitty* from programs/scripts not running inside a *kitty* window, see the section on [using a socket for remote control](https://sw.kovidgoyal.net/kitty/remote-control/#rc-via-socket) below.

Note that if all you want to do is run a single *kitty* “daemon” and have subsequent *kitty* invocations appear as new top-level windows, you can use the simpler [`kitty --single-instance`](https://sw.kovidgoyal.net/kitty/invocation/#cmdoption-kitty-single-instance) option, see `kitty --help` for that.

# Remote control via a socket

To control kitty from outside kitty, it is necessary to setup a socket to communicate with kitty. First, start *kitty* as:

kitty -o allow_remote_control=yes --listen-on unix:/tmp/mykitty

The [`kitty --listen-on`](https://sw.kovidgoyal.net/kitty/invocation/#cmdoption-kitty-listen-on) option tells *kitty* to listen for control messages at the specified UNIX-domain socket. See `kitty --help` for details. Now you can control this instance of *kitty* using the [`kitten @ --to`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-to) command line argument to `kitten @`. For example:

kitten @ --to unix:/tmp/mykitty ls

# The builtin kitty shell

You can explore the *kitty* command language more easily using the builtin *kitty* shell. Run `kitten @` with no arguments and you will be dropped into the *kitty* shell with completion for *kitty* command names and options.

You can even open the *kitty* shell inside a running *kitty* using a simple keyboard shortcut ([`ctrl+shift+escape`](https://sw.kovidgoyal.net/kitty/conf/#shortcut-kitty.Open-the-kitty-command-shell) by default).

Note

Using the keyboard shortcut has the added advantage that you don’t need to use [`allow_remote_control`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.allow_remote_control) to make it work.

# Allowing only some windows to control kitty

If you do not want to allow all programs running in *kitty* to control it, you can selectively enable remote control for only some *kitty* windows. Simply create a shortcut such as:

map ctrl+k launch --allow-remote-control some_program

Then programs running in windows created with that shortcut can use `kitten @` to control kitty. Note that any program with the right level of permissions can still write to the pipes of any other program on the same computer and therefore can control *kitty*. It can, however, be useful to block programs running on other computers (for example, over SSH) or as other users.

Note

You don’t need [`allow_remote_control`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.allow_remote_control) to make this work as it is limited to only programs running in that specific window. Be careful with what programs you run in such windows, since they can effectively control kitty, as if you were running with [`allow_remote_control`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.allow_remote_control) turned on.

> You can further restrict what is allowed in these windows by using [`kitten @ launch --remote-control-password`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-remote-control-password).

# Fine grained permissions for remote control

Added in version 0.26.0.

The [`allow_remote_control`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.allow_remote_control) option discussed so far is a blunt instrument, granting the ability to any program running on your computer or even on remote computers via SSH the ability to use remote control.

You can instead define remote control passwords that can be used to grant different levels of control to different places. You can even write your own script to decide which remote control requests are allowed. This is done using the [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password) option in `kitty.conf`. Set [`allow_remote_control`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.allow_remote_control) to `password` to use this feature. Let’s see some examples:

remote_control_password "control colors" get-colors set-colors

Now, using this password, you can, in scripts run the command:

kitten @ --password="control colors" set-colors background=red

Any script with access to the password can now change colors in kitty using remote control, but only that and nothing else. You can even supply the password via the [`KITTY_RC_PASSWORD`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_RC_PASSWORD) environment variable, or the file `~/.config/kitty/rc-pass` to avoid having to type it repeatedly. See [`kitten @ --password-file`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-password-file) and [`kitten @ --password-env`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-password-env).

The [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password) can be specified multiple times to create different passwords with different capabilities. Run the following to get a list of all action names:

kitten @ --help

You can even use glob patterns to match action names, for example:

remote_control_password "control colors" *-colors

If no action names are specified, all actions are allowed.

If `kitten @` is run with a password that is not present in `kitty.conf`, then kitty will interactively prompt the user to allow or disallow the remote control request. The user can choose to allow or disallow either just that request or all requests using that password. The user’s decision is remembered for the duration of that kitty instance.

Note

For password based authentication to work over SSH, you must pass the [`KITTY_PUBLIC_KEY`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_PUBLIC_KEY) environment variable to the remote host. The [ssh kitten](https://sw.kovidgoyal.net/kitty/kittens/ssh/) does this for you automatically. When using a password, [Encrypted communication](https://sw.kovidgoyal.net/kitty/rc_protocol/#rc-crypto) is used to ensure the password is kept secure. This does mean that using password based authentication is slower as the entire command is encrypted before transmission. This can be noticeable when using a command like `kitten @ set-background-image` which transmits large amounts of image data. Also, the clock on the remote system must match (within a few minutes) the clock on the local system. kitty uses a time based nonce to minimise the potential for replay attacks.

## Customizing authorization with your own program

If the ability to control access by action names is not fine grained enough, you can define your own Python script to examine every remote control command and allow/disallow it. To do so create a file in the kitty configuration directory, `~/.config/kitty/my_rc_auth.py` and add the following to `kitty.conf`:

remote_control_password "testing custom auth" my_rc_auth.py

`my_rc_auth.py` should define a `is_cmd_allowed` function as shown below:

def is_cmd_allowed(pcmd, window, from_socket, extra_data):
    cmd_name = pcmd['cmd']  # the name of the command
    cmd_payload = pcmd['payload']  # the arguments to the command
    # examine the cmd_name and cmd_payload and return True to allow
    # the command or False to disallow it. Return None to have no
    # effect on the command.

    # The command payload will vary from command to command, see
    # the rc protocol docs for details. Below is an example of
    # restricting the launch command to allow only running the
    # default shell.
    
    if cmd_name != 'launch':
        return None
    if cmd_payload.get('args') or cmd_payload.get('env') or cmd_payload.get('copy_cmdline') or cmd_payload.get('copy_env'):
        return False
    # prints in this function go to the parent kitty process STDOUT
    print('Allowing launch command:', cmd_payload)
    return True

Note

The payloads for the different remote control commands are documented in the [remote control protocol specification](https://sw.kovidgoyal.net/kitty/rc_protocol/).

# Mapping key presses to remote control commands

If you wish to trigger a remote control command easily with just a keypress, you can map it in `kitty.conf`. For example:

map f1 remote_control set-spacing margin=30

Then pressing the F1 key will set the active window margins to `30`. The syntax for what follows [`remote_control`](https://sw.kovidgoyal.net/kitty/actions/#action-remote_control) is exactly the same as the syntax for what follows `kitten @` above.

If you wish to ignore errors from the command, prefix the command with an `!`. For example, the following will not return an error when no windows are matched:

map f1 remote_control !focus-window --match XXXXXX

If you wish to run a more complex script, you can use:

map f1 remote_control_script /path/to/myscript

In this script you can use `kitten @` to run as many remote control commands as you like and process their output. [`remote_control_script`](https://sw.kovidgoyal.net/kitty/actions/#action-remote_control_script) is similar to the [`launch`](https://sw.kovidgoyal.net/kitty/actions/#action-launch) command with `--type=background --allow-remote-control`. For more advanced usage, including fine grained permissions, setting env vars, command line interpolation, passing data to STDIN, etc. the [launch](https://sw.kovidgoyal.net/kitty/launch/) command should be used.

Note

You do not need [`allow_remote_control`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.allow_remote_control) to use these mappings, as they are not actual remote programs, but are simply a way to reuse the remote control infrastructure via keybings.

# Broadcasting what you type to all kitty windows

As a simple illustration of the power of remote control, lets have what we type sent to all open kitty windows. To do that define the following mapping in `kitty.conf`:

map f1 launch --allow-remote-control kitty +kitten broadcast

Now press F1 and start typing, what you type will be sent to all windows, live, as you type it.

# The remote control protocol

If you wish to develop your own client to talk to *kitty*, you can use the [remote control protocol specification](https://sw.kovidgoyal.net/kitty/rc_protocol/). Note that there is a statically compiled, standalone executable, `kitten` available that can be used as a remote control client on any UNIX like computer. This can be downloaded and used directly from the [kitty releases](https://github.com/kovidgoyal/kitty/releases) page:

kitten @ --help

# Matching windows and tabs

Many remote control operations operate on windows or tabs. To select these, the `--match` option is often used. This allows matching using various sophisticated criteria such as title, ids, command lines, etc. These criteria are expressions of the form `field:query`. Where field is the field against which to match and query is the expression to match. They can be further combined using Boolean operators, best illustrated with some examples:

title:"My special window" or id:43
title:bash and env:USER=kovid
not id:1
(id:2 or id:3) and title:something

## Matching windows

When matching windows, match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

## Matching tabs

When matching tabs, match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

# kitten @

kitten @ [options] command ...

Control kitty by sending it commands. Set the [`allow_remote_control`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.allow_remote_control) option in `kitty.conf` or use a password, for this to work.

## Options

--to <TO>

An address for the kitty instance to control. Corresponds to the address given to the kitty instance via the [`kitty --listen-on`](https://sw.kovidgoyal.net/kitty/invocation/#cmdoption-kitty-listen-on) option or the [`listen_on`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.listen_on) setting in `kitty.conf`. If not specified, the environment variable [`KITTY_LISTEN_ON`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_LISTEN_ON) is checked. If that is also not found, messages are sent to the controlling terminal for this process, i.e. they will only work if this process is run within a kitty window.

--password <PASSWORD>

A password to use when contacting kitty. This will cause kitty to ask the user for permission to perform the specified action, unless the password has been accepted before or is pre-configured in `kitty.conf`. To use a blank password specify [`kitten @ --use-password`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-use-password) as `always`.

--password-file <PASSWORD_FILE>

A file from which to read the password. Trailing whitespace is ignored. Relative paths are resolved from the kitty configuration directory. Use - to read from STDIN. Use `fd:num` to read from the file descriptor `num`. Used if no [`kitten @ --password`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-password) is supplied. Defaults to checking for the `rc-pass` file in the kitty configuration directory. Default: `rc-pass`

--password-env <PASSWORD_ENV>

The name of an environment variable to read the password from. Used if no [`kitten @ --password-file`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-password-file) is supplied. Defaults to checking the environment variable [`KITTY_RC_PASSWORD`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_RC_PASSWORD). Default: `KITTY_RC_PASSWORD`

--use-password <USE_PASSWORD>

If no password is available, kitty will usually just send the remote control command without a password. This option can be used to force it to `always` or `never` use the supplied password. If set to always and no password is provided, the blank password is used. Default: `if-available` Choices: `always`, `if-available`, `never`

# kitten @ action

kitten @ action [options] ACTION [ARGS FOR ACTION...]

Run the specified mappable action. For a list of all available mappable actions, see [Mappable actions](https://sw.kovidgoyal.net/kitty/actions/). Any arguments for ACTION should follow the action. Note that parsing of arguments is action dependent so for best results specify all arguments as single string on the command line in the same format as you would use for that action in kitty.conf.

## Options

--self [=no]

Run the action on the window this command is run in instead of the active window.

--no-response [=no]

Don’t wait for a response indicating the success of the action. Note that using this option means that you will not be notified of failures. Default: `false`

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

# kitten @ close-tab

kitten @ close-tab [options]

Close an arbitrary set of tabs. The `--match` option can be used to specify complex sets of tabs to close. For example, to close all non-focused tabs in the currently focused OS window, use:

kitten @ close-tab --match "not state:focused and state:parent_focused"

## Options

--match <MATCH>, -m <MATCH>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

--no-response [=no]

Don’t wait for a response indicating the success of the action. Note that using this option means that you will not be notified of failures. Default: `false`

--self [=no]

Close the tab of the window this command is run in, rather than the active tab.

--ignore-no-match [=no]

Do not return an error if no tabs are matched to be closed.

# kitten @ close-window

kitten @ close-window [options]

Close the specified windows

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--no-response [=no]

Don’t wait for a response indicating the success of the action. Note that using this option means that you will not be notified of failures. Default: `false`

--self [=no]

Close the window this command is run in, rather than the active window.

--ignore-no-match [=no]

Do not return an error if no windows are matched to be closed.

# kitten @ create-marker

kitten @ create-marker [options] MARKER SPECIFICATION

Create a marker which can highlight text in the specified window. For example: `create_marker text 1 ERROR`. For full details see: [Mark text on screen](https://sw.kovidgoyal.net/kitty/marks/)

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--self [=no]

Apply marker to the window this command is run in, rather than the active window.

# kitten @ detach-tab

kitten @ detach-tab [options]

Detach the specified tabs and either move them into a new OS window or add them to the OS window containing the tab specified by [`kitten @ detach-tab --target-tab`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-detach-tab-target-tab)

## Options

--match <MATCH>, -m <MATCH>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

--target-tab <TARGET_TAB>, -t <TARGET_TAB>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

--self [=no]

Detach the tab this command is run in, rather than the active tab.

# kitten @ detach-window

kitten @ detach-window [options]

Detach the specified windows and either move them into a new tab, a new OS window or add them to the specified tab. Use the special value `new` for [`kitten @ detach-window --target-tab`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-detach-window-target-tab) to move to a new tab. If no target tab is specified the windows are moved to a new OS window.

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--target-tab <TARGET_TAB>, -t <TARGET_TAB>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs. Use the special value `new` to move to a new tab.

--self [=no]

Detach the window this command is run in, rather than the active window.

--stay-in-tab [=no]

Keep the focus on a window in the currently focused tab after moving the specified windows.

# kitten @ disable-ligatures

kitten @ disable-ligatures [options] STRATEGY

Control ligature rendering for the specified windows/tabs (defaults to active window). The STRATEGY can be one of: `never`, `always`, `cursor`.

## Options

--all [=no], -a [=no]

By default, ligatures are only affected in the active window. This option will cause ligatures to be changed in all windows.

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--match-tab <MATCH_TAB>, -t <MATCH_TAB>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

# kitten @ env

kitten @ env env_var1=val env_var2=val ...

Change the environment variables that will be seen in newly launched windows. Similar to the [`env`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.env) option in `kitty.conf`, but affects running kitty instances. If no = is present, the variable is removed from the environment.

# kitten @ focus-tab

kitten @ focus-tab [options]

The active window in the specified tab will be focused.

## Options

--match <MATCH>, -m <MATCH>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

--no-response [=no]

Don’t wait for a response indicating the success of the action. Note that using this option means that you will not be notified of failures. Default: `false`

# kitten @ focus-window

kitten @ focus-window [options]

Focus the specified window, if no window is specified, focus the window this command is run inside.

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--no-response [=no]

Don’t wait for a response from kitty. This means that even if no matching window is found, the command will exit with a success code. Default: `false`

# kitten @ get-colors

kitten @ get-colors [options]

Get the terminal colors for the specified window (defaults to active window). Colors will be output to STDOUT in the same syntax as used for `kitty.conf`.

To get a single color use:

get-colors | grep “^background “ | tr -s | cut -d” “ -f2

Change background above to whatever color you are interested in.

## Options

--configured [=no], -c [=no]

Instead of outputting the colors for the specified window, output the currently configured colors.

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

# kitten @ get-text

kitten @ get-text [options]

Get text from the specified window

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--extent <EXTENT>

What text to get. The default of `screen` means all text currently on the screen. `all` means all the screen+scrollback and `selection` means the currently selected text. `first_cmd_output_on_screen` means the output of the first command that was run in the window on screen. `last_cmd_output` means the output of the last command that was run in the window. `last_visited_cmd_output` means the first command output below the last scrolled position via scroll_to_prompt. `last_non_empty_output` is the output from the last command run in the window that had some non empty output. The last four require [Shell integration](https://sw.kovidgoyal.net/kitty/shell-integration/#shell-integration) to be enabled. Default: `screen` Choices: `all`, `first_cmd_output_on_screen`, `last_cmd_output`, `last_non_empty_output`, `last_visited_cmd_output`, `screen`, `selection`

--ansi [=no]

By default, only plain text is returned. With this flag, the text will include the ANSI formatting escape codes for colors, bold, italic, etc.

--add-cursor [=no]

Add ANSI escape codes specifying the cursor position and style to the end of the text.

--add-wrap-markers [=no]

Add carriage returns at every line wrap location (where long lines are wrapped at screen edges).

--clear-selection [=no]

Clear the selection in the matched window, if any.

--self [=no]

Get text from the window this command is run in, rather than the active window.

# kitten @ goto-layout

kitten @ goto-layout [options] LAYOUT_NAME

Set the window layout in the specified tabs (or the active tab if not specified). You can use special match value `all` to set the layout in all tabs. In case there are multiple layouts with the same name but different options, specify the full layout definition or a unique prefix of the full definition.

## Options

--match <MATCH>, -m <MATCH>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

# kitten @ kitten

kitten @ kitten [options] kitten_name

Run a kitten over the specified windows (active window by default). The kitten_name can be either the name of a builtin kitten or the path to a Python file containing a custom kitten. If a relative path is used it is searched for in the [kitty config directory](https://sw.kovidgoyal.net/kitty/conf/#confloc). If the kitten is a no_ui kitten and its handle response method returns a string or boolean, this is printed out to stdout.

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

# kitten @ last-used-layout

kitten @ last-used-layout [options]

Switch to the last used window layout in the specified tabs (or the active tab if not specified).

## Options

--all [=no], -a [=no]

Change the layout in all tabs.

--no-response [=no]

Don’t wait for a response from kitty. This means that even if no matching tab is found, the command will exit with a success code. Default: `false`

--match <MATCH>, -m <MATCH>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

# kitten @ launch

kitten @ launch [options] [CMD ...]

Prints out the id of the newly opened window. Any command line arguments are assumed to be the command line used to run in the new window, if none are provided, the default shell is run. For example:

kitten @ launch --title=Email mutt

## Options

--match <MATCH>, -m <MATCH>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

--wait-for-child-to-exit [=no]

Wait until the launched program exits and print out its exit code. The exit code is printed out instead of the window id. If the program exited normally its exit code is printed, which is always greater than or equal to zero. If the program was killed by a signal, the symbolic name of the SIGNAL is printed, if available, otherwise the signal number with a leading minus sign is printed.

--response-timeout <RESPONSE_TIMEOUT>

The time in seconds to wait for the started process to exit, when using the [`--wait-for-child-to-exit`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-wait-for-child-to-exit) option. Defaults to one day. Default: `86400`

--no-response [=no]

Do not print out the id of the newly created window.

--self [=no]

If specified the tab containing the window this command is run in is used instead of the active tab

--source-window <SOURCE_WINDOW>

A match expression to select the window from which data such as title, colors, env vars, screen contents, etc. are copied. When not specified the currently active window is used. See [Matching windows and tabs](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax) for the syntax used for specifying windows.

--title <WINDOW_TITLE>, --window-title <WINDOW_TITLE>

The title to set for the new window. By default, title is controlled by the child process. The special value `current` will copy the title from the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

--tab-title <TAB_TITLE>

The title for the new tab if launching in a new tab. By default, the title of the active window in the tab is used as the tab title. The special value `current` will copy the title from the tab containing the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

--type <TYPE>

Where to launch the child process:

`window`

A new [kitty window](https://sw.kovidgoyal.net/kitty/glossary/#term-window) in the current tab

`tab`

A new [tab](https://sw.kovidgoyal.net/kitty/glossary/#term-tab) in the current OS window. Not available when the [launch](https://sw.kovidgoyal.net/kitty/launch/) command is used in [startup sessions](https://sw.kovidgoyal.net/kitty/sessions/#sessions).

`os-window`

A new [operating system window](https://sw.kovidgoyal.net/kitty/glossary/#term-os_window). Not available when the [launch](https://sw.kovidgoyal.net/kitty/launch/) command is used in [startup sessions](https://sw.kovidgoyal.net/kitty/sessions/#sessions).

`overlay`

An [overlay window](https://sw.kovidgoyal.net/kitty/glossary/#term-overlay) covering the current active kitty window

`overlay-main`

An [overlay window](https://sw.kovidgoyal.net/kitty/glossary/#term-overlay) covering the current active kitty window. Unlike a plain overlay window, this window is considered as a main window which means it is used as the active window for getting the current working directory, the input text for kittens, launch commands, etc. Useful if this overlay is intended to run for a long time as a primary window.

`background`

The process will be run in the background, without a kitty window. Note that if [`kitten @ launch --allow-remote-control`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-allow-remote-control) is specified the [`KITTY_LISTEN_ON`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_LISTEN_ON) environment variable will be set to a dedicated socket pair file descriptor that the process can use for remote control.

`clipboard`, `primary`

These two are meant to work with [`--stdin-source`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-stdin-source) to copy data to the system clipboard or primary selection.

`os-panel`

Similar to `os-window`, except that it creates the new OS Window as a desktop panel. Only works on platforms that support this, such as Wayand compositors that support the layer shell protocol. Use the [`kitten @ launch --os-panel`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-os-panel) option to configure the panel.

Default: `window` Choices: `background`, `clipboard`, `os-panel`, `os-window`, `overlay`, `overlay-main`, `primary`, `tab`, `window`

--dont-take-focus [=no], --keep-focus [=no]

Keep the focus on the currently active window instead of switching to the newly opened window.

--cwd <CWD>

The working directory for the newly launched child. Use the special value `current` to use the working directory of the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window). The special value `last_reported` uses the last working directory reported by the shell (needs [Shell integration](https://sw.kovidgoyal.net/kitty/shell-integration/#shell-integration) to work). The special value `oldest` works like `current` but uses the working directory of the oldest foreground process associated with the currently active window rather than the newest foreground process. Finally, the special value `root` refers to the process that was originally started when the window was created.

When opening in the same working directory as the current window causes the new window to connect to a remote host, you can use the [`--hold-after-ssh`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-hold-after-ssh) flag to prevent the new window from closing when the connection is terminated.

--add-to-session <ADD_TO_SESSION>

Add the newly created window/tab to the specified session. Use `.` to add to the session of the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window), if any. See [Sessions](https://sw.kovidgoyal.net/kitty/sessions/#sessions) for what a session is and how to use one. By default, the window is added to the session of the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window) when [`kitten @ launch --cwd`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-cwd) is set to use the the working directory from that window, otherwise the newly created window does not belong to any session. To force adding to no session, use the value `!`. Adding a newly created window to a session is purely temporary, it does not change the actual session file, for that you have to resave the session. Note that using this flag in a launch command within a session file has no effect as the window is always added to the session belonging to that file.

--env <ENV>

Environment variables to set in the child process. Can be specified multiple times to set different environment variables. Syntax: `name=value`. Using `name=` will set to empty string and just `name` will remove the environment variable.

--var <VAR>

User variables to set in the created window. Can be specified multiple times to set different user variables. Syntax: `name=value`. Using `name=` will set to empty string.

--hold [=no]

Keep the window open even after the command being executed exits, at a shell prompt. The shell will be run after the launched command exits.

--copy-colors [=no]

Set the colors of the newly created window to be the same as the colors in the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

--copy-cmdline [=no]

Ignore any specified command line and instead use the command line from the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

--copy-env [=no]

Copy the environment variables from the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window) into the newly launched child process. Note that this only copies the environment when the window was first created, as it is not possible to get updated environment variables from arbitrary processes. To copy that environment, use either the [clone-in-kitty](https://sw.kovidgoyal.net/kitty/shell-integration/#clone-shell) feature or the kitty remote control feature with [`kitten @ launch --copy-env`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-copy-env).

--location <LOCATION>

Where to place the newly created window when it is added to a tab which already has existing windows in it. `after` and `before` place the new window before or after the active window. `neighbor` is a synonym for `after`. Also applies to creating a new tab, where the value of `after` will cause the new tab to be placed next to the current tab instead of at the end. The values of `vsplit`, `hsplit` and `split` are only used by the `splits` layout and control if the new window is placed in a vertical, horizontal or automatic split with the currently active window. The default is to place the window in a layout dependent manner, typically, after the currently active window. See [`--next-to`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-next-to) to use a window other than the currently active window. Default: `default` Choices: `after`, `before`, `default`, `first`, `hsplit`, `last`, `neighbor`, `split`, `vsplit`

--next-to <NEXT_TO>

A match expression to select the window next to which the new window is created. See [Matching windows and tabs](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax) for the syntax for specifying windows. If not specified defaults to the active window. When used via remote control and a target tab is specified this option is ignored unless the matched window is in the specified tab. When using [`--type`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-type) of `tab`, the tab will be created in the OS Window containing the matched window.

--bias <BIAS>

The bias used to alter the size of the window. It controls what fraction of available space the window takes. The exact meaning of bias depends on the current layout.

- Splits layout: The bias is interpreted as a percentage between 0 and 100. When splitting a window into two, the new window will take up the specified fraction of the space allotted to the original window and the original window will take up the remainder of the space.

- Vertical/horizontal layout: The bias is interpreted as adding/subtracting from the normal size of the window. It should be a number between -90 and 90. This number is the percentage of the OS Window size that should be added to the window size. So for example, if a window would normally have been size 50 in the layout inside an OS Window that is size 80 high and --bias -10 is used it will become *approximately* size 42 high. Note that sizes are approximations, you cannot use this method to create windows of fixed sizes.

- Tall layout: If the window being created is the *first* window in a column, then the bias is interpreted as a percentage, as for the splits layout, splitting the OS Window width between columns. If the window is a second or subsequent window in a column the bias is interpreted as adding/subtracting from the window size as for the vertical layout above.

- Fat layout: Same as tall layout except it goes by rows instead of columns.

- Grid layout: The bias is interpreted the same way as for the Vertical and Horizontal layouts, as something to be added/subtracted to the normal size. However, the since in a grid layout there are rows *and* columns, the bias on the first window in a column operates on the columns. Any later windows in that column operate on the row. So, for example, if you bias the first window in a grid layout it will change the width of the first column, the second window, the width of the second column, the third window, the height of the second row and so on.

The bias option was introduced in kitty version 0.36.0. Default: `0`

--allow-remote-control [=no]

Programs running in this window can control kitty (even if remote control is not enabled in `kitty.conf`). Note that any program with the right level of permissions can still write to the pipes of any other program on the same computer and therefore can control kitty. It can, however, be useful to block programs running on other computers (for example, over SSH) or as other users. See [`--remote-control-password`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-remote-control-password) for ways to restrict actions allowed by remote control.

--remote-control-password <REMOTE_CONTROL_PASSWORD>

Restrict the actions remote control is allowed to take. This works like [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password). You can specify a password and list of actions just as for [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password). For example:

--remote-control-password '"my passphrase" get-* set-colors'

This password will be in effect for this window only. Note that any passwords you have defined for [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password) in `kitty.conf` are also in effect. You can override them by using the same password here. You can also disable all [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password) global passwords for this window, by using:

--remote-control-password '!'

This option only takes effect if [`--allow-remote-control`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-allow-remote-control) is also specified. Can be specified multiple times to create multiple passwords. This option was added to kitty in version 0.26.0

--stdin-source <STDIN_SOURCE>

Pass the screen contents as `STDIN` to the child process.

`@selection`

is the currently selected text in the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

`@screen`

is the contents of the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

`@screen_scrollback`

is the same as `@screen`, but includes the scrollback buffer as well.

`@alternate`

is the secondary screen of the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window). For example if you run a full screen terminal application, the secondary screen will be the screen you return to when quitting the application.

`@first_cmd_output_on_screen`

is the output from the first command run in the shell on screen.

`@last_cmd_output`

is the output from the last command run in the shell.

`@last_visited_cmd_output`

is the first output below the last scrolled position via [`scroll_to_prompt`](https://sw.kovidgoyal.net/kitty/actions/#action-scroll_to_prompt), this needs [shell integration](https://sw.kovidgoyal.net/kitty/shell-integration/#shell-integration) to work.

Default: `none` Choices: `@alternate`, `@alternate_scrollback`, `@first_cmd_output_on_screen`, `@last_cmd_output`, `@last_visited_cmd_output`, `@screen`, `@screen_scrollback`, `@selection`, `none`

--stdin-add-formatting [=no]

When using [`--stdin-source`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-stdin-source) add formatting escape codes, without this only plain text will be sent.

--stdin-add-line-wrap-markers [=no]

When using [`--stdin-source`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-stdin-source) add a carriage return at every line wrap location (where long lines are wrapped at screen edges). This is useful if you want to pipe to program that wants to duplicate the screen layout of the screen.

--marker <MARKER>

Create a marker that highlights text in the newly created window. The syntax is the same as for the [`toggle_marker`](https://sw.kovidgoyal.net/kitty/actions/#action-toggle_marker) action (see [Mark text on screen](https://sw.kovidgoyal.net/kitty/marks/)).

--os-window-class <OS_WINDOW_CLASS>

Set the WM_CLASS property on X11 and the application id property on Wayland for the newly created OS window when using [`--type=os-window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-type). Defaults to whatever is used by the parent kitty process, which in turn defaults to `kitty`.

--os-window-name <OS_WINDOW_NAME>

Set the WM_NAME property on X11 for the newly created OS Window when using [`--type=os-window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-type). Defaults to [`--os-window-class`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-os-window-class).

--os-window-title <OS_WINDOW_TITLE>

Set the title for the newly created OS window. This title will override any titles set by programs running in kitty. The special value `current` will copy the title from the OS Window containing the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

--os-window-state <OS_WINDOW_STATE>

The initial state for the newly created OS Window. Default: `normal` Choices: `fullscreen`, `maximized`, `minimized`, `normal`

--logo <LOGO>

Path to a PNG image to use as the logo for the newly created window. See [`window_logo_path`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.window_logo_path). Relative paths are resolved from the kitty configuration directory.

--logo-position <LOGO_POSITION>

The position for the window logo. Only takes effect if [`--logo`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-logo) is specified. See [`window_logo_position`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.window_logo_position).

--logo-alpha <LOGO_ALPHA>

The amount the window logo should be faded into the background. Only takes effect if [`--logo`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-logo) is specified. See [`window_logo_alpha`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.window_logo_alpha). Default: `-1`

--color <COLOR>

Change colors in the newly launched window. You can either specify a path to a `.conf` file with the same syntax as `kitty.conf` to read the colors from, or specify them individually, for example:

--color background=white --color foreground=red

--spacing <SPACING>

Set the margin and padding for the newly created window. For example: `margin=20` or `padding-left=10` or `margin-h=30`. The shorthand form sets all values, the `*-h` and `*-v` variants set horizontal and vertical values. Can be specified multiple times. Note that this is ignored for overlay windows as these use the settings from the base window.

--watcher <WATCHER>, -w <WATCHER>

Path to a Python file. Appropriately named functions in this file will be called for various events, such as when the window is resized, focused or closed. See the section on watchers in the launch command documentation: [Watching launched windows](https://sw.kovidgoyal.net/kitty/launch/#watchers). Relative paths are resolved relative to the [kitty config directory](https://sw.kovidgoyal.net/kitty/conf/#confloc). Global watchers for all windows can be specified with [`watcher`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.watcher) in `kitty.conf`.

--os-panel <OS_PANEL>

Options to control the creation of desktop panels. Takes the same settings as the [panel kitten](https://sw.kovidgoyal.net/kitty/kittens/panel/), except for [`--override`](https://sw.kovidgoyal.net/kitty/kittens/panel/#cmdoption-kitty-kitten-panel-override) and [`--config`](https://sw.kovidgoyal.net/kitty/kittens/panel/#cmdoption-kitty-kitten-panel-config). Can be specified multiple times. For example, to create a desktop panel at the bottom of the screen two lines high:

launch --type os-panel --os-panel lines=2 --os-panel edge=bottom sh -c "echo; echo; echo hello; sleep 5s"

--hold-after-ssh [=no]

When using [`--cwd`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-cwd)`=current` or similar from a window that is running the ssh kitten, the new window will run a local shell after disconnecting from the remote host, when this option is specified.

# kitten @ load-config

kitten @ load-config [options] CONF_FILE ...

(Re)load the specified kitty.conf config files(s). If no files are specified the previously specified config file is reloaded. Note that the specified paths must exist and be readable by the kitty process on the computer that process is running on. Relative paths are resolved with respect to the kitty config directory on the computer running kitty.

## Options

--ignore-overrides [=no]

By default, any config overrides previously specified at the kitty invocation command line or a previous load-config-file command are respected. Use this option to have them ignored instead.

--override <OVERRIDE>, -o <OVERRIDE>

Override individual configuration options, can be specified multiple times. Syntax: name=value. For example: [`kitty -o`](https://sw.kovidgoyal.net/kitty/invocation/#cmdoption-kitty-override) font_size=20

--no-response [=no]

Don’t wait for a response indicating the success of the action. Note that using this option means that you will not be notified of failures. Default: `false`

# kitten @ ls

kitten @ ls [options]

List windows. The list is returned as JSON tree. The top-level is a list of operating system kitty windows. Each OS window has an id and a list of tabs. Each tab has its own id, a title and a list of windows. Each window has an id, title, current working directory, process id (PID), command-line and environment of the process running in the window. Additionally, when running the command inside a kitty window, that window can be identified by the is_self parameter.

You can use these criteria to select windows/tabs for the other commands.

You can limit the windows/tabs in the output by using the [`--match`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-ls-match) and [`--match-tab`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-ls-match-tab) options.

## Options

--all-env-vars [=no]

Show all environment variables in output, not just differing ones.

--self [=no]

Only list the window this command is run in.

--output-format <OUTPUT_FORMAT>

Output in JSON or kitty session format Default: `json` Choices: `json`, `session`

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--match-tab <MATCH_TAB>, -t <MATCH_TAB>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

# kitten @ new-window

kitten @ new-window [options] [CMD ...]

DEPRECATED: Use the [launch](https://sw.kovidgoyal.net/kitty/remote-control/#at-launch) command instead.

Open a new window in the specified tab. If you use the [`kitten @ new-window --match`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-new-window-match) option the first matching tab is used. Otherwise the currently active tab is used. Prints out the id of the newly opened window (unless [`--no-response`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-new-window-no-response) is used). Any command line arguments are assumed to be the command line used to run in the new window, if none are provided, the default shell is run. For example:

kitten @ new-window --title Email mutt

## Options

--match <MATCH>, -m <MATCH>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

--title <TITLE>

The title for the new window. By default it will use the title set by the program running in it.

--cwd <CWD>

The initial working directory for the new window. Defaults to whatever the working directory for the kitty process you are talking to is.

--dont-take-focus [=no], --keep-focus [=no]

Keep the current window focused instead of switching to the newly opened window.

--window-type <WINDOW_TYPE>

What kind of window to open. A kitty window or a top-level OS window. Default: `kitty` Choices: `kitty`, `os`

--new-tab [=no]

Open a new tab.

--tab-title <TAB_TITLE>

Set the title of the tab, when open a new tab.

--no-response [=no]

Don’t wait for a response giving the id of the newly opened window. Note that using this option means that you will not be notified of failures and that the id of the new window will not be printed out. Default: `false`

# kitten @ remove-marker

kitten @ remove-marker [options]

Remove the currently set marker, if any.

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--self [=no]

Apply marker to the window this command is run in, rather than the active window.

# kitten @ resize-os-window

kitten @ resize-os-window [options] [OS Panel settings ...]

Resize (or other operations) on the specified OS Windows. Note that some window managers/environments do not allow applications to resize their windows, for example, tiling window managers.

To modify OS Panels created with the panel kitten, use [`--action`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-resize-os-window-action)`` =:code:`os-panel` ``. Specify the modifications in the same syntax as used by the panel kitten, without the leading dashes. Use the [`--incremental`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-resize-os-window-incremental) option to only change the specified panel settings. For example, move the panel to bottom edge and make it two lines tall: `--action=os-panel --incremental lines=2 edge=bottom`

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--action <ACTION>

The action to perform. Default: `resize` Choices: `hide`, `os-panel`, `resize`, `show`, `toggle-fullscreen`, `toggle-maximized`, `toggle-visibility`

--unit <UNIT>

The unit in which to interpret specified sizes. Default: `cells` Choices: `cells`, `pixels`

--width <WIDTH>

Change the width of the window. Zero leaves the width unchanged. Default: `0`

--height <HEIGHT>

Change the height of the window. Zero leaves the height unchanged. Default: `0`

--incremental [=no]

Treat the specified sizes as increments on the existing window size instead of absolute sizes. When using [`--action`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-resize-os-window-action)``=:code:`os-panel``,` only the specified settings are changed, otherwise non-specified settings keep their current value.

--self [=no]

Resize the window this command is run in, rather than the active window.

--no-response [=no]

Don’t wait for a response indicating the success of the action. Note that using this option means that you will not be notified of failures. Default: `false`

# kitten @ resize-window

kitten @ resize-window [options]

Resize the specified windows in the current layout. Note that not all layouts can resize all windows in all directions.

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--increment <INCREMENT>, -i <INCREMENT>

The number of cells to change the size by, can be negative to decrease the size. Default: `2`

--axis <AXIS>, -a <AXIS>

The axis along which to resize. If `horizontal`, it will make the window wider or narrower by the specified increment. If `vertical`, it will make the window taller or shorter by the specified increment. The special value `reset` will reset the layout to its default configuration. Default: `horizontal` Choices: `horizontal`, `reset`, `vertical`

--self [=no]

Resize the window this command is run in, rather than the active window.

# kitten @ run

kitten @ run [options] CMD ...

Run the specified program on the computer in which kitty is running. When STDIN is not a TTY it is forwarded to the program as its STDIN. STDOUT and STDERR from the the program are forwarded here. The exit status of this invocation will be the exit status of the executed program. If you wish to just run a program without waiting for a response, use @ launch --type=background instead.

## Options

--env <ENV>

Environment variables to set in the child process. Can be specified multiple times to set different environment variables. Syntax: `name=value`. Using `name=` will set to empty string and just `name` will remove the environment variable.

--allow-remote-control [=no]

The executed program will have privileges to run remote control commands in kitty.

--remote-control-password <REMOTE_CONTROL_PASSWORD>

Restrict the actions remote control is allowed to take. This works like [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password). You can specify a password and list of actions just as for [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password). For example:

--remote-control-password '"my passphrase" get-* set-colors'

This password will be in effect for this window only. Note that any passwords you have defined for [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password) in `kitty.conf` are also in effect. You can override them by using the same password here. You can also disable all [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password) global passwords for this window, by using:

--remote-control-password '!'

This option only takes effect if [`--allow-remote-control`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-run-allow-remote-control) is also specified. Can be specified multiple times to create multiple passwords. This option was added to kitty in version 0.26.0

# kitten @ scroll-window

kitten @ scroll-window [options] SCROLL_AMOUNT

Scroll the specified windows, if no window is specified, scroll the window this command is run inside. SCROLL_AMOUNT can be either the keywords `start` or `end` or an argument of the form <number>[unit][+-]. `unit` can be `l` for lines, `p` for pages, `u` for unscroll and `r` for scroll to prompt. If unspecified, `l` is the default. For example, `30` will scroll down 30 lines, `2p-` will scroll up 2 pages and `0.5p` will scroll down half page. `3u` will *unscroll* by 3 lines, which means that 3 lines will move from the scrollback buffer onto the top of the screen. `1r-` will scroll to the previous prompt and 1r to the next prompt. See [`scroll_to_prompt`](https://sw.kovidgoyal.net/kitty/actions/#action-scroll_to_prompt) for details on how scrolling to prompt works.

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--no-response [=no]

Don’t wait for a response indicating the success of the action. Note that using this option means that you will not be notified of failures. Default: `false`

# kitten @ select-window

kitten @ select-window [options]

Prints out the id of the selected window. Other commands can then be chained to make use of it.

## Options

--match <MATCH>, -m <MATCH>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

--response-timeout <RESPONSE_TIMEOUT>

The time in seconds to wait for the user to select a window. Default: `60`

--self [=no]

Select window from the tab containing the window this command is run in, instead of the active tab.

--title <TITLE>

A title that will be displayed to the user to describe what this selection is for.

--exclude-active [=no]

Exclude the currently active window from the list of windows to pick.

--reactivate-prev-tab [=no]

When the selection is finished, the tab in the same OS window that was activated before the selection will be reactivated. The last activated OS window will also be refocused.

# kitten @ send-key

kitten @ send-key [options] [KEYS TO SEND ...]

Send arbitrary key presses to specified windows. All specified keys are sent first as press events then as release events in reverse order. Keys are sent to the programs running in the windows. They are sent only if the current keyboard mode for the program supports the particular key. For example: send-key ctrl+a ctrl+b. Note that errors are not reported, for technical reasons, so send-key always succeeds, even if no key was sent to any window.

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--match-tab <MATCH_TAB>, -t <MATCH_TAB>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

--all [=no]

Match all windows.

--exclude-active [=no]

Do not send text to the active window, even if it is one of the matched windows.

# kitten @ send-text

kitten @ send-text [options] [TEXT TO SEND]

Send arbitrary text to specified windows. The text follows Python escaping rules. So you can use [escapes](https://www.gnu.org/software/bash/manual/html_node/ANSI_002dC-Quoting.html) like `'\e'` to send control codes and `'\u21fa'` to send Unicode characters. Remember to use single-quotes otherwise the backslash is interpreted as a shell escape character. If you use the [`kitten @ send-text --match`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-send-text-match) option the text will be sent to all matched windows. By default, text is sent to only the currently active window. Note that errors are not reported, for technical reasons, so send-text always succeeds, even if no text was sent to any window.

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--match-tab <MATCH_TAB>, -t <MATCH_TAB>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

--all [=no]

Match all windows.

--exclude-active [=no]

Do not send text to the active window, even if it is one of the matched windows.

--stdin [=no]

Read the text to be sent from stdin. Note that in this case the text is sent as is, not interpreted for escapes. If stdin is a terminal, you can press Ctrl+D to end reading.

--from-file <FROM_FILE>

Path to a file whose contents you wish to send. Note that in this case the file contents are sent as is, not interpreted for escapes.

--bracketed-paste <BRACKETED_PASTE>

When sending text to a window, wrap the text in bracketed paste escape codes. The default is to not do this. A value of `auto` means, bracketed paste will be used only if the program running in the window has turned on bracketed paste mode. Default: `disable` Choices: `auto`, `disable`, `enable`

# kitten @ set-background-image

kitten @ set-background-image [options] PATH_TO_PNG_IMAGE

Set the background image for the specified OS windows. You must specify the path to an image that will be used as the background. If you specify the special value `none` then any existing image will be removed. Supported image formats are: PNG, JPEG, WEBP, GIF, BMP, TIFF

## Options

--all [=no], -a [=no]

By default, background image is only changed for the currently active OS window. This option will cause the image to be changed in all windows.

--configured [=no], -c [=no]

Change the configured background image which is used for new OS windows.

--layout <LAYOUT>

How the image should be displayed. A value of `configured` will use the configured value. Default: `configured` Choices: `clamped`, `configured`, `mirror-tiled`, `scaled`, `tiled`

--no-response [=no]

Don’t wait for a response from kitty. This means that even if setting the background image failed, the command will exit with a success code. Default: `false`

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

# kitten @ set-background-opacity

kitten @ set-background-opacity [options] OPACITY

Set the background opacity for the specified windows. This will only work if you have turned on [`dynamic_background_opacity`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.dynamic_background_opacity) in `kitty.conf`. The background opacity affects all kitty windows in a single OS window. For example:

kitten @ set-background-opacity 0.5

## Options

--all [=no], -a [=no]

By default, background opacity are only changed for the currently active OS window. This option will cause background opacity to be changed in all windows.

--toggle [=no]

When specified, the background opacity for the matching OS windows will be reset to default if it is currently equal to the specified value, otherwise it will be set to the specified value.

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--match-tab <MATCH_TAB>, -t <MATCH_TAB>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

# kitten @ set-colors

kitten @ set-colors [options] COLOR_OR_FILE ...

Set the terminal colors for the specified windows/tabs (defaults to active window). You can either specify the path to a conf file (in the same format as `kitty.conf`) to read the colors from or you can specify individual colors, for example:

kitten @ set-colors foreground=red background=white

## Options

--all [=no], -a [=no]

By default, colors are only changed for the currently active window. This option will cause colors to be changed in all windows.

--configured [=no], -c [=no]

Also change the configured colors (i.e. the colors kitty will use for new windows or after a reset).

--reset [=no]

Restore all colors to the values they had at kitty startup. Note that if you specify this option, any color arguments are ignored and [`kitten @ set-colors --configured`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-set-colors-configured) and [`kitten @ set-colors --all`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-set-colors-all) are implied.

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--match-tab <MATCH_TAB>, -t <MATCH_TAB>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

# kitten @ set-enabled-layouts

kitten @ set-enabled-layouts [options] LAYOUT ...

Set the enabled layouts in the specified tabs (or the active tab if not specified). You can use special match value `all` to set the enabled layouts in all tabs. If the current layout of the tab is not included in the enabled layouts, its layout is changed to the first enabled layout.

## Options

--match <MATCH>, -m <MATCH>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

--configured [=no]

Change the default enabled layout value so that the new value takes effect for all newly created tabs as well.

# kitten @ set-font-size

kitten @ set-font-size [options] FONT_SIZE

Sets the font size to the specified size, in pts. Note that in kitty all sub-windows in the same OS window must have the same font size. A value of zero resets the font size to default. Prefixing the value with a `+`, `-`, `*` or `/` changes the font size by the specified amount. Use -- before using - to have it not mistaken for a option. For example: kitten @ set-font-size -- -2

## Options

--all [=no], -a [=no]

By default, the font size is only changed in the active OS window, this option will cause it to be changed in all OS windows. It also changes the font size for any newly created OS Windows in the future.

# kitten @ set-spacing

kitten @ set-spacing [options] MARGIN_OR_PADDING ...

Set the paddings and margins for the specified windows (defaults to active window). For example: `margin=20` or `padding-left=10` or `margin-h=30`. The shorthand form sets all values, the `*-h` and `*-v` variants set horizontal and vertical values. The special value `default` resets to using the default value. If you specify a tab rather than a window, all windows in that tab are affected.

## Options

--all [=no], -a [=no]

By default, settings are only changed for the currently active window. This option will cause paddings and margins to be changed in all windows.

--configured [=no], -c [=no]

Also change the configured paddings and margins (i.e. the settings kitty will use for new windows).

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--match-tab <MATCH_TAB>, -t <MATCH_TAB>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

# kitten @ set-tab-color

kitten @ set-tab-color [options] COLORS

Change the color of the specified tabs in the tab bar

The foreground and background colors when active and inactive can be overridden using this command. The syntax for specifying colors is: active_fg=color active_bg=color inactive_fg=color inactive_bg=color. Where color can be either a color name or a value of the form #rrggbb or the keyword NONE to revert to using the default colors.

## Options

--match <MATCH>, -m <MATCH>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

--self [=no]

Close the tab this command is run in, rather than the active tab.

# kitten @ set-tab-title

kitten @ set-tab-title [options] TITLE ...

Set the title for the specified tabs. If you use the [`kitten @ set-tab-title --match`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-set-tab-title-match) option the title will be set for all matched tabs. By default, only the tab in which the command is run is affected. If you do not specify a title, the title of the currently active window in the tab is used.

## Options

--match <MATCH>, -m <MATCH>

The tab to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `index`, `title`, `window_id`, `window_title`, `pid`, `cwd`, `cmdline` `env`, `var`, `state`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all tabs.

For numeric fields: `id`, `index`, `window_id`, `pid` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id`/`window_id` match from the highest id number down, in particular, -1 is the most recently created tab/window.

When using `title` or `id`, first a matching tab is looked for, and if not found a matching window is looked for, and the tab for that window is used.

You can also use `window_id` and `window_title` to match the tab that contains the window with the specified id or title.

The `index` number is used to match the nth tab in the currently active OS window. The `recent` number matches recently active tabs in the currently active OS window, with zero being the currently active tab, one the previously active tab and so on.

The field `session` matches tabs that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`. Tabs containing any window with the specified environment variables are matched. Similarly, `var` matches tabs containing any window with the specified user variable.

The field `state` matches on the state of the tab. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused` and `focused_os_window`. Active tabs are the tabs that are active in their parent OS window. There is only one focused tab and it is the tab to which keyboard events are delivered. If no tab is focused, the last focused tab is matched. The value `focused_os_window` matches all tabs in the currently focused OS window.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of tabs.

# kitten @ set-user-vars

kitten @ set-user-vars [options] [NAME=VALUE ...]

Set user variables for the specified windows. If you use the [`kitten @ set-user-vars --match`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-set-user-vars-match) option the variables will be set for all matched windows. By default, only the window in which the command is run is affected. If you do not specify any variables, the current variables are printed out, one per line. To unset a variable specify just its name.

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

# kitten @ set-window-logo

kitten @ set-window-logo [options] PATH_TO_PNG_IMAGE

Set the logo image for the specified windows. You must specify the path to an image that will be used as the logo. If you specify the special value `none` then any existing logo will be removed. Supported image formats are: PNG, JPEG, WEBP, GIF, BMP, TIFF

## Options

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

--self [=no]

Act on the window this command is run in, rather than the active window.

--position <POSITION>

The position for the window logo. See [`window_logo_position`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.window_logo_position).

--alpha <ALPHA>

The amount the window logo should be faded into the background. See [`window_logo_position`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.window_logo_position). Default: `-1`

--no-response [=no]

Don’t wait for a response from kitty. This means that even if setting the image failed, the command will exit with a success code. Default: `false`

# kitten @ set-window-title

kitten @ set-window-title [options] [TITLE ...]

Set the title for the specified windows. If you use the [`kitten @ set-window-title --match`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-set-window-title-match) option the title will be set for all matched windows. By default, only the window in which the command is run is affected. If you do not specify a title, the last title set by the child process running in the window will be used.

## Options

--temporary [=no]

By default, the title will be permanently changed and programs running in the window will not be able to change it again. If you want to allow other programs to change it afterwards, use this option.

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

# kitten @ signal-child

kitten @ signal-child [options] [SIGNAL_NAME ...]

Send one or more signals to the foreground process in the specified windows. If you use the [`kitten @ signal-child --match`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-signal-child-match) option the signal will be sent for all matched windows. By default, only the active window is affected. If you do not specify any signals, `SIGINT` is sent by default. You can also map [`signal_child`](https://sw.kovidgoyal.net/kitty/actions/#action-signal_child) to a shortcut in `kitty.conf`, for example:

map f1 signal_child SIGTERM

## Options

--no-response [=no]

Don’t wait for a response indicating the success of the action. Note that using this option means that you will not be notified of failures. Default: `false`

--match <MATCH>, -m <MATCH>

The window to match. Match specifications are of the form: field:query. Where field can be one of: `id`, `title`, `pid`, `cwd`, `cmdline`, `num`, `env`, `var`, `state`, `neighbor`, `session` and `recent`. query is the expression to match. Expressions can be either a number or a regular expression, and can be [combined using Boolean operators](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax).

The special value `all` matches all windows.

For numeric fields: `id`, `pid`, `num` and `recent`, the expression is interpreted as a number, not a regular expression. Negative values for `id` match from the highest id number down, in particular, -1 is the most recently created window.

The field `num` refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command).

The window id of the current window is available as the [`KITTY_WINDOW_ID`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_WINDOW_ID) environment variable.

The field `recent` refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field `neighbor` refers to a neighbor of the active window in the specified direction, which can be: `left`, `right`, `top` or `bottom`.

The field `session` matches windows that were created in the specified session. Use the expression `^$` to match windows that were not created in a session and `.` to match the currently active session and `~` to match either the currently active sesison or the last active session when no session is active.

When using the `env` field to match on environment variables, you can specify only the environment variable name or a name and value, for example, `env:MY_ENV_VAR=2`.

Similarly, the `var` field matches on user variables set on the window. You can specify name or name and value as with the `env` field.

The field `state` matches on the state of the window. Supported states are: `active`, `focused`, `needs_attention`, `parent_active`, `parent_focused`, `focused_os_window`, `self`, `overlay_parent`. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value `focused_os_window` matches all windows in the currently focused OS window. The value `self` matches the window in which the remote control command is run. The value `overlay_parent` matches the window that is under the `self` window, when the self window is an overlay.

Note that you can use the [kitten @ ls](https://sw.kovidgoyal.net/kitty/remote-control/#at-ls) command to get a list of windows.

[

](https://sw.kovidgoyal.net/kitty/rc_protocol/)



# The kitty remote control protocol

The kitty remote control protocol is a simple protocol that involves sending data to kitty in the form of JSON. Any individual command of kitty has the form:

<ESC>P@kitty-cmd<JSON object><ESC>\

Where `<ESC>` is the byte `0x1b`. The JSON object has the form:

{
    "cmd": "command name",
    "version": "<kitty version>",
    "no_response": "<Optional Boolean>",
    "kitty_window_id": "<Optional value of the KITTY_WINDOW_ID env var>",
    "payload": "<Optional JSON object>"
}

The `version` above is an array of the form `[0, 14, 2]`. If you are developing a standalone client, use the kitty version that you are developing against. Using a version greater than the version of the kitty instance you are talking to, will cause a failure.

Set `no_response` to `true` if you don’t want a response from kitty.

The optional payload is a JSON object that is specific to the actual command being sent. The fields in the object for every command are documented below.

As a quick example showing how easy to use this protocol is, we will implement the `@ ls` command from the shell using only shell tools.

First, run kitty as:

kitty -o allow_remote_control=socket-only --listen-on unix:/tmp/test

Now, in a different terminal, you can get the pretty printed `@ ls` output with the following command line:

echo -en '\eP@kitty-cmd{"cmd":"ls","version":[0,14,2]}\e\\' | socat - unix:/tmp/test | awk '{ print substr($0, 13, length($0) - 14) }' | jq -c '.data | fromjson' | jq .

There is also the statically compiled stand-alone executable `kitten` that can be used for this, available from the [kitty releases](https://github.com/kovidgoyal/kitty/releases) page:

kitten @ --help

## Encrypted communication

Added in version 0.26.0.

When using the [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password) option communication to the terminal is encrypted to keep the password secure. A public key is used from the [`KITTY_PUBLIC_KEY`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_PUBLIC_KEY) environment variable. Currently, only one encryption protocol is supported. The protocol number is present in [`KITTY_PUBLIC_KEY`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_PUBLIC_KEY) as `1`. The key data in this environment variable is [**Base-85**](https://datatracker.ietf.org/doc/html/rfc1924.html) encoded. The algorithm used is [Elliptic Curve Diffie Helman](https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman) with the [X25519 curve](https://en.wikipedia.org/wiki/Curve25519). A time based nonce is used to minimise replay attacks. The original JSON command has the fields: `password` and `timestamp` added. The timestamp is the number of nanoseconds since the epoch, excluding leap seconds. Commands with a timestamp more than 5 minutes from the current time are rejected. The command is then encrypted using AES-256-GCM in authenticated encryption mode, with a symmetric key that is derived from the ECDH key-pair by running the shared secret through SHA-256 hashing, once. An IV of at least 96 bits of CSPRNG data is used. The tag for authenticated encryption **must** be at least 128 bits long. The tag **must** authenticate only the value of the `encrypted` field. A new command is created and transmitted that contains the fields:

{
    "version": "<kitty version>",
    "iv": "base85 encoded IV",
    "tag": "base85 encoded AEAD tag",
    "pubkey": "base85 encoded ECDH public key of sender",
    "encrypted": "The original command encrypted and base85 encoded"
}

## Async and streaming requests

Some remote control commands require asynchronous communication, that is, the response from the terminal can happen after an arbitrary amount of time. For example, the `select-window` command requires the user to select a window before a response can be sent. Such command must set the field `async` in the JSON block above to a random string that serves as a unique id. The client can cancel an async request in flight by adding the `cancel_async` field to the JSON block. A async response remains in flight until the terminal sends a response to the request. Note that cancellation requests dont need to be encrypted as users must not be prompted for these and the worst a malicious cancellation request can do is prevent another sync request from getting a response.

Similar to async requests are *streaming* requests. In these the client has to send a large amount of data to the terminal and so the request is split into chunks. In every chunk the JSON block must contain the field `stream` set to `true` and `stream_id` set to a random long string, that should be the same for all chunks in a request. End of data is indicated by sending a chunk with no data.

## action

Fields are:

`action (required)`

The action to perform. Of the form: action [optional args…]

`match_window (optional)`

Window to run the action on

`self (default: False)`

Whether to use the window this command is run in as the active window

## close-tab

Fields are:

`match (default: None)`

Which tab to close

`self (default: False)`

Boolean indicating whether to close the tab of the window the command is run in

`ignore_no_match (default: False)`

Boolean indicating whether no matches should be ignored or return an error

## close-window

Fields are:

`match (default: None)`

Which window to close

`self (default: False)`

Boolean indicating whether to close the window the command is run in

`ignore_no_match (default: False)`

Boolean indicating whether no matches should be ignored or return an error

## create-marker

Fields are:

`match (default: None)`

Which window to create the marker in

`self (default: False)`

Boolean indicating whether to create marker in the window the command is run in

`marker_spec (optional)`

A list or arguments that define the marker specification, for example: [‘text’, ‘1’, ‘ERROR’]

## detach-tab

Fields are:

`match (default: None)`

Which tab to detach

`target_tab (default: None)`

Which tab to move the detached tab to the OS window it is run in

`self (default: False)`

Boolean indicating whether to detach the tab the command is run in

## detach-window

Fields are:

`match (default: None)`

Which window to detach

`target_tab (default: None)`

Which tab to move the detached window to

`self (default: False)`

Boolean indicating whether to detach the window the command is run in

`stay_in_tab (default: False)`

Boolean indicating focus should remain in the active tab after windows are moved

## disable-ligatures

Fields are:

`strategy (required)`

One of `never`, `always` or `cursor`

`match_window (optional)`

Window to change opacity in

`match_tab (default: None)`

Tab to change opacity in

`all (default: False)`

Boolean indicating operate on all windows

## env

Fields are:

`env (required)`

Dictionary of environment variables to values. When a env var ends with = it is removed from the environment.

## focus-tab

Fields are:

`match (default: None)`

The tab to focus

## focus-window

Fields are:

`match (default: None)`

The window to focus

## get-colors

Fields are:

`match (default: None)`

The window to get the colors for

`configured (default: False)`

Boolean indicating whether to get configured or current colors

## get-text

Fields are:

`match (default: None)`

The window to get text from

`extent (default: screen)`

One of `screen`, `first_cmd_output_on_screen`, `last_cmd_output`, `last_visited_cmd_output`, `all`, or `selection`

`ansi (default: False)`

Boolean, if True send ANSI formatting codes

`cursor (optional)`

Boolean, if True send cursor position/style as ANSI codes

`wrap_markers (optional)`

Boolean, if True add wrap markers to output

`clear_selection (default: False)`

Boolean, if True clear the selection in the matched window

`self (default: False)`

Boolean, if True use window the command was run in

## goto-layout

Fields are:

`layout (required)`

The new layout name

`match (default: None)`

Which tab to change the layout of

## kitten

Fields are:

`kitten (required)`

The name of the kitten to run

`args (optional)`

Arguments to pass to the kitten as a list

`match (default: None)`

The window to run the kitten over

## last-used-layout

Fields are:

`match (default: None)`

Which tab to change the layout of

`all (default: False)`

Boolean to match all tabs

## launch

Fields are:

`args (required)`

The command line to run in the new window, as a list, use an empty list to run the default shell

`match (default: None)`

The tab to open the new window in

`next_to (default: None)`

The window next to which to create the new window or empty string to use active window

`source_window (default: None)`

The window to use as source for data or empty string to use active window

`window_title (default: None)`

Title for the new window

`cwd (default: None)`

Working directory for the new window

`add_to_session (default: None)`

Session name to add created window/tab to

`env (default: [])`

List of environment variables of the form NAME=VALUE

`var (default: [])`

List of user variables of the form NAME=VALUE

`os_panel (default: [])`

List of panel settings

`tab_title (default: None)`

Title for the new tab

`type (default: window)`

The type of window to open

`keep_focus (default: False)`

Boolean indicating whether the current window should retain focus or not

`copy_colors (default: False)`

Boolean indicating whether to copy the colors from the current window

`copy_cmdline (default: False)`

Boolean indicating whether to copy the cmdline from the current window

`copy_env (default: False)`

List of strings representing the local env vars

`hold (default: False)`

Boolean indicating whether to keep window open after cmd exits

`location (default: default)`

Where in the tab to open the new window

`allow_remote_control (default: False)`

Boolean indicating whether to allow remote control from the new window

`remote_control_password (default: [])`

A list of remote control passwords

`stdin_source (default: none)`

Where to get stdin for the process from

`stdin_add_formatting (default: False)`

Boolean indicating whether to add formatting codes to stdin

`stdin_add_line_wrap_markers (default: False)`

Boolean indicating whether to add line wrap markers to stdin

`spacing (default: [])`

A list of spacing specifications, see the docs for the set-spacing command

`marker (default: None)`

Specification for marker for new window, for example: “text 1 ERROR”

`logo (default: None)`

Path to window logo

`logo_position (default: None)`

Window logo position as string or empty string to use default

`logo_alpha (default: -1.0)`

Window logo alpha or -1 to use default

`self (default: False)`

Boolean, if True use tab the command was run in

`os_window_title (default: None)`

Title for OS Window

`os_window_name (default: None)`

WM_NAME for OS Window

`os_window_class (default: None)`

WM_CLASS for OS Window

`os_window_state (default: normal)`

The initial state for OS Window

`color (default: [])`

list of color specifications such as foreground=red

`watcher (default: [])`

list of paths to watcher files

`bias (default: 0.0)`

The bias with which to create the new window in the current layout

`wait_for_child_to_exit (default: False)`

Boolean indicating whether to wait and return child exit code

`hold_after_ssh (default: False)`

Boolean indicating whether to run a local shell after exiting the ssh session cloned via cwd=current or similar

## load-config

Fields are:

`paths (optional)`

List of config file paths to load

`override (default: [])`

List of individual config overrides

`ignore_overrides (default: False)`

Whether to apply previous overrides

## ls

Fields are:

`all_env_vars (default: False)`

Whether to send all environment variables for every window rather than just differing ones

`match (default: None)`

Window to change colors in

`match_tab (default: None)`

Tab to change colors in

`self (default: False)`

Boolean indicating whether to list only the window the command is run in

`output_format (default: json)`

Output in json or session format

## new-window

Fields are:

`args (required)`

The command line to run in the new window, as a list, use an empty list to run the default shell

`match (default: None)`

The tab to open the new window in

`title (default: None)`

Title for the new window

`cwd (default: None)`

Working directory for the new window

`keep_focus (default: False)`

Boolean indicating whether the current window should retain focus or not

`window_type (default: kitty)`

One of `kitty` or `os`

`new_tab (default: False)`

Boolean indicating whether to open a new tab

`tab_title (default: None)`

Title for the new tab

## remove-marker

Fields are:

`match (default: None)`

Which window to remove the marker from

`self (default: False)`

Boolean indicating whether to detach the window the command is run in

## resize-os-window

Fields are:

`match (default: None)`

Which window to resize

`self (default: False)`

Boolean indicating whether to close the window the command is run in

`incremental (default: False)`

Boolean indicating whether to adjust the size incrementally

`action (default: resize)`

The action to perform

`unit (default: cells)`

One of `cells` or `pixels`

`width (default: 0)`

Integer indicating desired window width

`height (default: 0)`

Integer indicating desired window height

`os_panel (optional)`

Settings for modifying the OS Panel

## resize-window

Fields are:

`match (default: None)`

Which window to resize

`self (default: False)`

Boolean indicating whether to resize the window the command is run in

`increment (default: 2)`

Integer specifying the resize increment

`axis (default: horizontal)`

One of `horizontal, vertical` or `reset`

## run

Fields are:

`data (required)`

Chunk of STDIN data, base64 encoded no more than 4096 bytes. Must send an empty chunk to indicate end of data.

`cmdline (required)`

The command line to run

`env (default: [])`

List of environment variables of the form NAME=VALUE

`allow_remote_control (default: False)`

A boolean indicating whether to allow remote control

`remote_control_password (default: [])`

A list of remote control passwords

## scroll-window

> for unscrolling by lines, or ‘r’ for scrolling ot prompt.

Fields are:

`amount (required)`

The amount to scroll, a two item list with the first item being either a number or the keywords, start and end. And the second item being either ‘p’ for pages or ‘l’ for lines or ‘u’

`match (default: None)`

The window to scroll

## select-window

Fields are:

`match (default: None)`

The tab to open the new window in

`self (default: False)`

Boolean, if True use tab the command was run in

`title (default: None)`

A title for this selection

`exclude_active (default: False)`

Exclude the currently active window from the list to pick

`reactivate_prev_tab (default: False)`

Reactivate the previously activated tab when finished

## send-key

Fields are:

`keys (required)`

The keys to send

`match (default: None)`

A string indicating the window to send text to

`match_tab (default: None)`

A string indicating the tab to send text to

`all (default: False)`

A boolean indicating all windows should be matched.

`exclude_active (default: False)`

A boolean that prevents sending text to the active window

## send-text

Fields are:

`data (required)`

The data being sent. Can be either: text: followed by text or base64: followed by standard base64 encoded bytes

`match (default: None)`

A string indicating the window to send text to

`match_tab (default: None)`

A string indicating the tab to send text to

`all (default: False)`

A boolean indicating all windows should be matched.

`exclude_active (default: False)`

A boolean that prevents sending text to the active window

`session_id (optional)`

A string that identifies a “broadcast session”

`bracketed_paste (default: disable)`

Whether to wrap the text in bracketed paste escape codes

## set-background-image

Fields are:

`data (required)`

Chunk of at most 512 bytes of PNG data, base64 encoded. Must send an empty chunk to indicate end of image. Or the special value - to indicate image must be removed.

`match (default: None)`

Window to change opacity in

`layout (default: configured)`

The image layout

`all (default: False)`

Boolean indicating operate on all windows

`configured (default: False)`

Boolean indicating if the configured value should be changed

## set-background-opacity

Fields are:

`opacity (required)`

A number between 0 and 1

`match_window (optional)`

Window to change opacity in

`match_tab (default: None)`

Tab to change opacity in

`all (default: False)`

Boolean indicating operate on all windows

`toggle (default: False)`

Boolean indicating if opacity should be toggled between the default and the specified value

## set-colors

Fields are:

`colors (required)`

An object mapping names to colors as 24-bit RGB integers or null for nullable colors. Or a string for transparent_background_colors.

`match_window (optional)`

Window to change colors in

`match_tab (default: None)`

Tab to change colors in

`all (default: False)`

Boolean indicating change colors everywhere or not

`configured (default: False)`

Boolean indicating whether to change the configured colors. Must be True if reset is True

`reset (default: False)`

Boolean indicating colors should be reset to startup values

## set-enabled-layouts

Fields are:

`layouts (required)`

The list of layout names

`match (default: None)`

Which tab to change the layout of

`configured (default: False)`

Boolean indicating whether to change the configured value

## set-font-size

Fields are:

`size (required)`

The new font size in pts (a positive number). If absent is assumed to be zero which means reset to default.

`all (default: False)`

Boolean whether to change font size in the current window or all windows

`increment_op (optional)`

The string `+`, `-`, `*` or `/` to interpret size as an increment

## set-spacing

Fields are:

`settings (required)`

An object mapping margins/paddings using canonical form {‘margin-top’: 50, ‘padding-left’: null} etc

`match_window (optional)`

Window to change paddings and margins in

`match_tab (default: None)`

Tab to change paddings and margins in

`all (default: False)`

Boolean indicating change paddings and margins everywhere or not

`configured (default: False)`

Boolean indicating whether to change the configured paddings and margins. Must be True if reset is True

## set-tab-color

Fields are:

`colors (required)`

An object mapping names to colors as 24-bit RGB integers. A color value of null indicates it should be unset.

`match (default: None)`

Which tab to change the color of

`self (default: False)`

Boolean indicating whether to use the tab of the window the command is run in

## set-tab-title

Fields are:

`title (required)`

The new title

`match (default: None)`

Which tab to change the title of

## set-user-vars

Fields are:

`var (optional)`

List of user variables of the form NAME=VALUE

`match (default: None)`

Which windows to change the title in

## set-window-logo

Fields are:

`data (required)`

Chunk of PNG data, base64 encoded no more than 2048 bytes. Must send an empty chunk to indicate end of image. Or the special value `-` to indicate image must be removed.

`position (default: None)`

The logo position as a string, empty string means default

`alpha (default: -1.0)`

The logo alpha between `0` and `1`. `-1` means use default

`match (default: None)`

Which window to change the logo in

`self (default: False)`

Boolean indicating whether to act on the window the command is run in

## set-window-title

Fields are:

`title (optional)`

The new title

`match (default: None)`

Which windows to change the title in

`temporary (default: False)`

Boolean indicating if the change is temporary or permanent

## signal-child

Fields are:

`signals (required)`

The signals, a list of names, such as `SIGTERM`, `SIGKILL`, `SIGUSR1`, etc.

`match (default: None)`

Which windows to send the signals to





# The **launch** command

*kitty* has a `launch` action that can be used to run arbitrary programs in new windows/tabs. It can be mapped to user defined shortcuts in `kitty.conf`. It is very powerful and allows sending the contents of the current window to the launched program, as well as many other options.

In the simplest form, you can use it to open a new kitty window running the shell, as shown below:

map f1 launch

To run a different program simply pass the command line as arguments to launch:

map f1 launch vim path/to/some/file

To open a new window with the same working directory as the currently active window:

map f1 launch --cwd=current

To open the new window in a new tab:

map f1 launch --type=tab

To run multiple commands in a shell, use:

map f1 launch sh -c "ls && exec zsh"

To pass the contents of the current screen and scrollback to the started process:

map f1 launch --stdin-source=@screen_scrollback less

There are many more powerful options, refer to the complete list below.

Note

To avoid duplicating launch actions with frequently used parameters, you can use [`action_alias`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.action_alias) to define launch action aliases. For example:

action_alias launch_tab launch --cwd=current --type=tab
map f1 launch_tab vim
map f2 launch_tab emacs

The F1 key will now open **vim** in a new tab with the current windows working directory.

# The piping environment

When using [`launch --stdin-source`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-stdin-source), the program to which the data is piped has a special environment variable declared, [`KITTY_PIPE_DATA`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_PIPE_DATA) whose contents are:

KITTY_PIPE_DATA={scrolled_by}:{cursor_x},{cursor_y}:{lines},{columns}

where `scrolled_by` is the number of lines kitty is currently scrolled by, `cursor_(x|y)` is the position of the cursor on the screen with `(1,1)` being the top left corner and `{lines},{columns}` being the number of rows and columns of the screen.

# Special arguments

There are a few special placeholder arguments that can be specified as part of the command line:

`@selection`

Replaced by the currently selected text.

`@active-kitty-window-id`

Replaced by the id of the currently active kitty window.

`@line-count`

Replaced by the number of lines in STDIN. Only present when passing some data to STDIN.

`@input-line-number`

Replaced by the number of lines a pager should scroll to match the current scroll position in kitty. See [`scrollback_pager`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.scrollback_pager) for details.

`@scrolled-by`

Replaced by the number of lines kitty is currently scrolled by.

`@cursor-x`

Replaced by the current cursor x position with 1 being the leftmost cell.

`@cursor-y`

Replaced by the current cursor y position with 1 being the topmost cell.

`@first-line-on-screen`

Replaced by the first line on screen. Can be used for pager positioning.

`@last-line-on-screen`

Replaced by the last line on screen. Can be used for pager positioning.

For example:

map f1 launch my-program @active-kitty-window-id

# Watching launched windows

The [`launch --watcher`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-watcher) option allows you to specify Python functions that will be called at specific events, such as when the window is resized or closed. Note that you can also specify watchers that are loaded for all windows, via [`watcher`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.watcher). To create a watcher, specify the path to a Python module that specifies callback functions for the events you are interested in, for create `~/.config/kitty/mywatcher.py` and use [`launch --watcher`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-watcher) = `mywatcher.py`:

# ~/.config/kitty/mywatcher.py

from typing import Any

from kitty.boss import Boss
from kitty.window import Window

def on_load(boss: Boss, data: dict[str, Any]) -> None:
    # This is a special function that is called just once when this watcher
    # module is first loaded, can be used to perform any initialization/one
    # time setup. Any exceptions in this function are printed to kitty's
    # STDERR but otherwise ignored.
    ...

def on_resize(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    # Here data will contain old_geometry and new_geometry
    # Note that resize is also called the first time a window is created
    # which can be detected as old_geometry will have all zero values, in
    # particular, old_geometry.xnum and old_geometry.ynum will be zero.
    ...

def on_focus_change(boss: Boss, window: Window, data: dict[str, Any])-> None:
    # Here data will contain focused
    ...

def on_close(boss: Boss, window: Window, data: dict[str, Any])-> None:
    # called when window is closed, typically when the program running in
    # it exits
    ...

def on_set_user_var(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    # called when a "user variable" is set or deleted on a window. Here
    # data will contain key and value
    ...

def on_title_change(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    # called when the window title is changed on a window. Here
    # data will contain title and from_child. from_child will be True
    # when a title change was requested via escape code from the program
    # running in the terminal
    ...

def on_cmd_startstop(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    # called when the shell starts/stops executing a command. Here
    # data will contain is_start, cmdline and time.
    ...

def on_color_scheme_preference_change(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    # called when the color scheme preference of this window changes from
    # light to dark or vice versa. data contains is_dark and via_escape_code
    # the latter will be true if the color scheme was changed via escape
    # code received from the program running in the window
    ...

def on_tab_bar_dirty(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    # called when any changes happen to the tab bar, such a new tabs being
    # created, tab titles changing, tabs moving, etc. Useful to display the
    # tab bar externally to kitty. This is called even if the tab bar is
    # hidden. Note that this is called only in *global watchers*, that is
    # watchers defined in kitty.conf or using the --watcher command line
    # flag. data contains tab_manager which is the object responsible for
    # managing all tabs in a single OS Window.
    ...

Every callback is passed a reference to the global `Boss` object as well as the `Window` object the action is occurring on. The `data` object is a dict that contains event dependent data. You have full access to kitty internals in the watcher scripts, however kitty internals are not documented/stable so for most things you are better off using the kitty [Remote control API](https://sw.kovidgoyal.net/kitty/remote-control/). Simply call `boss.call_remote_control()`, with the same arguments you would pass to `kitten @`. For example:

def on_resize(boss: Boss, window: Window, data: dict[str, Any]) -> None:
    # send some text to the resized window
    boss.call_remote_control(window, ('send-text', f'--match=id:{window.id}', 'hello world'))

Run, `kitten @ --help` in a kitty terminal, to see all the remote control commands available to you.

# Finding executables

When you specify a command to run as just a name rather than an absolute path, it is searched for in the system-wide [`PATH`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-PATH) environment variable. Note that this **may not** be the value of [`PATH`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-PATH) inside a shell, as shell startup scripts often change the value of this variable. If it is not found there, then a system specific list of default paths is searched. If it is still not found, then your shell is run and the value of [`PATH`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-PATH) inside the shell is used.

See [`exe_search_path`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.exe_search_path) for details and how to control this.

# Syntax reference

launch [options] [program-to-run ...]

Launch an arbitrary program in a new kitty window/tab. Note that if you specify a program-to-run you can use the special placeholder `@selection` which will be replaced by the current selection.

## Options

--source-window <SOURCE_WINDOW>

A match expression to select the window from which data such as title, colors, env vars, screen contents, etc. are copied. When not specified the currently active window is used. See [Matching windows and tabs](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax) for the syntax used for specifying windows.

--title <WINDOW_TITLE>, --window-title <WINDOW_TITLE>

The title to set for the new window. By default, title is controlled by the child process. The special value `current` will copy the title from the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

--tab-title <TAB_TITLE>

The title for the new tab if launching in a new tab. By default, the title of the active window in the tab is used as the tab title. The special value `current` will copy the title from the tab containing the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

--type <TYPE>

Where to launch the child process:

`window`

A new [kitty window](https://sw.kovidgoyal.net/kitty/glossary/#term-window) in the current tab

`tab`

A new [tab](https://sw.kovidgoyal.net/kitty/glossary/#term-tab) in the current OS window. Not available when the [launch](https://sw.kovidgoyal.net/kitty/launch/#) command is used in [startup sessions](https://sw.kovidgoyal.net/kitty/sessions/#sessions).

`os-window`

A new [operating system window](https://sw.kovidgoyal.net/kitty/glossary/#term-os_window). Not available when the [launch](https://sw.kovidgoyal.net/kitty/launch/#) command is used in [startup sessions](https://sw.kovidgoyal.net/kitty/sessions/#sessions).

`overlay`

An [overlay window](https://sw.kovidgoyal.net/kitty/glossary/#term-overlay) covering the current active kitty window

`overlay-main`

An [overlay window](https://sw.kovidgoyal.net/kitty/glossary/#term-overlay) covering the current active kitty window. Unlike a plain overlay window, this window is considered as a main window which means it is used as the active window for getting the current working directory, the input text for kittens, launch commands, etc. Useful if this overlay is intended to run for a long time as a primary window.

`background`

The process will be run in the background, without a kitty window. Note that if [`kitten @ launch --allow-remote-control`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-allow-remote-control) is specified the [`KITTY_LISTEN_ON`](https://sw.kovidgoyal.net/kitty/glossary/#envvar-KITTY_LISTEN_ON) environment variable will be set to a dedicated socket pair file descriptor that the process can use for remote control.

`clipboard`, `primary`

These two are meant to work with [`--stdin-source`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-stdin-source) to copy data to the system clipboard or primary selection.

`os-panel`

Similar to `os-window`, except that it creates the new OS Window as a desktop panel. Only works on platforms that support this, such as Wayand compositors that support the layer shell protocol. Use the [`kitten @ launch --os-panel`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-os-panel) option to configure the panel.

Default: `window` Choices: `background`, `clipboard`, `os-panel`, `os-window`, `overlay`, `overlay-main`, `primary`, `tab`, `window`

--dont-take-focus [=no], --keep-focus [=no]

Keep the focus on the currently active window instead of switching to the newly opened window.

--cwd <CWD>

The working directory for the newly launched child. Use the special value `current` to use the working directory of the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window). The special value `last_reported` uses the last working directory reported by the shell (needs [Shell integration](https://sw.kovidgoyal.net/kitty/shell-integration/#shell-integration) to work). The special value `oldest` works like `current` but uses the working directory of the oldest foreground process associated with the currently active window rather than the newest foreground process. Finally, the special value `root` refers to the process that was originally started when the window was created.

When opening in the same working directory as the current window causes the new window to connect to a remote host, you can use the [`--hold-after-ssh`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-hold-after-ssh) flag to prevent the new window from closing when the connection is terminated.

--add-to-session <ADD_TO_SESSION>

Add the newly created window/tab to the specified session. Use `.` to add to the session of the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window), if any. See [Sessions](https://sw.kovidgoyal.net/kitty/sessions/#sessions) for what a session is and how to use one. By default, the window is added to the session of the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window) when [`launch --cwd`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-cwd) is set to use the the working directory from that window, otherwise the newly created window does not belong to any session. To force adding to no session, use the value `!`. Adding a newly created window to a session is purely temporary, it does not change the actual session file, for that you have to resave the session. Note that using this flag in a launch command within a session file has no effect as the window is always added to the session belonging to that file.

--env <ENV>

Environment variables to set in the child process. Can be specified multiple times to set different environment variables. Syntax: `name=value`. Using `name=` will set to empty string and just `name` will remove the environment variable.

--var <VAR>

User variables to set in the created window. Can be specified multiple times to set different user variables. Syntax: `name=value`. Using `name=` will set to empty string.

--hold [=no]

Keep the window open even after the command being executed exits, at a shell prompt. The shell will be run after the launched command exits.

--copy-colors [=no]

Set the colors of the newly created window to be the same as the colors in the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

--copy-cmdline [=no]

Ignore any specified command line and instead use the command line from the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

--copy-env [=no]

Copy the environment variables from the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window) into the newly launched child process. Note that this only copies the environment when the window was first created, as it is not possible to get updated environment variables from arbitrary processes. To copy that environment, use either the [clone-in-kitty](https://sw.kovidgoyal.net/kitty/shell-integration/#clone-shell) feature or the kitty remote control feature with [`kitten @ launch --copy-env`](https://sw.kovidgoyal.net/kitty/remote-control/#cmdoption-kitten-launch-copy-env).

--location <LOCATION>

Where to place the newly created window when it is added to a tab which already has existing windows in it. `after` and `before` place the new window before or after the active window. `neighbor` is a synonym for `after`. Also applies to creating a new tab, where the value of `after` will cause the new tab to be placed next to the current tab instead of at the end. The values of `vsplit`, `hsplit` and `split` are only used by the `splits` layout and control if the new window is placed in a vertical, horizontal or automatic split with the currently active window. The default is to place the window in a layout dependent manner, typically, after the currently active window. See [`--next-to`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-next-to) to use a window other than the currently active window. Default: `default` Choices: `after`, `before`, `default`, `first`, `hsplit`, `last`, `neighbor`, `split`, `vsplit`

--next-to <NEXT_TO>

A match expression to select the window next to which the new window is created. See [Matching windows and tabs](https://sw.kovidgoyal.net/kitty/remote-control/#search-syntax) for the syntax for specifying windows. If not specified defaults to the active window. When used via remote control and a target tab is specified this option is ignored unless the matched window is in the specified tab. When using [`--type`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-type) of `tab`, the tab will be created in the OS Window containing the matched window.

--bias <BIAS>

The bias used to alter the size of the window. It controls what fraction of available space the window takes. The exact meaning of bias depends on the current layout.

- Splits layout: The bias is interpreted as a percentage between 0 and 100. When splitting a window into two, the new window will take up the specified fraction of the space allotted to the original window and the original window will take up the remainder of the space.

- Vertical/horizontal layout: The bias is interpreted as adding/subtracting from the normal size of the window. It should be a number between -90 and 90. This number is the percentage of the OS Window size that should be added to the window size. So for example, if a window would normally have been size 50 in the layout inside an OS Window that is size 80 high and --bias -10 is used it will become *approximately* size 42 high. Note that sizes are approximations, you cannot use this method to create windows of fixed sizes.

- Tall layout: If the window being created is the *first* window in a column, then the bias is interpreted as a percentage, as for the splits layout, splitting the OS Window width between columns. If the window is a second or subsequent window in a column the bias is interpreted as adding/subtracting from the window size as for the vertical layout above.

- Fat layout: Same as tall layout except it goes by rows instead of columns.

- Grid layout: The bias is interpreted the same way as for the Vertical and Horizontal layouts, as something to be added/subtracted to the normal size. However, the since in a grid layout there are rows *and* columns, the bias on the first window in a column operates on the columns. Any later windows in that column operate on the row. So, for example, if you bias the first window in a grid layout it will change the width of the first column, the second window, the width of the second column, the third window, the height of the second row and so on.

The bias option was introduced in kitty version 0.36.0. Default: `0`

--allow-remote-control [=no]

Programs running in this window can control kitty (even if remote control is not enabled in `kitty.conf`). Note that any program with the right level of permissions can still write to the pipes of any other program on the same computer and therefore can control kitty. It can, however, be useful to block programs running on other computers (for example, over SSH) or as other users. See [`--remote-control-password`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-remote-control-password) for ways to restrict actions allowed by remote control.

--remote-control-password <REMOTE_CONTROL_PASSWORD>

Restrict the actions remote control is allowed to take. This works like [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password). You can specify a password and list of actions just as for [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password). For example:

--remote-control-password '"my passphrase" get-* set-colors'

This password will be in effect for this window only. Note that any passwords you have defined for [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password) in `kitty.conf` are also in effect. You can override them by using the same password here. You can also disable all [`remote_control_password`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.remote_control_password) global passwords for this window, by using:

--remote-control-password '!'

This option only takes effect if [`--allow-remote-control`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-allow-remote-control) is also specified. Can be specified multiple times to create multiple passwords. This option was added to kitty in version 0.26.0

--stdin-source <STDIN_SOURCE>

Pass the screen contents as `STDIN` to the child process.

`@selection`

is the currently selected text in the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

`@screen`

is the contents of the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

`@screen_scrollback`

is the same as `@screen`, but includes the scrollback buffer as well.

`@alternate`

is the secondary screen of the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window). For example if you run a full screen terminal application, the secondary screen will be the screen you return to when quitting the application.

`@first_cmd_output_on_screen`

is the output from the first command run in the shell on screen.

`@last_cmd_output`

is the output from the last command run in the shell.

`@last_visited_cmd_output`

is the first output below the last scrolled position via [`scroll_to_prompt`](https://sw.kovidgoyal.net/kitty/actions/#action-scroll_to_prompt), this needs [shell integration](https://sw.kovidgoyal.net/kitty/shell-integration/#shell-integration) to work.

Default: `none` Choices: `@alternate`, `@alternate_scrollback`, `@first_cmd_output_on_screen`, `@last_cmd_output`, `@last_visited_cmd_output`, `@screen`, `@screen_scrollback`, `@selection`, `none`

--stdin-add-formatting [=no]

When using [`--stdin-source`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-stdin-source) add formatting escape codes, without this only plain text will be sent.

--stdin-add-line-wrap-markers [=no]

When using [`--stdin-source`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-stdin-source) add a carriage return at every line wrap location (where long lines are wrapped at screen edges). This is useful if you want to pipe to program that wants to duplicate the screen layout of the screen.

--marker <MARKER>

Create a marker that highlights text in the newly created window. The syntax is the same as for the [`toggle_marker`](https://sw.kovidgoyal.net/kitty/actions/#action-toggle_marker) action (see [Mark text on screen](https://sw.kovidgoyal.net/kitty/marks/)).

--os-window-class <OS_WINDOW_CLASS>

Set the WM_CLASS property on X11 and the application id property on Wayland for the newly created OS window when using [`--type=os-window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-type). Defaults to whatever is used by the parent kitty process, which in turn defaults to `kitty`.

--os-window-name <OS_WINDOW_NAME>

Set the WM_NAME property on X11 for the newly created OS Window when using [`--type=os-window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-type). Defaults to [`--os-window-class`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-os-window-class).

--os-window-title <OS_WINDOW_TITLE>

Set the title for the newly created OS window. This title will override any titles set by programs running in kitty. The special value `current` will copy the title from the OS Window containing the [`source window`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-source-window).

--os-window-state <OS_WINDOW_STATE>

The initial state for the newly created OS Window. Default: `normal` Choices: `fullscreen`, `maximized`, `minimized`, `normal`

--logo <LOGO>

Path to a PNG image to use as the logo for the newly created window. See [`window_logo_path`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.window_logo_path). Relative paths are resolved from the kitty configuration directory.

--logo-position <LOGO_POSITION>

The position for the window logo. Only takes effect if [`--logo`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-logo) is specified. See [`window_logo_position`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.window_logo_position).

--logo-alpha <LOGO_ALPHA>

The amount the window logo should be faded into the background. Only takes effect if [`--logo`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-logo) is specified. See [`window_logo_alpha`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.window_logo_alpha). Default: `-1`

--color <COLOR>

Change colors in the newly launched window. You can either specify a path to a `.conf` file with the same syntax as `kitty.conf` to read the colors from, or specify them individually, for example:

--color background=white --color foreground=red

--spacing <SPACING>

Set the margin and padding for the newly created window. For example: `margin=20` or `padding-left=10` or `margin-h=30`. The shorthand form sets all values, the `*-h` and `*-v` variants set horizontal and vertical values. Can be specified multiple times. Note that this is ignored for overlay windows as these use the settings from the base window.

--watcher <WATCHER>, -w <WATCHER>

Path to a Python file. Appropriately named functions in this file will be called for various events, such as when the window is resized, focused or closed. See the section on watchers in the launch command documentation: [Watching launched windows](https://sw.kovidgoyal.net/kitty/launch/#watchers). Relative paths are resolved relative to the [kitty config directory](https://sw.kovidgoyal.net/kitty/conf/#confloc). Global watchers for all windows can be specified with [`watcher`](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.watcher) in `kitty.conf`.

--os-panel <OS_PANEL>

Options to control the creation of desktop panels. Takes the same settings as the [panel kitten](https://sw.kovidgoyal.net/kitty/kittens/panel/), except for [`--override`](https://sw.kovidgoyal.net/kitty/kittens/panel/#cmdoption-kitty-kitten-panel-override) and [`--config`](https://sw.kovidgoyal.net/kitty/kittens/panel/#cmdoption-kitty-kitten-panel-config). Can be specified multiple times. For example, to create a desktop panel at the bottom of the screen two lines high:

launch --type os-panel --os-panel lines=2 --os-panel edge=bottom sh -c "echo; echo; echo hello; sleep 5s"

--hold-after-ssh [=no]

When using [`--cwd`](https://sw.kovidgoyal.net/kitty/launch/#cmdoption-launch-cwd)`=current` or similar from a window that is running the ssh kitten, the new window will run a local shell after disconnecting from the remote host, when this option is specified.




