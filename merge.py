def merge_sort(data):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])

    return merge_gabung(left, right)

def merge_gabung(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        a = left[i]
        b = right[j]

        if a['judul'].lower() < b['judul'].lower():
            result.append(a)
            i += 1
        elif a['judul'].lower() > b['judul'].lower():
            result.append(b)
            j += 1
        else:
            if int(a['tahun']) > int(b['tahun']):
                result.append(a)
                i += 1
            elif int(a['tahun']) < int(b['tahun']):
                result.append(b)
                j += 1
            else:
                if int(a['harga']) < int(b['harga']):
                    result.append(a)
                    i += 1
                else:
                    result.append(b)
                    j += 1
   
    result.extend(left[i:])
    result.extend(right[j:])
    return result