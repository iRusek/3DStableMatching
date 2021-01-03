import random

# permutations

group_size = 6


# X men, X women, X dogs

class Being:
    def __init__(self, name):
        self.preference = [0] * group_size
        self.name = name
        self.partner1 = 0
        self.partner2 = 0
        self.pursuers = []
        self.taken = 0
        self.dissatisfaction = [0, 0, 0]
        for j in range(2):
            self.preference[j] = (random_permutation(range(group_size)))

    def __str__(self):
        return self.name

    def print_pursuers(self):
        text = "["
        if self.pursuers != []:
            if type(self.pursuers[0][1]) == tuple:
                for e in self.pursuers:
                    if e != self.pursuers[0]:
                        text += ", "
                    text += "(" + e[0][0] + "," + e[1][0] + ")"
            else:
                for e in self.pursuers:
                    if e != self.pursuers[0]:
                        text += ", "
                    text += e[0][0]
        text += "]\n"
        print(text)

    def exchange_pursuers(self):
        for i in range(len(self.pursuers)):
            self.pursuers.insert(i, self.pursuers.pop(i)[::-1])


class Man(Being):
    # order of indexes in preference
    order = [1, 2]

    def __init__(self, name):
        Being.__init__(self, name)
        self.preference.insert(0, 0)

    def __str__(self):
        return Being.__str__(self) + ", Man. \tW: " + str(self.preference[1]) + ",\tD: " + str(self.preference[2])


class Woman(Being):
    # order of indexes in preference
    order = [0, 2]

    def __init__(self, name):
        Being.__init__(self, name)
        self.preference.insert(1, 0)

    def __str__(self):
        return Being.__str__(self) + ", Woman. \tM: " + str(self.preference[0]) + ",\tD: " + str(self.preference[2])


class Dog(Being):
    # order of indexes in preference
    order = [0, 1]

    def __init__(self, name):
        Being.__init__(self, name)
        self.preference.insert(2, 0)

    def __str__(self):
        return Being.__str__(self) + ", Dog. \tM: " + str(self.preference[0]) + ",\tW: " + str(self.preference[1])


def random_permutation(iterable, r=None):
    "Random selection from itertools.permutations(iterable, r)"
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(random.sample(pool, r))


def create_family(A, B, C, settings):
    if settings[2] == 0:
        return couples_are_pursuers(A, B, C, settings)
    else:
        return couples_are_pursued(A, B, C, settings)


def couples_are_pursuers(A, B, C, settings):
    aIndex = settings[0]
    bIndex = (settings[0] + settings[1] + 1) % 3
    cIndex = (settings[0] - settings[1] - 1) % 3
    iterations_num = 1
    # print("Iteration #: ", iterations_num, "\n")
    pursue([A, B][settings[3]], C, cIndex)
    while (sorting([A, B][settings[3]], C, [aIndex, bIndex][settings[3]], cIndex, settings[4],
                   [A, B][(settings[3] + settings[4] + 1) % 2],
                   [aIndex, bIndex][(settings[3] + settings[4] + 1) % 2]) != group_size):
        iterations_num += 1
        # print("Iteration #: ", iterations_num, "\n")
        pursue([A, B][settings[3]], C, cIndex)

    for i in range(group_size):
        # partner inception
        [A, B][settings[3]][i].partner2 = (
        C[[A, B][settings[3]][i].preference[cIndex][[A, B][settings[3]][i].dissatisfaction[cIndex]]].name,
        [A, B][settings[3]][i].preference[cIndex][[A, B][settings[3]][i].dissatisfaction[cIndex]])
        [A, B][(settings[3] + 1) % 2][[A, B][settings[3]][i].partner1[1]].partner2 = [A, B][settings[3]][i].partner2
        C[[A, B][settings[3]][i].partner2[1]].partner1 = ([A, B][settings[3]][i].name, i)
        C[[A, B][settings[3]][i].partner2[1]].partner2 = [A, B][settings[3]][i].partner1

        # incept dissatisfactions

        [A, B][(settings[3] + 1) % 2][[A, B][settings[3]][i].partner1[1]].dissatisfaction[cIndex] = \
        [A, B][(settings[3] + 1) % 2][[A, B][settings[3]][i].partner1[1]].preference[cIndex].index(
            [A, B][settings[3]][i].partner2[1])
        C[[A, B][settings[3]][i].partner2[1]].dissatisfaction[[aIndex, bIndex][settings[3]]] = \
        C[[A, B][settings[3]][i].partner2[1]].preference[[aIndex, bIndex][settings[3]]].index(i)
        C[[A, B][settings[3]][i].partner2[1]].dissatisfaction[[aIndex, bIndex][(settings[3] + 1) % 2]] = \
        C[[A, B][settings[3]][i].partner2[1]].preference[[aIndex, bIndex][(settings[3] + 1) % 2]].index(
            [A, B][settings[3]][i].partner1[1])

        # clear pursuers
        C[[A, B][settings[3]][i].partner2[1]].pursuers = []

    return iterations_num


