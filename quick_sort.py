def quick_sort(data, key, descending=False):
    if len(data) <= 1:
        return data

    pivot = data[0]

    try:
        pivot_val = float(pivot[key])
        convert = lambda x: float(x[key])
    except:
        pivot_val = pivot[key].lower()
        convert = lambda x: x[key].lower()

    if descending:
        less = [x for x in data[1:] if convert(x) > pivot_val]
        greater = [x for x in data[1:] if convert(x) <= pivot_val]
    else:
        less = [x for x in data[1:] if convert(x) <= pivot_val]
        greater = [x for x in data[1:] if convert(x) > pivot_val]

    return quick_sort(less, key, descending) + [pivot] + quick_sort(greater, key, descending)

