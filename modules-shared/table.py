def pad(string, required):
    return string + (required * " ")

def get_bigger(headers):
    last_length = 0

    for i in headers:
        i_length = len(i)

        if (i_length > last_length):
            last_length = i_length

    return last_length

def print_table(headers, values, *, decorator="::"):
    bigger = get_bigger(headers)

    table = zip(headers, values)

    for key, value in table:
        print(pad(key, bigger - len(key)), decorator, value)