def couples_are_pursued(A, B, C, settings):
    # C->A/B, then (A/B->C or B/A->C depending on settings[2])
    aIndex = settings[0]
    bIndex = (settings[0] + settings[1] + 1) % 3
    cIndex = (settings[0] - settings[1] - 1) % 3
    iterations_num = 1
    # print("Iteration #: ", iterations_num, "------------------------------------------------\n")
    pursue(C, [A, B][settings[3]], [aIndex, bIndex][settings[3]], settings[4],
           [A, B][(settings[3] + settings[4] + 1) % 2])
    while (sorting(C, [A, B][(settings[3] + settings[4] + 1) % 2], cIndex,
                   [aIndex, bIndex][settings[3]]) != group_size):
        iterations_num += 1
        # print("Iteration #: ", iterations_num, "------------------------------------------------\n")
        pursue(C, [A, B][settings[3]], [aIndex, bIndex][settings[3]], settings[4],
               [A, B][(settings[3] + settings[4] + 1) % 2])

    for i in range(group_size):
        # partner inception
        C[i].partner1 = ([A, B][settings[3]][C[i].preference[[aIndex, bIndex][settings[3]]][
            C[i].dissatisfaction[[aIndex, bIndex][settings[3]]]]].name, C[i].preference[[aIndex, bIndex][settings[3]]][
                             C[i].dissatisfaction[[aIndex, bIndex][settings[3]]]])
        C[i].partner2 = [A, B][settings[3]][C[i].partner1[1]].partner1
        [A, B][settings[3]][C[i].partner1[1]].partner2 = (C[i].name, i)
        [A, B][(settings[3] + 1) % 2][C[i].partner2[1]].partner2 = [A, B][settings[3]][C[i].partner1[1]].partner2

        # incept dissatisfactions
        C[i].dissatisfaction[[aIndex, bIndex][(settings[3] + 1) % 2]] = C[i].preference[
            [aIndex, bIndex][(settings[3] + 1) % 2]].index(C[i].partner2[1])
        [A, B][settings[3]][C[i].partner1[1]].dissatisfaction[cIndex] = \
        [A, B][settings[3]][C[i].partner1[1]].preference[cIndex].index(i)
        [A, B][(settings[3] + 1) % 2][C[i].partner2[1]].dissatisfaction[cIndex] = \
        [A, B][(settings[3] + 1) % 2][C[i].partner2[1]].preference[cIndex].index(i)

        # clear pursuers
        [A, B][(settings[3] + settings[4] + 1) % 2][i].pursuers = []

    return iterations_num


def print_group(group):
    print("Printing groups:\n")
    for i in range(3):
        for j in range(group_size):
            print(group[i][j])
        print()


