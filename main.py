# Djamalutdinov Isfandiyor
import timeit
import matplotlib.pyplot as plt
import numpy as np
import random

if __name__ == '__main__':

    # pattern = input('Enter a pattern: ')
    random_lines = []
    global book
    # print(book.readlines()[49])

    with open('book.txt', encoding='utf-8') as book:
        book_lines = book.readlines()
        book = '\t'.join(line.strip() for line in book_lines)

        def plot_graph(function):
            ts = []
            book_lengths = []
            for line in book_lines:
                book_lengths.append(len(line))
                pattern = line.strip()
                ts.append(timeit.timeit(
                    lambda: function(book, pattern),
                    # "{0}(book, {1})".format(function, pattern), globals=globals()
                    number=1,
                ))

            plt.plot(book_lengths, ts, 'or')

        def brute_force_search(text, pattern):
            N = len(text)
            M = len(pattern)

            for i in range(N):
                for j in range(M):
                    if i + j >= N:
                        break
                    if text[i+j] != pattern[j]:
                        break
                else:
                    print("Pattern found at index: ", i)

        # brute_force_search(book, pattern)
        # plot_graph(brute_force_search)

        # KMP Search Pattern

        def kpm_search(text, pattern):
            N = len(text)
            M = len(pattern)

            longest_prefix_suffix = [0]*M
            j = 0

            computeLPSArray(pattern, M, longest_prefix_suffix)

            for i in range(N):
                if pattern[j] == text[i]:
                    i += 1
                    j += 1

                if j == M:
                    print("Pattern found at index: ", str(i-j))
                    j = longest_prefix_suffix[j-1]

                elif i < N and pattern[j] != text[i]:
                    if j != 0:
                        j = longest_prefix_suffix[j-1]
                    else:
                        i += 1

        def computeLPSArray(pattern, M, lps):
            len = 0
            i = 1

            while i < M:
                if pattern[i] == pattern[len]:
                    len += 1
                    lps[i] = len
                    i += 1
                else:
                    if len != 0:
                        len = lps[len-1]
                    else:
                        lps[i] = 0
                        i += 1

        # kpm_search(book, pattern)

        # FSM Search Pattern

        def fsm_engine(state, a, n, pattern):
            n = min(n, state+1)
            if n > state:
                m = state+1
            else:
                m = n
            k = m

            while(k > 0):
                if(pattern[k-1] == a):
                    j = k - 2
                    w = state-1
                    while(j >= 0 and pattern[j] == pattern[w]):
                        j -= 1
                        w -= 1
                    if j < 0:
                        return k
                k -= 1
            return 0

        def fsm_search(text, pattern):
            N = len(text)
            M = len(pattern)

            state = 0

            S = []

            for j in range(M):
                if pattern[j] not in S:
                    S.append(pattern[j])
            S = tuple(S)

            for i in range(N):
                state = fsm_engine(state, text[i], M, pattern)
                if state == M:
                    print(f"Pattern found at index: {i-M+1}")

            return 0

        # fsm_search(book, pattern)

        # Sunday Search Pattern

        def sunday_search(text, pattern):
            M = len(pattern)
            N = len(text)

            for i in range(N - M + 1):
                j = 0

                while(j < M):
                    if (text[i + j] != pattern[j]):
                        break
                    j += 1

                if (j == M):
                    print("Pattern found at index ", i)
            # i, j, checker = 0, 0, 0

            # N = len(text)
            # M = len(pattern)

            # A = []

            # for a in range(128):
            #     A.append(M + 1)

            # for j in range(M):
            #     A[ord(pattern[j])] = M - j

            # i = 0
            # while i < N - M:
            #     j = 0
            #     while j < M and (text[i+j] == pattern[j]):
            #         j += 1
            #     if j == M:
            #         checker = 1
            #     v = ord(text[i+M])
            #     i += A[v]

            # if checker == 1:
            #     print("The given pattern is found")
            # else:
            #     print("The given pattern is not found")

            return 0
        plot_graph(sunday_search)
        # sunday_search(book, pattern)

        # Rabin Karp Search Pattern

        def rk_search(text, pattern):
            i, j, checker, L, S = 0, 0, 0, 13, 127

            N = len(text)
            M = len(pattern)

            hashp, hasht, Sn1 = 0, 0, 1

            for i in range(1, M):
                Sn1 = (Sn1 * S) % L

            for i in range(M):
                hashp = ((hashp * S) % L + ord(pattern[i])) % L
                hasht = ((hasht * S) % L + ord(text[i])) % L

            if hasht != hashp:
                # pass
                print("(1) No match at 0")
            else:
                print("Possible match ", i)
                while j < M and ord(text[j]) == ord(pattern[j]):
                    j += 1
                if j == M:
                    print("Match found in ", i)

            j = 0
            for i in range(1, (N-M) + 1):
                hasht = ((hasht + L - (ord(text[i - 1]) * Sn1) %
                          L) * S % L + ord(text[i + M - 1])) % L
                if hashp != hasht:
                    # pass
                    print("(2) No match at ", i)
                else:
                    print("Possible match ", i)
                    j = 0

                    while j < M and ord(text[j + i]) == ord(pattern[j]):
                        j += 1
                    if j == M:
                        print("Match found in ", i)
                    else:
                        print("Spurious hit")
            return 0

        # rk_search(book, pattern)
        # ns = np.linspace(10, 10_000, 100, dtype=int)

        # ts = [timeit.timeit('brute_force_search(book, pattern)',
        #                     globals=globals(), number=1) for n in ns]
        # plt.plot(ns, ts, 'or')
