# some other useful imports
import datetime, re, shlex, sys
# add DoX core to path
sys.path.append("dox")
# main class import
from dox import *
# utility functions
from util import *

class main:
    dox = None
    needSave = False
    def __init__(self):
        # create DoX API object
        self.dox = dox()
        args = sys.argv[1:]
        # no arguments, default to list
        if not len(args):
            args = ["list"]
        self.cmd(args, False)
        # save after action
        self.dox.saveTasks()
    def cmd(self, args, shell):
        args[0] = args[0].lower()
        print("")
        if shell:
            # load before action
            self.dox.loadTasks()
        # trying to use "dox" in a shell
        if args[0] == "dox" and shell:
            print("You don't need to prefix commands with \"dox\" here.")
        # show a list of all tasks
        elif args[0] in ["list", "ls", "l", "tasks", "all"]:
            self.list(args)
        # add a new task to the list
        elif args[0] in ["add", "a", "new", "task"]:
            self.add(args)
        # edit an existing task
        elif args[0] in ["edit", "e", "change"]:
            self.edit(args)
        # show info about the task
        elif args[0] in ["info", "i", "details"]:
            self.info(args)
        # move a task in the list
        elif args[0] in ["move", "m", "reorder"]:
            self.move(args)
        # mark a task as complete
        elif args[0] in ["done", "do", "d"]:
            self.done(args)
        # unmark a task as complete
        elif args[0] in ["undo", "undone", "u"]:
            self.undo(args)
        # remove a task without completing
        elif args[0] in ["delete", "del", "remove", "r", "x"]:
            self.delete(args)
        # interactive DoX shell
        elif args[0] in ["shell", "sh", "cmd", "dox"]:
            # no recursion allowed
            if shell:
                print("You can't launch a shell from a shell...")
            else:
                # welcome message
                print("DoX interactive shell: type \"help\" for a list of commands.\n")
                # enter shell loop
                while True:
                    try:
                        # get a command
                        args = shlex.split(raw_input("DoX > "))
                    # parse error (e.g. no closing quote)
                    except ValueError:
                        print("\nInvalid command; type \"help\" for a list of commands.\n")
                        args = []
                    if len(args):
                        # quit command
                        if args[0] in ["exit", "quit", "q", "qq"]:
                            # exit shell
                            sys.exit(0)
                        else:
                            # run command in shell mode
                            self.cmd(args, True)
                            # save after action
                            self.dox.saveTasks()
        # display command help
        elif args[0] in ["help", "h", "?"]:
            # display help with config file
            if len(args) > 1 and args[1] in ["config", "configuration", "settings"]:
                print("""New task options
----------------
* newTaskTags: list of tags to set if none given
* newTaskPriority: default priority to set if none given
* newTaskDue: default due date to set if none given
* newTaskRepeat: default repeat time to set if none given

Task list options
-----------------
* listSort: default sorting, use + or - to set direction""")
            # display full help on request
            elif len(args) > 1 and args[1] in ["more", "full", "doc", "docs", "man"]:
                # help text; prefix commands with "dox" when not in shell
                print("""{1}Commands
--------
{0}list [raw] [done] [+/-<field>] [!<pri>] [#<tag>] [@<due>]
{0}add [<title>] [~<desc>] [0|![![!]]|!<pri>] [@<due>] [&<repeat>[*]] [#<tag>]
{0}edit <id> [<title>] [~<desc>] [0|![![!]]|!<pri>] [@<due>] [&<repeat>[*]] [#<tag>]
{0}info <id>
{0}move <id> [<pos>]
{0}done|undo <id> [<id>...]
{0}del [<id>...] [<done>] [<id>...]
{2}

Listing your tasks
------------------
* Use `{0}list` to show all tasks in your list.
* Append `+<field to sort by>` for ascending sort, or `-<field>` for descending.
* Filter to specific tags by adding `#<tag>`.
* Filter by minimum priority by adding `!<pri>`.
* Only show tasks due on a certain date with `@<due>`.  Worded date expressions (e.g.
  "today", "next week", "overdue") are also valid.
* Mutliple sorts and filters can be used (sorts are applied in order).
* Use raw to show your tasks as DoX strings (as they would appear in tasks.txt).
* View more information on a task with `{0}info <id>`.
* Move tasks around in the list using `{0}move <id> <new position>`.

Adding tasks
------------
* Use `{0}add <title>` to add a quick task.
* Add a description by appending `~<description>`.
* Wrap multiple words in quotes.
* The priority can be set with `!<level>`, for a level between `0` and `3`.  You can
  also set the priority to `0`, or use up to three `!` marks for 1 to 3.
* Set a due date with `@<when>`.  Absolute and relative (eg. "tomorrow") dates/times
  are supported.  Split the date from the time using a `|`.
* Make the task repeat with `&<when>`.  Enter a number of days or a relative time (eg.
  "daily").  Repeats occur from the due date; append `*` to repeat from today instead.
* Assign tags using `#<tag>`.  Multiple tags are written `#<tag1> #<tag2>...`.

Completing tasks
----------------
* Use `{0}done <id>` to complete one or more tasks, and remove them from the list.
* Undo a task with `{0}undo <id>` (you can find the new ID with `{0}list done`).
* Use `{0}del <id>` to remove without completing.
* Delete completed tasks by writing `done` then the IDs.
* You can mix imcomplete and done task deletion with `{0}del <id> done <id>`. """.format(("" if shell else "dox "),
                                                            ("" if shell else "DoX: terminal to-do list manager\n================================\n\n"),
                                                            ("load|save\nhelp\nexit" if shell else "dox shell\ndox help")))
            # quick command help
            else:
                print("""{1}List your tasks: {0}list
Add a new task: {0}add [<title>] [~<desc>]
                [!<pri>] [@<due>] [&<repeat>[*]] [#<tag>]
Edit a task: {0}edit <id> [<title>] [~<desc>]
             [!<pri>] [@<due>] [&<repeat>[*]] [#<tag>]
Check info on a task: {0}info <id>
Mark a task as complete: {0}done <id>
Delete a task: {0}del <id>

Try `{0}help more` for the full help documentation.""".format(("" if shell else "dox "),
                                                              ("" if shell else "DoX: terminal to-do list manager\n================================\n\n")))
        # unrecognized command
        else:
            print("Unknown command \"{}\"; type \"{}help\" for a list of commands.".format(args[0], ("" if shell else "dox ")))
        print("")
    def list(self, args):
        tasks = self.dox.tasks
        # to handle after all arguments searched
        toSort = []
        toSub = []
        done = False
        raw = False
        # no arguments given in command, use from config
        if len(args) == 1:
            try:
                args.append(*shlex.split(self.dox.config["listSort"]))
            except:
                # no valid arguments
                args = ["list"]
        # loop arguments
        for i in range(1, len(args)):
            arg = args[i]
            # sort the list
            if re.match("^[\+-]", arg):
                desc = arg[0] == "-"
                field = arg[1:]
                # user-friendly aliases
                if field in ["title", "task", "name"]:
                    field = "title"
                elif field in ["pri", "priority", "!"]:
                    field = "pri"
                elif field in ["due", "date", "time", "when", "@"]:
                    field = "due"
                elif field in ["tags", "tag", "#"]:
                    field = "tags"
                # unrecognized field, ignore it
                else:
                    continue
                # sort by field later
                toSort.append((field, desc))
            # filter by a priority
            elif arg[0] == "!":
                toSub.append(("pri", arg[1:]))
            # filter by a tag
            elif arg[0] == "#":
                toSub.append(("tag", arg[1:]))
            # filter by due date
            elif arg[0] == "@":
                tag = arg[1:]
                toSub.append(("due", arg[1:]))
            # display from done list instead of to-do
            elif arg == "done":
                done = True
            # display DoX string format lines (ie. as they would appear in tasks.txt)
            elif arg == "raw":
                raw = True
        # if showing completed tasks, swap list to show
        if done:
            tasks = self.dox.done
        # reverse sort arguments (so first sort field is applied last but appears first)
        toSort.reverse()
        # apply sort in order
        for sort in toSort:
            # sort with undefined items at bottom regardless of order
            withField = sorted([x for x in tasks if not getattr(x, sort[0]) is None], key=(lambda x: getattr(x, sort[0])), reverse=sort[1])
            withoutField = [x for x in tasks if getattr(x, sort[0]) is None]
            tasks = withField + withoutField
        # now filter by fields
        for sub in toSub:
            if sub[0] == "pri":
                pri = sub[1]
                # check if a valid priority
                if len(pri) == 1 and pri.isdigit():
                    pri = int(pri)
                    # ignore 0 as does not affect filter
                    if 0 < pri <= 3:
                        filtered = []
                        # remove any tasks lower than given priority
                        for taskObj in tasks:
                            if taskObj.pri >= pri:
                                filtered.append(taskObj)
                        # replace task list
                        tasks = filtered
            elif sub[0] == "tag":
                tag = sub[1]
                filtered = []
                # remove any tasks not matching the given tag
                for taskObj in tasks:
                    if tag.lower() in [x.lower() for x in taskObj.tags]:
                        filtered.append(taskObj)
                # replace task list
                tasks = filtered
            elif sub[0] == "due":
                keyword = sub[1]
                filtered = []
                for taskObj in tasks:
                    if taskObj.due:
                        today = datetime.datetime.today().date()
                        due = taskObj.due[0].date()
                        # show all tasks with a due date
                        cond = (keyword in ["due", "date", "time"])
                        # or only show tasks due today
                        cond |= (keyword in ["today", "now"] and due <= today)
                        # or only show tasks due tomorrow
                        cond |= (keyword in ["tomorrow"] and due == today + datetime.timedelta(days=1))
                        # or only show tasks due in the next 7 days
                        cond |= (keyword in ["soon", "week", "this week"] and today <= due <= today + datetime.timedelta(days=7))
                        # or only show overdue tasks
                        cond |= (keyword in ["overdue", "late"] and due < today)
                        # task matches the criteria
                        if (cond):
                            filtered.append(taskObj)
                # replace task list
                tasks = filtered
        # if there are tasks
        if len(tasks):
            if raw:
                for taskObj in tasks:
                    print(taskObj)
            else:
                idWidth = len(str(len(tasks)))
                # table layout - four columns
                tmpl = "{:>" + str(idWidth) + "}  {:32}  {:1}  {:19}  {:16}  {:32}"
                # line fits all headers, plus space
                horiz = "-" * (idWidth + 32 + 1 + 19 + 16 + 32 + (2 * 5))
                # table header
                print(horiz)
                print(tmpl.format("#", "Task", "!", "Due", "Repeat", "Tags"))
                print(horiz)
                for taskObj in tasks:
                    # table row
                    due = None
                    if taskObj.due:
                        due = prettyDue(taskObj.due)
                    repeat = None
                    if taskObj.repeat:
                        repeat = prettyRepeat(taskObj.repeat)
                    print(tmpl.format(taskObj.id, (trunc(taskObj.title, 32) if taskObj.title else "<unnamed task>"), taskObj.pri,
                                      (due if due else "<none>"), (repeat if repeat else "<none>"), trunc(", ".join(taskObj.tags), 32) if taskObj.tags else "<none>"))
                print(horiz)
        # no tasks in file
        else:
            print("No tasks in your list that match the current filters.")
    def add(self, args):
        title, desc, pri, due, repeat, tags = parseArgs(args[1:])
        if title or desc or pri or len(tags):
            # add task via DoX interface
            self.dox.addTask(title, desc, pri, due, repeat, tags)
            print("Added task \"{}\".".format(title))
        # no valid arguments given
        else:
            print("Usage: add [<title>] [~<desc>] [0|![![!]]] [#<tag>]")
    def edit(self, args):
        # if id is valid
        if len(args) > 2 and args[1].isdigit() and not args[1] == "0":
            id = int(args[1])
            if id > 0 and id <= len(self.dox.tasks):
                # fetch the task
                taskObj = self.dox.getTask(id)
                title, desc, pri, due, repeat, tags = parseArgs(args[2:], taskObj.title, taskObj.desc, taskObj.pri, taskObj.due, taskObj.repeat, taskObj.tags)
                # edit task via DoX interface
                self.dox.editTask(id, title, desc, pri, due, repeat, tags)
                print("Updated task \"{}\".".format(title))
            # invalid id
            else:
                print("No task found for ID \"{}\".".format(id))
        # no valid arguments given
        else:
            print("Usage: edit <id> [<title>] [~<desc>] [0|![![!]]] [#<tag>]")
    def info(self, args):
        # if id is valid
        if len(args) > 1     and args[1].isdigit() and not args[1] == "0":
            id = int(args[1])
            if id > 0 and id <= len(self.dox.tasks):
                # fetch the task
                taskObj = self.dox.getTask(id)
                out = []
                if taskObj.title:
                    # title with underline
                    out.append("{}\n{}".format(taskObj.title, ("-" * len(taskObj.title))))
                    out.append("")
                if taskObj.desc:
                    # print description
                    out.append(taskObj.desc.replace("\\", "\n"))
                    out.append("")
                if taskObj.due:
                    # print full date
                    due = taskObj.due[0].strftime("%d/%m/%Y")
                    if taskObj.due[1]:
                        due = taskObj.due[0].strftime("%d/%m/%Y %H:%M:%S")
                    out.append("Due: {}".format(due))
                if taskObj.repeat:
                    # print pretty repeat
                    out.append("Repeat: {}".format(prettyRepeat(taskObj.repeat)))
                # print priority (even if 0)
                pris = ["Low", "Medium", "High", "Critical"]
                out.append("Priority: {} ({})".format(pris[taskObj.pri], taskObj.pri))
                if taskObj.tags:
                    # print tags
                    out.append("")
                    out.append("#{}".format(" #".join(taskObj.tags)))
                print("\n".join(out))
            # invalid id
            else:
                print("No task found for ID \"{}\".".format(id))
        # no valid arguments given
        else:
            print("Usage: info <id>")
    def move(self, args):
        # if id is valid
        if len(args) >= 2 and args[1].isdigit() and not args[1] == "0":
            id = int(args[1])
            # default to move to end of list
            pos = len(self.dox.tasks)
            if len(args) >= 3:
                # if pos is valid
                if args[2] in ["0", "start", "front", "top", "first"]:
                    pos = 1
                elif args[2].isdigit():
                    pos = int(args[2])
                    if pos > len(self.dox.tasks):
                        pos = len(self.dox.tasks)
            # if valid move
            if id > 0 and id <= len(self.dox.tasks):
                # id and pos different
                if not id == pos:
                    self.dox.moveTask(id, pos)
                    print("Moved task from position {} to {}.".format(id, pos))
                else:
                    print("The task is already in that position.")
            # invalid id
            else:
                print("No task found for ID \"{}\".".format(id))
        # no valid arguments given
        else:
            print("Usage: move <id> [<pos>]")
    def done(self, args):
        # store IDs to mark done
        tasks = []
        # extract task IDs
        for arg in args[1:]:
            if arg.isdigit() and not arg == "0" and 0 < int(arg) <= len(self.dox.tasks) and int(arg) not in tasks:
                tasks.append(int(arg))
        if len(tasks):
            # complete single task straight away
            if len(tasks) == 1:
                taskObj = self.dox.getTask(tasks[0])
                self.dox.doneTask(tasks[0])
                print("Marked \"{}\" complete.  Well done!".format(taskObj.title))
            # confirm done if multiple
            elif raw_input("Marking {} tasks as complete, are you sure (YES/no)? ".format(len(tasks))) not in ["no", "n"]:
                # do in reverse to avoid ID conflicts
                for id in sorted(tasks, reverse=True):
                    self.dox.doneTask(id)
                print("Marked {} tasks.  Well done!".format(len(tasks)))
            # aborted on confirm
            else:
                print("Aborted.")
        # no valid arguments given
        else:
            print("Usage: done <id> [<id>...]")
    def undo(self, args):
        # store IDs to mark done
        done = []
        # extract task IDs
        for arg in args[1:]:
            if arg.isdigit() and not arg == "0" and 0 < int(arg) <= len(self.dox.done) and int(arg) not in done:
                done.append(int(arg))
        if len(done):
            # complete single task straight away
            if len(done) == 1:
                taskObj = self.dox.getTask(done[0], False)
                self.dox.undoTask(done[0])
                print("Unmarked \"{}\" complete.  Oh...".format(taskObj.title))
            # confirm done if multiple
            elif raw_input("Unmarking {} tasks as complete, are you sure (YES/no)? ".format(len(done))) not in ["no", "n"]:
                # do in reverse to avoid ID conflicts
                for id in sorted(done, reverse=True):
                    self.dox.undoTask(id)
                print("Unmarked {} tasks.  Oh...".format(len(done)))
            # aborted on confirm
            else:
                print("Aborted.")
        # no valid arguments given
        else:
            print("Usage: undo <id> [<id>...]")
    def delete(self, args):
        # store IDs to delete
        tasks = []
        done = []
        # check done tasks after toggle
        switchDone = False
        # extract task IDs
        for arg in args[1:]:
            if arg.isdigit() and not arg == "0":
                id = int(arg)
                if switchDone and 0 < id <= len(self.dox.done):
                    done.append(id)
                elif 0 < id <= len(self.dox.tasks):
                    tasks.append(id)
            elif arg in ["done", "d"]:
                switchDone = True
        # confirm deletion
        output = []
        if len(tasks):
            output.append("{} uncompleted task{}".format(len(tasks), "" if len(tasks) == 1 else "s"))
        if len(done):
            output.append("{} completed task{}".format(len(done), "" if len(done) == 1 else "s"))
        if len(output):
            if raw_input("Deleting {}, are you sure (yes/NO)? ".format(" and ".join(output))) in ["yes", "y"]:
                # do in reverse to avoid ID conflicts
                for id in sorted(tasks, reverse=True):
                    self.dox.deleteTask(id)
                for id in sorted(done, reverse=True):
                    self.dox.deleteTask(id, False)
                print("Deleted {} task{}...  :(".format(len(tasks + done), "" if len(tasks + done) == 1 else "s"))
            else:
                print("Aborted.")
        # no valid arguments given
        else:
            print("Usage: del [<id>...] [<done>] [<id>...]")

if __name__ == "__main__":
    # Python 2/3 compatibility hack: allows use of raw_input in Python 3.x
    if not "raw_input" in dir(__builtins__):
        def raw_input(prompt):
            return input(prompt)
    # start main loop
    try:
        main()
    # user interrupted or ended session, end shell
    except KeyboardInterrupt:
        print("exit")
        print("")
        sys.exit(0)
    except EOFError:
        print("")
        sys.exit(0)