def print_results(group, pursuerIndex, pursued_to_left_of_pursuer, iterations):
    dissatisfaction = [0, 0, 0]
    print("Complete after a total of", iterations,
          "iterations!\nPrinting families, and total dissatisfaction from their partners:\n")
    for i in range(group_size):
        dissatisfaction[0] += sum(group[pursuerIndex][i].dissatisfaction)
        dissatisfaction[1] += sum(group[(pursuerIndex + pursued_to_left_of_pursuer + 1) % 3][
                                      group[pursuerIndex][i].partner1[1]].dissatisfaction)
        dissatisfaction[2] += sum(group[(pursuerIndex - pursued_to_left_of_pursuer - 1) % 3][
                                      group[pursuerIndex][i].partner2[1]].dissatisfaction)
        print((group[pursuerIndex][i].name, sum(group[pursuerIndex][i].dissatisfaction)), "+", (
        group[(pursuerIndex + pursued_to_left_of_pursuer + 1) % 3][group[pursuerIndex][i].partner1[1]].name, sum(
            group[(pursuerIndex + pursued_to_left_of_pursuer + 1) % 3][
                group[pursuerIndex][i].partner1[1]].dissatisfaction)), "+", (
              group[(pursuerIndex - pursued_to_left_of_pursuer - 1) % 3][group[pursuerIndex][i].partner2[1]].name, sum(
                  group[(pursuerIndex - pursued_to_left_of_pursuer - 1) % 3][
                      group[pursuerIndex][i].partner2[1]].dissatisfaction)))
    print("Pursuers' total dissatisfaction -", dissatisfaction[0], "\nFirst partners' total dissatisfaction - ",
          dissatisfaction[1], "\nLast partners' total dissatisfaction - ", dissatisfaction[2])


def dissatisfaction(group):
    dissatisfaction = [0, 0, 0]
    for i in range(group_size):
        dissatisfaction[0] += sum(group[0][i].dissatisfaction)
        dissatisfaction[1] += sum(group[1][i].dissatisfaction)
        dissatisfaction[2] += sum(group[2][i].dissatisfaction)
    return dissatisfaction


def print_partners(group):
    print("Printing partners for each participant:\n")
    for i in range(group_size):
        print(group[0][i].name, "+", group[0][i].partner1[0], "+", group[0][i].partner2[0])
        print(group[1][i].name, "+", group[1][i].partner1[0], "+", group[1][i].partner2[0])
        print(group[2][i].name, "+", group[2][i].partner1[0], "+", group[2][i].partner2[0])
    print()


def print_settings(settings):
    text = str(settings) + "\nFirst, "
    text += ["Men", "Women", "Dogs"][settings[0]] + " will pursue "
    text += ["Men", "Women", "Dogs"][(settings[0] + settings[1] + 1) % 3] + " and become couples.\n"
    if settings[2] == 0:
        text += "Then, the couples will pursue " + ["Men", "Women", "Dogs"][(settings[0] - settings[1] - 1) % 3]
        text += ", and the dominant will be: " + ["Men", "Women", "Dogs"][
            [settings[0], (settings[0] + settings[1] + 1) % 3][settings[3]]]
        text += ".\nThe influencer for the pursued is: " + ["Men", "Women", "Dogs"][
            [[settings[0], (settings[0] + settings[1] + 1) % 3][settings[3]],
             [settings[0], (settings[0] + settings[1] + 1) % 3][(settings[3] + 1) % 2]][(settings[4] + 1) % 2]] + ".\n"
    else:
        text += "Then, " + ["Men", "Women", "Dogs"][(settings[0] - settings[1] - 1) % 3] + " will pursue "
        text += ["Men", "Women", "Dogs"][[settings[0], (settings[0] + settings[1] + 1) % 3][settings[3]]]
        text += ".\nThe dominant will be: " + ["Men", "Women", "Dogs"][
            [[settings[0], (settings[0] + settings[1] + 1) % 3][settings[3]],
             [settings[0], (settings[0] + settings[1] + 1) % 3][(settings[3] + 1) % 2]][(settings[4] + 1) % 2]] + ".\n"
    print(text)


def create_pre_family(A, B, aIndex, bToLeftOfA):
    # forms group_size couples from group_size singles from 2 genders
    bIndex = (aIndex + bToLeftOfA + 1) % 3
    iterations_num = 1
    # print("Iteration #: ", iterations_num, "------------------------------------------------\n")
    pursue(A, B, bIndex)
    while (sorting(A, B, aIndex, bIndex) != group_size):
        iterations_num += 1
        # print("Iteration #: ", iterations_num, "------------------------------------------------\n")
        pursue(A, B, bIndex)

    for i in range(group_size):
        # partner inception
        A[i].partner1 = (B[A[i].preference[bIndex][A[i].dissatisfaction[bIndex]]].name,
                         A[i].preference[bIndex][A[i].dissatisfaction[bIndex]])
        B[A[i].partner1[1]].partner1 = (A[i].name, i)

        # incept dissatisfaction
        B[A[i].partner1[1]].dissatisfaction[aIndex] = B[A[i].partner1[1]].preference[aIndex].index(i)

        # clear pursuers
        B[A[i].partner1[1]].pursuers = []
        A[i].taken = 0

        # print couples
        # print(A[i].name, "+", B[A[i].partner1[1]].name)
    # print()
    return iterations_num


