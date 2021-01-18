import itertools
import random

def subset_sum(numbers, target, partial=[], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(numbers):
        # remaining = numbers[i + 1:]
        yield from subset_sum(numbers, target, partial + [n], partial_sum + n)

def add_zeros(list, no_responses):
    if len(list) >= no_responses:
        yield list
    for i in range(0,len(list)+1):
        new_list = list.copy()
        new_list.insert(i,0)
        if len(new_list) < no_responses:
            yield from add_zeros(new_list, no_responses)
        else:
            yield new_list

def get_all_pmfs(no_responses, step, unique = True):
    levels = [round(x * step, 3) for x in range(1, int(1 / step) + 1)]
    result = subset_sum(levels, 1)
    pmfs = []
    for r in result:
        if len(r) == no_responses:
            pmfs.append(r)
        if len(r) < no_responses:
            complete_lists = add_zeros(r, no_responses)
            for l in complete_lists:
                pmfs.append(l)
    if unique == True:
        pmfs_set = set(tuple(x) for x in pmfs)
        pmfs_unique = [list(x) for x in pmfs_set]
        pmfs_unique.sort()
        return pmfs_unique
    else:
        return pmfs

def get_all_combinations(lists1, lists2):
    list_combinations = []
    for l1 in lists1:
        for l2 in lists2:
            list_combinations.append((l1,l2))
    return list_combinations


def insert_noise(pmf, noise_size):
    found = False
    while not found:
        selection = False
        indices = []
        while not selection:
            index = random.randrange(len(pmf))
            if index not in indices:
                indices.append(index)
            if len(indices) == 2:
                selection = True
        if pmf[indices[0]] != 0 or pmf[indices[1]] != 0:
            found = True
    if pmf[indices[0]]!= 0:
        pmf[indices[0]] -= noise_size
        pmf[indices[1]] += noise_size
    else:
        pmf[indices[1]] -= noise_size
        pmf[indices[0]] += noise_size
    return pmf

def insert_noise_n(pmf, noise_size, n):
    for i in range(n):
        pmf = insert_noise(pmf, noise_size)
    return pmf

def insert_noise_into_pmfs(pmfs, noise_size, n):
    for pmf in pmfs:
        pmf = insert_noise_n(pmf, noise_size, n)
    return pmfs

no_responses = 3
no_effects = 4
step = 0.2
noise_size = 0.01

if __name__ == "__main__":
    print_output = True
    pmfs = get_all_pmfs(no_effects, step)
    insert_noise_into_pmfs(pmfs, noise_size, 5)
    tables = itertools.product(pmfs, repeat=no_responses)

    print(f"Writing csv files with {pow(len(pmfs),no_responses)} configurations...\n")

    row = 0
    i = 1
    for idx, val in enumerate(tables):
        row += 1
        with open(f"pmf_tables_for_evaluation_{i}.csv", 'a', newline='') as csvfile:

            file_string = ""
            print_string = ""
            for j in range(0,no_responses):
                if j == 0:
                    file_string = f"{no_effects},{no_responses},{step}"
                file_string += f",{','.join(map('{:.2f}'.format, val[j]))}"
                print_string += f"\n{' '.join(map('{:.2f}'.format, val[j]))}"

            csvfile.write(f"{file_string}\n")
            if print_output:
                print(print_string)
                # print(file_string)
        if row >= 500000:
            print(f"pmf_tables_for_evaluation_{i}.csv")
            i += 1
            row = 0

