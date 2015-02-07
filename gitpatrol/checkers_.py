from checker import Checker
import os
import re


class AlertChecker(Checker):
    HOOK_KEY = "alert"
    ALERT = r"alert"
    FILES_TO_SCREEN = [".js"]

    @property
    def err_messages(self):
        if not self.pref_on:
            return []
        mess = []
        if not self.excluded_dir:
            # If the file has a file extension of interest and it contains
            # "alert", then add a warning message to this checker's messages,
            # otherwise return an empty list of messages
            to_screen = os.path.splitext(self.file)[1] in self.FILES_TO_SCREEN
            m = re.search(self.ALERT, self.changed_code)
            if to_screen and m:
                mess.append(self.warning_message(m.group()))
        return mess


class ForbiddenStringChecker(Checker):
    HOOK_KEY = "forbiddenstring"

    FORBIDDEN_STRINGS = [
        r">>>>>>",
        r"<<<<<<",
        r"====",
    ]

    @property
    def err_messages(self):
        if not self.pref_on:
            return []
        mess = []
        # If the changed code contains a forbidden string, then append
        # a warning message for each forbidden string it contains
        for forbidden in self.FORBIDDEN_STRINGS:
            m = re.search(forbidden, self.changed_code)
            if m:
                mess.append(self.warning_message(m.group()))
        return mess


class PrivateKeyChecker(Checker):
    HOOK_KEY = "privatekey"

    PRIVATE_KEY_INDICATORS = [
        r"PRIVATE KEY",
        r"ssh-rsa"
    ]

    @property
    def err_messages(self):
        if not self.pref_on:
            return []
        mess = []
        # If the changed code contains an indicator of a private key, then
        # apend a warning message for each indicator it contains
        for indicator in self.PRIVATE_KEY_INDICATORS:
            m = re.search(indicator, self.changed_code)
            if m:
                mess.append(self.warning_message(m.group()))
        return mess


class StrictParenSpacingChecker(Checker):
    HOOK_KEY = "strictparenspacing"

    SHELL_SCRIPT_EXTS = [".sh", ".bash", ""]

    CHECKS = {
        "( ": r"\([ \t]+",
        " )": r"[ \t]+\)",
        "[ ": r"\[[ \t]+",
        " ]": r"[ \t]+\]"
    }

    @property
    def err_messages(self):
        if not self.pref_on:
            return []
        mess = []
        # If the file in question is not a bash script and it is not in an
        # excluded directory, then if it uses parens and brackets
        # incorrectly, then append a warning message for each invalid character
        is_bash = os.path.splitext(self.file)[1] in self.SHELL_SCRIPT_EXTS
        if not is_bash and not self.excluded_dir:
            for check in self.CHECKS.keys():
                if re.search(self.CHECKS.get(check), self.changed_code):
                    mess.append(self.warning_message(check))
        return mess


class UserHomeChecker(Checker):
    HOOK_KEY = "userhome"

    @property
    def user_home(self):
        return [
            r"home/{}".format(self.user),
            r"Users/{}".format(self.user),
            r"/exports/home/{}".format(self.user)
        ]

    @property
    def err_messages(self):
        if not self.pref_on:
            return []
        mess = []
        # If the file contains any code that looks like a home directory,
        # then append a warning message for the file
        for home in self.user_home:
            m = re.search(home, self.changed_code)
            if m:
                mess.append(self.warning_message(home))
        return mess
