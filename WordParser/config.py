
matrix = [
        {
            "\t":0, ' ':0, "\n":0, 'letter':1, "digit":2,
            "<":8, ">":9, "/":10,",":14, "=":14, "+":17,
            "-":18,"*":14,"(":14,")":14,";":14,"'":14,"{":14,
            "}":14,"&":14,"|":14 ,"=":15
        },# 0
        {"letter":1, "digit":1," ":13},# 1
        {"digit":2, ".":3, 'E':5, "e":5, "letter":float('inf')},# 2
        {"digit":4, },# 3
        {"digit":4, "e":5, "E":5},# 4
        {"digit":7, "+":6, "-":6},# 5
        {"digit":7},# 6
        {"digit":7},# 7
        {"=":14, ">":14},# 8
        {"=":14},# 9
        {"*":11},# 10
        {"any":11, "*":12},# 11
        {"/":14},# 12
        {},# 13
        {},# 14
        {"=":14},# 15
        {'/':13,'any':11},#16
        {'+':14},#17
        {'-':14}, 
    ]
final = [1,2,4,7,8,9,10,13,14,15, 17,18]

kwrd = set([
        "int",
        "float",
        "for",
        "long",
        "double",
        "while",
        "switch",
        "if",
        "else",
        "+",
        "-",
        "*",
        "/",
        ">",
        "<",
        ",",
        "=",
        ">=",
        "<=",
        "==",
        "!=",
        "<<",
        "!",
        "&&",
        "||",
        "&",
        "(",
        ")",
        "[",
        "]",
        ";",
        "{",
        "}",
        '++',
        '--',
        'or',
        'and'
])