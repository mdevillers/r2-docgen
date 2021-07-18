
import r2pipe
import re
import hashlib

allcmds = {}

def strip_description(line):
    if line:
        for i in range(len(line)-1, -1, -1):
            s2 = line[i:]
            r = re.match(r"\s{3,}[a-zA-Z]{3,}", s2)
            if r:
                return s2.strip()


def get_radare2_version(r2):
    output = r2.cmd("!r2 -v")
    r = re.match(r"^radare2 (.*?) ", output)
    if r:
        return r.group(1)
    else:
        return ""

def clean_cmd(cmd):
    if cmd:
        if "[" in cmd:
            cmd = cmd.split("[")[0]
        if cmd.endswith("?"):
            cmd = cmd[:-1]
        cmd += "?"
        if cmd.startswith("Usage: "):
            cmd = cmd.replace("Usage: ", "")
        if cmd.endswith(" ?"):
            cmd = cmd.replace(" ?", "?")
    else:
        cmd = "?"
    return cmd

def call_help_cmd(r2, cmd):
    cmd = clean_cmd(cmd)
    output = r2.cmd(cmd)
    if cmd:
        link = hashlib.md5(bytes(cmd, "utf8")).hexdigest() + ".html"
        with open(f"pages/{link}", "w") as f:
            f.write(f"<!DOCTYPE html>\n")
            f.write(f"<html>\n")
            output = output.replace("\n", "<br>")
            f.write(output)
            f.write(f"</html>\n")

    cmds = []
    output = r2.cmd(cmd)

    for line in output.split("\n| "):
        line = line.strip()
        r = re.match(r"^(.*?)\[.*\?.*\]", line)
        if r:
            c = r.group(1)
            c = clean_cmd(c)
            if not c in allcmds:
                cmds.append(c)
                allcmds[c] = {}
                allcmds[c]['link'] = hashlib.md5(bytes(c, "utf8")).hexdigest() + ".html"
                allcmds[c]['description'] = strip_description(line)
        else:
            line = line.split(" ")
            if line:
                line = line[0].strip()
                if line.endswith("??") and not line.endswith("=??"):                    
                    c = clean_cmd(line)
                    if not c in allcmds:
                        cmds.append(c)
                        allcmds[c] = {}
                        allcmds[c]['link'] = hashlib.md5(bytes(c, "utf8")).hexdigest() + ".html"
                        allcmds[c]['description'] = strip_description(line)
                    if not c in allcmds:
                        cmds.append(c)
                elif line.endswith("?"):
                    c = line
                    c = clean_cmd(c)
                    if not c in allcmds:
                        cmds.append(c)
                        allcmds[c] = {}
                        allcmds[c]['link'] = hashlib.md5(bytes(c, "utf8")).hexdigest() + ".html"
                        allcmds[c]['description'] = strip_description(line)

    for c in cmds:        
        call_help_cmd(r2, c)

def main():

    r2 = r2pipe.open('--')
    allcmds["?"] = {}
    allcmds["?"]["link"] = hashlib.md5(bytes("?", "utf8")).hexdigest() + ".html"
    allcmds["?"]["description"] = f"radare2 {get_radare2_version(r2)} help"
    call_help_cmd(r2, "")
    r2.quit()

    with open("html/frame_commands.html", "w") as f:
        f.write(f"<!DOCTYPE html>\n")
        f.write(f"<head>\n")        
        f.write(f'<link rel="stylesheet" href="./style.css>"\n')
        f.write(f"</head>\n")
        f.write(f"<html>\n")
        for cmd in allcmds:
            if "link" in allcmds[cmd]:
                link = allcmds[cmd]["link"]
                f.write(f'<a href="../pages/{link}" target="help_frame">{cmd}</a><br>\n')
        f.write(f"</html>\n")

    for cmd in allcmds:
        if "description" in allcmds[cmd]:
            link = allcmds[cmd]["link"]
            desc = allcmds[cmd]["description"]
            if desc:
                filename = f"pages/{link}"
                with open(filename) as f:
                    content = f.read()
                with open(filename, "w") as f:
                    f.write(desc + "<br>")
                    f.write("<br>")
                    f.write(content)

if __name__ == '__main__':
    main()
    
