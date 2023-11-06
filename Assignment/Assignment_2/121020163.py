import numpy as np


def pass1(f):
    # item counts
    item_counts = dict()
    for line in f:
        items = list(set(line.split()))
        for i in items:
            if i not in item_counts:
                item_counts[i] = 1
            else:
                item_counts[i] += 1
    # frequent items
    result = {key: value for key, value in item_counts.items() if value >= 100}
    selected_keys = sorted(list(result.keys()))
    return item_counts, selected_keys


def pass2(frequent_items, f):
    # pair counts
    tri_matrix = np.zeros((len(frequent_items), len(frequent_items)))
    f.seek(0)
    for line in f:
        items = list(set(line.split()))
        if len(items) > 1:
            pairs = [(items[i], items[j]) for i in range(len(items)) for j in range(i + 1, len(items))]
            for p in pairs:
                if p[0] in frequent_items and p[1] in frequent_items:
                    indices = sorted([frequent_items.index(i) for i in p])
                    tri_matrix[indices[0]][indices[1]] += 1
    # frequent pairs
    frequent_indices = np.where(tri_matrix >= 100)
    frequent_indices = list(zip(frequent_indices[0], frequent_indices[1]))
    frequent_pairs = sorted([(frequent_items[i[0]], frequent_items[i[1]]) for i in frequent_indices])
    return tri_matrix, frequent_pairs


def top_pairs(item_counts, pair_counts, frequent_items, frequent_pairs):
    # calculate confidence
    conf = list()
    rules = [((i[0], i[1]), (i[1], i[0])) for i in frequent_pairs]
    rules = [i for sublist in rules for i in sublist]
    for p in rules:
        total = item_counts[p[0]]
        indices = sorted([frequent_items.index(i) for i in p])
        union = pair_counts[indices[0]][indices[1]]
        conf.append(union / total)
    rule_conf_pairs = list(zip(rules, conf))
    top_five_conf = sorted(rule_conf_pairs, reverse=True, key=lambda x: (x[1], x[0][0]))[:5]
    return top_five_conf


def pass3(frequent_items, f):
    # triple counts
    triple_counts = dict()
    f.seek(0)
    for line in f:
        items = list(set(line.split()))
        if len(items) > 1:
            triples = [(items[i], items[j], items[k]) for i in range(len(items)) for j in range(i + 1, len(items)) for k
                       in range(j + 1, len(items))]
            for t in triples:
                if t[0] in frequent_items and t[1] in frequent_items and t[2] in frequent_items:
                    t = tuple(sorted(t))
                    if t not in triple_counts:
                        triple_counts[t] = 1
                    else:
                        triple_counts[t] += 1
    # frequent triples
    result = {key: value for key, value in triple_counts.items() if value >= 100}
    frequent_triples = sorted(list(result.keys()))
    return triple_counts, frequent_triples


def top_triples(pair_counts, triple_counts, frequent_items, frequent_triples):
    # calculate confidence
    conf = list()
    rules = list()
    for i in frequent_triples:
        rules.append(tuple([i[0], i[1], i[2]])) if i[0] < i[1] else rules.append(tuple([i[1], i[0], i[2]]))
        rules.append(tuple([i[0], i[2], i[1]])) if i[0] < i[2] else rules.append(tuple([i[2], i[0], i[1]]))
        rules.append(tuple([i[1], i[2], i[0]])) if i[1] < i[2] else rules.append(tuple([i[2], i[1], i[0]]))
    for t in rules:
        left = [t[0], t[1]]
        indices = sorted([frequent_items.index(i) for i in left])
        total = pair_counts[indices[0]][indices[1]]
        union = triple_counts[tuple(sorted(t))]
        conf.append(union / total)
    rule_conf_triples = list(zip(rules, conf))
    top_five_conf = sorted(rule_conf_triples, reverse=True, key=lambda x: (x[1], x[0][0], x[0][1]))[:5]
    return top_five_conf


def main():
    with open("browsing.txt", "r") as f:
        item_counts, frequent_items = pass1(f)
        pair_counts, frequent_pairs = pass2(frequent_items, f)
        pairs = top_pairs(item_counts, pair_counts, frequent_items, frequent_pairs)
        print("Top 5 rules for pairs:")
        for p in pairs:
            print(f"{p[0][0]} -> {p[0][1]}: {p[1]}")
        triple_counts, frequent_triples = pass3(frequent_items, f)
        triples = top_triples(pair_counts, triple_counts, frequent_items, frequent_triples)
        print("Top 5 rules for tuples:")
        for t in triples:
            print(f"({t[0][0]}, {t[0][1]}) -> {t[0][2]}: {t[1]}")


if __name__ == '__main__':
    main()