def pursue(A, B, bIndex, fair_pursue=1, C=0):
    # each a that isn't taken joins pursuers of prefered (+self.dissatisfaction[bIndex]) b
    # in case of unfair-pursue when the couple is being pursued, the partner (which eventually decides) is actually pursued
    for i in range(len(A)):
        if A[i].taken == 0 and fair_pursue == 1:
            B[A[i].preference[bIndex][A[i].dissatisfaction[bIndex]]].pursuers.append(((A[i].name, i), A[i].partner1))
        elif C != 0 and A[i].taken == 0 and fair_pursue == 0:
            C[B[A[i].preference[bIndex][A[i].dissatisfaction[bIndex]]].partner1[1]].pursuers.append(
                ((A[i].name, i), A[i].partner1))
    return


def sorting(A, B, aIndex, bIndex, fair_pursue=1, C=0, cIndex=0):
    matches = 0
    for b in B:
        if len(b.pursuers) >= 1:
            # lucky fellow, need to sort out by preference
            # if (len(b.pursuers)>1):
            # print("Printing all pursuers for: ",b)
            # b.print_pursuers()
            if fair_pursue == 1:
                for i in b.preference[aIndex]:
                    if ((A[i].name, i), A[i].partner1) in b.pursuers:
                        # i is our best match right now, all other pursuers are scattered
                        for a in b.pursuers:
                            if a[0][1] != i:
                                A[a[0][1]].taken = 0
                                A[a[0][1]].dissatisfaction[bIndex] += 1
                                # print(A[a[0][1]].name,"scattered\n")
                        b.pursuers = [((A[i].name, i), A[i].partner1)]
                        A[i].taken = 1
                        matches += 1
                        b.dissatisfaction[aIndex] = b.preference[aIndex].index(i)
            elif fair_pursue == 0:
                for i in b.preference[cIndex]:
                    if (C[i].partner1, (C[i].name, i)) in b.pursuers:
                        # i is our best match right now, all other pursuers are scattered
                        for c in b.pursuers:
                            if c[1][1] != i:
                                A[c[0][1]].taken = 0
                                A[c[0][1]].dissatisfaction[bIndex] += 1
                                # print(A[c[0][1]].name,"scattered\n")
                        b.pursuers = [(C[i].partner1, (C[i].name, i))]
                        A[C[i].partner1[1]].taken = 1
                        matches += 1
                        b.dissatisfaction[aIndex] = b.preference[aIndex].index(i)
                        break
            # print("Printing final pursuer for: ",b)
            # b.print_pursuers()
    return matches


def stable_match(settings=None):
    # Initialization
    group = [[], [], []]
    for i in range(group_size):
        group[0].append(Man("M" + str(i)))
        group[1].append(Woman("W" + str(i)))
        group[2].append(Dog("D" + str(i)))

    # print_group(group)

    if settings == None:
        # define pursuers, pursued, dominants and influencers
        settings = [random.choice([0, 1, 2])]
        for i in range(4):
            settings.append(random.choice([0, 1]))
    """
    settings define who pursues who, and who is the main influencer or the dominant in the pursued's decision
    settings[0] defines who is the first pursuer
    settings[1] defines whether the pursuer pursues who is to his (cyclic) left
    settings[2] defines whether the third pursues the couple or vice versa
    settings[3] defines who is (influencer for the third) or (dominant for couple) depending on settings[2]
    settings[4] defines if the (dominant for couple) and (influencer for the third) is the same one
    """
    # print_settings(settings)

    iterations = create_pre_family(group[settings[0]], group[(settings[0] + settings[1] + 1) % 3], settings[0],
                                   settings[1])

    iterations += create_family(group[settings[0]], group[(settings[0] + settings[1] + 1) % 3],
                                group[(settings[0] - settings[1] - 1) % 3], settings)

    # print_results(group,settings[0],settings[1],iterations)
    return dissatisfaction(group) + [iterations]