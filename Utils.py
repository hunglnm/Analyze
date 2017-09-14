import re


def re_show_data(pattern1, tmp_str):
    result = re.search(pattern1, tmp_str,)
    print result.groups(), result.start(), result.end()
    #pattern = re.compile(pattern1, re.MULTILINE)
    #print pattern.groupindex
    #i = 0
    #for every_part in pattern.finditer(tmp_str):
    #    print every_part.groups(), every_part.start(), every_part.end()
    #    print i, ';'.join('%s:%s' % (key, every_part.group(key)) for key in pattern.groupindex)
    #    i += 1
